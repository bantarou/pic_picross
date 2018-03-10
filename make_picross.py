#encoding:utf-8
import sys
import cv2
import numpy as np
sys.path.append('./src')

from image_processing import *
from picross_graphic import *
from picross_processing import *

if __name__ == '__main__' :
  args = sys.argv
  img = args[1]
  size = int(args[2])

  mosaic_img = convert_mosaic(img, 0, size, 0.0002)

  draw_main(mosaic_img, 11)
  cv2.imwrite("./img/picross_ans.png", mosaic_img)
  
  cv2.waitKey(0)
  cv2.destroyAllWindows()
