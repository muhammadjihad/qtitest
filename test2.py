data=[x for x in range(1,101)]
n=len(data)
for i in range(n):
    if data[i]%2 == 0:
        if data[i]%7 == 0:
            data[i]="tiktok"
        else:
            data[i]="tok"
    else:
        if data[i]%7 == 0:
            data[i]="tiktok"
        else:
            data[i]="tik"
print(data)