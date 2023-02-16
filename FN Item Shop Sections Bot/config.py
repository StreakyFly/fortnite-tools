"""
The section below is your twitter develepor keys & tokens required for posting to your twitter!
You must have a twitter developer account for which you can apply at https://developer.twitter.com/
You must create an app to acess your keys at https://developer.twitter.com/en/portal/projects-and-apps
Whatever you name your app is what will appear as the source of where your tweet was posted from eg. Twitter for iPhone
"""

class Keys:
    consumer_key = "REPLACE_WITH_YOUR_CONSUMER_KEY"  # this is found under the Consumer Keys section and is the API key
    consumer_secret_key = "REPLACE_WITH_YOUR_CONSUMER_SECRET_KEY"  # this is found under the Consumer Keys section and is the Secret API key
    access_token = "REPLACE_WITH_YOUR_ACCESS_TOKEN"  # this is found under Authentication Tokens and is the Access token
    access_token_secret = "REPLACE_WITH_YOUR_ACCESS_TOKEN_SECRET"  # this is found under Authentication Tokens and is the Secret Access token


'''
The section below is for the customisation of the tweet itself.
'''

class Customisation:
    heading = "🛒 Tonight's #Fortnite Shop Sections:"  # this will be the text displayed in the post above the sections
    footer = ""  # this is what will appear under the sections! Leave blank ("") if you do not want a footer
    shape = " • {section} ({quantity}x)"  # how the sections will look like, this example will print " - Daily (2x)"
    language = "en"  # The language you would like the shop swctions to post in. Options: ar / de / en / es / es-419 / fr / it / ja / ko / pl / pt-BR / ru / tr


'''
Leave this on 'False' unless you know how to download "wxPython" library. If any errors occur, turn this to False.
This option sorts Shop Sections by text length measured in pixels rather than by the quantity of characters.
This will rarely make any difference and if it does, it will be minimal.
'''

class Platform:
    wxPython_library = False  # if set to True, it will sort sections by text length, otherwise by character quantity
