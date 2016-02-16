#!/usr/bin/env python

import sys
import oauth2 as oauth
import time
import json
import urllib

TWEET_SIZE = 140
INITIAL_MSG = ".@NSAGov @stupidhackathon I just want a safer America"
TWEET_PREFIX = ".@NSAGov @stupidhackathon "
RATE_BUFFER_SECS = 7.0


# Set up instances of our Token and Consumer. The Consumer.key and
# Consumer.secret are given to you by the API provider. The Token.key and
# Token.secret is given to you after a three-legged authentication.
token = oauth.Token(key="4882253895-arMyoLh08m1gsYlDZP4mrHAFilc5IuS4grHvsF3", secret="BcbeqAu5cgdrfU5i48nQblkASUNKfiy1SlEhVDNZRDcGq")
consumer = oauth.Consumer(key="XgOrRE1xFOtw18Tixd7j6sl2G", secret="TiDS6b0fkmw6SwcnyDTtTRIkIjjUT7RPaI9C97aDRJnb4Tb3mX")
client = oauth.Client(consumer, token)


buffer = ''
def got_key(c):
    global buffer
    buffer += c
    if len(buffer) == TWEET_SIZE - len(TWEET_PREFIX):
        tweet(TWEET_PREFIX + buffer)
        buffer = ''
    pass


go_time, last_text = time.time(), None
def tweet(text):
    global go_time
    if time.time() < go_time:
        return

    # Twitter ignores duplicate tweets, so don't bother sending
    global last_text
    if text == last_text:
        print >>sys.stderr, "Dropping duplicate tweet"
        return
    last_text = text

    # Make request!
    url = "https://api.twitter.com/1.1/statuses/update.json"
    body = {'status': text}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    resp_headers, content = client.request(url, method='POST', headers=headers, body=urllib.urlencode(body))
    if int(resp_headers['status']) != 200:
        print >>sys.stderr, "Got", str(resp_headers['status']+':'), content
    if resp_headers['status'] == 429 or resp_headers.get('x-rate-limit-remaining', 1) == 0:
        print >>sys.stderr, 'Dropping until', go_time
        go_time = float(resp_headers['x-rate-limit-remaining']) + RATE_BUFFER_SECS


def run():
    if len(INITIAL_MSG):
        tweet(INITIAL_MSG)

    c = sys.stdin.read(1)
    while len(c) > 0:
        if len(c.strip()) > 0:
            got_key(c.strip())
        c = sys.stdin.read(1)


if __name__ == '__main__':
    run()
