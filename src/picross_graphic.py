#encoding:utf-8
import os
import cv2
import numpy as np
import sys

from constants import constans as co
from picross_processing import *
from picross_verify import *

#ドットを描画する関数
def draw_pic_dot(picross_img, img, box_size, hint_width, hint_height):
  for y in range(0, len(img)):
    for x in range(0, len(img[0])):
      if img[y][x] == 0:
        piv_x = hint_width + x * box_size
        piv_y = hint_height + y * box_size
        cv2.rectangle(picross_img, (piv_x, piv_y), (piv_x + box_size, piv_y + box_size), (0, 0, 0), cv2.FILLED)

#線を描画する関数
def draw_pic_line(picross_img, img, box_size, hint_width, hint_height):
  row_length = hint_width + len(img[0]) * box_size
  column_length = hint_height + len(img) * box_size
  #行の線を描画
  for y in range(0, len(img) + 1):
    if y % co.BOLD_LINE_SPAN == 0:
      cv2.line(picross_img, (0, hint_height + y * box_size), (row_length, hint_height + y * box_size), (0, 0, 0), co.BOLD_LINE_SIZE)
    else:
      cv2.line(picross_img, (0, hint_height + y * box_size), (row_length, hint_height + y * box_size), (0, 0, 0), co.NORMAL_LINE_SIZE)

  #列の線を描画
  for x in range(0, len(img[0]) + 1):
    if x % co.BOLD_LINE_SPAN == 0:
      cv2.line(picross_img, (hint_width + x * box_size, 0), (hint_width + x * box_size, column_length), (0, 0, 0), co.BOLD_LINE_SIZE)
    else:
      cv2.line(picross_img, (hint_width + x * box_size, 0), (hint_width + x * box_size, column_length), (0, 0, 0), co.NORMAL_LINE_SIZE)

#ヒントの描画用関数
def draw_pic_hint(picross_img, img, box_size, hint_width, hint_height, row_hint, column_hint):
  #行方向のヒントの描画
  for y in range(0, len(img)):
    hint = row_hint[y][::-1]
    
    for i in range(0, len(hint)):
      cv2.putText(picross_img, hint[i], \
        (int(hint_width - co.ROW_HINT_LINE_WIDTH_MARGIN - co.ROW_HINT_MARGIN * i), \
        int(hint_height + y * box_size + co.ROW_HINT_LINE_HEIGHT_MARGIN)), \
        cv2.FONT_HERSHEY_SIMPLEX, co.HINT_FONT_SIZE, (0, 0, 0),\
        co.HINT_FONT_WIDTH, cv2.LINE_AA)

  #列方向のヒントの描画
  for x in range(0, len(img[0])):
    #縦書きに変換
    hint = column_hint[x].split(',')
    #Reverse処理
    hint = hint[::-1]
    for i in range(0, len(hint)):
      if int(hint[i]) >= 10:
        cv2.putText(picross_img, hint[i],\
      (int(hint_width + x * box_size + co.COLUMN_HINT_LINE_WIDTH_MARGIN - co.COLUMN_HINT_DIGIT_MARGIN),\
      int(hint_height - co.COLUMN_HINT_LINE_HEIGHT_MARGIN - i * co.COLUMN_HINT_MARGIN)), \
      cv2.FONT_HERSHEY_SIMPLEX, co.HINT_FONT_SIZE, (0, 0, 0),\
      co.HINT_FONT_WIDTH, cv2.LINE_AA)

      else:
        cv2.putText(picross_img, hint[i],\
      (int(hint_width + x * box_size + co.COLUMN_HINT_LINE_WIDTH_MARGIN),\
      int(hint_height - co.COLUMN_HINT_LINE_HEIGHT_MARGIN - i * co.COLUMN_HINT_MARGIN)), \
      cv2.FONT_HERSHEY_SIMPLEX, co.HINT_FONT_SIZE, (0, 0, 0),\
      co.HINT_FONT_WIDTH, cv2.LINE_AA)



#GUIの制御部分
def draw_main(img, box_size):

  #ピクロスの端の部分を導出
  row_hint, column_hint = calc_pic_hint(img)
  row_num_length = calc_pic_num_length(row_hint)
  column_num_length = calc_pic_num_length(column_hint)

  #ピクロスが回答可能かの検証
  is_solved_flag = picross_verify(img, row_hint, column_hint)

  if is_solved_flag:
    #ヒント部分の長さ
    hint_width = row_num_length * co.HINT_MARGIN_WIDTH
    hint_height = column_num_length * co.HINT_MARGIN_WIDTH
  
    pic_width = len(img[0]) * box_size + hint_width
    pic_height = len(img) * box_size + hint_height
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
    draw_pic_line(picross_img, img, box_size, hint_width, hint_height)
    draw_pic_hint(picross_img, img, box_size, hint_width, hint_height, row_hint, column_hint)
    cv2.namedWindow("Picross Paper Image", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Picross Paper Image",picross_img)
    cv2.imwrite("./img/picross_paper.png", picross_img)

    ##答えの保存
    draw_pic_dot(picross_img, img, box_size, hint_width, hint_height) 
    cv2.namedWindow("Picross Answer Image", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Picross Answer Image",picross_img)
    cv2.imwrite("./img/picross_ans.png", picross_img)
  else:
    print("Error: Sorry, we could not make the solvable picross in this picture.")
