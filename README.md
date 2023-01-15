# ○ を探せ!!

## 概要

- 起動方法は`python app.py`
  - `sched`などライブラリが入ってなければインストールしてください
- 10 秒間の間に丸を全部消せばクリア
  - 5 秒以内だと CONGRATULATIONS!!、5〜7 秒だと GREAT!、7〜9 秒だと GOOD(資料になかったので勝手に決めちゃいました、必要であれば 199 行目で変えてください)
- 三角をクリック or10 秒経ったらゲーム失敗となり FAILED!!を表示

## コード周り

- 6 行目の`WINDOW_WIDTH`と 7 行目の`WINDOW_HEIGHT`を変えて画面の縦横を設定
- 9 行目の`NUM_CIRCLE`で丸の数を設定
- 10 行目の`NUM_TRIANGLE`で三角の数を設定
- 12~14 行目で各種色を設定
  - デフォルトはタイマーが青、成功メッセージが緑、失敗メッセージが赤
- 構成
  - `Timer`クラス(時間管理)
  - `Position`クラス(二次元ベクトル)
  - `Position3D`クラス(三次元ベクトル)
  - `Circle`クラス(丸の図形)
  - `Triangle`クラス(三角の図形)
  - `App`クラス(メイン実行部分)

## 参考にしたサイト

- [pyxel の色々な実装例](https://github.com/kitao/pyxel/blob/main/docs/README.ja.md)
- [外積を使って三角形の内側かどうか判定する](https://gihyo.jp/dev/serial/01/as3/0055)
- [タイマー](https://teratail.com/questions/313239)
