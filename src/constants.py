#encoding:utf-8

#定数クラス
class constans:
  #
  # 画面表示に関係する定数
  #

  #画面の端のマージン領域の設定
  WINDOW_MARGIN_WIDTH = 25
  WINDOW_MARGIN_HEIGHT = 25

  #
  #ピクロスの生成に関係する定数
  #

  #検証用関数のループ上限
  MAX_LOOP_VERIFY = 5

  #塗りつぶしを意味する数値
  FILLED_NUM = 0
  #塗られてないことを意味する数値
  NO_FILLED_NUM = 255
  #塗りが確定していないことを意味する数値
  UNSOLVED_NUM = -1

  #
  # ピクロスのマス目の描画　に関係する定数
  #

  #普通の線の太さ
  NORMAL_LINE_SIZE = 0.5
  #太線の太さ
  BOLD_LINE_SIZE = 1.5
  #太線を引く間隔
  BOLD_LINE_SPAN = 5

  #
  # 数字の表示に関係する定数
  #
  #ヒントのフォント
  HINT_FONT = 'fixsys'
  #ヒントのフォントサイズ
  HINT_FONT_SIZE = 6
  #ヒント部分と線とのマージンの長さ
  ROW_HINT_LINE_HEIGHT_MARGIN = 1.5
  ROW_HINT_LINE_WIDTH_MARGIN = 5
  COLUMN_HINT_LINE_HEIGHT_MARGIN = 5
  COLUMN_HINT_LINE_WIDTH_MARGIN = 5
  #列方向のヒントの各数値の間隔
  COLUMN_HINT_NUM_MARGIN = 9

  #ヒントとなる数字の1文字あたりの表示領域
  HINT_MARGIN_WIDTH = 7

