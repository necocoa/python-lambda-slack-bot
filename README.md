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
#### TwitterAPIの環境変数
CONSUMER_SECRET

CONSUMER_KEY

ACCESS_TOKEN

ACCESS_TOKEN_SECRET
#### S3BucketNameの環境変数
S3_BUCKET_NAME

#### SlackAPIの環境変数
SLACK_TOKEN

SLACK_CHANNEL

### LET's RUN!!!