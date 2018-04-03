#encoding:utf-8
import cv2
import numpy as np

class ImageProcessing:
  __img = []
  __mosaic_img = []
  __img_path = ""
  __blur_times = 0
  __size = 10
  __zero_rato = 0.0002

  __binarize_flag = False
  __reverse_flag = False

  def __init__(self, img_path, blur_times, size, zero_rate):
    self.__img_path = img_path
    self.__blur_times = blur_times
    self.__size = size
    self.__zero_rate = zero_rate
    #画像を二値化
    self.__img = cv2.imread(self.__img_path, cv2.IMREAD_GRAYSCALE)

  def set_flags(self, binarize_flag, reverse_flag):
    self.__binarize_flag = binarize_flag
    self.__reverse_flag = reverse_flag

  #画像をぼかす関数
  def __blur_image(self):
    for i in range(0, self.__blur_times):
      self.__img = cv2.pyrDown(self.__img)
      self.__img = cv2.pyrUp(self.__img)

  #画像のエッジを抽出
  def __extract_edge(self):
    self.__img = cv2.Canny(self.__img, 50, 120)
  
  #画像のネガポジ反転用関数
  def __reverse_bw(self):
    self.__img = 255 - self.__img
  
  #線をモザイクに変換する関数
  def __line_to_mosaic(self):
    box_size = (int)(len(self.__img) / self.__size)
    y_length = (int)(len(self.__img) / box_size)
    x_length = (int)(len(self.__img[0]) / box_size)
    mosaic = np.zeros(shape = (y_length, x_length))
  
    for y in range(0, y_length):
      for x in range(0, x_length):
        div = self.__img[y * box_size : (y + 1) * box_size, x * box_size : (x + 1) * box_size]
        #divの中に0(白)がzero_rate以上の割合で存在する場合0(白)に変換
        zero_count = 0
        for div_y in range(0,box_size):
          for div_x in range(0, box_size):
            if div[div_y][div_x] < 1:
              zero_count += 1
        if zero_count / (box_size * box_size) > self.__zero_rate:
          mosaic[y][x] = 0
        else:
          mosaic[y][x] = 255

    self.__mosaic_img = mosaic

  def convert_mosaic(self):
    #画像のぼかし処理
    self.__blur_image()

    if not self.__binarize_flag:
      #画像のエッジを抽出
      self.__extract_edge()
      #画像のネガポジを反転
      self.__reverse_bw()

    #画像のモザイク処理
    self.__line_to_mosaic()

    #画像の反転
    if self.__reverse_flag:
      self.__reverse_bw()

    return self.__mosaic_img
