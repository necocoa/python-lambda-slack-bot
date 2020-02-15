import os
import json
import boto3
import urllib3
from requests_oauthlib import OAuth1Session

# Twitter API TOKEN
CK = os.environ['CONSUMER_KEY']
CS = os.environ['CONSUMER_SECRET']
AT = os.environ['ACCESS_TOKEN']
AS = os.environ['ACCESS_TOKEN_SECRET']

# 環境変数を取得
BUCKET_NAME = os.environ['S3_BUCKET_NAME']
OBJECT_KEY_NAME = 'latest_tweet_id.txt'
SLACK_TOKEN = os.environ['SLACK_TOKEN']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']


# Lambda実行fanc
def lambda_handler(event, context):
    newest_tweet = get_newest_tweets()
    post_newest_tweet_to_slack(newest_tweet)


# 最新の差分ツイートを取得
def get_newest_tweets():
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    twitter = OAuth1Session(CK, CS, AT, AS)
    # 前回の最新ツイートIDを取得
    latest_tweet_id = get_latest_tweet_id_in_s3()
    # AtCoderの取得params
    params = {
        'user_id': 298062842,
        'count': 10,
        'exclude_replies': True,
        'include_rts': False,
        'since_id': latest_tweet_id
    }
    # Twitter APIにGET Request
    req = twitter.get(url, params=params)
    if req.status_code == 200:
        newest_tweet = json.loads(req.text)
        return newest_tweet
    else:
        return req.status_code


# S3に保存した最新のツイートIDを取得
def get_latest_tweet_id_in_s3():
    # S3オブジェクトを取得
    s3 = boto3.client('s3')
    # S3から指定したファイルオブジェクトを取得
    object = s3.get_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY_NAME)
    # objectのBodyを取得
    body = object['Body'].read()
    # バイト列を文字列にデコード
    body_str = body.decode('utf-8')
    return body_str


# newest_tweetを昇順でslackにpost
def post_newest_tweet_to_slack(newest_tweet):
    if isinstance(newest_tweet, int):
        print('TwitterAPI status: %s' % newest_tweet)
    else:
        if newest_tweet:
            # 最新ツイートIDをS3に保存
            put_latest_tweet_id_in_s3(newest_tweet[0]['id_str'])
            for line in reversed(newest_tweet):
                if 'ABC' in line['text'] or 'AtCoder Beginner Contest' in line['text']:
                    post_message_to_slack(line['text'])


# S3に最新のツイートIDを保存
def put_latest_tweet_id_in_s3(latest_tweet_id):
    s3 = boto3.client('s3')
    # S3にアップロード
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=OBJECT_KEY_NAME,
        ContentType='text/plain',
        Body=latest_tweet_id
    )


# Slackにメッセージをpost
def post_message_to_slack(text):
    url = 'https://slack.com/api/chat.postMessage'
    http = urllib3.PoolManager()
    method = 'POST'
    headers = {
        'Content-type': 'application/json; charset=utf-8',
        'Authorization': ('Bearer %s' % SLACK_TOKEN)
    }
    # PythonオブジェクトをJSONに変換する
    data = {
        'channel': SLACK_CHANNEL,
        'text': text
    }
    encoded_data = json.dumps(data).encode('utf-8')
    # httpリクエストを準備してPOST
    req = http.request(method, url, body=encoded_data, headers=headers)
    if req.status == 200:
        res = json.loads(req.data.decode('utf-8'))
        if res['ok'] == False:
            print('SlackAPI error messsage: %s' % res['error'])
    else:
        print('SlackAPI status: %s' % req.status)
