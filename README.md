# snail_shogi
カタツムリのようにとてもとても遅い将棋のライブラリ

# 概要
- 将棋を自力実装してみた(まだ途中)
- 今のところはPython標準ライブラリすらimportしていない。(setup.py以外)
- 大変汚い実装・驚異的遅さ・そして低機能
- リバーシ(オセロ)版はこちら: https://github.com/YuaHyodo/snail_reversi

# 機能
- 合法手精製などの基本的な機能(バグあり)
- USIプロトコルのmoveによる盤面操作、sfenによる盤面セット、現局面に対応するsfenの生成などの機能

# 想定している使い方
- 探索部・機械学習のような速度が非常に重要な部分ではなく、対局サーバーやGUIでの合法手チェックなどの部分に使用する事を想定して設計している。
- 速度が欲しい方は、cshogi( https://github.com/TadaoYamaoka/cshogi )、
python-shogi( https://github.com/gunyarakun/python-shogi )あたりを使う事を強く推奨する。

# ライセンス
- snail_shogiはMITライセンスです。
- 詳細はLICENSEファイルをご確認ください。
