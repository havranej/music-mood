from PIL import Image 
import numpy as np
import webcolors

class ColorMapper():
    def __init__(self, map_path):
        self.colormap = np.asarray(Image.open(map_path))[:,:,:3]
        self.names = None
        self.rgb_values = None
        self.init_color_names()
    
    def get_color(self, arousal, valence):
        a_coord = int((1 - arousal) * self.colormap.shape[0])
        v_coord = int((valence) * self.colormap.shape[1])
        return self.colormap[a_coord, v_coord]

    def init_color_names(self):
        self.names = []
        self.rgb_values = []

        for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
            self.names.append(name)
            self.rgb_values.append(list(webcolors.hex_to_rgb(key)))

        self.rgb_values = np.array(self.rgb_values)

    def rgb_to_name(self, rgb):
        rgb = np.array(rgb)
        return self.names[np.argmin(((self.rgb_values - rgb)**2).sum(axis = 1))]


