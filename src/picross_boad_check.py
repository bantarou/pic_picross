#encoding:utf-8
import cv2
import numpy as np

from picross_boad_info import boad_infomation as info
from constants import constans as co

class boad_check:
  #確実に黒マスが届かないマスの処理
  def check_length(line, hint):

    def is_divide(line, length_1, length_2, hint_num):
      for i in range(length_1[1], length_1[1] + hint_num):
        if line[i] == co.NO_FILLED_NUM:
          return True
      if length_1[1] + hint_num < length_2[1]:
        return True

      return False

    length_num = info.filled_sequential_info(line)

     #重複している塊が存在した場合処理を停止
    if len(length_num) == len(hint):
      for cnt in range(0, len(length_num) - 1):
        if not is_divide(line, length_num[cnt],length_num[cnt + 1], hint[cnt]):
          return line

      reverse_line = np.copy(line)[::-1]
      reverse_hint = np.copy(hint)[::-1]
      reverse_length_num = info.filled_sequential_info(reverse_line)
      for cnt in range(0, len(reverse_length_num) - 1):
        if not is_divide(reverse_line, reverse_length_num[cnt], \
          reverse_length_num[cnt + 1], reverse_hint[cnt]):
          return line

    tmp_line = np.copy(line)
    if len(length_num) == len(hint):
      for cnt in range(0, len(length_num)):
        for i in range(0, hint[cnt]):
          right_pivot = sum(length_num[cnt]) - 1 
          left_pivot = length_num[cnt][1]
          if right_pivot - i >= 0 \
            and tmp_line[right_pivot - i] == co.UNSOLVED_NUM:
            tmp_line[right_pivot - i] = co.CHECK_NUM

          if left_pivot + i < len(line) \
            and tmp_line[left_pivot + i] == co.UNSOLVED_NUM:
            tmp_line[left_pivot + i] = co.CHECK_NUM

      for i in range(0, len(line)):
        if line[i] == co.UNSOLVED_NUM and tmp_line[i] != co.CHECK_NUM:
          line[i] = co.NO_FILLED_NUM

    return line

  #ヒントの最小値以下の狭小マスの処理
  def check_sparse_min(line, hint):
    sparse_num = info.no_filled_sparse_without_filled_info(line)
    solved_num = info.solved_certain_num_info(line)

    #確定しているヒントを削除する処理
    delete_num = []
    for cnt in range(0, len(hint)):
      for cnt2 in range(0, len(solved_num)):
        if hint[cnt] == solved_num[cnt2]:
          delete_num.append(cnt)
          solved_num = np.delete(solved_num, cnt2, 0)
          break

    tmp_hint = hint.copy()
    tmp_hint = np.delete(tmp_hint, delete_num, 0)

    #最小のヒント数だけ考慮してNO_FILLEDマスを決定
    if len(tmp_hint) > 0:
      min_hint = min(tmp_hint)
    else:
      min_hint = 0
    for cnt in range(0, len(sparse_num)):
      if sparse_num[cnt][1] - sparse_num[cnt][0] < min_hint:
        for i in range(sparse_num[cnt][0], sparse_num[cnt][1]):
          line[i] = co.NO_FILLED_NUM

    return line

  #左右詰めの狭小マスの処理(左右から処理する必要があり)
  def check_sparse_justified(line, hint):

    def line_test(line, num):
      for i in range(0, num):
        if line[i] == co.UNSOLVED_NUM:
          return False

      return True

    #ヒントの順番を考慮してNO_FILLEDマスを決定
    sparse_num = info.no_filled_sparse_without_filled_info(line)
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


    for cnt in range(0, len(sparse_num)):
      if sparse_num[cnt][1] - sparse_num[cnt][0] < tmp_hint[0] \
        and line_test(line, sparse_num[cnt][0]):

        for i in range(sparse_num[cnt][0], sparse_num[cnt][1]):
          line[i] = co.NO_FILLED_NUM
      else:
        break

    return line

  #埋まっているマスの塊の左右を確認する処理(両側から処理を行う必要がある)
  def check_around_filled(line, hint):
    continue_cnt = 0
    hint_num = 0
    start_num = 0
    span_cnt = 0
    max_span = 0
    cnt_flag = False

    for i in range(0, len(line)):
      if cnt_flag:
        if line[i] == co.FILLED_NUM:
          continue_cnt += 1
        else:
          if span_cnt > max_span:
            max_span = span_cnt

          if span_cnt == 0:
            if hint[hint_num] == continue_cnt and max_span <= hint[hint_num]:
              line[i] = co.NO_FILLED_NUM
              contiue_cnt = max_span = span_cnt = 0
              cnt_flag = False
              hint_num += 1
            else:
              break
          else:
            if hint[hint_num] == continue_cnt and max_span <= hint[hint_num]:
              if start_num - 1 >= 0:
                line[start_num - 1] = co.NO_FILLED_NUM
              line[i] = co.NO_FILLED_NUM
              contiue_cnt = max_span = span_cnt = 0
              cnt_flag = False
              break
            else:
              break

      else:
        if line[i] == co.FILLED_NUM:
          continue_cnt += 1
          start_num = i
          cnt_flag = True
        elif line[i] == co.NO_FILLED_NUM:
          if span_cnt > max_span:
            max_span = span_cnt
          continue_cnt = 0
          span_cnt = 0
        elif line[i] == co.UNSOLVED_NUM:
          continue_cnt = 0
          span_cnt += 1

    return line

  #ヒントの最大値の左右を確認する処理
  def check_around_max(line, hint):
    line_num = info.solved_uncertain_num_info(line)

    continue_flag = True

    #ヒント行列をコピー
    tmp_hint = hint.copy()
    while continue_flag:
      continue_flag = False
      for cnt in range(0, len(line_num)):
        if len(tmp_hint) > 0:
          max_hint = max(tmp_hint)
        else:
          max_hint = 0

        if line_num[cnt][0] == max_hint:
          if line_num[cnt][1] - 1 >= 0:
            line[line_num[cnt][1] - 1] = co.NO_FILLED_NUM
          if sum(line_num[cnt]) < len(line):
            line[sum(line_num[cnt])] = co.NO_FILLED_NUM
          tmp_hint = np.delete(tmp_hint, np.argmax(tmp_hint), 0)
          line_num.pop(cnt)
          continue_flag = True
          break

    return line

  #ヒントの数とNO_FILLEDマスで分割された区間の数が一致した際のNO_FILLEDマスの推論処理
  def check_divide_hint(line, hint):
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

    tmp_line = np.copy(line)
    if exist_filled_cnt == len(hint):
      for cnt in range(0, len(hint)):
        right_limit = no_filled_sparse[cnt][1]
        right_pivot = 0
        left_limit = no_filled_sparse[cnt][0]
        left_pivot = 0

        fill_flag = False
        for i in range(left_limit, right_limit):
          if fill_flag:
            if line[i] != co.FILLED_NUM or i == right_limit - 1:
              right_pivot = i - 1
              break
          else:
            if line[i] == co.FILLED_NUM:
              fill_flag = True
              left_pivot = i
              if i == right_limit - 1:
                right_pivot = i
                break

        for i in range(0, hint[cnt]):
          if right_pivot - i >= left_limit \
            and tmp_line[right_pivot - i] == co.UNSOLVED_NUM:
            tmp_line[right_pivot - i] = co.CHECK_NUM

          if left_pivot + i < right_limit \
            and tmp_line[left_pivot + i] == co.UNSOLVED_NUM:
            tmp_line[left_pivot + i] = co.CHECK_NUM

      for i in range(0, len(line)):
        if line[i] == co.UNSOLVED_NUM and tmp_line[i] != co.CHECK_NUM:
          line[i] = co.NO_FILLED_NUM

    return line

