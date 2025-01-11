import os
from custom_dither import custom_dither_directory

base_path = os.path.dirname(__file__)

# effects
custom_dither_directory(os.path.join(base_path, "effects", "64"))
custom_dither_directory(os.path.join(base_path, "effects", "256"))
