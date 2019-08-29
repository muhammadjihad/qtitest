with open("file.txt") as f:
    data=f.read().split("\n")
    data=list(map(lambda el:[el,data.count(f"{el}")],data))
    countData=list()
    for el in data:
        if el not in countData:
            countData.append(el)
    print(countData)