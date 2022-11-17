
from requests import get
from time import sleep, localtime
from datetime import datetime
import tweepy
import json
from PIL import Image
import os
import platform


script = os.path.realpath(__file__)
if platform.system() == "Windows":
    path_list = script.split("\\")
    cwd = "\\".join(path_list[:-1]) + "\\"
elif platform.system() == "Linux":
    path_list = script.split("/")
    cwd = "/".join(path_list[:-1]) + "/"
else:
    print("PLATFORM UNDEFINED! (not in [Windows, Linux], Stopping...")
    exit()

posts_quantity = []

with open(f"{cwd}twitter-keys.json") as file:
    keysjson = json.load(file)

accessToken = keysjson["access_token"]
accessTokenSecret = keysjson["access_token_secret"]
consumerKey = keysjson["consumer_key"]
consumerSecret = keysjson["consumer_secret"]


def main():
    response = get("https://fn-api.com/api/backgrounds").json()['data']['lobby']

    background_link = response['image']
    background_name = response['name']  # always seems to be 'default'?

    with open(f"{cwd}old_url.json") as f:
        old_link = json.load(f)

    if background_link != old_link:
        print(f"[{datetime.now()}] | New lobby background named: '{background_name}'.\nImage URL: {background_link}")
        download_image(background_link)
        # tweet_image(f"New #Fortnite Lobby Background! (name: '{background_name}')", "lobby_background.jpg")
        tweet_image(f"New #Fortnite Lobby Background!", "lobby_background.jpg")

        with open(f"{cwd}old_url.json", "w") as f:  # saves the new lobby background link to the file
            json.dump(background_link, f)


def resize_image():
    image = Image.open(f"{cwd}lobby_background.jpg")
    new_res_image = image.resize((2048, 1152))
    new_res_image.save("lobby_background.jpg")


def download_image(image_url):
    img_data = get(image_url).content
    with open(f"{cwd}lobby_background.jpg", "wb") as handler:
        handler.write(img_data)
    resize_image()


def tweet_image(text, image_name):
    print("Uploading image to twitter...")
    image = tweepy_api.media_upload(image_name)
    print("Uploaded. Posting...\n")
    tweepy_api.update_status(status=text, media_ids=[image.media_id])
    print(f"{text}\nImage name: {image_name}\nPosted!\n\n")
    posts_quantity.append((localtime()[2], localtime()[3]))


def prevent_tweet_spam():
    if len(posts_quantity) > 0:
        if localtime()[2] != posts_quantity[0][0] or localtime()[3] != posts_quantity[0][1]:
            del posts_quantity[0]
        if len(posts_quantity) > 3:
            print("\n\nATTENTION!\nThe bot is going into SLEEP mode for the next 8 HOURS due to too many posts in the past hour."
                  "If you believe this is a mistake, simply restart the bot.")
            sleep(28800)


if __name__ == "__main__":
    while True:
        try:
            authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)
            authenticate.set_access_token(accessToken, accessTokenSecret)
            tweepy_api = tweepy.API(authenticate)

            prevent_tweet_spam()
            main()
            sleep(50)
        except Exception as e:
            print("An exception occurred: " + str(e))
            sleep(150)
