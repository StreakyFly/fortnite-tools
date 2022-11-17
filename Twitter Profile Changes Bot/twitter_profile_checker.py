
import tweepy
import json
import time
import requests
from datetime import datetime


with open("twitter-keys.json") as file:
    keysjson = json.load(file)

accessToken = keysjson["access_token"]
accessTokenSecret = keysjson["access_token_secret"]
consumerKey = keysjson["consumer_key"]
consumerSecret = keysjson["consumer_secret"]

# users_removed_banner = []
posts_quantity = []


def jsonify_tweepy(tweepy_object):
    json_str = json.dumps(tweepy_object._json, indent=2)
    return json.loads(json_str)


def get_user_data(user_id):
    user_data = tweepy_api.get_user(user_id=user_id)
    # print(user_data)
    return user_data


def post_text(text):
    tweepy_api.update_status(status=text)
    print(text, "\nPosted!")
    posts_quantity.append((time.localtime()[2], time.localtime()[3]))


def post_1_img(text, image_name):
    image = tweepy_api.media_upload(image_name)
    tweepy_api.update_status(status=text, media_ids=[image.media_id])
    print(text, "Image name:", image_name, "\nPosted!")
    posts_quantity.append((time.localtime()[2], time.localtime()[3]))


def post_2_imgs(text, image_1_name, image_2_name):
    image_1 = tweepy_api.media_upload(image_1_name)
    image_2 = tweepy_api.media_upload(image_2_name)
    tweepy_api.update_status(status=text, media_ids=[image_1.media_id, image_2.media_id])
    print(text, "\nFirst image:", image_1_name, "\nSecond image:", image_2_name, "\nPosted!")
    posts_quantity.append((time.localtime()[2], time.localtime()[3]))


def location_rem_add(location, pronoun):
    if location[1] == "":
        return f"added {pronoun} location"
    elif location[2] == "":
        return f"removed {pronoun} location"
    else:
        return "location"


def all_profile_changes(user_id, pronoun, plural):
    username = jsonify_tweepy(get_user_data(user_id))['screen_name']
    lc = location_change(username, user_id)
    bc = banner_change(username, user_id)
    pc = profile_change(username, user_id)

    now = datetime.now()
    print(f"[{now.strftime('%d/%m/%Y-%H:%M:%S')}] {username:>15}: {lc} | {bc} | {pc}")

    if lc is None and bc is None and pc is None:
        pass

    # if all are changed, it posts them
    elif None not in (lc, bc, pc):
        if location_rem_add(lc, pronoun) == "location":
            post_2_imgs(f".@{username} {plural} just updated {pronoun} {bc[0]}, {pc} & {location_rem_add(lc, pronoun)}!\n\nBefore: '{lc[1]}'\nAfter: '{lc[2]}'",
                        f"Data/pfp_{username}.jpg", f"Data/banner_{username}.jpg")
        else:
            post_2_imgs(f".@{username} {plural} just updated {pronoun} {bc[0]} & {pc} and {location_rem_add(lc, pronoun)}!\n\nBefore: '{lc[1]}'\nAfter: '{lc[2]}'",
                        f"Data/pfp_{username}.jpg", f"Data/banner_{username}.jpg")

    # if two are changed, it posts them
    elif pc is not None and lc is not None:
        post_1_img(f".@{username} {plural} just updated {pronoun} {pc} and {location_rem_add(lc, pronoun)}!\n\nBefore: '{lc[1]}'\nAfter: '{lc[2]}'", f"Data/pfp_{username}.jpg")
    elif bc is not None and lc is not None:
        if bc[1] is False and lc[2] == "":
            post_1_img(f".@{username} {plural} just removed {pronoun} {bc[0]} and {lc[0]}!\n\nBefore: '{lc[1]}'\nAfter: '{lc[2]}'\n\nOld banner:", f"Data/banner_{username}.jpg")
        elif bc[1] is False and lc[1] == "":
            post_1_img(f".@{username} {plural} just removed {pronoun} {bc[0]} and added {pronoun} {lc[0]}!\n\nBefore: '{lc[1]}'\nAfter: '{lc[2]}'\n\nOld banner:", f"Data/banner_{username}.jpg")
        elif bc[1] is False and lc[1] != "":
            post_1_img(f".@{username} {plural} just removed {pronoun} {bc[0]} and updated {pronoun} {lc[0]}!\n\nBefore: '{lc[1]}'\nAfter: '{lc[2]}'\n\nOld banner:", f"Data/banner_{username}.jpg")
        elif bc[1] is True and lc[1] != "":
            post_1_img(f".@{username} {plural} just updated {pronoun} {bc[0]} and {location_rem_add(lc, pronoun)}!\n\nBefore: '{lc[1]}'\nAfter: '{lc[2]}'", f"Data/banner_{username}.jpg")
    elif bc is not None and pc is not None:
        if bc[1] is False:
            post_1_img(f".@{username} {plural} just removed {pronoun} {bc[0]} and updated {pronoun} {pc}!", f"Data/pfp_{username}.jpg")
        elif bc[1] is True:
            post_2_imgs(f".@{username} {plural} just updated {pronoun} {bc[0]} and {pc}!", f"Data/pfp_{username}.jpg", f"Data/banner_{username}.jpg")

    # if only one is changed, it posts it
    elif lc is not None:
        if lc[1] == "":
            post_text(f".@{username} {plural} just added {pronoun} {lc[0]}!\n\nBefore: '{lc[1]}'\nAfter: '{lc[2]}'")
        elif lc[2] == "":
            post_text(f".@{username} {plural} just removed {pronoun} {lc[0]}!\n\nBefore: '{lc[1]}'\nAfter: '{lc[2]}'")
        else:
            post_text(f".@{username} {plural} just updated {pronoun} {lc[0]}!\n\nBefore: '{lc[1]}'\nAfter: '{lc[2]}'")
    elif bc is not None:
        if bc[1] is False:
            post_1_img(f".@{username} {plural} just REMOVED {pronoun} {bc[0]}!", f"Data/banner_{username}.jpg")
        elif bc[1] is True:
            post_1_img(f".@{username} {plural} just updated {pronoun} {bc[0]}!", f"Data/banner_{username}.jpg")
    elif pc is not None:
        post_1_img(f".@{username} {plural} just updated {pronoun} {pc}!", f"Data/pfp_{username}.jpg")

    else:
        print("How did you even get this message? 🤨")


def location_change(username, user_id):
    new_location = jsonify_tweepy(get_user_data(user_id))['location']
    old_location_f = open(f"Data/location_{username}.txt", "r+")
    old_location = old_location_f.read()

    if new_location != old_location:
        old_location_f.truncate(0)
        old_location_f.seek(0)
        old_location_f.write(new_location)
        return "location", old_location, new_location
    else:
        pass
    old_location_f.close()


def banner_change(username, user_id):
    try:
        data = jsonify_tweepy(get_user_data(user_id))
        if 'profile_banner_url' in data:
            new_banner = data['profile_banner_url']
        else:
            new_banner = ""
        old_banner = open(f"Data/banner_url_{username}.txt", "r+")
        old_banner_str = old_banner.read()

        if new_banner != old_banner_str:
            print("Old banner string:", old_banner_str, "\nNew banner string:", new_banner)
            if new_banner == "":
                # print(username, users_removed_banner)
                # if username not in users_removed_banner:
                #     users_removed_banner.append(username)
                with open(f"Data/banner_url_{username}.txt", "w+"):
                    pass
                return "banner", False
            else:
                tweepy_api.media_upload(download_image(f"{new_banner}/1500x500", f"banner_{username}.jpg"))
                old_banner.truncate(0)
                old_banner.seek(0)
                old_banner.write(new_banner)
                old_banner.close()
                # print(username, users_removed_banner)
                # if username in users_removed_banner:
                #     users_removed_banner.remove(username)
                return "banner", True
        else:
            old_banner.close()
            # print(username, users_removed_banner)
            # if username in users_removed_banner:
            #     users_removed_banner.remove(username)

    except Exception as error1:
        print(f"A banner_change exception occurred: {error1}")


def profile_change(username, user_id):
    new_pfp = jsonify_tweepy(get_user_data(user_id))['profile_image_url'].replace("normal.jpg", "400x400.jpg").replace("normal.png", "400x400.png")
    old_pfp = open(f"Data/pfp_url_{username}.txt", "r+")
    old_pfp_str = old_pfp.read()

    if new_pfp != old_pfp_str:
        tweepy_api.media_upload(download_image(new_pfp, f"pfp_{username}.jpg"))
        old_pfp.truncate(0)
        old_pfp.seek(0)
        old_pfp.write(new_pfp)
        return "profile picture"
    else:
        pass
    old_pfp.close()


def download_image(image_url, image_name):
    img_data = requests.get(image_url).content
    with open(f"Data/{image_name}", "wb") as handler:
        handler.write(img_data)
    return f"Data/{image_name}"


# this is used to prevent unwanted tweet spam
def prevent_tweet_spam():
    if len(posts_quantity) > 0:
        if time.localtime()[2] != posts_quantity[0][0] or time.localtime()[3] != posts_quantity[0][1]:
            del posts_quantity[0]
        if len(posts_quantity) > 3:
            print("\n\nATTENTION!\nThe bot is going into SLEEP mode for the next 8 HOURS due to too many posts in the past hour."
                  "If you believe this is a mistake, simply restart the bot.")
            time.sleep(28800)


if __name__ == "__main__":
    while True:
        try:
            prevent_tweet_spam()
            authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)
            authenticate.set_access_token(accessToken, accessTokenSecret)
            tweepy_api = tweepy.API(authenticate)

            all_profile_changes(27280073, "his", "has")  # Donald Mustard's ID
            all_profile_changes(425871040, "their", "has")  # FortniteGame's ID
            # all_profile_changes(1105501165385584641, "his", "has")  # iStreakyFly's ID
            time.sleep(50)
        except Exception as error:
            print(f"An exception occurred: {error}")
            time.sleep(140)
