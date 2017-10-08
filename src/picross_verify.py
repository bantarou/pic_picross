#encoding:utf-8
import cv2
import numpy as np

#列が完成しているかの判定
def check_filled(tmp_boad):
  for i in range(0, len(tmp_boad)):
    if tmp_boad[i] == -1:
      return False

  return True

#確定したものと合致しないものを取り除く
def check_match(origin, now):
  for i in range(0, len(origin)):
    if (origin[i] == 0 and now[i] == 255) \
      or (origin[i] == 255 and now[i] == 0):
      return False

  return True

#考えられる全パターンを算出
def calc_all_pattern(hint, tmp_boad):
  boad_length = len(tmp_boad)
  hint_num = len(hint) - 1
  for i in range(0, len(hint)):
    hint_num += hint[i]

  #即答できる場合
  if boad_length == hint_num:
    for j in range(0, len(hint)):
      ret = np.empty(boad_length)
      count = 0
      if j != 0:
        empty[count] = 255
        count += 1
      for k in range(count, count + hint[j]):
        empty[k] = 0
      count += hint[j]
    
    if check_match(ret, tmp_boad):
      return ret
    else:
      ret = []
      return ret

  elif boad_length < hint_num:
    return False

  #hintが一つの場合(再帰終了)
  if len(hint) == 1:
    save = np.empty(boad_length)
    if hint[0] == 0:
      for i in range(0, boad_length):
        save[i] = 0
    elif hint[0] == boad_length:
      for i in range(0, boad_length):
        save[i] = 255
    else:
      #前後に空白が生じる場合
      before_space = 0
      before_max_space = boad_length - hint[0]
      while before_space <= before_max_space:
        after_space = boad_length - hint[0] - before_space
        tmp = np.empty(boad_length)
        for j in range(0,before_space):
          tmp[j] = 255
        for j in range(before_space, before_space + hint[0]):
          tmp[j] = 0
        for j in range(before_space + hint[0]):
          tmp[j] = 255
        np.append(save, tmp, axis = 0)

        space += 1

    ret = []
    for i in range(0, len(save)):
      if check_match(save[i], tmp_boad):
        ret.append(save[i])

    return ret

  #hintが複数の場合(hintを減らして再帰する)
  else:
    space_count = 0
    max_space_count = boad_length - hint_num
    save = np.zeros(boad_length)
    while space_count <= max_space_count:
      for i in range(0, space_count):
        save[i] = 255
      for i in range(space_count, hint[0]):
        save[i] = 0
      space_count += 1
      
      flag = True
      for i in range(0, hint[0] + 1):
        if (save[i] == 0 and tmp_boad[i] == 255) or \
          (save[i] == 255 and tmp_boad[i] == 0):
          flag = False

      if flag:
        #ヒントを減らして再帰
        new_hint = hint[1:]
        new_tmp_boad = tmp_boad[hint[0] + 1:]
        child_ret = calc_all_pattern(new_hint, new_tmp_boad)
        if len(child_ret) > 0 and child_ret:
          for j in range(0, len(child_ret)):


#第一段階の処理
def first_process(hint, length):
  if hint[0] == 0:
    #何も埋まらない場合
    ret = np.empty(length)
    return ret.fill(255)
  elif hint[0] == length:
    #すべてが埋まる場合
    ret = np.zeros(length)
    return ret

  total_num = len(hint) - 1
  max_num = 0
  for i in range(0, len(hint)):
    total_num += hint[i]
    if max_num < hint[i]:
      max_num = hint[i]

  #条件によって一意的に点が埋まる際の処理
  if(total_num == length):
    ret = np.empty(length)
    count = 0
    for i in range(0, len(hint)):
      #間の点
      if i != 0:
        ret[count] = 255
        count += 1

      for cnt in range(count, count + hint[i]):
        ret[cnt] = 0

      count += hint[i]

    return ret

  #条件によっていくつか点が定まる際の処理
  min_num = length - total_num
  if min_num < max_num:
    ret = np.empty(length)
    ret.fill(-1)
    count = 0
    for i in range(0, len(hint)):
      if i != 0:
        ret[count] == -1
        count += 1
      if hint[i] > min_num:
        for cnt in range(count, count + min_num):
          ret[cnt] = -1
        count += min_num
        for cnt in range(count, count + hint[i] - min_num):
          ret[cnt] = 0
        count += (hint[i] - min_num)
      else:
        for cnt in range(count, count + hint[i]):
          ret[cnt] = -1

        count += hint[i]
    return ret
  #何も埋まらない際の処理
  else:
    ret = np.empty(length)
    ret.fill(-1)

    return ret

#第二段階の処理
def secound_process(hint, tmp_boad):
  first = 0
  for i in range(0, len(tmp_boad)):
    if tmp_boad[first] == -1:
      break
    if tmp_boad[first] == 0:
      for cnt in range(0, hint[0]):
        tmp_boad[cnt] = 0
      tmp_boad[hint[0]] = 255
      break

    first += 1

  last = len(tmp_boad) - 1
  for i in range(0, len(tmp_boad)):
    if tmp_boad[last] != -1:
      break
    if tmp_boad[last] == 0:
      for cnt in range(len(tmp_boad) - hint[last], len(tmp_boad)):
        tmp_boad[cnt] = 0
      tmp_boad[last - hint[last]] = 255
      break

    last -= 1

  return tmp_boad

#三段階目の処理
def third_process(hint, tmp_boad):
  first = 0


#ピクロスの回答を行う関数
def calc_solutions(img, row_hint, col_hint, row_length, col_length):
  #ボードの情報
  boad_data = np.empty(shape = (row_length, col_length))
  boad_data.fill(-1)

  #一段階目の操作
  #行方向の捜査
  for i in range(0, row_length):
    tmp = first_process(row_hint[i], row_length)
    for cnt in range(0, len(tmp)):
      if boad_data[i][cnt] == -1:
        boad_data[i][cnt] = tmp[cnt]

  #列方向の捜査
  for i in range(0, col_length):
    tmp = first_process(col_hint[i], col_length)
    for cnt in range(0, len(tmp)):
      if boad_data[cnt][i] == -1:
        boad_data[cnt][i] = tmp[cnt]

  #二段階目の捜査
  #行方向の捜査
  for i in range(0, row_length):
    tmp = secound_process(row_hint[i], boad_data[i])
    boad_data[i] = tmp

  #列方向の捜査
  for i in range(0, col_length):
    tmp = secound_process(col_hint[i], boad_data[:,i])
    boad_data[:,i] = tmp

  #確定部分と未確定部分の判定
  check_row = []
  check_col = []
  for i in range(0, row_length):
    if check_filled(boad_data[i]):
      check_row.append(True)
    else:
      check_row.append(False)

  for i in range(0, col_length):
    if check_filled(boad_data[:,i]):
      check_col.append(True)
    else:
      check_col.append(False)

  print(boad_data)


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

  calc_solutions(img, tmp_row_hint, tmp_col_hint, row_length, col_length)

