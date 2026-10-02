# 3. 测试报告统计：练文件与异常处理
# 读取 UTF-8 CSV，列为 case_id,status,duration_ms。状态只允许 PASS、FAIL、SKIP，耗时必须是非负整数，case_id 不得重复。
# 输出总数、各状态数量和失败用例 ID 列表。格式错误时抛出带行号的 ValueError。
# 测试空文件、正常文件、重复 ID、非法状态、负耗时，以及含中文或逗号的用例 ID。可以使用标准库 csv 和临时文件。