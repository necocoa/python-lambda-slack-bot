# python-lambda-slack-bot
[Lambda : Python]AtCoderのABCコンテスト情報を取得してSlackに投稿するプログラム

## 事前準備
### 必要なライブラリをカレントディレクトリにインストール
`pip install boto3 -t .`

`pip install requests_oauthlib -t .`

### カレントディレクトリをzip化する
`zip -r lambda_coins.zip ./`

### Lambdaにアップロードする
zip化したフォルダをアップロード

### Lambdaの環境変数を設定する
#### Twitter API
CONSUMER_SECRET

CONSUMER_KEY

ACCESS_TOKEN

ACCESS_TOKEN_SECRET
#### S3 Bucket Name
S3_BUCKET_NAME

### LET's RUN!!!