import os
import json
import boto3
from requests_oauthlib import OAuth1Session

# TwitterのOAuth1設定
CK = os.environ['CONSUMER_KEY']
CS = os.environ['CONSUMER_SECRET']
AT = os.environ['ACCESS_TOKEN']
AS = os.environ['ACCESS_TOKEN_SECRET']
twitter = OAuth1Session(CK, CS, AT, AS)

# 環境変数からBucket名を取得
BUCKET_NAME = os.environ['S3_BUCKET_NAME']
OBJECT_KEY_NAME = 'latest_tweet_id.txt'


# Lambda実行fanc
def lambda_handler(event, context):
    newest_tweet = _get_newest_tweets()
    if isinstance(newest_tweet, int):
        print(newest_tweet)
    else:
        for line in reversed(newest_tweet):
            print('**********************')
            print(line['id_str'])
            print(line['text'])


def _get_newest_tweets():
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    _put_latest_tweet_id_in_s3('1226505925210435584')
    latest_tweet_id = _get_latest_tweet_id_in_s3()
    params = {
        "user_id": 298062842,
        "count": 10,
        "exclude_replies": True,
        "include_rts": False,
        "since_id": latest_tweet_id
    }
    req = twitter.get(url, params=params)
    if req.status_code == 200:
        newest_tweet = json.loads(req.text)
        return newest_tweet
    else:
        return req.status_code


# S3に保存した最新のツイートIDを取得
def _get_latest_tweet_id_in_s3():
    # S3オブジェクトを取得
    s3 = boto3.client('s3')
    # S3から指定したファイルオブジェクトを取得
    object = s3.get_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY_NAME)
    # objectのBodyを取得
    body = object['Body'].read()
    # バイト列を文字列にデコード
    body_str = body.decode('utf-8')
    return body_str


# S3に最新のツイートIDを保存
def _put_latest_tweet_id_in_s3(latest_tweet_id):
    s3 = boto3.client('s3')
    # S3にアップロード
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=OBJECT_KEY_NAME,
        ContentType='text/plain',
        Body=latest_tweet_id
    )
