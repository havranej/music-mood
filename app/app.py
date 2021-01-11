import pyaudio
import numpy as np
import struct

from pyAudioAnalysis import ShortTermFeatures

from predictor import Ensemble

BUFFER_SIZE = 3.0 # Buffer size in seconds
FS = 16000 # Sampling frequency

WINDOW = 0.050 # Feature extraction window
STEP = 0.050

ROLLING_FACTOR = 0.5 # How big influence have the new values 

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


ensemble = Ensemble()
ensemble.load_models("./models", n_models = 5)

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels = 1, rate = FS,
                 input = True, frames_per_buffer = int(FS*BUFFER_SIZE))

a_rolling, v_rolling = 0, 0

while True:
    x = read_and_process_stream(stream)
    features, f_names = ShortTermFeatures.feature_extraction(x, FS, WINDOW*FS, STEP*FS)
    a_current, v_current = ensemble.predict_from_features(features)

    a_rolling = update_rolling_value(a_rolling, a_current)
    v_rolling = update_rolling_value(v_rolling, v_current)

    print(f"Arousal: {a_rolling:.4f} Valence: {v_rolling:.4f} || Arousal: {a_current:.4f} Valence: {v_current:.4f}")