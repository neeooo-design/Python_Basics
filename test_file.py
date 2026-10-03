# 3. 测试报告统计：练文件与异常处理
# 读取 UTF-8 CSV，列为 case_id,status,duration_ms。状态只允许 PASS、FAIL、SKIP，耗时必须是非负整数，case_id 不得重复。
# 输出总数、各状态数量和失败用例 ID 列表。格式错误时抛出带行号的 ValueError。
# 测试空文件、正常文件、重复 ID、非法状态、负耗时，以及含中文或逗号的用例 ID。可以使用标准库 csv 和临时文件。

import csv
import os
import tempfile
import unittest


def analyze_test_report(file_path):
    total = 0
    status_counts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    failed_ids = []
    seen_ids = set()

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)

        for line_num, row in enumerate(reader, start=1):
            # 跳过空行
            if not row:
                continue

            # 第一行如果是表头，跳过表头
            if line_num == 1 and [col.strip() for col in row] == ["case_id", "status", "duration_ms"]:
                continue

            # 1. 校验列数
            if len(row) != 3:
                raise ValueError(f"第 {line_num} 行格式错误：列数必须为 3")

            case_id = row[0].strip()
            status = row[1].strip()
            duration_str = row[2].strip()

            # 2. 校验 case_id 重复
            if case_id in seen_ids:
                raise ValueError(f"第 {line_num} 行 case_id 重复：'{case_id}'")
            seen_ids.add(case_id)

            # 3. 校验状态合法性
            if status not in ("PASS", "FAIL", "SKIP"):
                raise ValueError(f"第 {line_num} 行状态非法：'{status}'")

            # 4. 校验耗时必须是非负整数
            try:
                duration = int(duration_str)
                if duration < 0:
                    raise ValueError
            except ValueError:
                raise ValueError(f"第 {line_num} 行耗时必须是非负整数：'{duration_str}'")

            # 5. 累加统计
            total += 1
            status_counts[status] += 1
            if status == "FAIL":
                failed_ids.append(case_id)

    return {
        "total": total,
        "status_counts": status_counts,
        "failed_ids": failed_ids,
    }


class TestReportAnalysis(unittest.TestCase):
    def setUp(self):
        # 记录本次测试生成的所有临时文件路径
        self.temp_files = []

    def tearDown(self):
        # 测试结束后，清理所有临时文件
        for file_path in self.temp_files:
            if os.path.exists(file_path):
                os.remove(file_path)

    def create_temp_file(self, content):
        """辅助方法：传入 CSV 内容，写入临时文件并返回文件路径"""
        temp = tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False)
        temp.write(content)
        temp.close()
        self.temp_files.append(temp.name)
        return temp.name

    def test_normal_file(self):
        """测试正常文件统计"""
        content = (
            "case_id,status,duration_ms\n"
            "case_01,PASS,100\n"
            "case_02,FAIL,250\n"
            "case_03,SKIP,0\n"
            "case_04,FAIL,300\n"
        )
        file_path = self.create_temp_file(content)
        result = analyze_test_report(file_path)

        self.assertEqual(result["total"], 4)
        self.assertEqual(result["status_counts"]["PASS"], 1)
        self.assertEqual(result["status_counts"]["FAIL"], 2)
        self.assertEqual(result["status_counts"]["SKIP"], 1)
        self.assertEqual(result["failed_ids"], ["case_02", "case_04"])

    def test_empty_file(self):
        """测试完全空的文件"""
        file_path = self.create_temp_file("")
        result = analyze_test_report(file_path)

        self.assertEqual(result["total"], 0)
        self.assertEqual(result["status_counts"]["PASS"], 0)
        self.assertEqual(result["status_counts"]["FAIL"], 0)
        self.assertEqual(result["status_counts"]["SKIP"], 0)
        self.assertEqual(result["failed_ids"], [])

    def test_duplicate_id(self):
        """测试 case_id 重复抛出异常并带行号"""
        content = (
            "case_id,status,duration_ms\n"
            "case_01,PASS,100\n"
            "case_01,FAIL,200\n"
        )
        file_path = self.create_temp_file(content)
        with self.assertRaises(ValueError) as cm:
            analyze_test_report(file_path)
        self.assertIn("第 3 行", str(cm.exception))

    def test_invalid_status(self):
        """测试非法状态抛出异常并带行号"""
        content = (
            "case_id,status,duration_ms\n"
            "case_01,ERROR,100\n"
        )
        file_path = self.create_temp_file(content)
        with self.assertRaises(ValueError) as cm:
            analyze_test_report(file_path)
        self.assertIn("第 2 行", str(cm.exception))

    def test_negative_duration(self):
        """测试负数耗时抛出异常并带行号"""
        content = (
            "case_id,status,duration_ms\n"
            "case_01,PASS,-10\n"
        )
        file_path = self.create_temp_file(content)
        with self.assertRaises(ValueError) as cm:
            analyze_test_report(file_path)
        self.assertIn("第 2 行", str(cm.exception))

    def test_non_integer_duration(self):
        """测试非整数耗时（如小数、文本）抛出异常并带行号"""
        content = (
            "case_id,status,duration_ms\n"
            "case_01,PASS,12.5\n"
        )
        file_path = self.create_temp_file(content)
        with self.assertRaises(ValueError) as cm:
            analyze_test_report(file_path)
        self.assertIn("第 2 行", str(cm.exception))

    def test_chinese_and_comma_case_id(self):
        """测试 case_id 包含中文以及包含逗号"""
        content = (
            "case_id,status,duration_ms\n"
            '"用例,01",FAIL,150\n'
            "登录模块测试,PASS,80\n"
        )
        file_path = self.create_temp_file(content)
        result = analyze_test_report(file_path)

        self.assertEqual(result["total"], 2)
        self.assertEqual(result["status_counts"]["FAIL"], 1)
        self.assertEqual(result["status_counts"]["PASS"], 1)
        self.assertEqual(result["failed_ids"], ["用例,01"])


if __name__ == "__main__":
    unittest.main()
