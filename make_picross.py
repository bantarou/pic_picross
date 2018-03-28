#encoding:utf-8
import sys
import cv2
import numpy as np
import argparse
sys.path.append('./src')

from image_processing import *
from picross_graphic import *
from picross_processing import *

if __name__ == '__main__' :

  parser = argparse.ArgumentParser(
    prog='Pic_picross', # プログラム名
    usage='$python3 make_picross.py <image file path> <picross_size>', # プログラムの利用方法
    description='description', # 引数のヘルプの前に表示
    epilog='end', # 引数のヘルプの後で表示
    add_help=True, # -h/–help オプションの追加
    )

  # 引数の追加
  parser.add_argument('image_file_path', help='image file path',  type=str)
  parser.add_argument('picross_size', help='picross size', type=int)
  parser.add_argument('-r', '--reverse', help='Reverse white and black area.', action='store_true')

  # 引数の解析
  args = parser.parse_args()

  #画像データの反転用フラグ
  reverse_flag = False
  if args.reverse:
    reverse_flag = True

  img = args.image_file_path
  size = args.picross_size

  mosaic_img = convert_mosaic(img, 0, size, 0.0002, reverse_flag)

  draw_main(mosaic_img, 11)
  
  cv2.waitKey(0)
  cv2.destroyAllWindows()
