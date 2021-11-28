from PIL import Image
import pandas as pd
import numpy as np

class ImageSteg:

  def __fillMSB(self, inp):
    '''
    0b01100 -> [0,0,0,0,1,1,0,0]
    '''
    inp = inp.split("b")[-1]
    inp = '0'*(7-len(inp))+inp
    return [int(x) for x in inp]

  def __decrypt_pixels(self, pixels):
    '''
    Given list of 7 pixel values -> Determine 0/1 -> Join 7 0/1s to form binary -> integer -> character
    '''

    pixels = [str(x%2) for x in pixels]
    bin_repr = "".join(pixels)
    return chr(int(bin_repr,2))

  def encrypt_text_in_image(self, image_path, msg, target_path=""):
    '''
    Read image -> Flatten -> encrypt images using LSB -> reshape and repack -> return image
    '''
    img = np.array(Image.open(image_path))
    imgArr = img.flatten()
    msg += "<-END->"
    msgArr = [self.__fillMSB(bin(ord(ch))) for ch in msg]
    
    idx = 0
    for char in msgArr:
      for bit in char:
        if bit==1:
          if imgArr[idx]==0:
            imgArr[idx] = 1
          else:
            imgArr[idx] = imgArr[idx] if imgArr[idx]%2==1 else imgArr[idx]-1
        else: 
          if imgArr[idx]==255:
            imgArr[idx] = 254
          else:
            imgArr[idx] = imgArr[idx] if imgArr[idx]%2==0 else imgArr[idx]+1   
        idx += 1
      
    savePath = target_path+ image_path.split(".")[0] + "_encrypted.png"

    resImg = Image.fromarray(np.reshape(imgArr, img.shape))
    resImg.save(savePath)
    return 

  def decrypt_text_in_image(self, image_path,target_path=""):
    '''
    Read image -> Extract Text -> Return
    '''
    img = np.array(Image.open(image_path))
    imgArr = np.array(img).flatten()
    
    decrypted_message = ""
    for i in range(7,len(imgArr),7):
      decrypted_char = self.__decrypt_pixels(imgArr[i-7:i])
      decrypted_message += decrypted_char

      if len(decrypted_message)>10 and decrypted_message[-7:] == "<-END->":
        break

    return decrypted_message[:-7]





