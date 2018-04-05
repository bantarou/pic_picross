#encoding:utf-8
import sys
import cv2
import numpy as np
import argparse
sys.path.append('./src')

from image_processing import ImageProcessing
from picross_processing import PicrossProcessing

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
  parser.add_argument('-r', '--reverse', help='Reverse white and black area', action='store_true')
  parser.add_argument('-b', '--binarize', help='Binarize the image', action='store_true')
  parser.add_argument('-s', '--show', help='Show the image and save the dot image', action='store_true')
  parser.add_argument('-t', '--times', help='Set a blur time for image', type=int)

  # 引数の解析
  args = parser.parse_args()

  #画像二値化用のフラグ
  binarize_flag = False
  #画像データの反転用フラグ
  reverse_flag = False
  #各種画像を表示するフラグ
  show_flag = False
  #画像のぼかし処理の回数
  blur_times = 0
  if args.binarize:
    binarize_flag = True
  if args.reverse:
    reverse_flag = True
  if args.show:
    show_flag = True
  if args.times:
    blur_times = 0 if not type(args.times) == int else args.times

  img_path = args.image_file_path
  size = args.picross_size

  #画像を0と255の二値データに変換
  img_processor = ImageProcessing(img_path, blur_times, size, 0.0002)
  img_processor.set_flags(binarize_flag, reverse_flag, show_flag)
  mosaic_img = img_processor.convert_mosaic()

  #ピクロスの生成と描画処理
  picross_processor = PicrossProcessing(mosaic_img, 11)
  picross_processor.draw_main()

  cv2.waitKey(0)
  cv2.destroyAllWindows()
