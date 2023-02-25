# 仅供娱乐，类Windows 95风格的注册码生成验证
# https://gurney.dev/posts/mod7/
import random


# 生成激活码
def generate_key():
    # 随机生成日期部分（格式为 "DDDYY"，其中 DDD 代表一年中的第几天，YY 代表年份）
    day_of_year = str(random.randint(1, 366)).zfill(3)
    year = str(random.randint(95, 99)).zfill(2)
    date_part = f"{day_of_year}{year}"

    # 生成数字部分，直到其数位之和能被7整除，并且第一位为0
    while True:
        key_digits = str(random.randint(0, 9999999)).zfill(7)
        if sum(int(digit) for digit in key_digits) % 7 == 0 and key_digits[0] == "0":
            break

    # 将日期部分和数字部分组合在一起
    key = f"{date_part}{key_digits}"

    # 无意义，但检验
    if not validate_key(key):
        return generate_key()

    return key


# 验证激活码
def validate_key(key):
    # 检查激活码的格式
    if not key or len(key) != 12:
        return False

    date_part = key[:5]
    key_digits = key[5:]

    # 第一段日期部分必须是格式为 "DDDYY" 的字符串
    if not date_part.isdigit() or len(date_part) != 5:
        return False

    day_of_year = int(date_part[:3])
    year = int(date_part[3:])

    # DDD必须在001-366之间，YY必须在95-99之间
    if not (1 <= day_of_year <= 366) or not (95 <= year <= 99):
        return False

    # 数字部分的数位之和必须能被7整除，并且第一位为0
    if sum(int(digit) for digit in key_digits) % 7 != 0 or key_digits[0] != "0":
        return False

    return True


if __name__ == "__main__":
    print(generate_key())
