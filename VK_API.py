import requests
import datetime
from config import VK_TOKEN

version = 5.199
url_images = []

def get_post_info(post):
    global date_post, answer, url_images
    response = requests.get("https://api.vk.com/method/wall.getById",
                            params={
                                "access_token": VK_TOKEN,
                                "v": version,
                                "posts": post,
                            }
                            )

    data = response.json()

    if "copy_history" in data["response"]["items"][0]:
        answer = data["response"]["items"][0]["copy_history"][0]["text"]
        timestamp = data["response"]["items"][0]["date"]
        date_post = datetime.datetime.fromtimestamp(timestamp)
        i = 0
        while i < len(data["response"]["items"][0]["copy_history"][0]["attachments"]):
            if "photo" in data["response"]["items"][0]["copy_history"][0]["attachments"][i]:
                url_images.append(data["response"]["items"][0]["copy_history"][0]["attachments"][i]["photo"]["orig_photo"]["url"])
            i += 1
    else:
        answer = data["response"]["items"][0]["text"]
        timestamp = data["response"]["items"][0]["date"]
        date_post = datetime.datetime.fromtimestamp(timestamp)
        i = 0
        while i < len(data["response"]["items"][0]["attachments"]):
            if "photo" in data["response"]["items"][0]["attachments"][i]:
                url_images.append(data["response"]["items"][0]["attachments"][i]["photo"]["orig_photo"]["url"])
            i += 1

    return answer, date_post, url_images
