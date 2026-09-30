# 1. 运费计算：练边界值测试
# 编写 shipping_fee(amount_cents, region)：
# - region 为 "domestic" 时，订单金额低于 9900 分收 800 分运费；达到 9900 分免运费。
# - region 为 "international" 时，固定收 3000 分。
# - 金额为负数或地区无效时抛出 ValueError；金额不是整数时抛出 TypeError。
# 用 unittest 至少覆盖金额 0、9899、9900、9901，两个地区，以及错误输入。特别想想：
# Python 中 True 算不算整数，你希望函数怎样处理？
import unittest
def shipping_fee(region,amount_cents):
    if  not isinstance(amount_cents,int) or isinstance(amount_cents,bool):
         raise TypeError("金额不是整数")
    elif amount_cents<0 or region not in ["domestic","international"]:
        raise ValueError("金币为负或地区无效")
    else:
        if region=="domestic":
            if amount_cents<9900:
                return 800
            else:
                return 0
        else:
            return 3000
class TestShippingFee(unittest.TestCase):
    def test_domestic_shipping_fee(self):
        self.assertEqual(shipping_fee("domestic",9899),800)
        self.assertEqual(shipping_fee("domestic",9901),0)
        self.assertEqual(shipping_fee("domestic",0),800)
        self.assertEqual(shipping_fee("domestic",9900),0)

    def test_international_shipping_fee(self):
        self.assertEqual(shipping_fee("international",9899),3000)
        self.assertEqual(shipping_fee("international",9901),3000)
        self.assertEqual(shipping_fee("international",0),3000)
        self.assertEqual(shipping_fee("international",9900),3000)

    def test_error_region(self):
        with self.assertRaises(ValueError):
            shipping_fee("home",9900)

    def test_amount_cents(self):
        with self.assertRaises(ValueError):
            shipping_fee("domestic",-1)

    def test_error_type(self):
        with self.assertRaises(TypeError):
            shipping_fee("domestic",500.5)
        with self.assertRaises(TypeError):
            shipping_fee("domestic",True)