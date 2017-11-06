#encoding:utf-8
import cv2
import numpy as np

from constants import constans as co

#左右詰めの回答の共通部分を返す関数
def calc_marge_part(hint, row_length, col_length):
  tmp_num = 0
  tmp1 = np.empty(col_length)
  tmp2 = np.empty(col_length)
  tmp1.fill(co.UNSOLVED_NUM)
  tmp2.fill(co.UNSOLVED_NUM)

  num_tmp1 = np.empty(col_length)
  num_tmp2 = np.empty(col_length)
  num_tmp1.fill(-1)
  num_tmp2.fill(-1)

  for cnt in range(0, len(hint)):
    for j in range(tmp_num, tmp_num + hint[cnt]):
      tmp1[j] = co.FILLED_NUM
      num_tmp1[j] = cnt
    tmp_num += hint[cnt]
    if tmp_num < row_length:
      tmp1[tmp_num] = co.NO_FILLED_NUM
      tmp_num += 1

  tmp_num = col_length
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
  ans = np.empty(col_length)
  for i in range(0, col_length):
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
    line = calc_marge_part(row_hint[i], row_length, col_length)

    for j in range(0, len(line)):
      if line[j] == co.FILLED_NUM:
        boad[i][j] = line[j]

  #列方向の処理
  for j in range(0, col_length):
    line = calc_marge_part(col_hint[j], col_length, row_length)

    for i in range(0, len(line)):
      if line[i] == co.FILLED_NUM:
        boad[i][j] = line[i]

  return boad

#上下左右の端の部分が確定する場合の処理
def third_process(line, hint):
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
    elif line[j] == co.UNSOLVED_NUM:
      break
    elif line[j] == co.FILLED_NUM:
      fill_count = hint[hint_cnt] - 1
      fill_flag = True

  hint_cnt = len(hint) - 1
  fill_count = 0
  fill_flag = False
  for j in range(0, len(line))[::-1]:
    if fill_flag:
      if fill_count != 0:
        line[j] = co.FILLED_NUM
      else:
        line[j] = co.NO_FILLED_NUM
      fill_count -= 1
      if fill_count < 0:
        fill_flag = False
        hint_cnt -= 1
    elif line[j] == co.UNSOLVED_NUM:
      break
    elif line[j] == co.FILLED_NUM:
      fill_count = hint[hint_cnt] - 1
      fill_flag = True

  #確定部分の数=ヒントの合計数の場合の埋めの処理
  line = fill_line(line, hint)
  return line

#確実に黒マスが届かないマスの処理
def check_length(line, hint):
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

  #重複している塊が存在した場合処理を停止
  if len(length_num) == len(hint):
    for cnt in range(0, len(length_num) - 1):
      if not (length_num[cnt][0] + hint[cnt]) < (length_num[cnt + 1][1] - 1):
        return line

  tmp_line = np.copy(line)
  if len(length_num) == len(hint):
    for cnt in range(0, len(length_num)):
      for i in range(0, hint[cnt]):
        right_pivot = sum(length_num[cnt]) - 1 
        left_pivot = length_num[cnt][1]
        if right_pivot - i >= 0 and tmp_line[right_pivot - i] == co.UNSOLVED_NUM:
          tmp_line[right_pivot - i] = co.CHECK_NUM

        if left_pivot + i < len(line) and tmp_line[left_pivot + i] == co.UNSOLVED_NUM:
          tmp_line[left_pivot + i] = co.CHECK_NUM

    for i in range(0, len(line)):
      if line[i] == co.UNSOLVED_NUM and tmp_line[i] != co.CHECK_NUM:
        line[i] = co.NO_FILLED_NUM

  return line




#狭小マスの処理
def check_sparse(line, hint):
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


  #確定しているヒントを削除する処理
  delete_num = []
  for cnt in range(0, len(hint)):
    for cnt2 in range(0, len(solved_num)):
      if hint[cnt] == solved_num[cnt2]:
        delete_num.append(cnt)

  tmp_hint = hint.copy()
  print("before", hint)
  tmp_hint = np.delete(tmp_hint, delete_num, 0)

  if len(tmp_hint) > 0:
    min_hint = min(tmp_hint)
  else:
    min_hint = 0
  for cnt in range(0, len(sparse_num)):
    if sparse_num[cnt][0] < min_hint:
      for i in range(sparse_num[cnt][1], sum(sparse_num[cnt])):
        line[i] = co.NO_FILLED_NUM

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

  continue_flag = True

  #ヒントをコピー
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

#分断されたマスの処理
def fill_divide(line, hint):
  print(line)

#埋まらないマスを推定する処理
def fourth_process(line, hint):
  line = check_around_filled(line, hint)
  line = check_around_filled(line[::-1],hint[::-1])
  line = line[::-1]
  line = check_around_max(line, hint)
  line = check_sparse(line, hint)
  line = check_length(line, hint)
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
def solve_picross(row_hint, col_hint, row_length, col_length):
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
        if line_check(line):
          row_flag[i] = True

    #列方向の処理
    for j in range(0, col_length):
      if not col_flag[j]:
        line = third_process(boad[:,j], col_hint[j])
        line = fourth_process(boad[:,j], col_hint[j])
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
  line = np.array([0, -1, -1, -1, 0, -1, -1, -1, -1 , -1, -1, -1])
  hint = np.array([1, 2, 5])

  line = check_around_filled(line, hint)
  print(line)
  line = check_around_filled(line[::-1],hint[::-1])
  line = line[::-1]
  print(line)
  line = check_around_max(line, hint)
  print(line)
  line = check_sparse(line, hint)
  line = check_length(line, hint)
  print(line)

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

  solve = solve_picross(tmp_row_hint, tmp_col_hint, row_length, col_length)
  picross_check(solve)

