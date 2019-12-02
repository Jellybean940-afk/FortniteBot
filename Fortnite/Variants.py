def GetVariant(Variant,All):
    i = 0
    args = All.split(" ")
    lenOfArgs = len(args) - 1
    for arg in args:
        i += 1
        if arg.startswith(Variant):
            indexOfVariant = All.index(Variant)
            while i < lenOfArgs or i == lenOfArgs:
                if "=" in args[i]:
                    return(All[indexOfVariant:(All.index(args[i]))]).strip()
                i += 1
            return All[indexOfVariant:]

def GetVariantNames(All):
    i = 0
    VariantNames = []
    args = All.split(" ")
    lenOfArgs = len(args) - 1
    for arg in args:
        i += 1
        if "=" in arg:
            indexOfVariant = All.index(arg)
            indexOfEqual = arg.index("=")
            VariantNames.append(All[indexOfVariant:(indexOfVariant + indexOfEqual + 1)])
    return VariantNames
