import datetime,os,fortnitepy,time,requests,json,fn_api_wrapper

from Fortnite import colored
TimeInUTC = datetime.datetime.utcnow().strftime('%H:%M:%S')
fnapi = fn_api_wrapper.FortniteAPI()

async def event_party_invite(self, invitation):
    if (self.Settings["JoinPartyOnInvitation"]) or (invitation.author.id in self.Settings["GiveFullAccessTo"]):
        await self.user.party.me.set_emote('EID_Wave')
        await invitation.accept()

async def event_party_member_promote(self, Member):
    if self.Settings["ThanksOnPromote"]:
        if Member.id == self.user.id:
            await self.user.party.send("Thanks for promoting me ♥")
            await self.user.party.me.set_emote("EID_TrueLove")

async def event_party_member_join(self, Member):
    if Member.id == self.user.id:

        if self.user.party.me.is_leader and self.user.party.member_count == 1:
            os.system(colored.Colored(f'[BOT {self.user.display_name}] [{TimeInUTC}] Created Party', "green"))
        else:
            os.system(colored.Colored(f'[BOT {self.user.display_name}] [{TimeInUTC}] Joined Party', "green"))

        try:
            Level = int(self.Settings["SeasonLevel"])
            await self.user.party.me.set_banner(season_level=Level)
        except:
            await self.user.party.me.set_banner(season_level=100)

        await self.user.party.me.set_banner(icon=self.Settings["Banner"])

        CID = fnapi.GetSkin(NameorId=self.Settings["DefaultSkin"],matchMethod="starts")
        if CID.status != 200:
            os.system(colored.Colored(f'Can\'t find {self.Settings["DefaultSkin"]}',"red"))
            CID = "CID_022_Athena_Commando_F"
        else:
            CID = CID.id
        await self.user.party.me.set_outfit(asset=CID)

        if self.Settings["EmoteAfterJoiningParty"] and not self.Settings["EmoteName"] == "":
            EID = fnapi.GetEmote(NameorId=self.Settings["EmoteName"],matchMethod="starts")
            if EID.status != 200:
                os.system(colored.Colored(f'Can\'t find {self.Settings["EmoteName"]}',"red"))
            else:
                await self.user.party.me.set_emote(asset=EID.id)

        if self.Settings["DefaultBackpack"] != "":
            BID = fnapi.GetBackpack(NameorId=self.Settings["DefaultBackpack"],matchMethod="starts")
            if BID != 200:
                os.system(colored.Colored(f'Can\'t find {self.Settings["DefaultBackpack"]}',"red"))
            else:
                await self.user.party.me.set_backpack(asset=BID.id)
    else:
        os.system(colored.Colored(f'[BOT {self.user.display_name}] [{TimeInUTC}] {Member.display_name} Joined the Party', "green"))
        await self.user.party.send(f"Welcome {Member.display_name} type !help if you need any help, if you want your own bot join my discord Server : https://discord.gg/2n2c7Pn")