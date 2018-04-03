#encoding:utf-8
import os
import cv2
import numpy as np
import sys

from constants import constans as co
from picross_verify import *

class PicrossProcessing:
  __img = []
  __box_size = 10
  __row_hint = []
  __column_hint = []

  def __init__(self, img, box_size):
    self.__img = img
    self.__box_size = box_size
  #
  # ピクロスの生成を行う処理
  #
  #ピクロスの数字を計算する関数
  def __calc_pic_hint(self):
    column_num = []
    row_num = []
  
    #行方向の処理
    for i in range(0, len(self.__img)):
      str_num = ""
      count_flag = False
      count = 0
      for k in range(0, len(self.__img[0])):
        if self.__img[i][k] == 0:
          if count_flag:
            count += 1
          else:
            count_flag = True
            count = 1
  
        else:
          if count_flag:
            str_num += str(count) + ","
            count_flag = False
            count = 0
  
      if count != 0:
        str_num += str(count) + ","
  
      if str_num == "":
        row_num.append('0')
      else:
        row_num.append(str_num[:-1])
  
    #列方向の処理
    for j in range(0, len(self.__img[0])):
      str_num = ""
      count_flag = False
      count = 0
      for k in range(0, len(self.__img)):
        if self.__img[k][j] == 0:
          if count_flag:
            count += 1
          else:
            count_flag = True
            count = 1
  
        else:
          if count_flag:
            str_num += str(count) + ","
            count_flag = False
            count = 0
  
      if count != 0:
        str_num += str(count) + ","
  
      if str_num == "":
        column_num.append('0')
      else:
        column_num.append(str_num[:-1])
  
    self.__row_hint = row_num
    self.__column_hint = column_num
  
  #最も長い文字列の長さを返す処理
  def __calc_pic_num_length(self, num_list):
    max_num = 0
    for i in range(0, len(num_list)):
      tmp = len(num_list[i])
      if max_num < tmp:
        max_num = tmp
  
    return max_num
  
  #
  # ピクロスを描画する処理
  #
  #ドットを描画する関数
  def __draw_pic_dot(self, picross_img, hint_width, hint_height):
    for y in range(0, len(self.__img)):
      for x in range(0, len(self.__img[0])):
        if self.__img[y][x] == 0:
          piv_x = hint_width + x * self.__box_size
          piv_y = hint_height + y * self.__box_size
          cv2.rectangle(picross_img, (piv_x, piv_y), (piv_x + self.__box_size, piv_y + self.__box_size), (0, 0, 0), cv2.FILLED)
  
  #線を描画する関数
  def __draw_pic_line(self, picross_img, hint_width, hint_height):
    row_length = hint_width + len(self.__img[0]) * self.__box_size
    column_length = hint_height + len(self.__img) * self.__box_size
    #行の線を描画
    for y in range(0, len(self.__img) + 1):
      if y % co.BOLD_LINE_SPAN == 0:
        cv2.line(picross_img, (0, hint_height + y * self.__box_size), (row_length, hint_height + y * self.__box_size), (0, 0, 0), co.BOLD_LINE_SIZE)
      else:
        cv2.line(picross_img, (0, hint_height + y * self.__box_size), (row_length, hint_height + y * self.__box_size), (0, 0, 0), co.NORMAL_LINE_SIZE)
  
    #列の線を描画
    for x in range(0, len(self.__img[0]) + 1):
      if x % co.BOLD_LINE_SPAN == 0:
        cv2.line(picross_img, (hint_width + x * self.__box_size, 0), (hint_width + x * self.__box_size, column_length), (0, 0, 0), co.BOLD_LINE_SIZE)
      else:
        cv2.line(picross_img, (hint_width + x * self.__box_size, 0), (hint_width + x * self.__box_size, column_length), (0, 0, 0), co.NORMAL_LINE_SIZE)
  
  #ヒントの描画用関数
  def __draw_pic_hint(self, picross_img, hint_width, hint_height):
    #行方向のヒントの描画
    for y in range(0, len(self.__img)):
      hint = self.__row_hint[y][::-1]
      
      for i in range(0, len(hint)):
        cv2.putText(picross_img, hint[i], \
          (int(hint_width - co.ROW_HINT_LINE_WIDTH_MARGIN - co.ROW_HINT_MARGIN * i), \
          int(hint_height + y * self.__box_size + co.ROW_HINT_LINE_HEIGHT_MARGIN)), \
          cv2.FONT_HERSHEY_SIMPLEX, co.HINT_FONT_SIZE, (0, 0, 0),\
          co.HINT_FONT_WIDTH, cv2.LINE_AA)
  
    #列方向のヒントの描画
    for x in range(0, len(self.__img[0])):
      #縦書きに変換
      hint = self.__column_hint[x].split(',')
      #reverse処理
      hint = hint[::-1]
      for i in range(0, len(hint)):
        if int(hint[i]) >= 10:
          cv2.putText(picross_img, hint[i],\
        (int(hint_width + x * self.__box_size + co.COLUMN_HINT_LINE_WIDTH_MARGIN - co.COLUMN_HINT_DIGIT_MARGIN),\
        int(hint_height - co.COLUMN_HINT_LINE_HEIGHT_MARGIN - i * co.COLUMN_HINT_MARGIN)), \
        cv2.FONT_HERSHEY_SIMPLEX, co.HINT_FONT_SIZE, (0, 0, 0),\
        co.HINT_FONT_WIDTH, cv2.LINE_AA)
  
        else:
          cv2.putText(picross_img, hint[i],\
        (int(hint_width + x * self.__box_size + co.COLUMN_HINT_LINE_WIDTH_MARGIN),\
        int(hint_height - co.COLUMN_HINT_LINE_HEIGHT_MARGIN - i * co.COLUMN_HINT_MARGIN)), \
        cv2.FONT_HERSHEY_SIMPLEX, co.HINT_FONT_SIZE, (0, 0, 0),\
        co.HINT_FONT_WIDTH, cv2.LINE_AA)

  #guiの制御部分
  def draw_main(self):
  
    #ピクロスの端の部分を導出
    self.__calc_pic_hint()
    row_num_length = self.__calc_pic_num_length(self.__row_hint)
    column_num_length = self.__calc_pic_num_length(self.__column_hint)
  
    #ピクロスが回答可能かの検証
    is_solved_flag = picross_verify(self.__img, self.__row_hint, self.__column_hint)
  
    if is_solved_flag:
      #ヒント部分の長さ
      hint_width = row_num_length * co.HINT_MARGIN_WIDTH
      hint_height = column_num_length * co.HINT_MARGIN_WIDTH
    
      pic_width = len(self.__img[0]) * self.__box_size + hint_width
      pic_height = len(self.__img) * self.__box_size + hint_height
      #
      # GUI設定
      #
      size = (pic_height + co.WINDOW_MARGIN_HEIGHT, pic_width + co.WINDOW_MARGIN_WIDTH, 3)
      # np.fillで白に埋める
      picross_img = np.zeros(size, dtype=np.uint8)
      picross_img.fill(255)
    
      #ピクロスのドット部を描画
      ##保存用ディレクトリの作成
      if not os.path.exists("./img"):
        os.mkdir("./img")
  
      ##記入用紙の作成
      self.__draw_pic_line(picross_img, hint_width, hint_height)
      self.__draw_pic_hint(picross_img, hint_width, hint_height)
      cv2.namedWindow("Picross Paper Image", cv2.WINDOW_AUTOSIZE)
      cv2.imshow("Picross Paper Image",picross_img)
      cv2.imwrite("./img/picross_paper.png", picross_img)
  
      ##答えの保存
      self.__draw_pic_dot(picross_img, hint_width, hint_height) 
      cv2.namedWindow("Picross Answer Image", cv2.WINDOW_AUTOSIZE)
      cv2.imshow("Picross Answer Image",picross_img)
      cv2.imwrite("./img/picross_ans.png", picross_img)
    else:
      print("Error: Sorry, we could not make the solvable picross in this picture.")
