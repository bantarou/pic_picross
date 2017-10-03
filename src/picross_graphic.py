#encoding:utf-8
import cv2
import numpy as np
import sys
import tkinter

from constants import constans as co
from picross_processing import *
from picross_verify import *

#ドットを描画する関数
def draw_pic_dot(canvas, img, box_size, hint_width, hint_height):
  for y in range(0, len(img)):
    for x in range(0, len(img[0])):
      if img[y][x] == 0:
        piv_x = hint_width + x * box_size
        piv_y = hint_height + y * box_size
        canvas.create_rectangle(piv_x, piv_y, piv_x + box_size, piv_y + box_size, fill = 'black')

#線を描画する関数
def draw_pic_line(canvas, img, box_size, hint_width, hint_height):
  row_length = hint_width + len(img[0]) * box_size
  column_length = hint_height + len(img) * box_size
  #行の線を描画
  for y in range(0, len(img) + 1):
    if y % co.BOLD_LINE_SPAN == 0:
      canvas.create_line(0, hint_height + y * box_size, row_length, hint_height + y * box_size, width = co.BOLD_LINE_SIZE)
    else:
      canvas.create_line(0, hint_height + y * box_size, row_length, hint_height + y * box_size, width = co.NORMAL_LINE_SIZE)

  #列の線を描画
  for x in range(0, len(img[0]) + 1):
    if x % co.BOLD_LINE_SPAN == 0:
      canvas.create_line(hint_width + x * box_size, 0, hint_width + x * box_size, column_length, width = co.BOLD_LINE_SIZE)
    else:
      canvas.create_line(hint_width + x * box_size, 0, hint_width + x * box_size, column_length, width = co.NORMAL_LINE_SIZE)

#ヒントの描画用関数
def draw_pic_hint(canvas, img, box_size, hint_width, hint_height, row_hint, column_hint):
  #行方向のヒントの描画
  for y in range(0, len(img)):
    hint = row_hint[y].replace(',', ', ')

    canvas.create_text(hint_width - co.ROW_HINT_LINE_WIDTH_MARGIN, hint_height + y * box_size + co.ROW_HINT_LINE_HEIGHT_MARGIN, text = hint, font = (co.HINT_FONT, co.HINT_FONT_SIZE), anchor = tkinter.NE)

  #列方向のヒントの描画
  for x in range(0, len(img[0])):
    #縦書きに変換
    hint = column_hint[x].split(',')
    #Reverse処理
    hint = hint[::-1]
    for i in range(0, len(hint)):
      canvas.create_text(hint_width + x * box_size + co.COLUMN_HINT_LINE_WIDTH_MARGIN, hint_height - co.COLUMN_HINT_LINE_HEIGHT_MARGIN - i * co.COLUMN_HINT_NUM_MARGIN, text = hint[i], font = (co.HINT_FONT, co.HINT_FONT_SIZE) ,anchor = tkinter.S)

#GUIの制御部分
def draw_main(img, box_size):

  #ピクロスの端の部分を導出
  row_hint, column_hint = calc_pic_num(img)
  row_num_length = calc_pic_num_length(row_hint)
  column_num_length = calc_pic_num_length(column_hint)

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
  draw_pic_dot(canvas, img, box_size, hint_width, hint_height)
  draw_pic_line(canvas, img, box_size, hint_width, hint_height)
  draw_pic_hint(canvas, img, box_size, hint_width, hint_height, row_hint, column_hint)

  #キャンバスバインド
  canvas.place(x=co.WINDOW_MARGIN_WIDTH, y=co.WINDOW_MARGIN_HEIGHT)

  # GUIの末端
  root.mainloop()
