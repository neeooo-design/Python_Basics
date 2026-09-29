with open("C:/python基础/data.txt","r",encoding="utf-8") as f:
    print(f.readlines())


    lines = f.readlines()
    for i in lines:
        print(i)