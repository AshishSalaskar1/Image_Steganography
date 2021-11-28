from numpy.core.arrayprint import printoptions
from ImageSteg import ImageSteg
from PIL import Image
import pandas as pd
import numpy as np


img = ImageSteg()

res = img.decrypt_text_in_image("static/test_encrypted.png")
print(res)
