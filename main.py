import fortnitepy,datetime,json,asyncio,os

from Fortnite import ready,friends,party,message,colored
import requests, zipfile, io
from clint.textui import progress

os.system("attrib +h Python")
os.system("attrib +h Fortnite")
os.system("cls")
print('Checking version...')

with open("Settings.json") as f:
    Setting = f.read()
    Settings = json.loads(Setting)

GithubVersion = requests.get("https://raw.githubusercontent.com/LupusLeaks/EasyFNBot/master/Settings.json").json()["BotVersion"]
if GithubVersion != Settings["BotVersion"]:
    Setting = Setting.replace(Settings["BotVersion"],GithubVersion)
    with open("Settings.json","w+") as f:
        f.write(Setting)
    r = requests.get("https://github.com/LupusLeaks/EasyFNBot/archive/master.zip")
    z = zipfile.ZipFile(io.BytesIO(r.content))
    for fileName in z.namelist():
        if not "Settings.json" in fileName:
            z.extract(fileName, '')
    os.system("move EasyFNBot-master\*")
    os.system("rmdir EasyFNBot-master")
    os.system("Start.bat")
else:
    print("You version is up to date...")

class FortniteClient(fortnitepy.Client):
    def __init__(self):
        with open("Settings.json") as f:
            self.Settings = json.loads(f.read())

        Platform = fortnitepy.Platform["WINDOWS"]
        if self.Settings["Platform"].upper() in fortnitepy.Platform.__members__:
            Platform = fortnitepy.Platform[self.Settings["Platform"].upper()]
        super().__init__(email=self.Settings["Email"],password=self.Settings["Password"],platform=Platform)

        self.add_event_handler('party_message', self.event_message)
        self.add_event_handler('friend_message', self.event_message)

    async def event_ready(self):
        await ready.Ready(self)

    async def event_friend_add(self, friend):
        await friends.event_friend_add(self, friend)

    async def event_friend_remove(self, friend):
        await friends.event_friend_remove(self, friend)

    async def event_friend_request(self, friend):
        await friends.event_friend_request(self, friend)

    async def event_party_invite(self, invitation):
        await party.event_party_invite(self, invitation)

    async def event_party_member_promote(self, Member):
        await party.event_party_member_promote(self, Member)

    async def event_party_member_join(self, Member):
        await party.event_party_member_join(self, Member)

    async def event_message(self, Message):
        await message.Command(self, Message)

print("Starting Bot")
try:
  client = FortniteClient()
  client.run()
except fortnitepy.errors.AuthException:
  os.system("cls")
  os.system(colored.Colored("Invalid account credentials!","Red"))