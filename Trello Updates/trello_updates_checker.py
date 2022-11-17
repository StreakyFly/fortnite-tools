
import requests
import json
import tweepy
import time
from colorama import Fore, Style

"""
 - It compares old IDs with current ones. If there's a different one, it posts contents of that card.
 - If len(name) + len(desc) less than 280, it adds both, otherwise only the name. If there's still place left, it also
 adds 'Workaround' and/or the rest.
 
  - I was planning to calculate Priority Score for each piece of info*, and then make all possible combinations under
  280 characters and tweet the one with the highest total Priority Score... BUTT
  considering there is not that many options, I decided to hardcode it.
  It checks if description + workaround fit under 280 char (these two usually hold the most important info), if not, it
  tries with name + workaround (name is usually a shorter version of description), if not, it only tries description,
  and finally if that doesn't work, it posts just the name.

*All useful thingy thingies:
 - Name
 - Description
 - Workaround
 - Platform
 - Example
 - List Name (Battle Royale Top Issues, Creative Top Issues, STW TI, Switch & Mobile TI)
"""

rc = Style.RESET_ALL

with open("twitter-keys.json") as file:
    keysjson = json.load(file)

accessToken = keysjson["access_token"]
accessTokenSecret = keysjson["access_token_secret"]
consumerKey = keysjson["consumer_key"]
consumerSecret = keysjson["consumer_secret"]

posts_quantity = []


list_ids = {"issue": "5d42ac7f1de207797fe9222d",
            "Battle Royale issue": "5a8ae9c6b95d537ef2173cd3",
            "Creative issue": "5c091fe07b09812cc6e55a54",
            "Save the World issue": "5a8ae9c6b95d537ef2173cd2",
            "Mobile/Switch issue": "5b7582903bdc2e2f5821d6f1"}

# gets ALL cards on board
# cards_response = requests.get("https://api.trello.com/1/boards/5a8ae9c6b95d537ef2173cd1/cards/").json()
# print(cards_response.json())

# for x in cards_response:
#     print(x['id'])
#     response = requests.get(url=f"https://api.trello.com/1/cards/{x['id']}", headers={"Accept": "application/json"})
#     print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

# print("\nTotal number of cards on this board is:", len(cards_response))


def main():
    card_ids_file = open("card_ids.json")
    old_card_ids = json.load(card_ids_file)

    new_card_ids = []
    for list_n in list_ids:
        list_id = list_ids[list_n]
        cards_from_list = requests.get(f"https://api.trello.com/1/lists/{list_id}/cards", ).json()

        for card in cards_from_list:
            card_id = card['id']
            new_card_ids.append(card_id)
            if card_id not in old_card_ids:
                time.sleep(150)  # waits in case they change anything real quick (which they did multiple times)
                print(f"\n\n--------------------/CARD\--------------------\n")
                card_data = requests.get(url=f"https://api.trello.com/1/cards/{card_id}").json()

                final = f"Epic is aware of the following {list_n}:\n"
                card_name = card_data['name']

                if card_name[-1] not in ".!?" and card_name[-2] not in ".!?":
                    final += card_name + "."
                else:
                    final += card_name

                try:
                    card_desc = card_data['desc']

                    cd_rn = card_desc.replace("\n", "")
                    # DO NOT. AND I REPEAT. DO NOT QUESTION ME ABOUT THIS.
                    cd_r = cd_rn.replace("--------------------------", "").replace("-------------------------", "").replace("------------------------", "")\
                        .replace("-----------------------", "").replace("----------------------", "").replace("---------------------", "").\
                        replace("--------------------", "").replace("-------------------", "").replace("------------------", "")\
                        .replace("-----------------", "").replace("----------------", "").replace("---------------", "")\
                        .replace("--------------", "").replace("-------------", "").replace("------------", "")\
                        .replace("-----------", "").replace("----------", "").replace("---------", "").replace("--------", "")\
                        .replace("-------", "").replace("------", "").replace("-----", "").replace("----", "")

                    cd_parsed = cd_r.split("**")[1:]
                    if "Fort-" in cd_parsed[1][-12:] or "FORT-" in cd_parsed[1][-12:]:
                        cd_parsed[1] = cd_parsed[1].split("Fort-", 1)[0]
                        cd_parsed[1] = cd_parsed[1].split("FORT-", 1)[0]
                    if len(cd_parsed) > 2 and ("Fort-" in cd_parsed[3][-12:] or "FORT-" in cd_parsed[3][-12:]):
                        cd_parsed[3] = cd_parsed[3].split("Fort-", 1)[0]
                        cd_parsed[3] = cd_parsed[3].split("FORT-", 1)[0]
                    try:
                        if len(cd_parsed) > 4 and ("Fort-" in cd_parsed[5][-10:] or "FORT-" in cd_parsed[5][-10:]):
                            cd_parsed[5] = cd_parsed[5].split("Fort-", 1)[0]
                            cd_parsed[5] = cd_parsed[5].split("FORT-", 1)[0]
                    except IndexError:
                        pass

                    try:
                        cd_parsed = cd_parsed[:cd_parsed.index("JIRA")]
                    except:
                        try:
                            cd_parsed = cd_parsed[:cd_parsed.index("Jira")]
                        except ValueError:
                            pass

                    if len(cd_parsed) > 8:
                        print(f"{Fore.LIGHTRED_EX}Elements length: {len(cd_parsed)}{rc}")
                        print(f"{Fore.YELLOW}\n{cd_parsed}\n{rc}")
                    else:
                        if "Workaround" in cd_parsed or "Workaround:" in cd_parsed and len((final + "\n\n" + cd_parsed[0] + ": " + cd_parsed[1] + "\n\n" + cd_parsed[2] + ": " + cd_parsed[3])) > 280:
                            cd_parsed = cd_parsed[2:]

                        card_dict = {}
                        for num, item in enumerate(cd_parsed):
                            if num % 2 == 0:
                                if str(item).endswith(':'):
                                    item = item[:-1]
                                card_dict[item] = cd_parsed[num + 1]

                        for info in card_dict:
                            data = card_dict[info].strip()
                            if data[-1] not in ".!?" and data[-2] not in ".!?":
                                data = card_dict[info] + "."
                            if len((final + "\n\n" + info + ": " + data)) < 280:
                                # print("1:", len((final + "\n\n" + info + ": " + data)))
                                final += f"\n\n{info}: {data}"
                                # print("2:", len(final))

                except Exception as e:
                    print("Error: ", e, "\n")

                print(final)
                tweepy_api.update_status(status=final)
                print("Posted!")
                posts_quantity.append((time.localtime()[2], time.localtime()[3]))

    card_ids_file.close()

    # at the end of the program, it updates the json file with new card IDs
    with open("card_ids.json", "w") as file:
        json.dump(new_card_ids, file, indent=4)


def prevent_tweet_spam():
    if len(posts_quantity) > 0:
        if time.localtime()[2] != posts_quantity[0][0] or time.localtime()[3] != posts_quantity[0][1]:
            del posts_quantity[0]
        if len(posts_quantity) > 5:
            print("\n\nATTENTION!\nThe bot is going into SLEEP mode for the next 8 HOURS due to too many posts in the past hour."
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
            time.sleep(60)
        except Exception as error:
            print(f"An exception occurred: {error}")
            time.sleep(150)


# gets the board info... kinda? (not all labels)
# board_response = requests.get(url="https://api.trello.com/1/boards/Bs7hgkma", headers={"Accept": "application/json"})
# print(json.dumps(json.loads(board_response.text), sort_keys=True, indent=4, separators=(",", ": ")))

# gets info about specific card
# response = requests.get(url="https://api.trello.com/1/cards/620d35e09983d78999bd6d75", headers={"Accept": "application/json"})
# print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

# gets all labels
# labels_response = requests.get("https://api.trello.com/1/boards/5a8ae9c6b95d537ef2173cd1/labels")
# print(labels_response.text)

# gets all lists
# response = requests.get("https://api.trello.com/1/boards/Bs7hgkma/lists")
# print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

# gets cards in a list
# response = requests.get("https://api.trello.com/1/lists/5a8ae9c6b95d537ef2173cd3/cards",)
# print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
