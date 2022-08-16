# snail_shogi
カタツムリのようにとてもとても遅い将棋のライブラリ

# 概要
- 将棋を自力実装してみた
- 今のところはPython標準ライブラリすらimportしていない。(setup.py以外)
- 大変汚い実装・驚異的遅さ・そして低機能
- リバーシ(オセロ)版はこちら: https://github.com/YuaHyodo/snail_reversi

# 機能
- 合法手生成などの基本的な機能
- USIプロトコルのmoveによる盤面操作、sfenによる盤面セット、現局面に対応するsfenの生成などの機能

# 想定している使い方
- 探索部・機械学習のような速度が非常に重要な部分ではなく、対局サーバーやGUIでの合法手チェックなどの部分に使用する事を想定して設計している。
- 以上の理由から、高速化にリソースを費やす予定は無い。
- 速度が欲しい方は、cshogi( https://github.com/TadaoYamaoka/cshogi )、
python-shogi( https://github.com/gunyarakun/python-shogi )あたりを使う事を強く推奨する。

# 皆さんのPCで使えるようにする方法
- snail_shogiは、Ari-Shogi-Server( https://github.com/YuaHyodo/Ari-Shogi-Server )などの実行に必要です。
- 注意: 間違っているやり方の可能性が非常に高い
- 警告: このやり方でのインストールはまだ試していない。
- 間違いの指摘を大募集

## 手順
- 1: ダウンロードする
- 2: コマンドプロンプトを開く
- 3: cdコマンドでsetup.pyがあるディレクトリまで移動する
- 4: "python setup.py install"と入力してエンターキーを押す
- 5: 終わり

# ライセンス
- snail_shogiはMITライセンスです。
- 詳細はLICENSEファイルをご確認ください。
