# BMI=体重/(身高**2)
weight = input("请输入你的体重(单位:kg):")
height = input("请输入你的身高(单位:m):")
BMI = float(weight) / (float(height) ** 2)
print("您的BMI为" + str(BMI))

# 偏瘦：BMI<=18.5
# 正常：18.5<BMI<=25
# 偏胖：25<BMI<=30
# 肥胖：BMI>30
if BMI < 18.5:
    print("偏瘦")
elif 18.5 < BMI <= 25:
    print("正常")
elif 25 < BMI <= 30:
    print("偏胖")
else :
    print("肥胖")
