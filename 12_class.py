"""
写一个计算BMI的函数，函数名为calculate_BMI。
1、可以计算任意体重和身高的BMI值
2、执行过程中打印一句话，“您的BMI分类为：**”
3、返回计算出的BMI值
"""


def calculate_BMI(height, weight):
    BMI = weight / (height ** 2)
    if BMI <= 18.5:
        category="偏瘦"
    elif 18.5 < BMI <= 25:
        category="正常"
    elif 25 < BMI <= 30:
        category="偏胖"
    else:
        category="肥胖"
    print(f"您的BMI分类为：{category}")
    return BMI


height = float(input("请输入你的身高（单位：m）："))
weight = float(input("请输入你的体重（单位：kg）："))

print("您的BMI为", calculate_BMI(height, weight))
