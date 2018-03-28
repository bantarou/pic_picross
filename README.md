pic_picross
===

## Overview
画像データからピクロス(お絵かきロジック)を生成するプログラムです。<BR>
実際に回答可能な問題の場合、解答用紙と答えの画像データが出力されます。<BR>
回答不可能な場合はErrorと表示され、何も出力されません。

## Requirement
- Python3 (more ver3.2)
- OpenCV
- Numpy

## Usage
`$ python3 make_picross.py <image_file_path> <picorss_size>`

コードを実行するとimgディレクトリが生成され、それ以下に作成したピクロスの画像データが保存されます。

## Example
`$ python3 make_picross.py test_img/test1.png 20`
![test1](https://github.com/bantarou/image/blob/master/pic_picross_test1.png)

`$ python3 make_picross.py -r test_img/test2.png 45`
![test2](https://github.com/bantarou/image/blob/master/pic_picross_test2.png)ic_picross
