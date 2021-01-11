import pyaudio
import numpy as np
import struct

from pyAudioAnalysis import ShortTermFeatures

from predictor import Ensemble

ensemble = Ensemble()
ensemble.load_models("./models", n_models = 5)

BUFFER_SIZE = 3.0 # Buffer size in seconds
FS = 16000 # Sampling frequency

WINDOW = 0.050 # Feature extraction window
STEP = 0.050

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels = 1, rate = FS,
                 input = True, frames_per_buffer = int(FS*BUFFER_SIZE))

while True:
    block = stream.read(int(FS*BUFFER_SIZE))

    form = "%dh" % (len(block) / 2)
    shorts = struct.unpack(form, block)

    # then normalize and convert to numpy array:
    x = np.double(list(shorts)) / (2**15)

    features, f_names = ShortTermFeatures.feature_extraction(x, FS, WINDOW*FS, STEP*FS)
    a_pred, v_pred = ensemble.predict_from_features(features)
    
    print(f"Arousal: {a_pred:.4f} Valence: {v_pred:.4f}")