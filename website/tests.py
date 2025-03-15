from django.test import TestCase
from .views.views import luhn_check_digit
# Create your tests here.
# 测试Luhn算法
def test_luhn_check_digit():
    # 已知有效的银行卡号：6228481234567892（校验位为 2）
    partial_number = '622848123456789'  # 前 15 位
    check_digit = luhn_check_digit(partial_number + '0')  # 补 0 计算校验位
    assert check_digit == '2', f"Expected 2, got {check_digit}"

def test_luhn_check_digit_random():
    # 随机生成 15 位数字
    import random
    partial_number = ''.join([str(random.randint(0, 9)) for _ in range(15)])
    check_digit = luhn_check_digit(partial_number + '0')
    full_number = partial_number + check_digit
    # 验证生成的卡号是否通过 Luhn 校验
    assert luhn_check_digit(full_number + '0') == '0', "Generated card number is invalid"