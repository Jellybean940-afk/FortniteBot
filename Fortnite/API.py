import requests,json,asyncio

def GetSkinVariant(Variant,All):
    i = 0
    args = All.split(" ")
    lenOfArgs = len(args) - 1
    for arg in args:
        if Variant in arg:
            indexOfVariant = All.index(Variant)
            i += 1
            while i < lenOfArgs or i == lenOfArgs:
                if "=" in args[i]:
                    return(All[indexOfVariant:(All.index(args[i]))])
                i += 1
            return(All[indexOfVariant:])

def CheckIfSkinVariantExists(Skin,Variant,VariantChannelName):
    r = json.loads((requests.get(f"https://fortniteapi--lupusleaks.repl.co/Cosmetic?skin={Skin}")).text)
    if len(r["Variants"]) > 0:
      if r["Variants"][VariantChannelName]:
        for Variant2 in r["Variants"][VariantChannelName]:
            if Variant2.upper() == Variant.upper():
                return Variant2
        for Variant2 in r["Variants"][VariantChannelName]:
            if Variant2.startswith(Variant):
                return Variant2
        return "Not Found!"

def GetVariantIndex(Skin,Variant,VariantChannelName):
    r = json.loads((requests.get(f"https://fortniteapi--lupusleaks.repl.co/Cosmetic?skin={Skin}")).text)
    if len(r["Variants"]) > 0:
      if r["Variants"][VariantChannelName]:
        i = 0
        for Variant2 in r["Variants"][VariantChannelName]:
            if Variant2.upper() == Variant.upper():
                return i
            i += 1
        i = 0
        for Variant2 in r["Variants"][VariantChannelName]:
            if Variant2.startswith(Variant):
                return i
            i += 1
        return "Not Found!"

async def SetSkin(self, message):
    Skin = message.content.upper()[6:]
    r = json.loads((requests.get(f"https://fortniteapi--lupusleaks.repl.co/Cosmetic?skin={Skin}")).text)
    if r == "Not Found!":
        await message.reply("Skin wasn't found")

        def isYes(msg):
            if msg.author.id == message.author.id and msg.content.upper() == "USE CID":
                return True
            else:
                return False

        if not Skin.startswith("CID_"):
            await message.reply("If you are sure that skin exists please try again with the CID")
        else:
            await message.reply('If you are sure this skin does exists write "Use CID"')
        try:
            UseCID = await self.wait_for('message', check=isYes, timeout=100)
            if UseCID:
                await self.user.party.me.set_outfit(Skin)
        except asyncio.TimeoutError:
            return

    else:
        await self.user.party.me.set_outfit(asset=json.loads((requests.get(f"https://fortniteapi--lupusleaks.repl.co/Cosmetic?skin={Skin}")).text)["CID"],variants=None)
