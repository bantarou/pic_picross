#encoding:utf-8
import numpy as np

#
# ピクロスの生成を行う処理
#

#ピクロスの数字を計算する関数
def calc_pic_hint(img):
  column_num = []
  row_num = []

  #行方向の処理
  for i in range(0, len(img)):
    str_num = ""
    count_flag = False
    count = 0
    for k in range(0, len(img[0])):
      if img[i][k] == 0:
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
  for j in range(0, len(img[0])):
    str_num = ""
    count_flag = False
    count = 0
    for k in range(0, len(img)):
      if img[k][j] == 0:
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

  return row_num, column_num

#最も長い文字列の長さを返す処理
def calc_pic_num_length(num_list):
  max_num = 0
  for i in range(0, len(num_list)):
    tmp = len(num_list[i])
    if max_num < tmp:
      max_num = tmp

  return max_num

