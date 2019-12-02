def isNaN(Nummer):
    try:
        Nummer = int(Nummer)
        return False
    except:
        return True

def MtxCurrencyConverter(VBucks):
    VBucks = int(VBucks)
    Price = int(0)

    while VBucks > 13500 or VBucks == 13500:
        Price += 99.99
        VBucks -= 13500

    while VBucks > 7500 or VBucks ==  7500:
        Price += 59.99
        VBucks -= 7500

    while VBucks > 2800 or VBucks ==  2800:
        Price += 24.99
        VBucks -= 2800

    while VBucks > 1000 or VBucks ==  1000:
        Price += 9.99
        VBucks -= 1000

    while VBucks > 0:
        Price += 9.99
        VBucks -= 1000

    return round(Price, 2)
