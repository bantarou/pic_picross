#encoding:utf-8
import cv2
import numpy as np

from image_processing import *
from picross_graphic import *
from picross_processing import *

#
# 定数定義
#
ORG_WINDOW_NAME = "org"
GRAY_WINDOW_NAME = "gray"
CANNY_WINDOW_NAME = "canny"
MOSAIC_WINDOW_NAME = "mosaic"

ORG_FILE_NAME = "../test_img/test1.png"
GRAY_FILE_NAME = "../test_img/gray.png"
CANNY_FILE_NAME = "../test_img/canny.png"
MOSAIC_FILE_NAME = "../test_img/mosaic.png"


# 元の画像を読み込む
org_img = cv2.imread(ORG_FILE_NAME, cv2.IMREAD_UNCHANGED)
# グレースケールに変換
gray_img = cv2.imread(ORG_FILE_NAME, cv2.IMREAD_GRAYSCALE)

#画像のぼかし処理
gray_img = blur_image(gray_img, 1)
# エッジ抽出
canny_img = cv2.Canny(gray_img, 50, 120)

mosaic_img = convert_mosaic(ORG_FILE_NAME, 0, 12, 0.0002)

draw_main(mosaic_img, 11)

#
# ウィンドウに表示
#
cv2.namedWindow(ORG_WINDOW_NAME)
cv2.namedWindow(GRAY_WINDOW_NAME)
cv2.namedWindow(CANNY_WINDOW_NAME)
cv2.namedWindow(MOSAIC_WINDOW_NAME)



cv2.imshow(ORG_WINDOW_NAME, org_img)
cv2.imshow(GRAY_WINDOW_NAME, gray_img)
cv2.imshow(CANNY_WINDOW_NAME, canny_img)
cv2.imshow(MOSAIC_WINDOW_NAME, mosaic_img)

#
# ファイルに保存
#
cv2.imwrite(GRAY_FILE_NAME, gray_img)
cv2.imwrite(CANNY_FILE_NAME, canny_img)

#
# 終了処理
#
cv2.waitKey(0)
cv2.destroyAllWindows()

