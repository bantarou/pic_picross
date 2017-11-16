#encoding:utf-8
import numpy as np

from constants import constans as co

class boad_infomation:

  #FILLEDマスの塊を返す関数
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

  #UNSOLVEDマスの開始位置と連続数を返す処理
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
          if i == len(line) - 1 and line[i - 1] == co.NO_FILLED_NUM:
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

  #確定しているFILLEDマスの塊の数値情報を返す関数
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

  #確定していないFILLDEDマスの塊の数値情報を返す関数
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
  
  #連続して確定しているFILLEDマスの塊の数値情報を返す関数
  def solved_sequential_certain_num_info(line):
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
          break

      else:
        if line[i] == co.FILLED_NUM:
          if (i - 1 >= 0 and line[i - 1] == co.NO_FILLED_NUM) or i - 1 < 0:
            continue_num += 1
            cnt_flag = True
        elif line[i] == co.UNSOLVED_NUM:
          break

    return solved_num

  #NO_FILLEDマスの間隔が開く際の開始位置と終了位置を返す関数
  def no_filled_sparse_info(line):
    sparse_num = []
    start_num = 0
    end_num = 0
    cnt_flag = False
    for i in range(0, len(line)):
      if cnt_flag:
        if line[i] == co.NO_FILLED_NUM:
          end_num = i
          tmp_list = []
          tmp_list.append(start_num)
          tmp_list.append(end_num)
          sparse_num.append(tmp_list)
          cnt_flag = False
        elif i == len(line) - 1:
          end_num = i + 1
          tmp_list = []
          tmp_list.append(start_num)
          tmp_list.append(end_num)
          sparse_num.append(tmp_list)
      else:
        if line[i] != co.NO_FILLED_NUM:
          start_num = i
          cnt_flag = True
          if i == len(line) - 1:
            end_num = i + 1
            tmp_list = []
            tmp_list.append(start_num)
            tmp_list.append(end_num)
            sparse_num.append(tmp_list)

    return sparse_num

  #FILLEDマスを含まないNO_FILLEDマスの間の開始位置と終了位置を返す関数
  def no_filled_sparse_without_filled_info(line):
    sparse_num = []
    start_num = 0
    end_num = 0
    cnt_flag = False
    for i in range(0, len(line)):
      if cnt_flag:
        if line[i] == co.NO_FILLED_NUM:
          end_num = i
          tmp_list = []
          tmp_list.append(start_num)
          tmp_list.append(end_num)
          sparse_num.append(tmp_list)
          cnt_flag = False
        elif i == len(line) - 1:
          end_num = i + 1
          tmp_list = []
          tmp_list.append(start_num)
          tmp_list.append(end_num)
          sparse_num.append(tmp_list)
      else:
        if line[i] != co.NO_FILLED_NUM:
          start_num = i
          cnt_flag = True
          if i == len(line) - 1:
            end_num = i + 1
            tmp_list = []
            tmp_list.append(start_num)
            tmp_list.append(end_num)
            sparse_num.append(tmp_list)

    delete_num = []
    for cnt in range(0, len(sparse_num)):
      for i in range(sparse_num[cnt][0], sparse_num[cnt][1]):
        if line[i] == co.FILLED_NUM:
          delete_num.append(cnt)
          break

    sparse_num = np.delete(sparse_num, delete_num, 0)

    return sparse_num

