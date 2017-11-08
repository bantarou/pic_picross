#encoding:utf-8
import numpy as np

from constants import constans as co

class boad_infomation:

  #塗られたマスの塊を返す関数
  def filled_sequential_info(line):
    length_num = []
    continue_num = 0
    start_num = 0
    cnt_flag = False
    for i in range(0, len(line)):
      if cnt_flag:
        if line[i] == co.FILLED_NUM:
          continue_num += 1
        else:
          tmp = []
          tmp.append(continue_num)
          tmp.append(start_num)
          length_num.append(tmp)
          continue_num = 0
          cnt_flag = False

      else:
        if line[i] == co.FILLED_NUM:
          start_num = i
          continue_num += 1
          cnt_flag = True

    return  length_num

  #回答されていないマスの開始位置と連続数を返す処理
  def unsolved_sequential_point_info(line):
    sparse_num = []

    sparse_cnt = 0
    start_num = 0
    cnt_flag = False
    for i in range(0, len(line)):
      if cnt_flag:
        if line[i] == co.UNSOLVED_NUM:
          if i == len(line) - 1:
            sparse_cnt += 1
            tmp = []
            tmp.append(sparse_cnt)
            tmp.append(start_num)
            sparse_num.append(tmp)
            sparse_cnt = 0
            cnt_flag = False
          else:
            sparse_cnt += 1

        elif line[i] == co.NO_FILLED_NUM:
          tmp = []
          tmp.append(sparse_cnt)
          tmp.append(start_num)
          sparse_num.append(tmp)
          sparse_cnt = 0
          cnt_flag = False

        elif line[i] == co.FILLED_NUM:
          sparse_cnt = 0
          cnt_flag = False

      else:
        if line[i] == co.UNSOLVED_NUM:
          if i == len(line) - 1 and line[i - 1] == co. NO_FILLED_NUM:
            tmp = []
            tmp.append(1)
            tmp.append(i)
            sparse_num.append(tmp)

          elif (i - 1) >= 0:
            if line[i - 1] == co.NO_FILLED_NUM:
              sparse_cnt += 1
              start_num = i
              cnt_flag = True

          else:
            sparse_cnt += 1
            start_num = i
            cnt_flag = True

    return sparse_num

  #確定マスの数値情報
  def solved_certain_num_info(line):
    solved_num = []
    continue_num = 0
    cnt_flag = False
    for i in range(0, len(line)):

      if cnt_flag:
        if line[i] == co.FILLED_NUM:
          continue_num += 1
        elif line[i] == co.NO_FILLED_NUM:
          solved_num.append(continue_num)
          continue_num = 0
          cnt_flag = False
        elif line[i] == co.UNSOLVED_NUM:
          continue_num = 0
          cnt_flag = False

      else:
        if line[i] == co.FILLED_NUM:
          if (i - 1 >= 0 and line[i - 1] == co.NO_FILLED_NUM) or i - 1 < 0:
            continue_num += 1
            cnt_flag = True

    return solved_num

  #確定していないマスの数値情報
  def solved_uncertain_num_info(line):
    line_num = []
    continue_cnt = 0
    start_num = 0
    cnt_flag = False
    for i in range(0, len(line)):
      if cnt_flag:
        if i != (len(line) - 1):
          if line[i] == co.FILLED_NUM:
            continue_cnt += 1

          else:
            tmp = []
            tmp.append(continue_cnt)
            tmp.append(start_num)
            line_num.append(tmp)
            continue_cnt = start_num = 0
            cnt_flag = False

        else:
          if line[i] == co.FILLED_NUM:
            continue_cnt += 1
          tmp = []
          tmp.append(continue_cnt)
          tmp.append(start_num)
          line_num.append(tmp)

      else:
        if line[i] == co.FILLED_NUM:
          continue_cnt += 1
          start_num = i
          cnt_flag = True

    return line_num
