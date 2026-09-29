# 定义一个学生类
# 要求:
# 1，属性包括学生姓名、学号，以及语数英三科的成绩
# 2.能够设置学生某科目的成绩
# 3，能够打印出该学生的所有科目成绩

class Student:
    def __init__(self, name, student_id,
                 # chinese_score,math_score,english_score
                 ):
        self.name = name
        self.student_id = student_id
        self.score_list = {"语文": 0, "数学": 0, "英语": 0}
        # self.chinese_score=chinese_score
        # self.math_score=math_score
        # self.english_score=english_score

    # def set_chinese_score(self, chinese_score):
    #     self.chinese_score = chinese_score
    #
    # def set_math_score(self, math_score):
    #     self.math_score = math_score
    #
    # def set_english_score(self, english_score):
    #     self.english_score = english_score

    # def print_score(self):
    #     print("你的语文成绩是", self.chinese_score, "你的数学成绩是", self.math_score, "你的英语成绩是",
    #           self.english_score)
    def set_score(self, course, score):
        if course in self.score_list:
            self.score_list[course] = score

    # def print_information(self):
    #     print(f"姓名：{self.name},学号：{self.student_id},语文成绩为{self.score_list['语文']},数学成绩为{self.score_list['数学']},英语成绩为{self.score_list['英语']}")

    def print_score(self):
        print(f"学生{self.name}的成绩是：")
        for course in self.score_list:
            print(f"{course}:{self.score_list[course]}分")

student1 = Student("张三", "2001111",
                    # 60, 70, 80
                    )
# student1.print_score()
# student1.set_chinese_score(70)
# student1.print_score()
student1.set_score("数学", 95)
print(student1.name)
print("语文成绩为", student1.score_list["语文"])
print(student1.score_list)
# student1.print_information()
student1.print_score()