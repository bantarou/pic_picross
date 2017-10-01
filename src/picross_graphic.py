#encoding:utf-8
import cv2
import numpy as np
import sys
import tkinter

from constants import constans as co
from picross_processing import *

#ドットを描画する関数
def draw_dot(canvas, img, box_size, hint_width, hint_height):
  for y in range(0, len(img)):
    for x in range(0, len(img[0])):
      if img[y][x] == 0:
        piv_x = hint_width + x * box_size
        piv_y = hint_height + y * box_size
        canvas.create_rectangle(piv_x, piv_y, piv_x + box_size, piv_y + box_size, fill = 'black')

#GUIの制御部分
def draw_main(img, box_size):

  #ピクロスの端の部分を導出
  row_num, column_num = calc_pic_num(img)
  row_num_length = calc_pic_num_length(row_num)
  column_num_length = calc_pic_num_length(column_num)

  #ヒント部分の長さ
  hint_width = row_num_length * co.HINT_MARGIN_WIDTH
  hint_height = column_num_length * co.HINT_MARGIN_WIDTH

  pic_width = len(img[0]) * box_size + hint_width
  pic_height = len(img) * box_size + hint_height
  #
  # GUI設定
  #
  root = tkinter.Tk()
  root.title(u"Picross")
  root.geometry(str(pic_width + co.WINDOW_MARGIN_WIDTH * 2) + "x" + str(pic_height + co.WINDOW_MARGIN_HEIGHT * 2))

  #キャンバスエリア
  canvas = tkinter.Canvas(root, width = pic_width, height = pic_height)

  #ピクロスのドット部を描画
  draw_dot(canvas, img, box_size, hint_width, hint_height)

  #キャンバスバインド
  canvas.place(x=co.WINDOW_MARGIN_WIDTH, y=co.WINDOW_MARGIN_HEIGHT)

  # GUIの末端
  root.mainloop()
