
import requests
import json
import time
import tweepy
from datetime import datetime
import re
from pytube import YouTube
from colorama import Fore, Style
import traceback


rc = Style.RESET_ALL


with open("twitter-keys.json") as file:
    keysjson = json.load(file)

accessToken = keysjson["access_token"]
accessTokenSecret = keysjson["access_token_secret"]
consumerKey = keysjson["consumer_key"]
consumerSecret = keysjson["consumer_secret"]

posts_quantity = []
posts = []
video_data = []


def main():
    response = requests.get("https://fn-api.com/api/blogposts").json()

    if response:
        data = response['data']

        data_fn = data['fortnite']
        # data_cm = data['competitive']

        updated_fn = data_fn['updated']
        # updated_cm = data_cm['updated']
        new_hash_fn = data_fn['hash']
        # hash_cm = data_cm['hash']

        posts_fn = data_fn['posts']
        # posts_cm = data_cm['posts']

        # now = datetime.now()
        # print(f"[{now.strftime('%d/%m/%Y-%H:%M:%S')}] {new_hash_fn} | {updated_fn}")  # e062bffa8aa9bb88733bc80a4d9e9fcbb3149bd5 | 2022-03-23T23:59:50.884Z
        # print(hash_cm)  # e18e09168859c7316276cefb8631ccff91467224
        # print(updated_cm)  # 2022-03-23T14:52:59.560Z

        with open("hash_fn.txt", "r") as hash_file:
            old_hash_fn = hash_file.read()

        if new_hash_fn != old_hash_fn:  # add 'or True' when testing
            blog_ids_file = open("blog_ids.json", "r")
            old_blog_ids = json.load(blog_ids_file)

            new_blog_ids = []
            for post in posts_fn:
                id = post['id']
                url = post['url']

                new_blog_ids.append(id)

                if id not in old_blog_ids:
                    now = datetime.now()
                    curr_date = now.strftime("%Y-%m-%d")  # "%Y-%m-%d" removed -%d in case it appears a second before the next day
                    post_date = post['date']

                    print("CURR:", str(curr_date), "POST:", str(post_date))
                    if str(curr_date) in str(post_date):  # add 'or True' when testing
                        now = datetime.now()
                        print(f"{Fore.RED}-------------------------------------------------------{rc}\n"
                              f"[{now.strftime('%d/%m/%Y-%H:%M:%S')}] {new_hash_fn} | {updated_fn}\n"
                              f"{Fore.LIGHTGREEN_EX}Added blog ID: {rc}{id}\n"
                              f"{Fore.GREEN}Blog date: {rc}{post_date}\n"
                              f"{Fore.GREEN}Curr date: {rc}{now}\n"
                              f"{Fore.GREEN}Blog URL: {rc}{url}\n")

                        blog_title = post['title']
                        blog_description = post['description']

                        if blog_title is not None and blog_description is not None and \
                                (blog_title.lower() == blog_description.lower() or blog_title.lower() in blog_description.lower()):
                            final_both = final_title = final_desc = f"{blog_description}\n\n🔗 {url}"
                        else:
                            final_both = final_title = final_desc = None
                            if blog_title is not None and blog_description is not None:
                                final_both = f"{blog_title}\n\n{blog_description}\n\n🔗 {url}"
                                # print("BOTH: ", final_both)
                            if blog_title is not None:
                                final_title = f"{blog_title}\n\n🔗 {url}"
                                # print("TITLE: ", blog_title)
                            if blog_description is not None:
                                final_desc = f"{blog_description}\n\n🔗 {url}"
                                # print("DESC: ", blog_description)

                        """
                        pls don't question me about this try/except hell
                        I was like: one try/except can't hurt. Then I added another. And another. And another and so on...
                        What all this mess does is basically, it tries posting different combinations of info on that blog, from the one
                        with most important info to less and less. First it tries to tweet a video and some text and if the video or the text
                        is too long, it tries a different video or image on that blog and different text etc. until it can finally post it.
                        This is a great example of how you should NOT write your programs...
                        """
                        try:
                            try:
                                # print(re.findall("(?P<url>https?://[^\s]+.mp4)", str(post)))
                                video_url = re.search("(?P<url>https?://[^\s]+.mp4)", str(post['content'])).group("url")
                                print("Selected blogpost video URL (NOT from Youtube):\n", video_url)
                                media = download_file(video_url)
                                print(f"Local video filename: {Fore.LIGHTYELLOW_EX}{media}{rc}")
                            except:
                                if "https://www.youtube.com/" in post['content']:
                                    links = re.findall('"(https://www.youtube.com/.*?)"', post['content'])
                                    print("All Youtube video URLs:\n", links)
                                    x = 0
                                    try:
                                        if YouTube(links[x]).length < 140:
                                            video_url = links[x]
                                        else:
                                            while YouTube(links[x]).length >= 140:
                                                video_url = links[x]
                                                x += 1
                                        print(f"Selected Youtube video url: {video_url}")
                                        media = download_video(video_url)
                                    except:
                                        image_url = post['images']['share']
                                        if image_url is None:
                                            image_url = post['images']['image']
                                        print("Image URL:", image_url)
                                        media = download_image(image_url)
                                else:
                                    image_url = post['images']['share']
                                    if image_url is None:
                                        image_url = post['images']['image']
                                    print("Image URL:", image_url)
                                    media = download_image(image_url)

                            if "blog_image.jpg" in media:
                                if blog_title is not None and blog_description is not None:
                                    try:
                                        tweet_image(final_both, media)
                                    except Exception as e:
                                        print("EXCEPTION: ", e)
                                        try:
                                            tweet_image(final_desc, media)
                                        except Exception as e:
                                            print("EXCEPTION: ", e)
                                            tweet_image(final_title, media)
                                elif blog_description is not None:
                                    try:
                                        tweet_image(final_desc, media)
                                    except Exception as e:
                                        print("EXCEPTION: ", e)
                                elif blog_title is not None:
                                    try:
                                        tweet_image(final_title, media)
                                    except Exception as e:
                                        print("EXCEPTION: ", e)

                            else:
                                # print(blog_title, "\n", blog_description, type(blog_description))
                                if blog_title is not None and blog_description is not None:
                                    try:
                                        tweet_video(final_both, media)
                                    except Exception as e:
                                        print("EXCEPTION: ", e)
                                        try:
                                            try:
                                                tweet_video(final_desc, media)
                                            except Exception as e:
                                                print("EXCEPTION: ", e)
                                                tweet_video_retry(final_desc, media, video_data[0])
                                        except Exception as e:
                                            print("EXCEPTION: ", e)
                                            try:
                                                tweet_video(final_title, media)
                                            except Exception as e:
                                                print("EXCEPTION: ", e)
                                                tweet_video_retry(final_title, media, video_data[0])
                                elif blog_description is not None:
                                    try:
                                        tweet_video(final_desc, media)
                                    except Exception as e:
                                        print("EXCEPTION: ", e)
                                elif blog_title is not None:
                                    try:
                                        tweet_video(final_title, media)
                                    except Exception as e:
                                        print("EXCEPTION: ", e)

                        except Exception as error:
                            print(f"{Fore.RED}An exception occurred: {error}.\nTHE BLOGPOST HAS NOT BEEN POSTED!{rc}")

            with open("blog_ids.json", "w+") as f:
                json.dump(new_blog_ids, f, indent=4)
            with open("hash_fn.txt", "w") as hash_file:
                hash_file.write(new_hash_fn)
            print("File 'blog_ids.json' updated!")


def tweet_image(text, image_name):
    if text in posts:
        print(f"{Fore.RED}Duplicate post. Skipping...{rc}")
    else:
        print("Uploading image to twitter...")
        image = tweepy_api.media_upload(image_name)
        print("Uploaded. Posting...\n")
        tweepy_api.update_status(status=text, media_ids=[image.media_id])
        print(f"{Fore.BLUE}{text}{rc}\nImage name: {Fore.LIGHTYELLOW_EX}{image_name}{rc}\nPosted!\n")
        posts.append(text)
        posts_quantity.append((time.localtime()[2], time.localtime()[3]))


def tweet_video(text, video_name):
    if text in posts:
        print(f"{Fore.RED}Duplicate post. Skipping...{rc}")
    else:
        video_data.clear()
        if video_name.endswith(".mp4"):
            video_file_name = f"videos/{video_name}"
        else:
            video_file_name = f"videos/{video_name}.mp4"
        print("Uploading video to twitter...")
        video = tweepy_api.media_upload(filename=video_file_name, media_category="TWEET_VIDEO")
        video_data.append(video)
        print(f"Uploaded video data: {Fore.YELLOW}{video}{rc}\nPosting...\n")
        tweepy_api.update_status(status=text, media_ids=[video.media_id])
        print(f"{Fore.BLUE}{text}{rc}\n\nVideo name: {Fore.LIGHTYELLOW_EX}{video_name}{rc}\nPosted!\n")
        posts.append(text)


def tweet_video_retry(text, video_name, video):
    """
    if it retries tweeting because of too long text, this function is used, so the video
    that was fine, does not need to be uploaded to twitter servers once again
    """
    if text in posts:
        print(f"{Fore.RED}Duplicate post. Skipping...{rc}")
    else:
        print("Retrying posting with less text...")
        tweepy_api.update_status(status=text, media_ids=[video.media_id])
        print(f"{Fore.BLUE}{text}{rc}\nVideo name: {Fore.LIGHTYELLOW_EX}{video_name}{rc}\nPosted!\n")
        posts.append(text)


def download_video(video_url):
    video = YouTube(video_url)
    print(f"\nDownloading {Fore.LIGHTGREEN_EX}{video.length}s long video{rc} titled: {Fore.LIGHTBLUE_EX}{video.title}{rc}."
          f" Video data: {Fore.YELLOW}{video.streams.get_highest_resolution()}{rc}.")
    video.streams.get_highest_resolution().download("videos")
    print("Video downloaded.")
    return video.title


def download_image(image_url):
    img_data = requests.get(image_url).content
    with open("blog_image.jpg", "wb") as handler:
        handler.write(img_data)
    return "blog_image.jpg"


def download_file(url):
    """
    can be either a pic or a video, but i will be using it for html5
    videos that aren't on youtube but only on the blogpost
    """
    filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    print("Downloading file (video)...")
    with open(f"videos/{filename}", 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush()  # commented by recommendation from J.F.Sebastian
    return filename


def prevent_tweet_spam():
    if len(posts_quantity) > 0:
        if time.localtime()[2] != posts_quantity[0][0] or time.localtime()[3] != posts_quantity[0][1]:
            del posts_quantity[0]
        if len(posts_quantity) > 3:
            print(f"{Fore.RED}\n\nATTENTION!\nThe bot is going into SLEEP mode for the next 8 HOURS due to too many posts in the past hour. "
                  "If you believe this is a mistake, simply restart the bot.{rc}")
            time.sleep(28800)


if __name__ == "__main__":
    while True:
        try:
            prevent_tweet_spam()
            if len(posts) > 10:
                del posts[0]
            authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)
            authenticate.set_access_token(accessToken, accessTokenSecret)
            tweepy_api = tweepy.API(authenticate)

            main()
            time.sleep(25)
        except Exception as error:
            print(f"{Fore.RED}An exception occurred: {error}\n{traceback.format_exc()}{rc}")
            time.sleep(100)

