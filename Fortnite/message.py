import os,fortnitepy,datetime,requests,json,asyncio,time,random,threading,fn_api_wrapper

from threading import Thread

from Fortnite import Variants,API,Extras,colored

fnapi = fn_api_wrapper.FortniteAPI()

async def Command(self, message):
    HasFullAccess = False
    TimeInUTC = datetime.datetime.utcnow().strftime('%H:%M:%S')
    GiveFullAccess = self.Settings["GiveFullAccessTo"]
    if "," in GiveFullAccess:
        if message.author.id in (GiveFullAccess.split(",")):
            HasFullAccess = True
    elif GiveFullAccess == message.author.id:
        HasFullAccess = True

    author = message.author
    msg = message.content.upper()
    args = msg.split(" ")

    def GetValue(fullLine,startWith,endWith):
        startIndex = fullLine.index(startWith) + len(startWith)
        endIndex = fullLine[startIndex:].index(endWith) + startIndex
        return fullLine[startIndex:endIndex]

    def GetValues(fullLine):
        Variants = []
        for Variant in range(0,fullLine.count("--")):
            try:
                startIndex = fullLine.index("--")
                ValueStartIndex = fullLine[startIndex:].index("=") + startIndex + 1
        
                try:
                    endIndex = fullLine[ValueStartIndex:].index("--") + ValueStartIndex
                except:
                    endIndex = len(fullLine)
                Variants.append(fullLine[startIndex:endIndex])
                fullLine = fullLine.replace(fullLine[startIndex:endIndex],"")
            except:
                return None
        return Variants

    if args[0] == "!BANNER" and len(args) > 1:
        if self.Settings["ChangeBannerOnCommand"] or HasFullAccess:
            if "--LEVEL=" in msg:
                msg = msg + " "
                Level = GetValue(msg,"--LEVEL="," ")
                try:
                    Level = int(Level)
                except:
                    await message.reply("Sorry you can only use numbers as level")
                    return
                msg = msg.replace("--LEVEL=" + str(Level), "").strip()
                await self.user.party.me.set_banner(icon=msg[8:], season_level=Level)
                await message.reply("Banner and Level set")
            else:
                await self.user.party.me.set_banner(icon=msg[8:])
                await message.reply("Banner set")
        else:
            await message.reply("Can't change Banner. The Bot owner has disabled this command!")

    if msg == "!LOGOUT":
        if self.Settings["LogoutOnCommand"] or HasFullAccess:
            await message.reply("Logged out")
            await self.logout()
            print("\033c", end="")
            os.system(colored.Colored(f"[BOT] [{TimeInUTC}] Logged out.", "red"))
        else:
            await message.reply("Can't Logout. The Bot owner has disabled this command!")

    if msg == "!RESTART":
        if self.Settings["RestartOnCommand"] or HasFullAccess:
            await message.reply("Restarting...")
            await self.logout()
            await self.start()
        else:
            await message.reply("Can't Restart. The Bot owner has disabled this command!")

    if "!BP" == args[0] and len(args) > 1:
        try:
            if self.Settings["ChangeBattlePassInfoOnCommand"] or HasFullAccess:
                await self.user.party.me.set_battlepass_info(has_purchased=bool(args[1]), level=int(args[2]), self_boost_xp=int(args[3]), friend_boost_xp=int(args[4]))
                await message.reply("New Battle Pass Info set")
                os.system(colored.Colored(f"[BOT {self.user.display_name}] [{TimeInUTC}] New Battle Pass Info set by {message.author.display_name}", "green"))
            else:
                await message.reply("Can't set new Battle Pass Info. The Bot owner has disabled this command!")
        except:
            await message.reply("Command : !BP <True/False> <Level> <Self XP Boost> <Friend XP Boost>")

    if args[0] == "!STATUS" and len(args) > 1:
        if self.Settings["ChangeStatusOnCommand"] or HasFullAccess:
            await self.send_status(message.content[8:])
            await message.reply(f"Status set to : {message.content[8:]}")
            os.system(colored.Colored(f"[BOT {self.user.display_name}] [{TimeInUTC}] New status set by {message.author.display_name}", "green"))
        else:
            await message.reply("Can't set new status. The Bot owner has disabled this command!")

    if "!PLATFORM" == args[0] and len(args) > 1:
        if self.Settings["ChangePlatformOnCommand"] or HasFullAccess:
            if msg[10:] in fortnitepy.Platform.__members__:
                self.platform = fortnitepy.Platform[msg[10:]]
            else:
                await message.reply("Can't find the Platform!")
                return

            if self.Settings["TryToRejoinOldParty"] or (HasFullAccess and not self.Settings["ReinviteOldPartyMembers"]):
                Members = []
                for Member in self.user.party.members:
                    Members.append(Member)
                await self.user.party.me.leave()
                os.system(colored.Colored(f"[BOT {self.user.display_name}] [{TimeInUTC}] Changed Platform to {(str((self.platform))[9:]).lower().capitalize()}", "green"))
                await message.reply(f"Successfuly changed Platform to {(str((self.platform))[9:]).lower().capitalize()}")

                for Member in Members:
                    if Member != self.user.id:
                        UserName = (await self.fetch_profile(Member,cache=True, raw=False)).display_name
                        if self.get_friend(Member):
                            await self.get_friend(Member).join_party()
                            await message.reply(f"Tryied to join {UserName}")
                return

            if self.Settings["ReinviteOldPartyMembers"] or (HasFullAccess and not self.Settings["TryToRejoinOldParty"]):
                Members = []
                for Member in self.user.party.members:
                    Members.append(Member)
                await self.user.party.me.leave()
                os.system(colored.Colored(f"[BOT {self.user.display_name}] [{TimeInUTC}] Changed Platform to {(str((self.platform))[9:]).lower().capitalize()}", "green"))
                await message.reply(f"Successfuly changed Platform to {(str((self.platform))[9:]).lower().capitalize()}")

                for Member in Members:
                    if Member != self.user.id:
                        await self.user.party.invite(Member)
                        UserName = (await self.fetch_profile(Member,cache=True, raw=False)).display_name
                        await message.reply(f"Invited : {UserName}")
                return

    if args[0] == "!KICK" and len(args) > 1:
        if self.Settings["KickMembersOnCommand"] or HasFullAccess:
            UserToKick = await self.fetch_profile(msg[6:],cache=True, raw=False)
            if UserToKick.id == self.user.id:
                await message.reply('Can\'t kick myself. Use "!Leave Party" insteand')
                return
            if UserToKick.id in self.user.party.members:
                User = self.user.party.members.get(UserToKick.id)
                try:
                    await User.kick()
                    await message.reply("Kicked {User.display_name}")
                    os.system(colored.Colored(f"[BOT {self.user.display_name}] [{TimeInUTC}] Kicked {User.display_name}", "red"))
                except fortnitepy.Forbidden:
                    await message.reply(f"Can't kick {User.display_name}.I am not the leader of the party.")
            else:
                await message.reply("User isn't in my party")
        else:
            await message.reply("Can't kick. The Bot owner has disabled this command!")

    if args[0] == "!PROMOTE":
        if self.Settings["PromoteMembersOnCommand"] or HasFullAccess:
            if msg == "!PROMOTE":
                UserToPromote = await self.fetch_profile(message.author.id,cache=True, raw=False)
            else:
                UserToPromote = await self.fetch_profile(msg[9:],cache=True, raw=False)
            if UserToPromote.id in self.user.party.members:
                User = self.user.party.members.get(UserToPromote.id)
                try:
                    await User.promote()
                    await message.reply(f"Promoted {User.display_name}")
                    os.system(colored.Colored(f"[BOT {self.user.display_name}] [{TimeInUTC}] Promoted {User.display_name}", "green"))
                except fortnitepy.Forbidden:
                    await message.reply(f"Can't Promote {User.display_name}, I am not the party leader")
            else:
                await message.reply("User isnt in my party")
        else:
            await message.reply("Can't promote. The Bot owner has disabled this command!")

    if args[0] == "!INVITE" and msg != "!INVITE ALL BOTS":
        if self.Settings["InviteUserOnCommand"] or HasFullAccess:
            if msg == "!INVITE":
                User = await self.fetch_profile(message.author.id, cache=True, raw=False)
            else:
                User = await self.fetch_profile(msg[8:], cache=True, raw=False)
            if User is None:
                await message.reply(f"Can't invite {message.content[8:]}, the user isn't my friend")
                return
            try:
                if User.id in self.user.party.members:
                    await message.reply(f"{User.display_name} is already member of the party")
                    return
                else:
                    Friend = self.get_friend(User.id)
                    await Friend.invite()
                    os.system(colored.Colored(f"[BOT {self.user.display_name}] [{TimeInUTC}] Invited {Friend.display_name}", "green"))
                    await message.reply(f"Invited {Friend.display_name}")
            except fortnitepy.errors.PartyError:
                await message.reply(f"Can't invite {User.display_name}, the party is full.")

    if msg == "!LEAVE PARTY":
        if self.Settings["LeavePartyOnCommand"] or HasFullAccess:
            await self.user.party.me.set_emote('EID_Wave')
            await asyncio.sleep(2)
            await self.user.party.me.leave()
            await message.reply("Successfuly left Party.")
            os.system(colored.Colored(f"[BOT {self.user.display_name}] [{TimeInUTC}] Left party", "red"))
        else:
            await message.reply("Can't leave party. The Bot owner has disabled this command!")

    if msg == "!READY":
        if self.Settings["SetReadyOnCommand"] or HasFullAccess:
            await self.user.party.me.set_ready(True)
            await message.reply("Successfuly set my readiness to ready")
            os.system(colored.Colored(f"[BOT {self.user.display_name}] [{TimeInUTC}] Set readiness to ready", "green"))
        else:
            await message.reply("Can't set my readiness to ready. The Bot owner has disabled this command!")

    if msg == "!NOT READY":
        if self.Settings["SetNotReadyOnCommand"] or HasFullAccess:
            await self.user.party.me.set_ready(False)
            await message.reply("Successfuly set my readiness to not ready")
            os.system(colored.Colored(f"[BOT {self.user.display_namee}] [{TimeInUTC}] Set readiness to not ready", "green"))
        else:
            await message.reply("Can't set my readiness to not ready. The Bot owner has disabled this command!")

    if msg == "!STOP EMOTE":
        if self.Settings["LetOthersStopEmote"] or HasFullAccess:
            if self.user.party.me.emote is None:
                await message.reply("I am not dancing!")
            else:
                await self.user.party.me.clear_emote()
                if self.user.party.me.emote is None:
                    await message.reply("Stopped Dancing!")
                    os.system(colored.Colored(f"[BOT {self.user.display_name}] [{TimeInUTC}] Stopped dancing", "green"))
                else:
                    await self.user.party.me.set_emote("EID_InvaildEmoteToStopDancing")
                    if self.user.party.me.emote is None:
                        await message.reply("Stopped Dancing!")
                        os.system(colored.Colored(f"[BOT {self.user.display_name}] [{TimeInUTC}] Stopped dancing", "green"))
        else:
            await message.reply("Can't set stop dancing. The Bot owner has disabled this command!")

    if "!ADD" == args[0] and len(args) > 1:
        if self.Settings["SendFriendRequestsOnCommand"] or HasFullAccess:
            User = await self.fetch_profile(msg[5:], cache=False, raw=False)
            if User is None:
                await message.reply(f"Can't find user {message.content[5:]}")
                return
            try:
                await self.add_friend(User.id)
                await message.reply(f"Friend request send to {User.display_name}")
                os.system(colored.Colored(f"[BOT {self.user.display_name}] [{TimeInUTC}] Added {User.display_name}", "green"))
            except fortnitepy.errors.HTTPException as Error:
                Error2Send = Error.message
                for message_var in Error.message_vars:
                    if self.is_id(message_var):
                        UserName = (self.fetch_profile(message_var, cache=False, raw=False)).display_name
                        Error2Send.replace(message_var, UserName)
                await message.reply(Error2Send)
        else:
            await message.reply(f"Can't add {message.content[5:]}. The Bot owner has disabled this command!")

    if "!REMOVE" == args[0] and len(args) > 1:
        if self.Settings["RemoveOthersOnCommand"] or HasFullAccess:
            if await self.fetch_profile(msg[8:], cache=False, raw=False) is not None:
                User = await self.fetch_profile(msg[8:], cache=False, raw=False)
                if self.get_friend(User.id) is not None:
                    await self.remove_friend(User.id)
                    await message.reply(f"Removed {User.display_name} as my friend")
                    os.system(colored.Colored(f"Removed {User.display_name} as my friend","red"))
                else:
                    await message.reply("Can't find user in my friend list")
            else:
                await message.reply("Can't find user")
        else:
          await message.reply(f"Can't remove {message.content[5:]}. The Bot owner has disabled this command!")

    if msg == "!REMOVE":
        await message.reply('Are you sure that I should delete you as my friend? Please write "Yes delete me"')

        def isYes(message):
            if (message.author.id == author.id) and (message.content.upper() == "YES DELETE ME"):
                return True
            else:
                return False

        try:
            DeleteMe = await self.wait_for('message', check=isYes, timeout=200)
            if DeleteMe:
                try:
                    await self.remove_friend(message.author.id)
                    await message.reply("Removed you as my friend")
                    os.system(colored.Colored(f"[BOT {self.user.display_name}] [{TimeInUTC}] Removed {message.author.display_name} as my friend", "red"))
                except fortnitepy.errors.HTTPException as Error:
                    Error2Send = Error.message
                    for message_var in Error.message_vars:
                        if self.is_id(Error.message_vars):
                            UserName = (self.fetch_profile(message_var, cache=False, raw=False)).display_name
                            Error2Send.replace(message_var, UserName)
                    await message.reply(Error2Send)
        except asyncio.TimeoutError:
            await message.reply("You took too long, canceled removing you as a friend ♥")

    if msg == "?FRIENDS":
        if self.Settings["SendCurrentFriendCountOnCommand"] or HasFullAccess:
            Friend_count = len(self.friends.items())
            if Friend_count == 0:
                await message.reply("I dont have Friends")
            elif Friend_count == 1:
                await message.reply("I have one Friend")
            elif Friend_count > 1:
              await message.reply(f"I have {str(Friend_count)} friends")
        else:
            await message.reply("Can't send the count of my Friends. The Bot owner has disabled this command!")

    if msg == "?BLOCKED":
        if self.Settings["SendCurrentBlockedUserCountOnCommand"] or HasFullAccess:
            Blocked_count = len(await self.get_blocklist())
            if Blocked_count == 0:
                await message.reply("I dont have Blocked anyone")
            elif Blocked_count == 1:
                await message.reply("I have blocked one user")
            elif Blocked_count > 1:
                await message.reply("I have blocked {str(Blocked_count)} users")
        else:
            await message.reply("Can't send the count of my Friends. The Bot owner has disabled this command!")

    if msg == "?SHOP PRICE":
        if self.Settings["SendShopPriceOnCommand"] or HasFullAccess:
            Price = 0
            for item in (await self.fetch_item_shop()).featured_items + (await self.fetch_item_shop()).daily_items:
                Price += item.price
            await message.reply(f"Price in VBucks : {Price}, Price in $ : {Extras.MtxCurrencyConverter(Price)}")
        else:
            await message.reply("Can't send the current Price. The Bot owner has disabled this command!")

    if msg == "?ASSISTED CHALLENGE":
        if self.Settings["SendAssistedChallengeOnCommand"] or HasFullAccess:
            if self.user.party.me.assisted_challenge is not None:
                await message.reply(f"Current assisted challenge : {self.user.party.me.assisted_challenge}")
            else:
                await message.reply("I haven't set an assited challange")
        else:
            await message.reply("Can't send my assisted challenge. The Bot owner has disabled this command!")

    if msg == "?BANNER":
        if self.Settings["SendCurrentBannerNameOnCommand"] or HasFullAccess:
            await message.reply(f"Current Banner Name : {self.user.party.me.banner[0]}")
        else:
            await message.reply("Can't send the banner name. The Bot owner has disabled this command!")

    if args[0] == "?ID":
        if self.Settings["SendIDOnCommand"] or HasFullAccess:
            if msg == "?ID":
                await message.reply(f"My ID is : {str(self.user.id)}")
            elif len(args) > 1:
                User = await self.fetch_profile(msg[4:],cache=False,raw=False)
                await message.reply(f"ID : {User.id}")
        else:
            await message.reply("Can't send the Account ID. The Bot owner has disabled this command!")

    if msg == "?PARTY LEADER":
        if self.Settings["SendCurrentPartyLeaderOnCommand"] or HasFullAccess:
            PartyLeaderName = str(self.user.party.leader.display_name)
            await message.reply(f"Current Party Leader : {PartyLeaderName}")
        else:
            await message.reply("Can't send the current Party Leader Name.The Bot owner has disabled this command!")

    if msg == "?JOINED":
        if self.Settings["SendTimeBotJoinedTheLobbyOnCommand"] or HasFullAccess:
            delta_time = datetime.datetime.utcnow() - self.user.party.me.joined_at
            Time = datetime.timedelta(seconds=delta_time.seconds)
            await message.reply(f"Joined {Time} ago")
        else:
            await message.reply("Can't send join time. The Bot owner has disabled this command!")

    if msg == "?PARTY":
        if self.Settings["SendPartyInfosOnCommand"] or HasFullAccess:
            PartyLeader = str(self.user.party.leader.display_name)
            Members = str(self.user.party.member_count)
            PlayList = self.user.party.playlist_info[0]
            Privacy = str(self.user.party.privacy)[13:]
            Fill = str(self.user.party.squad_fill_enabled)
            await message.reply(f"Party leader : {PartyLeader} | Members : {Members} | Playlist : {PlayList} | Privacy : {Privacy} + | Fill : {Fill}")
        else:
            await message.reply("Can't send Party info. The Bot owner has disabled this command!")

    if msg == "!JOIN":
        if self.Settings["AcceptIncomingFriendRequest"] or HasFullAccess:
            if self.get_friend(author.id):
                try:
                    await self.get_friend(author.id).join_party()
                except:
                    await message.reply("Can't join your Party")
            else:
                await message.reply("You aren't my friend")
        else:
            await message.reply("Can't join. The Bot owner has disabled this command!")

    if args[0] == "!EMOTE" and len(args) > 1:
        if self.Settings["SetEmoteOnCommand"] or HasFullAccess:
            Lang = "en"
            if "--LANG=" in msg:
                msg = msg + " "
                Lang = GetValue(msg,"--LANG="," ")
                msg = msg.replace("--LANG=" + Lang, "").strip()
            Lang = Lang.lower()
            r = fnapi.GetEmote(NameorId=msg[7:],matchMethod="starts",searchLanguage=Lang,Language=Lang)
            if r.status != 200:
                await message.reply("Emote wasn't found")

                def isYes(msg):
                    if msg.author.id == message.author.id and msg.content.upper() == "USE EID":
                        return True
                    else:
                        return False

                if not msg[7:].startswith("EID_"):
                    await message.reply("If you are sure that emote exists please try again with the EID")
                else:
                    await message.reply('If you are sure this emote does exists write "Use EID"')
                try:
                    UseEID = await self.wait_for('message', check=isYes, timeout=100)
                    if UseEID:
                        await self.user.party.me.set_emote(msg[7:])
                except asyncio.TimeoutError:
                    return
            else:
                await self.user.party.me.set_emote(r.id)
                await message.reply(f'Emote set to {r.name}')

    if args[0] == "?SKIN" and args[0] ==  "VARIANTS" and len(args) > 2:
        Lang = "en"
        if "--LANG=" in msg:
            msg = msg + " "
            Lang = GetValue(msg,"--LANG="," ")
            msg = msg.replace("--LANG=" + Lang, "").strip()
        Lang = Lang.lower()

        r = fnapi.GetSkin(NameorId=msg[6:],matchMethod="starts",searchLanguage=Lang,Language=Lang)
        if r.status != 200:
            await message.reply("Skin wasn't found")
        terax = requests.get(f"https://fnapi.terax235.com/api/v1.2/cosmetics/search?query={r.id}&type=skin").json()
        allvariants = ""
        if terax.statusCode != 200:
            await message.reply("Sorry the server for variants isn't updated")
            return
        else:
            if "variants" in terax["data"]:
                for variant in terax["data"]["variants"]:
                    allvariants += f'{variant["channel"]}:\n'
                    for v in variant["tags"]:
                        allvariants += f'-{v["name"][Lang]}\n'
                await message.reply(allvariants)
            else:
                await message.reply("This skin doesn't have any variants or the server isn't updated")

    if args[0] == "!SKIN" and len(args) > 1:
        if self.Settings["SetSkinOnCommand"] or HasFullAccess:
            Lang = "en"
            if "--LANG=" in msg:
                msg = msg + " "
                Lang = GetValue(msg,"--LANG="," ")
                msg = msg.replace("--LANG=" + Lang, "").strip()
            Lang = Lang.lower()

            try:
                if msg.count("--") != 0:
                    Skin = GetValue(msg,"!SKIN ","--")
                else:
                    Skin = msg[6:]
            except:
                await message.reply("Command : !Skin <Skin Name> *--<Variant Channel Name>=<Variant Name>")

            r = fnapi.GetSkin(NameorId=Skin.strip(),matchMethod="starts",searchLanguage=Lang,Language=Lang)
            if r.status != 200:
                await message.reply("Skin wasn't found")

                def isYes(msg):
                    if msg.author.id == message.author.id and msg.content.upper() == "USE CID":
                        return True
                    else:
                        return False

                if not msg[10:].startswith("CID_"):
                    await message.reply("If you are sure that skin exists please try again with the CID")
                else:
                    await message.reply('If you are sure this skin does exists write "Use CID"')
                try:
                    UseCID = await self.wait_for('message', check=isYes, timeout=100)
                    if UseCID:
                        await self.user.party.me.set_outfit(msg[10:])
                except asyncio.TimeoutError:
                    return
            else:
                if msg.count("--") != 0:
                    terax = requests.get(f"https://fnapi.terax235.com/api/v1.2/cosmetics/search?query={r.id}&type=skin").json()
                    if terax.statusCode != 200:
                        await message.reply("Sorry the server for variants isn't updated")
                        return
                    v = []

                    def create_variant(VariantChannelName,Variant,item="AthenaCharacter"):
                        v = {
                            'item': item,
                            'channel': VariantChannelName,
                            'variant': Variant
                            }
                        return v

                    if "variants" in terax["data"]:
                        for Variant in GetValues(msg):
                            VariantChannelName = (Variant.split("=")[0])[2:]
                            Variant = Variant.split("=")[1]
                            for variant in terax["data"]["variants"]:
                                print(variant["channel"].upper() + " -> " + VariantChannelName)
                                if variant["channel"].upper() == VariantChannelName:
                                    for tag in variant["tags"]:
                                        if tag["name"][Lang].upper() == Variant:
                                            v.append(create_variant(variant["channel"],tag["tag"]))
                    
                    await self.user.party.me.set_outfit(r.id,variants=v)
                    await message.reply(f'Outfit set to {r.name}')

                else:
                    await self.user.party.me.set_outfit(r.id)
                    await message.reply(f'Outfit set to {r.name}')

    if args[0] == "!BACKPACK" and len(args) > 1:
        if self.Settings["SetBackpackOnCommand"] or HasFullAccess:
            Lang = "en"
            if "--LANG=" in msg:
                msg = msg + " "
                Lang = GetValue(msg,"--LANG="," ")
                msg = msg.replace("--LANG=" + Lang, "").strip()
            Lang = Lang.lower()
            r = fnapi.GetBackpack(NameorId=msg[10:],matchMethod="starts",searchLanguage=Lang,Language=Lang)
            if r.status != 200:
                await message.reply("Backpack wasn't found")

                def isYes(msg):
                    if msg.author.id == message.author.id and msg.content.upper() == "USE BID":
                        return True
                    else:
                        return False

                if not msg[10:].startswith("BID_"):
                    await message.reply("If you are sure that backpack exists please try again with the BID")
                else:
                    await message.reply('If you are sure this backpack does exists write "Use BID"')
                try:
                    UseBID = await self.wait_for('message', check=isYes, timeout=100)
                    if UseBID:
                        await self.user.party.me.set_backpack(msg[10:])
                except asyncio.TimeoutError:
                    return
            else:
                await self.user.party.me.set_backpack(r.id)
                await message.reply(f'Backpack set to {r.name}')