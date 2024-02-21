#!/usr/bin/env python
# coding: utf-8

# In[8]:



import requests
import json
import re
import urllib.parse
import os
import configs as cf


# In[9]:


# Define the path to your JSON file here. 
# For example, if your JSON file is in the same directory as your notebook, just use the file name.
json_file_path = r"C:\Users\mnsnn\Documents\AI\AI Assisted Reels Generator\AI-Assisted-Content-Creator\twitter-video-dl\src\twitter_video_dl\RequestDetails.json"

json_file_path = os.path.join(cf.FILE_PATH, cf.twdl_path, cf.rqdetails_json_path)

"""
Hey, thanks for reading the comments.  I love you.
Here's how this works:
1. To download a video you need a Bearer Token and a guest token.  The guest token definitely expires and the Bearer Token could, though in practice I don't think it does.
2. Use the video id get both of those as if you were an unauthenticated browser.
3. Call "TweetDetails" graphql endpoint with your tokens.
4. TweetDetails response includes a 'variants' key which is a list of video urls and details.  Find the one with the highest bitrate (bigger is better, right?) and then just download that.
5. Some videos are small.  They are contained in a single mp4 file.  Other videos are big.  They have an mp4 file that's a "container" and then a bunch of m4s files.  Once we know the name of the video file we are looking for we can look up what the m4s files are, download all of them, and then put them all together into one big file.  This currently all happens in memory.  I would guess that a very huge video might cause an out of memory error.  I don't know, I haven't tried it.
5. If it's broken, fix it yourself because I'm very slow.  Or, hey, let me know, but I might not reply for months.
"""

request_details = json.load(open(json_file_path, 'r'))

features, variables = request_details['features'], request_details['variables']


# In[10]:


def get_tokens(tweet_url):
    """
    Welcome to the world of getting a bearer token and guest id.
    1. If you request the twitter url for the tweet you'll get back a blank 'tweet not found' page.  In the browser, subsequent javascript calls will populate this page with data.  The blank page includes a script tag for a 'main.js' file that contains the bearer token.
    2. 'main.js' has a random string of numbers and letters in the filename.  We will request the tweet url, use a regex to find our unique main.js file, and then request that main.js file.
    3. The main.js file contains a bearer token.  We will extract that token and return it.  We can find the token by looking for a lot of A characters in a row.
    4. Now that we have the bearer token, how do we get the guest id?  Easy, we activate the bearer token to get it.
    """

    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
        "Accept": "*/*",
        "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "TE": "trailers",
    }

    html = requests.get(tweet_url, headers=headers)

    assert html.status_code == 200, f'Failed to get tweet page.  If you are using the correct Twitter URL this suggests a bug in the script.  Please open a GitHub issue and copy and paste this message.  Status code: {html.status_code}.  Tweet url: {tweet_url}'

    mainjs_url = re.findall(r'https://abs.twimg.com/responsive-web/client-web-legacy/main.[^\.]+.js', html.text)

    assert mainjs_url is not None and len(
        mainjs_url) > 0, f'Failed to find main.js file.  If you are using the correct Twitter URL this suggests a bug in the script.  Please open a GitHub issue and copy and paste this message.  Tweet url: {tweet_url}'

    mainjs_url = mainjs_url[0]

    mainjs = requests.get(mainjs_url)

    assert mainjs.status_code == 200, f'Failed to get main.js file.  If you are using the correct Twitter URL this suggests a bug in the script.  Please open a GitHub issue and copy and paste this message.  Status code: {mainjs.status_code}.  Tweet url: {tweet_url}'

    bearer_token = re.findall(r'AAAAAAAAA[^"]+', mainjs.text)

    assert bearer_token is not None and len(
        bearer_token) > 0, f'Failed to find bearer token.  If you are using the correct Twitter URL this suggests a bug in the script.  Please open a GitHub issue and copy and paste this message.  Tweet url: {tweet_url}, main.js url: {mainjs_url}'

    bearer_token = bearer_token[0]
    
    # get the guest token
    with requests.Session() as s:
 
        s.headers.update({
            "user-agent"	:	"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
            "accept"	:	"*/*",
            "accept-language"	:	"de,en-US;q=0.7,en;q=0.3",
            "accept-encoding"	:	"gzip, deflate, br",
            "te"	:	"trailers",})
            
        s.headers.update({"authorization"	:	f"Bearer {bearer_token}"})

        # activate bearer token and get guest token
        guest_token = s.post(
            "https://api.twitter.com/1.1/guest/activate.json").json()["guest_token"]


    assert guest_token is not None, f'Failed to find guest token.  If you are using the correct Twitter URL this suggests a bug in the script.  Please open a GitHub issue and copy and paste this message.  Tweet url: {tweet_url}, main.js url: {mainjs_url}'

    return bearer_token, guest_token


# In[11]:


def get_tweet_details(tweet_url, guest_token, bearer_token):
    tweet_id = re.findall(r'(?<=status/)\d+', tweet_url)

    assert tweet_id is not None and len(
        tweet_id) == 1, f'Could not parse tweet id from your url.  Make sure you are using the correct url.  If you are, then file a GitHub issue and copy and paste this message.  Tweet url: {tweet_url}'

    tweet_id = tweet_id[0]

    # the url needs a url encoded version of variables and features as a query string
    url = get_details_url(tweet_id, features, variables)

    details = requests.get(url, headers={
        'authorization': f'Bearer {bearer_token}',
        'x-guest-token': guest_token,
    })

    max_retries = 10
    cur_retry = 0
    while details.status_code == 400 and cur_retry < max_retries:
        try:
            error_json = json.loads(details.text)
        except:
            assert False, f'Failed to parse json from details error. details text: {details.text}  If you are using the correct Twitter URL this suggests a bug in the script.  Please open a GitHub issue and copy and paste this message.  Status code: {details.status_code}.  Tweet url: {tweet_url}'

        assert "errors" in error_json, f'Failed to find errors in details error json.  If you are using the correct Twitter URL this suggests a bug in the script.  Please open a GitHub issue and copy and paste this message.  Status code: {details.status_code}.  Tweet url: {tweet_url}'

        needed_variable_pattern = re.compile(r"Variable '([^']+)'")
        needed_features_pattern = re.compile(r'The following features cannot be null: ([^"]+)')

        for error in error_json["errors"]:
            needed_vars = needed_variable_pattern.findall(error["message"])
            for needed_var in needed_vars:
                variables[needed_var] = True

            needed_features = needed_features_pattern.findall(error["message"])
            for nf in needed_features:
                for feature in nf.split(','):
                    features[feature.strip()] = True

        url = get_details_url(tweet_id, features, variables)

        details = requests.get(url, headers={
            'authorization': f'Bearer {bearer_token}',
            'x-guest-token': guest_token,
        })

        cur_retry += 1

        if details.status_code == 200:
            # save new variables
            request_details['variables'] = variables
            request_details['features'] = features

            with open(request_details_file, 'w') as f:
                json.dump(request_details, f, indent=4)

    assert details.status_code == 200, f'Failed to get tweet details.  If you are using the correct Twitter URL this suggests a bug in the script.  Please open a GitHub issue and copy and paste this message.  Status code: {details.status_code}.  Tweet url: {tweet_url}'

    return details


# In[12]:


def get_details_url(tweet_id, features, variables):
    # create a copy of variables - we don't want to modify the original
    variables = {**variables}
    variables["tweetId"] = tweet_id

    return f"https://twitter.com/i/api/graphql/0hWvDhmW8YQ-S_ib3azIrw/TweetResultByRestId?variables={urllib.parse.quote(json.dumps(variables))}&features={urllib.parse.quote(json.dumps(features))}"


# In[19]:


def get_description_details(tweet_url, guest_token, bearer_token):
    
    tweet_details = get_tweet_details(tweet_url, guest_token, bearer_token)
    tweet_json = tweet_details.json()

    # Collecting the tweet description
    tweet_description = tweet_json['data']['tweetResult']['result']['legacy']['full_text']
    
    # Collecting the profile name for credits
    profile_name = tweet_json['data']['tweetResult']['result']['core']['user_results']['result']['legacy']['screen_name']
    
    return profile_name, tweet_description


# In[20]:


def get_description(tweet_url):
    
    bearer_token, guest_token = get_tokens(tweet_url)
    
    profile_name, tweet_description = get_description_details(tweet_url, guest_token, bearer_token)
    
    return profile_name, tweet_description





