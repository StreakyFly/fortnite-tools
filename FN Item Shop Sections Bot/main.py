
import requests
import tweepy
from config import Keys, Customisation, Platform
import time
import json
from collections import Counter
from datetime import datetime


# if Platform.wxPython_library is True:
#     try:
#         import wx
#         wx_imported = True
#     except:
#         print("The 'wxPython' library has failed to import!")


if not all((Keys.consumer_key, Keys.consumer_secret_key, Keys.access_token, Keys.access_token_secret)):
    print("\n\nWARNING!\nYou have not entered your Twitter API keys into the 'config.py' file!"
          "\nThis bot will not be able to tweet unless you enter these keys.\n\n")

heading = Customisation.heading
footer = Customisation.footer
language = Customisation.language
shape = Customisation.shape


with open('translations.json', 'r', encoding='utf8') as translation:
    translation = json.load(translation)

sect_fix_1 = ["9", "8", "7", "6", "5", "4", "3", "2", "1", "B", "C"]
sect_fix_2 = ["20", "19", "18", "17", "16", "15", "14", "13", "12", "11", "10", "9B", "8B", "7B", "6B", "5B", "4B", "3B", "2B", "1B", "9C", "8C", "7C", "6C", "5C", "4C", "3C", "2C", "1C"]


print("\n\nFortnite Shop Sections Bot\n\n")

posts_quantity = []


def main():
    try:
        sections_data = get_data("calendar")['channels']['client-events']['states'][1]['state']['sectionStoreEnds']

        time_start = time.time()

        auth = tweepy.OAuthHandler(Keys.consumer_key, Keys.consumer_secret_key)
        auth.set_access_token(Keys.access_token, Keys.access_token_secret)
        tweepy_api = tweepy.API(auth)

        with open('Cache/cache1.json', 'r') as cache:
            cache1 = json.load(cache)

        if sections_data != cache1:  # or True:  # todo remove "or True" once done testing!!
            sections = []

            """
            namesto te čorbe naredi list VSEH sectionov, kot pri all_sections_bot.py (sectionDisplayName | sectionId)
            in list sectionov na koledarju ter od tistih, ki imajo enak sectionId, appendaj sectionDisplayName če gre,
            drugače pa sectionId (naredi malo bolj fancy ofc)
            """

            for a in sections_data:
                # print(sections_data)  # all active sections in the Fortnite API
                match = False
                for b in get_data("all_data"):
                    name = a
                    section_id = b['sectionId']

                    if name == section_id:
                        # print(f"NAME: {name}, SECTION_ID: {section_id}\n")
                        match = True
                        try:
                            name = b['sectionDisplayName']
                        except:
                            name = a

                            success = False
                            for o in translation:
                                if name.startswith(o):
                                    name = translation[o][language]
                                    success = True
                            if success is False:
                                if name.endswith(tuple(sect_fix_2)):
                                    name = name[:-2]
                                elif name.endswith(tuple(sect_fix_1)):
                                    name = name[:-1]

                        sections.append(name)
                if match is False:
                    name = a

                    success = False
                    for o in translation:
                        if name.startswith(o):
                            name = translation[o][language]
                            success = True
                    if success is False:
                        if name.endswith(tuple(sect_fix_2)):
                            name = name[:-2]
                        elif name.endswith(tuple(sect_fix_1)):
                            name = name[:-1]

                    sections.append(name)

            count = Counter(sections)

            sections_f = open("sections.txt", "wb")
            if len(sections) > 4:
                sections_f.write(f"🛒 TONIGHT'S SHOP SECTIONS! 👀 #Fortnite\n\n".encode("utf-8"))
            else:
                sections_f.write(f"🛒 Tonight's Shop Sections! #Fortnite\n\n".encode("utf-8"))

            len_sort = []
            for name in count:
                quantity = count[name]
                formatted_sect = Customisation.shape.format(section=name, quantity=quantity)
                len_sort.append(formatted_sect)
                # sections_f.write(f"{formatted_sect}\n".encode("utf-8"))

            # if Platform.wxPython_library is True and wx_imported is True:
            #     # sorts by text length (in pixels, not in amount of characters, needs a 'wxPython' library tho
            #     len_sorted = sort_by_text_lenght(list=len_sort)
            # else:
            #     len_sorted = sorted(len_sort, key=len)

            len_sorted = sort_by_text_lenght_char_method(list=len_sort)


            for item in len_sorted:
                # print(item)
                sections_f.write(f"{item}\n".encode("utf-8"))

            if footer != "":
                sections_f.write(f"\n{footer}".encode("utf-8"))
            sections_f.close()

            with open("sections.txt", "r", encoding="utf8") as file:
                file_contents = file.read()
            time_end = time.time()
            # tweepy_api.update_status(f"{file_contents}")
            # print("Posted!")
            print(f"\n{file_contents}\n\nText contains {len(file_contents)} characters.\n")
            print("Time spent computing:", time_end - time_start)
            posts_quantity.append((time.localtime()[2], time.localtime()[3]))

            with open("Cache/cache1.json", "w") as file:
                json.dump(sections_data, file, indent=3)

    except BaseException as error:
        if str(error) == "list index out of range":
            pass
        else:
            print(f"An exception occurred: {error}")


# if only sectionId is given (missing sectionDisplayName), use the saved translation
def section_id_styler(name):
    """
    for some reason this function doesn't work
    """
    success = False
    for o in translation:
        if name.startswith(o):
            print(name)
            name = translation[o][language]
            success = True
    if success is False:
        if name.endswith(tuple(sect_fix_2)):
            name = name[:-2]
            return name
        elif name.endswith(tuple(sect_fix_1)):
            name = name[:-1]
            return name


# # sorts a list by text length from shortest to longest
# def sort_by_text_length(list):
#     wx_app = wx.App()
#     font = wx.Font(pointSize=11, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, faceName='Chirp')
#     dc = wx.ScreenDC()
#     dc.SetFont(font)
#
#     length_sort = []
#     for line in list:
#         length = dc.GetTextExtent(line)[0]
#         length_sort.append((line, length))
#         # print(f"{line} | Lenght: {length}")
#
#     length_sort.sort(key=lambda length: length[1])
#
#     length_sorted = []
#     for ls in length_sort:
#         length_sorted.append(ls[0])
#
#     return length_sorted


def sort_by_text_lenght_char_method(list):
    char_length = {' ': 4, '•': 6, "'": 4, '.': 4, '!': 4, ',': 4, '-': 6, '?': 7, '(': 5, ')': 5, '&': 10, '%': 12,
                   '$': 9, '#': 10, '"': 6, '=': 9, '*': 5, '_': 6, ':': 4, ';': 5, '>': 9, '<': 9, '+': 9, 'A': 10,
                   'B': 10, 'C': 10, 'D': 11, 'E': 9, 'F': 8, 'G': 11, 'H': 11, 'I': 4, 'J': 6, 'K': 10, 'L': 8,
                   'M': 13, 'N': 11, 'O': 11, 'P': 9, 'Q': 11, 'R': 10, 'S': 9, 'T': 9, 'U': 11, 'V': 9, 'W': 14,
                   'X': 10, 'Y': 9, 'Z': 9, 'a': 8, 'b': 9, 'c': 8, 'd': 9, 'e': 8, 'f': 5, 'g': 8, 'h': 8, 'i': 4,
                   'j': 4, 'k': 8, 'l': 4, 'm': 12, 'n': 8, 'o': 8, 'p': 9, 'q': 9, 'r': 5, 's': 7, 't': 5, 'u': 8,
                   'v': 7, 'w': 11, 'x': 7, 'y': 7, 'z': 7, '0': 9, '1': 6, '2': 8, '3': 8, '4': 9, '5': 8, '6': 8,
                   '7': 7, '8': 9, '9': 8}

    length_sort = []
    for sect in list:
        length = 0
        for char in sect:
            try:
                length += char_length[char]
            except:
                length += 6
                print(f"A new unmeasured character has been detected: {char}")
                with open("unmeasured_characters.txt", "a") as file:
                    file.write(f"\n{char}")

        length_sort.append((sect, length))

    length_sort.sort(key=lambda length: length[1])

    length_sorted = []
    for ls in length_sort:
        length_sorted.append(ls[0])
    print(length_sorted)
    return length_sorted


# gets all the data needed from the Fortnite APIs
def get_data(which):
    try:
        calendar_api = requests.get(url="https://api.nitestats.com/v1/epic/modes-smart", timeout=7)
        all_data_api = requests.get(url=f"https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game/shop-sections?lang={language}", timeout=7)
        if calendar_api.status_code == 200 and all_data_api.status_code == 200:
            calendar = calendar_api.json()
            all_data = all_data_api.json()['sectionList']['sections']
            """
            calendar = {"channels":{"standalone-store":{"states":[{"validFrom":"2022-03-02T22:24:17.205Z","activeEvents":[],"state":{"activePurchaseLimitingEventIds":[],"storefront":[],"rmtPromotionConfig":[],"storeEnd":"0001-01-01T00:00:00.000Z"}}],"cacheExpire":"2022-03-03T00:24:17.205Z"},"client-matchmaking":{"states":[{"validFrom":"2022-03-02T22:24:17.205Z","activeEvents":[],"state":{"region":{"OCE":{"eventFlagsForcedOff":["Playlist_DefaultDuo"]},"CN":{"eventFlagsForcedOff":["Playlist_DefaultDuo","Playlist_Bots_DefaultDuo","Playlist_Deimos_DuoCN"]},"REGIONID":{"eventFlagsForcedOff":["Playlist_Deimos_Duo_WinterCN"]},"ASIA":{"eventFlagsForcedOff":["Playlist_DefaultDuo"]}}}},{"validFrom":"2022-03-03T00:30:00.000Z","activeEvents":[],"state":{"region":{"CN":{"eventFlagsForcedOff":["Playlist_DefaultDuo","Playlist_Bots_DefaultDuo","Playlist_Deimos_DuoCN"]},"REGIONID":{"eventFlagsForcedOff":["Playlist_Deimos_Duo_WinterCN"]},"ASIA":{"eventFlagsForcedOff":["Playlist_DefaultDuo"]}}}}],"cacheExpire":"2022-03-03T00:24:17.205Z"},"tk":{"states":[{"validFrom":"2022-03-02T22:24:17.205Z","activeEvents":[],"state":{"k":["1162D72490AB6D040106B276D14B20D2:UoybfdmMPLyXmLpTKBZB0sqSOvXnKHabF/nv5olkuoQ=","E66DF3CF1BFE84F0B1966967210DD6D9:DGLD/iFbdLvaiZnAfWrHIW5yJ5SfsQQyjeW2IBQe+zw=","B4BE2A5487426AFF06CB7089EA9B75BE:w7Hbt5PsQ4MDg9EjvOU8WdtL/BrWxZNp9NM2UrHSjRg=","2648ACDF6B7E55495928F2319101BB8A:tKha+iiFKUamRIWCxq0gOtbN/G1B5J5eOIElAx9T3rc=","E098A699B1A5E20B03B5CBBCDB85D4E3:oKYx1AqjUax4YhKirSQDeyBSQNkSmEKDS7q+U/4KszU=","57C0A809F1C608D62307954035E3DFCD:FuMI1S1xM1U7UrdX4qZhPq77674JV+EV4HWsn59bmbE=","A69EA08281B5018543EC525AC7716B70:1W0iCKEIuEfDSOaJfl4gQEpenDKjLQGAovP3LWc/FTw="]}}],"cacheExpire":"2022-03-03T00:24:17.205Z"},"featured-islands":{"states":[{"validFrom":"2022-03-02T22:24:17.205Z","activeEvents":[],"state":{"islandCodes":["2800-3365-7403?v=18","5087-5535-3072?v=6","0444-2689-6036?v=9","0446-0600-1321?v=3"],"playlistCuratedContent":[],"playlistCuratedHub":{"Playlist_PlaygroundV2":"0235-6765-1879","Playlist_Creative_PlayOnly":"0235-6765-1879"},"islandTemplates":[]}}],"cacheExpire":"2022-03-03T00:24:17.205Z"},"community-votes":{"states":[{"validFrom":"2022-03-02T22:24:17.205Z","activeEvents":[],"state":{"electionId":"","candidates":[],"electionEnds":"9999-12-31T23:59:59.999Z","numWinners":1}}],"cacheExpire":"2022-03-03T00:24:17.205Z"},"client-events":{"states":[{"validFrom":"2022-03-02T22:24:17.205Z","activeEvents":[{"eventType":"EventFlag.BBPromo.Quests","activeUntil":"2090-02-14T00:00:00.000Z","activeSince":"2019-11-19T00:00:00.000Z"},{"eventType":"WL0","activeUntil":"2022-09-14T07:00:00.000Z","activeSince":"2020-08-01T07:00:00.000Z"},{"eventType":"EventFlag.Event_TheMarch","activeUntil":"2022-08-30T13:00:00.000Z","activeSince":"2021-08-26T13:00:00.000Z"},{"eventType":"EventFlag.LobbySeason19","activeUntil":"2022-03-29T13:00:00.000Z","activeSince":"2021-12-02T14:00:00.000Z"},{"eventType":"EventFlag.STWIrwin","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-01-01T00:00:00.000Z"},{"eventType":"EventFlag.PassiveIceStorms","activeUntil":"2022-03-14T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.PassiveFireStorms","activeUntil":"2022-03-14T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.PassiveLightningStorms","activeUntil":"2022-03-14T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.ActiveMiniBosses","activeUntil":"2022-03-14T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.MissionAlert.MegaAlert","activeUntil":"2022-03-14T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.MissionAlert.MegaAlertMiniboss","activeUntil":"2022-03-14T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.Season12.NoDancing.Quests","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.Phoenix.NewBeginnings","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.ElderGroupMissions","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.Phoenix.NewBeginnings.Quests","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.LoveStorm.EnableEnemyVariants","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.Wargames.Start","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.Outpost","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.Wargames.Phase2","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-01T00:00:00.000Z"},{"eventType":"EventFlag.Blockbuster2018","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-08T00:00:00.000Z"},{"eventType":"EventFlag.Blockbuster2018Phase1","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-08T00:00:00.000Z"},{"eventType":"EventFlag.Blockbuster2018Phase2","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-08T00:00:00.000Z"},{"eventType":"EventFlag.Blockbuster2018Phase3","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-08T00:00:00.000Z"},{"eventType":"EventFlag.Blockbuster2018Phase4","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-08T00:00:00.000Z"},{"eventType":"EventFlag.LobbyStW.Blockbuster","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-08T00:00:00.000Z"},{"eventType":"EventFlag.Wargames.Phase3","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-08T00:00:00.000Z"},{"eventType":"EventFlag.Wargames.Phase4","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-15T00:00:00.000Z"},{"eventType":"EventFlag.Event_MonarchLevelUpPack","activeUntil":"2022-04-01T13:00:00.000Z","activeSince":"2022-02-16T14:00:00.000Z"},{"eventType":"EventFlag.Wargames.Phase5","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-22T00:00:00.000Z"},{"eventType":"EventFlag.Phoenix.NewBeginnings.SpringTraining","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-28T00:00:00.000Z"},{"eventType":"EventFlag.Wargames.Phase6","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-28T00:00:00.000Z"},{"eventType":"EventFlag.LTM_UV_Q","activeUntil":"2022-03-16T00:00:00.000Z","activeSince":"2022-03-01T00:00:00.000Z"},{"eventType":"EventFlag.S19_WildWeeks_Spider","activeUntil":"2022-03-08T14:00:00.000Z","activeSince":"2022-03-01T14:00:00.000Z"}],"state":{"activeStorefronts":[],"eventNamedWeights":[],"activeEvents":[{"instanceId":"42e4qrq8b28d9jlqovnglg8d25[2]0","devName":"Event_TheMarch","eventName":"CalendarEvent_TheMarch","eventStart":"2021-08-26T13:00:00Z","eventEnd":"2022-08-30T13:00:00Z","eventType":"EventFlag.Event_TheMarch"},{"instanceId":"3pll7mg9m03eirtcf0p2mp9fuo[2]0","devName":"Event_S19_MonarchLevelUpPack","eventName":"CalendarEvent_Season19_MonarchLevelUpPack","eventStart":"2022-02-16T14:00:00Z","eventEnd":"2022-04-01T13:00:00Z","eventType":"EventFlag.Event_S19_MonarchLevelUpPack"},{"instanceId":"6dd963np0uuf8gv54gq6c0712v[2]0","devName":"S19_UnvaultedQuests","eventName":"CalendarEvent_S19_UnvaultedQuests","eventStart":"2022-03-01T00:00:00Z","eventEnd":"2022-03-16T00:00:00Z","eventType":"EventFlag.LTM_UV_Q"},{"instanceId":"6t5ifdtlgr7vcnub4qd9tn6q0r[2]0","devName":"Event_S19_WildWeeks_Spider","eventName":"CalendarEvent_S19_WildWeeks_Spider","eventStart":"2022-03-01T14:00:00Z","eventEnd":"2022-03-08T14:00:00Z","eventType":"EventFlag.S19_WildWeeks_Spider"}],"seasonNumber":19,"seasonTemplateId":"AthenaSeason:athenaseason19","matchXpBonusPoints":0,"eventPunchCardTemplateId":"","seasonBegin":"2021-12-02T14:00:00Z","seasonEnd":"2022-03-29T13:00:00Z","seasonDisplayedEnd":"2022-03-15T04:00:00Z","weeklyStoreEnd":"2022-03-03T00:00:00Z","stwEventStoreEnd":"2022-04-04T00:00:00.000Z","stwWeeklyStoreEnd":"2022-03-03T00:00:00.000Z","sectionStoreEnds":{"ShadowStrike": "2022-03-03T00:00:00Z","Rogue&GambitB": "2012-03-03T00:00:00Z","Rogue&Gambit2B": "2022-03-03T00:00:00Z","MarvelB": "2022-03-03T00:00:00Z","Marvel2B": "2022-03-03T00:00:00Z","UnchartedB": "2022-03-03T00:00:00Z","HorizonZeroDawnB": "2022-03-03T00:00:00Z"},"rmtPromotion":"","dailyStoreEnd":"2022-03-03T00:00:00Z"}},{"validFrom":"2022-03-03T00:00:00.000Z","activeEvents":[{"eventType":"EventFlag.BBPromo.Quests","activeUntil":"2090-02-14T00:00:00.000Z","activeSince":"2019-11-19T00:00:00.000Z"},{"eventType":"WL0","activeUntil":"2022-09-14T07:00:00.000Z","activeSince":"2020-08-01T07:00:00.000Z"},{"eventType":"EventFlag.Event_TheMarch","activeUntil":"2022-08-30T13:00:00.000Z","activeSince":"2021-08-26T13:00:00.000Z"},{"eventType":"EventFlag.LobbySeason19","activeUntil":"2022-03-29T13:00:00.000Z","activeSince":"2021-12-02T14:00:00.000Z"},{"eventType":"EventFlag.STWIrwin","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-01-01T00:00:00.000Z"},{"eventType":"EventFlag.PassiveIceStorms","activeUntil":"2022-03-14T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.PassiveFireStorms","activeUntil":"2022-03-14T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.PassiveLightningStorms","activeUntil":"2022-03-14T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.ActiveMiniBosses","activeUntil":"2022-03-14T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.MissionAlert.MegaAlert","activeUntil":"2022-03-14T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.MissionAlert.MegaAlertMiniboss","activeUntil":"2022-03-14T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.Season12.NoDancing.Quests","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.Phoenix.NewBeginnings","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.ElderGroupMissions","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.Phoenix.NewBeginnings.Quests","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.LoveStorm.EnableEnemyVariants","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.Wargames.Start","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.Outpost","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-01-25T00:00:00.000Z"},{"eventType":"EventFlag.Wargames.Phase2","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-01T00:00:00.000Z"},{"eventType":"EventFlag.Blockbuster2018","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-08T00:00:00.000Z"},{"eventType":"EventFlag.Blockbuster2018Phase1","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-08T00:00:00.000Z"},{"eventType":"EventFlag.Blockbuster2018Phase2","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-08T00:00:00.000Z"},{"eventType":"EventFlag.Blockbuster2018Phase3","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-08T00:00:00.000Z"},{"eventType":"EventFlag.Blockbuster2018Phase4","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-08T00:00:00.000Z"},{"eventType":"EventFlag.LobbyStW.Blockbuster","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-08T00:00:00.000Z"},{"eventType":"EventFlag.Wargames.Phase3","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-08T00:00:00.000Z"},{"eventType":"EventFlag.Wargames.Phase4","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-15T00:00:00.000Z"},{"eventType":"EventFlag.Event_MonarchLevelUpPack","activeUntil":"2022-04-01T13:00:00.000Z","activeSince":"2022-02-16T14:00:00.000Z"},{"eventType":"EventFlag.Wargames.Phase5","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-22T00:00:00.000Z"},{"eventType":"EventFlag.Phoenix.NewBeginnings.SpringTraining","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-28T00:00:00.000Z"},{"eventType":"EventFlag.Wargames.Phase6","activeUntil":"2022-04-06T00:00:00.000Z","activeSince":"2022-02-28T00:00:00.000Z"},{"eventType":"EventFlag.LTM_UV_Q","activeUntil":"2022-03-16T00:00:00.000Z","activeSince":"2022-03-01T00:00:00.000Z"},{"eventType":"EventFlag.S19_WildWeeks_Spider","activeUntil":"2022-03-08T14:00:00.000Z","activeSince":"2022-03-01T14:00:00.000Z"}],"state":{"activeStorefronts":[],"eventNamedWeights":[],"activeEvents":[{"instanceId":"42e4qrq8b28d9jlqovnglg8d25[2]0","devName":"Event_TheMarch","eventName":"CalendarEvent_TheMarch","eventStart":"2021-08-26T13:00:00Z","eventEnd":"2022-08-30T13:00:00Z","eventType":"EventFlag.Event_TheMarch"},{"instanceId":"3pll7mg9m03eirtcf0p2mp9fuo[2]0","devName":"Event_S19_MonarchLevelUpPack","eventName":"CalendarEvent_Season19_MonarchLevelUpPack","eventStart":"2022-02-16T14:00:00Z","eventEnd":"2022-04-01T13:00:00Z","eventType":"EventFlag.Event_S19_MonarchLevelUpPack"},{"instanceId":"6dd963np0uuf8gv54gq6c0712v[2]0","devName":"S19_UnvaultedQuests","eventName":"CalendarEvent_S19_UnvaultedQuests","eventStart":"2022-03-01T00:00:00Z","eventEnd":"2022-03-16T00:00:00Z","eventType":"EventFlag.LTM_UV_Q"},{"instanceId":"6t5ifdtlgr7vcnub4qd9tn6q0r[2]0","devName":"Event_S19_WildWeeks_Spider","eventName":"CalendarEvent_S19_WildWeeks_Spider","eventStart":"2022-03-01T14:00:00Z","eventEnd":"2022-03-08T14:00:00Z","eventType":"EventFlag.S19_WildWeeks_Spider"}],"seasonNumber":19,"seasonTemplateId":"AthenaSeason:athenaseason19","matchXpBonusPoints":0,"eventPunchCardTemplateId":"","seasonBegin":"2021-12-02T14:00:00Z","seasonEnd":"2022-03-29T13:00:00Z","seasonDisplayedEnd":"2022-03-15T04:00:00Z","weeklyStoreEnd":"2022-03-04T00:00:00Z","stwEventStoreEnd":"2022-04-04T00:00:00.000Z","stwWeeklyStoreEnd":"2022-03-10T00:00:00.000Z","sectionStoreEnds":{
                            "DC8": "2022-07-18T00:00:00Z",
                            "DC9": "2022-07-18T00:00:00Z",
                            "SquadOriginsB": "2022-07-18T00:00:00Z",
                            "SquadOrigins2B": "2022-07-18T00:00:00Z",
                            "DC4": "2022-07-18T00:00:00Z",
                            "DC5": "2022-07-18T00:00:00Z",
                            "DC6": "2022-07-18T00:00:00Z",
                            "DC7": "2022-07-18T00:00:00Z",
                            "DC": "2022-07-18T00:00:00Z",
                            "DC2": "2022-07-18T00:00:00Z",
                            "DC3": "2022-07-18T00:00:00Z",
                            "Daily": "2022-07-18T00:00:00Z",
                            "Featured": "2022-07-18T00:00:00Z",
                            "Featured2": "2022-07-18T00:00:00Z",
                            "ShowWrapsB":"2022-03-04T00:00:00Z",
                            "WrapEnabledGearB":"2022-03-04T00:00:00Z",
                            "WrapsB":"2022-03-04T00:00:00Z",
                            "Marvel2B":"2022-03-04T00:00:00Z",
                            "UnchartedB":"2022-03-04T00:00:00Z",
                            "Wraps2B":"2022-03-04T00:00:00Z",
                            "Rogue&GambitB":"2022-03-04T00:00:00Z",
                            "Featured53":"2022-03-04T00:00:00Z",
                            "Rogue&Gambit2B":"2022-03-04T00:00:00Z",
                            "MarvelB":"2022-03-04T00:00:00Z"
                        },"rmtPromotion":"","dailyStoreEnd":"2022-03-04T00:00:00Z"}}],"cacheExpire":"2022-03-03T00:24:17.205Z"}},"cacheIntervalMins":15,"currentTime":"2022-03-02T22:46:25.213Z"}
            """

            if which == "calendar":
                return calendar
            elif which == "all_data":
                return all_data
            else:
                print("Function 'get_data' received an undefined input.")
        else:
            print(f"\nThere has been a problem connecting to the API."
                  f"\nCalendar status code: {calendar_api.status_code}"
                  f"\nSections status code: {all_data_api.status_code}\n")

    except BaseException as error:
        print("There has been a problem getting the required data from the Fortnite APIs.\nAn exception occurred: {}".format(error))


# this is used to prevent unwanted tweet spam
def prevent_tweet_spam():
    if len(posts_quantity) > 0:
        if time.localtime()[2] != posts_quantity[0][0] or time.localtime()[3] != posts_quantity[0][1]:
            del posts_quantity[0]
        if len(posts_quantity) > 3:
            print("\n\nATTENTION!\nThe bot is going into SLEEP mode for the next 2 HOURS due to too many posts in the past hour."
                  "If you believe this is a mistake, simply restart the bot.")
            time.sleep(7200)


# checks if connected to internet and pauses the code
def refresh_time(t):
    now = datetime.now()
    print(f"[{now.strftime('%d/%m/%Y-%H:%M:%S')}] Checking for section changes... Next check in ~{t}s.")
    try:
        requests.get("https://www.google.com/", timeout=4)
        main()
    except (requests.ConnectionError, requests.Timeout):
        print("No internet connection.")
    time.sleep(t)


# loops the bot
if __name__ == "__main__":
    while True:
        prevent_tweet_spam()
        if 22 <= time.localtime()[3] <= 23 or 0 == time.localtime()[3]:  # from 22:00 until 0:59
            refresh_time(7)  # 7s = 1543 calls in 3h
        else:
            refresh_time(16)  # 16s = 2908 calls in 21h
