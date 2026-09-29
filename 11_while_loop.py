# input_number = [0]
# while input_number[len(input_number) - 1] != "q":
#     num = input("请输入数字(输入q结束):")
#     input_number.append(num)
#
# input_number.remove("q")
# sum = 0
# average = 0
#
# for i in input_number:
#     sum += float(i)
#
# if sum == 0:
#     average = 0
# else:
#     average = sum / (len(input_number) - 1)
# print("输入数字的和为", str(sum), "\n", "输入数字的平均值为", str(average), "\n")

total = 0
count = 0
user_input = input("请输入数字（完成所有数字输入后，请输入q终止程序）：")
while user_input != "q":
    num = float(user_input)
    total += num
    count += 1
    user_input = input("请输入数字（完成所有数字输入后，请输入q终止程序）：")
if count == 0:
    result = 0
else:
    result = total / count
print("您输入的数字平均值为" + str(result))
