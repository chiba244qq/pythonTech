# マイクロサービス

# 自己紹介

# この発表の目的
- マイクロサービスアーキテクチャを知ってもらう
- 有効性を体験してもらう

# マイクロサービス(MSA)とは
What  
  マイクロサービスは、協調して動作する小規模で自律的なサービス  

Why  
  ビジネスの変化の速度に、ソフトウェアのリリース速度を追いつかせるため  
（速さが欲しい!!）

$ それっぽいこと、言ってますけど基本概念は
$  対して難しくありません。

# 我々が目指すべき
  必要とされている物を、よりシンプルに、より速く

# 導入企業
Netflix, Cookpad, Yahoo! Japan, Amazon, Microsoft...

大規模なサービスを運営している企業ばかり

# 動向とトレンド
SOAとMSAのトレンド比較グラフ  
https://trends.google.co.jp/trends/explore?date=today%205-y&q=Microservices%20architecture,service%20oriented%20architecture

# 複雑で大きなシステムを速く作るには
大きなシステムを、小さくさなサービスに分割して統治すること

## みなさんに質問
みなさんは...
- プログラマ
- アーキテクト
- インフラエンジニア..etc

## プログラマのみなさんに質問
プログラムを書く上で気をつけることは?
(優れたプログラムとは?)

## イメージ
プログラミングと同じで、システムも大きいものは制御が難しい
だから、小さく作って組み合わせる。

# プログラムの複雑さとは
でかい1つの関数と、関数化されたプログラムでどちらが
優れているか選んでもらう
(コードの比較画像でもつける)

大きさが2倍 ≠ 複雑さ2倍

## 大きいものはコントールが難しい
あるPJで突貫工事で作成したPJを優秀な技術者を含む10人で  
 1年以上かけてリファクタ(爆弾解体的な作業)
➡︎　S-Inしてからサービスを細分化していくことは非常に難しい

$ 大きなシステムを組み立てるこよりも、小さく分割していくことの方が何倍も難しい。

## 例外
プロトタイプ作成等の状況で、大きく作ってしまうことの方が、
細かく作ることよりも速く簡単であることがあるのは認めるが
サービスを継続的に開発していきたいなら、細かく分割して作り上げていくべき。

$ プロトタイプはプロトタイプでしかない

では、どのように分割するか...

## 基本的な考え方はプログラムも同じ

## プログラミングの場合
モジュール結合度、モジュール強度　
モジュール間の結合度は疎結合の方が良いし、
凝縮性（強度）は高い方がいいと言われているよね(基本情報レベル？)

内容結合 ... データ結合
https://qiita.com/eKushida/items/39bdb3f88fb68ecd66f6

## システムの場合も同じ
疎結合,　高凝縮

「単一責任の原則」（Single Responsibility Principle)
変更する理由が同じものは集める、変更する理由が違うものは分ける
➡︎ある、塊（モジュール/サービス）は単一の機能のみをもつべき

## サービスの分割手法
DDD(Domain Driven Design=ドメイン駆動設計)  
➡︎出発地点は、システム化対象そのものを観察し、
　そこで得た知識を、取捨選択し、抽象化してモデル化していく。
　モデルは実際の業務と結びつきを持っている。

## 例えば
ショッピングサイトなら、
- カタログ
- カート
- 配達
- 在庫管理
- レコメンド
- 注文
- レビュー

## 余談) ...といっても、どこまで小さくすればいいか
マイクロサービスを「2 週間で書き直せるもの」と言っている人もいる。  
➡︎ どのPJにも当てはまる指針を定義されてはいないが、  
　サービスを構築/修正/デプロイするにあったって、他のサービスへストレスを  
　与えない作りになっていることが基本的な基準

# マイクロサービスアーキテクチャが可能になった技術的背景
ここ10年で変わってきたこと
## クラウドが柔軟な構成変更/スケールアウト能力を与えた  
　サービス性能をあげたい場合は、インスタンスの追加/性能増強による
　水平/垂直なスケールアウトが可能

  クラウド登場以前は、サービスを追加しようとするたびに  
  性能の見積もり ＋ ハードウェア選定 ＋ 物理的/論理的なネットワーク設計 ＋
  データセンターのラックの確保...

## Dockerなどのコンテナ(管理)技術によって、手軽で迅速なデプロイ能力を与えた
  コンテナ登場以前のデプロイは、  
  よくて数GiBの仮想マシンイメージをアップロードしてデプロイ。
  悪くて、環境構築用のshellを流して結果を目視確認...etc  
  デプロイおよびその計画の作成で1週間以上かかることもあった。

## XML -> JSON -> ... GraphQL?
  サービス間の通信は、XMLベースのSOAPなどが使用されてきたが、
  最近では、JSONで十分であることがわかってきた。


#マイクロサービス技術的な要素
##  デザインパターン
- API Gateway : App/Web向けにAPIを集約する
- Service Registry / Service Discovery：サービス群の登録管理/検出を管理する
- Circuit Breaker : 障害時に該当APIを遮断し、影響がサービス全体へ波及するのを防止する
- Polyglot Persistence : 異なるデータベースを統合する
- Command Query Responsibility Segregation (CQRS) : 副作用のあるコマンド(書き込み)と副作用のないクエリ(よみこみ)を完全に分けて管理する
- Tolerant Reader : 相互接続性のために、送信は厳密に、受信は寛容に行う
- Chained Services : サービスが数珠つなぎに接続し通信を行う。Linux のパイプの概念に似ているが、分岐することも可能
- Asynchronous Messaging : メッセージを複数のサービスで非同期に共有する
- Bulkhead : システム障害を局所化するために、同一システムを構築しておく
- Service Instantiation : サービスをVM単位やホスト単位でインスタンス化する

# 実践


## Case 1 サービス間インタフェース仕様書 編

## Case 2 仕様フレームワーク選定編


# メリット/デメリット
  ・個々のサービス中で使用する技術が選択できる



# 実習
