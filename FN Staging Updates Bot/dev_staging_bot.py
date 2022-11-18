
import requests
import json
import tweepy
import time
from datetime import datetime


with open("twitter-keys.json") as file:
    keysjson = json.load(file)

accessToken = keysjson["access_token"]
accessTokenSecret = keysjson["access_token_secret"]
consumerKey = keysjson["consumer_key"]
consumerSecret = keysjson["consumer_secret"]

posts_quantity = []


"""
it checks if there's a new version, that's not in stage_versions; if it's not, it tweets it and adds it to the file
it checks if there's a new version, that's not in test_versions; if it's not, it tweets it and adds it to the file
"""


def main():
    response = requests.get("https://api.nitestats.com/v1/epic/staging/fortnite").json()

    stage_v_save_read = []
    test_v_save_read = []

    with open("stage_versions.json") as sf:
        stage_versions = json.load(sf)
    with open("test_versions.json") as tf:
        test_versions = json.load(tf)

    for server in response:
        new_version = response[server]['version']

        if server in ("FortniteStageMain", "FortniteStageNSCert", "CertStagingB", "CertStagingC") and\
                new_version not in stage_versions and new_version not in stage_v_save_read and\
                any(char.isdigit() for char in new_version):  # checks if it includes numbers
            text = f"⬆️ v{new_version} has been added to the Staging servers! Expect the update next week."
            now = datetime.now()
            print(f"[{now.strftime('%d/%m/%Y-%H:%M:%S')}] {new_version} - {server}")
            try:
                tweet_image(text, "images/clock_purple.jpg")
            except:
                tweepy_api.update_status(status=text)
            posts_quantity.append((time.localtime()[2], time.localtime()[3]))
            stage_v_save_read.append(new_version)
            stage_versions.append(new_version)
            print(text)
            print("Posted!\n")

        elif new_version not in test_versions and new_version not in test_v_save_read and\
                any(char.isdigit() for char in new_version):
            text = f"Epic started testing v{new_version}! 🛠️"
            now = datetime.now()
            print(f"[{now.strftime('%d/%m/%Y-%H:%M:%S')}] {new_version} - {server}")
            try:
                tweet_image(text, "images/tools_2.jpg")
            except:
                tweepy_api.update_status(status=text)
            posts_quantity.append((time.localtime()[2], time.localtime()[3]))
            test_v_save_read.append(new_version)
            test_versions.append(new_version)

            print(text)
            print("Posted!\n")

    with open("stage_versions.json", "w") as f:
        json.dump(stage_versions, f, indent=0, separators=(',', ': '))
    with open("test_versions.json", "w") as f:
        json.dump(test_versions, f, indent=0, separators=(',', ': '))

    stage_v_save_read.clear()
    test_v_save_read.clear()


def tweet_image(text, image):
    print("Uploading image to twitter...")
    image = tweepy_api.media_upload(image)
    print("Uploaded. Posting...")
    tweepy_api.update_status(status=text, media_ids=[image.media_id])


# this is used to prevent unwanted tweet spam
def prevent_tweet_spam():
    if len(posts_quantity) > 0:
        if time.localtime()[2] != posts_quantity[0][0] or time.localtime()[3] != posts_quantity[0][1]:
            del posts_quantity[0]
        if len(posts_quantity) > 3:
            print(
                "\n\nATTENTION!\nThe bot is going into SLEEP mode for the next 8 HOURS due to too many posts in the past hour."
                " If you believe this is a mistake, simply restart the bot.")
            time.sleep(28800)


if __name__ == "__main__":
    while True:
        try:
            prevent_tweet_spam()

            authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)
            authenticate.set_access_token(accessToken, accessTokenSecret)
            tweepy_api = tweepy.API(authenticate)

            main()
            time.sleep(20)
        except Exception as error:
            print(f"An exception occurred: {error}")
            time.sleep(90)
