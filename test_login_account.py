# 2. 登录锁定：练状态转换测试
# 编写 LoginAccount 类，提供 login(password) 和 reset_lock()：
# - 连续输错 3 次后锁定。
# - 登录成功会清零错误次数。
# - 锁定后，即使密码正确也不能登录，直到调用 reset_lock()。
# - login() 返回 "success"、"wrong_password" 或 "locked"。
# 测试完整操作序列，例如“错两次 → 成功 → 再错三次 → 正确密码仍被拒绝 → 重置 → 成功”。不要只测试单次调用。
import unittest
class LoginAccount():
    def __init__(self,password:str):
        self.password=password
        self.lock_num=0
        self.lock_click=0
        
    def login(self,input_password):
        if self.lock_click==1:
            return "locked"
        else:
            if input_password==self.password:
                self.lock_num=0
                return "success"
            else:
                self.lock_num+=1
                if self.lock_num==3:
                    self.lock_click=1
                    return "locked"
                return "wrong_password"
          
        
    def reset_lock(self):
        self.lock_click=0
        self.lock_num=0

class TestLoginAccount(unittest.TestCase):
    def setUp(self):
        self.account=LoginAccount("12345")
        
    def test_password(self):
        self.assertEqual(self.account.login("1"),"wrong_password")
        self.assertEqual(self.account.login("2"),"wrong_password")
        self.assertEqual(self.account.login("12345"),"success")
        self.assertEqual(self.account.login("1"),"wrong_password")
        self.assertEqual(self.account.login("2"),"wrong_password")
        self.assertEqual(self.account.login("3"),"locked")
        self.assertEqual(self.account.login("12345"),"locked")
        self.account.reset_lock()
        self.assertEqual(self.account.login("12345"),"success")