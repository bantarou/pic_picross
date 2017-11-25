#encoding:utf-8
import cv2
import numpy as np

from picross_boad_info import boad_infomation as info
from constants import constans as co

class boad_fill:
  #左右詰めの回答の共通部分を返す関数
  def calc_marge_part(hint, length):
    tmp_num = 0
    tmp1 = np.empty(length)
    tmp2 = np.empty(length)
    tmp1.fill(co.UNSOLVED_NUM)
    tmp2.fill(co.UNSOLVED_NUM)
  
    num_tmp1 = np.empty(length)
    num_tmp2 = np.empty(length)
    num_tmp1.fill(co.UNSOLVED_NUM)
    num_tmp2.fill(co.UNSOLVED_NUM)
  
    for cnt in range(0, len(hint)):
      for j in range(tmp_num, tmp_num + hint[cnt]):
        tmp1[j] = co.FILLED_NUM
        num_tmp1[j] = cnt
      tmp_num += hint[cnt]
      if tmp_num < length:
        tmp1[tmp_num] = co.NO_FILLED_NUM
        tmp_num += 1
  
    tmp_num = length
    hint_num = len(hint) - 1
    for cnt in range(0, len(hint)):
      for j in range(tmp_num - hint[hint_num], tmp_num):
        tmp2[j] = co.FILLED_NUM
        num_tmp2[j] = hint_num
      tmp_num -= (hint[hint_num] + 1)
      hint_num -= 1
      if tmp_num >= 0:
        tmp2[tmp_num] = co.NO_FILLED_NUM
  
    #左詰めと右詰めの共通部分かつ同じブロックに属する部分を算出
    ans = np.empty(length)
    for i in range(0, length):
      if tmp1[i] == tmp2[i] and num_tmp1[i] == num_tmp2[i]:
        ans[i] = tmp1[i]
      else:
        ans[i] = co.UNSOLVED_NUM
  
    return ans
  

  #埋まっているマスの合計あるいは未確定マスの合計がヒントの合計と一致した場合の処理
  def fill_line(line, hint):
    hint_sum = 0
    fill_sum = 0
    unsolved_sum = 0
    for cnt in range(0, len(hint)):
      hint_sum += hint[cnt]

    for i in range(0, len(line)):
      if line[i] == co.FILLED_NUM:
        fill_sum += 1
      elif line[i] == co.UNSOLVED_NUM:
        unsolved_sum += 1

    if hint_sum == fill_sum:
      for i in range(0, len(line)):
        if line[i] == co.UNSOLVED_NUM:
          line[i] = co.NO_FILLED_NUM
    elif hint_sum == (fill_sum + unsolved_sum):
      for i in range(0, len(line)):
        if line[i] == co.UNSOLVED_NUM:
          line[i] = co.FILLED_NUM

    return line

  #端の部分を埋める処理(左右から処理する必要あり)
  def fill_edge(line, hint):
    sequential_filled_num_left = info.solved_sequential_certain_num_info(line)

    tmp_hint = np.copy(hint)
    for cnt in range(0, len(sequential_filled_num_left)):
      tmp_hint = np.delete(tmp_hint, 0, 0)

    if len(tmp_hint) == 0:
      return line

    pivot = 0
    for i in range(0, len(line)):
      if line[i] == co.UNSOLVED_NUM:
        pivot = i
        break
    #エラー回避処理
    if pivot - 1 >= 0 and line[pivot - 1] == co.FILLED_NUM:
      return line

    fill_flag = False
    if pivot + tmp_hint[0] < len(line)\
      and line[pivot + tmp_hint[0]] == co.NO_FILLED_NUM:
      for i in range(pivot, pivot + tmp_hint[0]):
        if line[i] == co.FILLED_NUM:
          fill_flag = True
          break
    if pivot + tmp_hint[0] > len(line) - 1:
      return line

    for i in range(pivot, pivot + tmp_hint[0]):
      if fill_flag:
        line[i] = co.FILLED_NUM
      else:
        if line[i] == co.FILLED_NUM:
          fill_flag = True

    return line

  #ヒントの数とNO_FILLEDマスで分割された区間の数が一致した際の処理
  def fill_divide_hint(line, hint):
    no_filled_sparse = info.no_filled_sparse_info(line)

    exist_filled_cnt = 0
    delete_num = []
    for cnt in range(0, len(no_filled_sparse)):
      for i in range(no_filled_sparse[cnt][0], no_filled_sparse[cnt][1]):
        if line[i] == co.FILLED_NUM:
          exist_filled_cnt += 1
          break
        elif i == no_filled_sparse[cnt][1] - 1:
          delete_num.append(cnt)

    no_filled_sparse = np.delete(no_filled_sparse, delete_num, 0)

    if exist_filled_cnt == len(hint):
      for cnt in range(0, len(hint)):
        tmp_line = boad_fill.calc_marge_part([hint[cnt]], no_filled_sparse[cnt][1] - no_filled_sparse[cnt][0])
        for i in range(0, len(tmp_line)):
          if tmp_line[i] == co.FILLED_NUM:
            line[i + no_filled_sparse[cnt][0]] = co.FILLED_NUM

    return line

  #左右の端の決定部分を考慮して残ったヒントの共通部分を導出する関数
  def fill_divide_justified(line, hint):
    sequential_filled_num_left = info.solved_sequential_certain_num_info(line)
    sequential_filled_num_right = info.solved_sequential_certain_num_info(line[::-1])
    tmp_hint = hint.copy()

    if len(sequential_filled_num_left) + \
      len(sequential_filled_num_right) >= len(hint):
      return line

    for cnt in range(0, len(sequential_filled_num_left)):
      tmp_hint = np.delete(tmp_hint, 0, 0)

    for cnt in range(0, len(sequential_filled_num_right)):
      tmp_hint = np.delete(tmp_hint, len(tmp_hint) - 1, 0)

    pivot_left = 0
    pivot_right = 0
    for i in range(0, len(line)):
      if line[i] == co.UNSOLVED_NUM:
        if i - 1 >= 0 and line[i - 1] == co.NO_FILLED_NUM:
          pivot_left = i

        break

    for i in range(0, len(line))[::-1]:
      if line[i] == co.UNSOLVED_NUM:
        if i + 1 < len(line) and line[i + 1] == co.NO_FILLED_NUM:
          pivot_right = len(line) - i - 1

        break

    tmp_line = boad_fill.calc_marge_part(tmp_hint, len(line) - pivot_left - pivot_right)

    for i in range(pivot_left, len(line) - pivot_right):
      if tmp_line[i - pivot_left] == co.FILLED_NUM:
        line[i] = co.FILLED_NUM

    return line

  #NO_FILLEDマスの隣にFILLEDマスが存在する時の処理(左右から処理する必要がある)
  def fill_no_filled_side(line, hint):
    sequential_filled_num_left = info.solved_sequential_certain_num_info(line)
    sequential_filled_num_right = info.solved_sequential_certain_num_info(line[::-1])
    filled_num = info.solved_uncertain_num_info(line)
    tmp_hint = hint.copy()

    if len(sequential_filled_num_left) + \
      len(sequential_filled_num_right) >= len(hint):
      return line

    for cnt in range(0, len(sequential_filled_num_left)):
      tmp_hint = np.delete(tmp_hint, 0, 0)
      filled_num = np.delete(filled_num, 0, 0)

    for cnt in range(0, len(sequential_filled_num_right)):
      tmp_hint = np.delete(tmp_hint, len(tmp_hint) - 1, 0)
      filled_num = np.delete(filled_num, len(filled_num) - 1, 0)

    if len(filled_num) > 0:
      pivot = filled_num[len(filled_num) - 1][1]
      if pivot - 1 >= 0 and line[pivot - 1] == co.NO_FILLED_NUM:
        sparse_sum = 0
        for i in range(pivot, len(line)):
          if line[i] == co.UNSOLVED_NUM:
            sparse_sum += 1

        if sparse_sum < tmp_hint[len(tmp_hint) - 1]:
          for i in range(pivot, pivot + filled_num[len(filled_num) - 1][0]):
            line[i] = co.FILLED_NUM
          return line

    hint_cnt = 0

    for cnt in range(0, len(filled_num)):
      if filled_num[cnt][1] - 1 >= 0 and \
        line[filled_num[cnt][1] - 1] == co.NO_FILLED_NUM:
        while True:
          if hint_cnt >= len(tmp_hint):
            return line

          if filled_num[cnt][0] > tmp_hint[hint_cnt]:
            hint_cnt += 1
          else:
            break

        possible_hint = []
        for cnt2 in range(hint_cnt, len(tmp_hint)):
          filled_num_pivot = 0
          hint_sum = 0
          for cnt3 in range(cnt, len(filled_num)):
            if filled_num[cnt][1] + tmp_hint[cnt2] > filled_num[cnt3][1]:
              filled_num_pivot = cnt3 + 1

          if len(filled_num) - filled_num_pivot <= len(tmp_hint) - (cnt2 + 1):
            possible_hint.append(tmp_hint[cnt2])

        possible_num = 0
        uncertain_flag = False
        min_hint = 0
        if len(possible_hint) > 0:
          possible_num = possible_hint[0]
          min_hint = min(possible_hint)
        else:
          return line

        for cnt2 in range(0, len(possible_hint)):
          if possible_hint[0] != possible_hint[cnt2]:
            uncertain_flag = True
            break

        renge_top = filled_num[cnt][1] + min_hint
        renge_bottom = filled_num[cnt][1]
        for i in range(renge_bottom, renge_top):
          line[i] = co.FILLED_NUM
        if not uncertain_flag:
          if renge_top < len(line):
            line[renge_top] = co.NO_FILLED_NUM

        hint_cnt += 1
    return line
