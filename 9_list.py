shop_list=[]
shop_list.append("键盘")
shop_list.append("键帽")
print(shop_list)
shop_list.remove("键帽")
print(shop_list)
shop_list.append("音响")
shop_list.append("电竞椅")
shop_list[1]="硬盘"
print(shop_list,len(shop_list))
print(shop_list[2])

price =[799,1024,200,800]
max_price=max(price)
min_price=min(price)
sorted_price=sorted(price)
print(max_price,min_price,sorted_price)