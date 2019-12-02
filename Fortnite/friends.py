import datetime,os,fortnitepy

from Fortnite import colored
TimeInUTC = datetime.datetime.utcnow().strftime('%H:%M:%S')

async def event_friend_add(self, Friend):
    TimeInUTC = datetime.datetime.utcnow().strftime('%H:%M:%S')
    if self.Settings["InviteFriendOnFriendAdded"] or Friend.id in self.Settings["GiveFullAccessTo"]:
        try:
            await Friend.invite()
            os.system(colored.Colored(f'[BOT {self.user.display_name}] [{TimeInUTC}] Invited {Friend.display_name}', "green"))
        except fortnitepy.errors.PartyError:
            await Friend.send("Can't invite you, the party is full")
        await Friend.send("Hey thanks for adding my bot, this bot was made by @LupusLeaks on Twitter, for help just write !help or join my discord Server : https://discord.gg/2n2c7Pn")
        os.system(colored.Colored(f'[BOT {self.user.display_name}] [{TimeInUTC}] {Friend.display_name} is now your friend', "green"))

async def event_friend_remove(self, Friend):
    if self.Settings["SendFriendRequestOnFriendRemove"] or Friend.id in self.Settings["GiveFullAccessTo"]:
        try:
            await self.add_friend(Friend.id)
            os.system(colored.Colored(f'[BOT {self.user.display_name}] [{TimeInUTC}] {Friend.display_name} removed you as a friend, bot sent him a friend request', "green"))
        except fortnitepy.errors.HTTPException as Error:
            os.system(colored.Colored(f'[BOT {self.user.display_name}] [{TimeInUTC}] {Friend.display_name} removed you as a friend', "red"))
    else:
        os.system(colored.Colored(f'[BOT {self.user.display_name}] [{TimeInUTC}] {Friend.display_name} removed you as a friend', "red"))

async def event_friend_request(self, Friend):
    if self.Settings["AcceptIncomingFriendRequest"] or Friend.id in self.Settings["GiveFullAccessTo"]:
        await Friend.accept()
