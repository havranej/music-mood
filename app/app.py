import pyaudio
import numpy as np
import struct
import curses


from pyAudioAnalysis import ShortTermFeatures

from predictor import Ensemble
import ui

BUFFER_SIZE = 3.0 # Buffer size in seconds
FS = 16000 # Sampling frequency

WINDOW = 0.050 # Feature extraction window
STEP = 0.050

ROLLING_FACTOR = 0.25 # How big influence have the new values 

def read_and_process_stream(stream):
    # Read stream and convert from bytes
    block = stream.read(int(FS*BUFFER_SIZE))
    form = "%dh" % (len(block) / 2)
    shorts = struct.unpack(form, block)

    # Normalize and convert to numpy array:
    x = np.double(list(shorts)) / (2**15)
    return x


def update_rolling_value(rolling, new):
    return new * ROLLING_FACTOR + rolling * (1 - ROLLING_FACTOR)

def scale_value(value):
    value = value + 0.5 # Predicted values are usually within [-0.5, 0.5]
    value = np.clip(value, 0, 1)
    return value


def main(stdscr):
    ensemble = Ensemble()
    ensemble.load_models("./models", n_models = 5)

    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels = 1, rate = FS,
                    input = True, frames_per_buffer = int(FS*BUFFER_SIZE))

    # UI init
    curses.start_color()
    curses.curs_set(False)
    stdscr.clear()
    
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    num_rows, num_cols = stdscr.getmaxyx()
    mainframe_x = int((num_cols - ui.WIDTH) / 2)
    mainframe_y = int((num_rows - ui.HEIGHT) / 2)

    mainframe_x = max([mainframe_x, 0])
    mainframe_y = max([mainframe_y, 0])

    mainframe = ui.MainFrame(mainframe_y, mainframe_x)

    a_rolling, v_rolling = 0.5, 0.5

    while True:
        x = read_and_process_stream(stream)
        features, f_names = ShortTermFeatures.feature_extraction(x, FS, WINDOW*FS, STEP*FS)
        a_current, v_current = ensemble.predict_from_features(features)
        a_current, v_current = scale_value(a_current), scale_value(v_current),

        a_rolling = update_rolling_value(a_rolling, a_current)
        v_rolling = update_rolling_value(v_rolling, v_current)

        mainframe.set_bar_value("a_current", int(a_current * 50), f"Arousal: {a_current:.4f}")
        mainframe.set_bar_value("v_current", int(v_current * 50), f"Valence: {v_current:.4f}")

        mainframe.set_bar_value("a_rolling", int(a_rolling * 50), f"Arousal: {a_rolling:.4f}")
        mainframe.set_bar_value("v_rolling", int(v_rolling * 50), f"Valence: {v_rolling:.4f}")

        # print(f"Arousal: {a_rolling:.4f} Valence: {v_rolling:.4f} || Arousal: {a_current:.4f} Valence: {v_current:.4f}")

try:
    curses.wrapper(main)
except KeyboardInterrupt:
    pass