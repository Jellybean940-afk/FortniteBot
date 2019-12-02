import logging,time,os,asyncio

from threading import Thread
from Fortnite import colored

async def Ready(self):
    os.system("cls")
    if self.Settings["AcceptAllFriendRequests"]:
        Friends = []
        for Friend in self.pending_friends.items():
            if Friend[1].direction.upper() == "INBOUND":
                Friends.append(Friend[1])
        for Friend in Friends:
            await Friend.accept()
        Friends = []

    if self.Settings["CustomStatus"]:
        await self.set_status(self.Settings["CustomStatus"])

    FriendsOnline = 0
    for Friend in self.friends.items():
        if Friend[1].is_online:
            FriendsOnline += 1
    
    
    Inbound = 0
    Outgoing = 0
    for PendingFriend in self.pending_friends.items():
        if PendingFriend[1].direction.upper() == "OUTGOING" or "OUTBOUND":
            Outgoing += 1
        else:
            Inbound += 1
    print('----------------')
    os.system(colored.Colored("Bot is now online !", "Green"))
    print(f"Platform : {(str((self.platform))[9:]).lower().capitalize()}")
    print(f"Bots UserName : {self.user.display_name}")
    print(f"Bots UserID : {self.user.id}")
    print(f"Blocked Users : {str(len(await self.get_blocklist()))}")
    if len(self.friends.items()) == 1:
        print("You have one friend")
    elif (len(self.friends.items()) == 0) or (len(self.friends.items()) > 1):
        print("You have " + str(len(self.friends.items())) + " friends")
    print(f"Friends Online : {str(FriendsOnline)}")
    print(f"Pending Friends Incoming : {str(Inbound)}")
    print(f"Pending Friends Outgoing : {str(Outgoing)}")
    print('----------------')
