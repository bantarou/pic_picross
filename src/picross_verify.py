#encoding:utf-8
import cv2
import numpy as np

from picross_boad_info import boad_infomation as info
from constants import constans as co

#エラー検出用関数
def error_check(line, origin_line, hint):
  for i in range(0, len(line)):
    if line[i] != co.UNSOLVED_NUM:
      if line[i] != origin_line[i]:
        print(i, line[i], origin_line[i])
        print("error_line", line)
        print("error_origin", origin_line)
        print("error_hint", hint)
        assert False, 'Verify Error'

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

#列の全てのマスが回答できる場合の処理
def first_process(boad, row_hint, col_hint):
  row_length = len(boad)
  col_length = len(boad[0])
  for i in range(0, row_length):
    if row_hint[i][0] == 0:
      for j in range(0, col_length):
        boad[i][j] = co.NO_FILLED_NUM
    if row_hint[i][0] == col_length:
      for j in range(0, col_length):
        boad[i][j] = co.FILLED_NUM

  for j in range(0, col_length):
    if col_hint[j][0] == 0:
      for i in range(0, row_length):
        boad[i][j] = co.NO_FILLED_NUM
    if col_hint[j][0] == row_length:
      for i in range(0, row_length):
        boad[i][j] = co.FILLED_NUM
  return boad


#左右詰めにした際回答できる場合の処理
def secound_process(boad, row_hint, col_hint):
  row_length = len(boad)
  col_length = len(boad[0])

  #行方向の処理
  for i in range(0, row_length):
    line = calc_marge_part(row_hint[i], row_length)

    for j in range(0, len(line)):
      if line[j] == co.FILLED_NUM:
        boad[i][j] = line[j]

  #列方向の処理
  for j in range(0, col_length):
    line = calc_marge_part(col_hint[j], col_length)

    for i in range(0, len(line)):
      if line[i] == co.FILLED_NUM:
        boad[i][j] = line[i]

  return boad

#上下左右の端の部分が確定する場合の処理
def third_process(line, hint):

  def third_process_main(line, hint):
    hint_cnt = 0
    fill_count = 0
    fill_flag = False
    for j in range(0, len(line)):
      if fill_flag:
        if fill_count != 0:
          line[j] = co.FILLED_NUM
        else:
          line[j] = co.NO_FILLED_NUM
        fill_count -= 1
        if fill_count < 0:
          fill_flag = False
          hint_cnt += 1
      else:
        if line[j] == co.UNSOLVED_NUM:
          break
        if line[j] == co.FILLED_NUM:
          fill_count = hint[hint_cnt] - 1
          fill_flag = True
    return line

  line = third_process_main(line, hint)
  line = third_process_main(line[::-1], hint[::-1])
  line = line[::-1]

  #確定部分の数=ヒントの合計数の場合の埋めの処理
  line = fill_line(line, hint)
  
  return line

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
    reverse_length_num = np.copy(length_num)[::-1]
    for cnt in range(0, len(length_num) - 1):
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

  fill_flag = False
  if pivot + tmp_hint[0] < len(line)\
    and line[pivot + tmp_hint[0]] == co.NO_FILLED_NUM:
    for i in range(pivot, pivot + tmp_hint[0]):
      if line[i] == co.FILLED_NUM:
        fill_flag = True
        break

  if pivot + tmp_hint[0] > len(line) - 1:
    return line

  for i in range(pivot, pivot + tmp_hint[0] - 1):
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
      tmp_line = calc_marge_part([hint[cnt]], no_filled_sparse[cnt][1] - no_filled_sparse[cnt][0])
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

  tmp_line = calc_marge_part(tmp_hint, len(line) - pivot_left - pivot_right)

  for i in range(pivot_left, len(line) - pivot_right):
    if tmp_line[i - pivot_left] == co.FILLED_NUM:
      line[i] = co.FILLED_NUM

  return line

#埋まらないマスを推定する処理
def fourth_process(line, hint):
  #左右から行う必要がある処理
  line = check_around_filled(line, hint)
  line = check_around_filled(line[::-1],hint[::-1])
  line = line[::-1]
  line = check_sparse_justified(line, hint)
  line = check_sparse_justified(line[::-1], hint[::-1])
  line = line[::-1]

  #一方向からで十分な処理
  line = check_sparse_min(line, hint)
  line = check_around_max(line, hint)
  line = check_length(line, hint)
  return line

#マスを推定して埋める処理
def fifth_process(line, hint):
  #左右から行う必要がある処理
  line = fill_edge(line, hint)
  line = fill_edge(line[::-1], hint[::-1])
  line = line[::-1]

  #一方向からで十分な処理
  line = fill_divide_justified(line, hint)
  line = fill_divide_hint(line, hint)

  return line

#フラグの初期化用関数
def init_check(boad, row_flag, col_flag):
  for i in range(0, len(row_flag)):
    row_flag[i] = True
    for j in range(0, len(col_flag)):
      if boad[i][j] == co.UNSOLVED_NUM:
        row_flag[i] = False
        break

  for j in range(0, len(col_flag)):
    col_flag[j] = True
    for i in range(0, len(row_flag)):
      if boad[i][j] == co.UNSOLVED_NUM:
        col_flag[j] = False
        break
  return row_flag, col_flag

#
def line_check(line):
  for i in range(0, len(line)):
    if line[i] == co.UNSOLVED_NUM:
      return False
  return True

#盤面が埋まっているかの判定関数
def filled_check(row_flag, col_flag):
  for cnt in range(0, len(row_flag)):
    if not row_flag[cnt]:
      return False
  for cnt in range(0, len(col_flag)):
    if not col_flag[cnt]:
      return False
  return True

#ピクロスを回答する関数
def solve_picross(row_hint, col_hint, row_length, col_length, origin):
  #盤面
  boad = np.zeros(shape = (row_length, col_length))
  boad.fill(co.UNSOLVED_NUM)

  row_flag = np.zeros(row_length, dtype = bool)
  row_flag.fill(False)
  col_flag = np.zeros(col_length, dtype = bool)
  col_flag.fill(False)

  #最初の処理
  boad = first_process(boad, row_hint, col_hint)
  #二番目の処理
  boad = secound_process(boad, row_hint, col_hint)
  #フラグの初期化
  row_flag, col_flag = init_check(boad, row_flag, col_flag)

  solve_cnt = 0

  while not filled_check(row_flag, col_flag):
    #行方向の処理
    for i in range(0, row_length):
      if not row_flag[i]:
        line = third_process(boad[i], row_hint[i])
        line = fourth_process(boad[i], row_hint[i])
        line = fifth_process(boad[i], row_hint[i])

        error_check(line, origin[i], row_hint[i])

        if line_check(line):
          row_flag[i] = True

    #列方向の処理
    for j in range(0, col_length):
      if not col_flag[j]:
        line = third_process(boad[:,j], col_hint[j])
        line = fourth_process(boad[:,j], col_hint[j])
        line = fifth_process(boad[:,j], col_hint[j])

        error_check(line, origin[:,j], col_hint[j])

        if line_check(line):
          col_flag[j] = True

    if solve_cnt > co.MAX_LOOP_VERIFY:
      break
    solve_cnt += 1

  return boad

#ピクロスの確認用関数
def picross_check(img):
  row_length = len(img)
  col_length = len(img[0])
  import sys
  for i in range(0, row_length):
    for j in range(0, col_length):
      if img[i][j] == co.FILLED_NUM:
        sys.stdout.write("o")
      elif img[i][j] == co.NO_FILLED_NUM:
        sys.stdout.write("x")
      else:
        sys.stdout.write("-")
    sys.stdout.write("\n")

#テスト用関数
def verify_test():
  line = np.array( [ 255,  255,  255,  255,    0,    0,  255,   -1,   -1,   -1,   -1,   -1,   -1,   -1,  255,   -1,   -1,   -1,   -1,   -1,    0,   -1,    0,    0,   -1,   -1,   -1,   -1,    0,    0,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,   -1,  255,    0,    0,  255])
  hint = np.array([2, 10, 2, 2, 3, 1, 1, 2])

  print(line)
  line = fill_edge(line, hint)
  print(line)
  #line = third_process(line, hint)
  #line = fifth_process(line, hint)


#ピクロスが回答可能かどうかの検証用関数
def picross_verify(img, row_hint, col_hint):

  row_length = len(img)
  col_length = len(img[0])
  #ヒントを数字の2次元配列に変換
  tmp_row_hint = []
  tmp_col_hint = []
  #列方向のヒントの処理
  for y in range(0, row_length):
    hint = row_hint[y].split(',')
    hint = list(map(int, hint))
    tmp_row_hint.append(hint)
  #行方向のヒントの処理
  for x in range(0, col_length):
    hint = col_hint[x].split(',')
    hint = list(map(int, hint))
    tmp_col_hint.append(hint)

  verify_test()

  solve = solve_picross(tmp_row_hint, tmp_col_hint, row_length, col_length, img)
  picross_check(solve)

