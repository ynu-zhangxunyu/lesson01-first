step01指令：用 Python 写一个复利计算程序：
- 本金 10000 元，年利率 5%，存 3 年，每年复利 1 次
- 输出最终本息和，保留两位小数
- 代码要带注释，逐行解释公式含义

# -*- coding: utf-8 -*-
# 复利计算程序
#
# 复利的意思：每年产生的利息会加入本金，下一年继续产生利息（利滚利）。
# 本题每年复利 1 次，公式为：
#
#       A = P * (1 + r) ** t
#
#   A —— 最终本息和（本金 + 所有利息）
#   P —— 本金（最初存入的钱）
#   r —— 年利率（百分数要先换成小数，5% 就是 0.05）
#   t —— 存款年数

P = 10000          # 本金 P = 10000 元
r = 5 / 100        # 年利率 r = 5%，除以 100 换成小数 0.05
t = 3              # 存款年限 t = 3 年

# (1 + r)：1 元钱存满 1 年后变成的钱，即本金 1 元 + 利息 0.05 元 = 1.05 元
# ** t  ：连存 3 年，就是把 1.05 自乘 3 次（1.05 * 1.05 * 1.05），即 1.05 的 3 次方
# P * …：本金有 10000 元，所以再乘以本金 P，得到第 3 年末的本息和
A = P * (1 + r) ** t

# :.2f 表示按浮点数格式输出并保留两位小数
print("最终本息和为：{:.2f} 元".format(A))








指令：用 Python 写一个复利计算程序
# -*- coding: utf-8 -*-
"""
复利计算程序

复利公式: A = P * (1 + r/n) ** (n*t)
  P : 本金
  r : 年利率(小数)
  n : 每年复利次数(1=年复利, 12=月复利, 365=日复利)
  t : 投资年限(支持小数)
  A : 到期本息合计

用法:
  1) 交互式:  python compound_interest.py
  2) 命令行:  python compound_interest.py 10000 3.5 10 --periods 12
"""

import sys
import argparse


# ---------- 输入解析 ----------

def parse_rate(text: str) -> float:
    """把利率解析为小数。

    兼容三种写法:
      "3.5%"  -> 0.035
      "3.5"   -> 0.035   (大于 1 视为百分数)
      "0.035" -> 0.035   (小于等于 1 视为小数)
    """
    s = str(text).strip().replace('％', '%')
    is_percent = s.endswith('%')
    s = s.rstrip('%').strip()
    value = float(s)

    if is_percent:
        return value / 100.0
    # 没写百分号: 3.5 这种明显是百分数, 0.035 这种明显是小数
    if value > 1.0:
        return value / 100.0
    return value


def ask(prompt: str, cast=float, default=None):
    """带默认值和容错的交互式输入。"""
    tip = f"{prompt}"
    if default is not None:
        tip += f" [默认 {default}]"
    tip += ": "

    while True:
        raw = input(tip).strip()
        if not raw and default is not None:
            return default
        try:
            return cast(raw)
        except ValueError:
            print("  输入无效, 请重新输入。")


# ---------- 核心计算 ----------

def compound_amount(principal: float, rate: float, years: float,
                    periods_per_year: int = 1) -> float:
    """计算复利到期本息合计。"""
    if periods_per_year <= 0:
        raise ValueError("每年复利次数必须为正整数")
    return principal * (1 + rate / periods_per_year) ** (periods_per_year * years)


def yearly_schedule(principal: float, rate: float, years: int,
                    periods_per_year: int = 1):
    """生成逐年明细表, 返回 [(年份, 年末本息, 当年利息), ...]。"""
    rows = []
    prev = principal
    for year in range(1, years + 1):
        amount = compound_amount(principal, rate, year, periods_per_year)
        rows.append((year, amount, amount - prev))
        prev = amount
    return rows


# ---------- 输出 ----------

def print_result(principal, rate, years, periods_per_year):
    amount = compound_amount(principal, rate, years, periods_per_year)
    interest = amount - principal

    period_name = {1: "每年复利", 12: "每月复利", 365: "每日复利"}.get(
        periods_per_year, f"每年复利 {periods_per_year} 次")

    print("=" * 46)
    print("           复 利 计 算 结 果")
    print("=" * 46)
    print(f"  本金         : {principal:>16,.2f} 元")
    print(f"  年利率       : {rate * 100:>15.2f} %")
    print(f"  投资年限     : {years:>16.2f} 年")
    print(f"  复利方式     : {period_name}")
    print("-" * 46)
    print(f"  到期本息合计 : {amount:>16,.2f} 元")
    print(f"  累计利息     : {interest:>16,.2f} 元")
    print(f"  资产增长倍数 : {amount / principal:>16.2f} 倍")
    print("=" * 46)

    # 整数年时给出逐年明细
    if float(years).is_integer():
        print("\n逐年明细:")
        print(f"  {'年份':<6}{'年末本息(元)':>18}{'当年利息(元)':>18}")
        print("  " + "-" * 42)
        for year, bal, yearly_interest in yearly_schedule(
                principal, rate, int(years), periods_per_year):
            print(f"  {year:<6}{bal:>18,.2f}{yearly_interest:>18,.2f}")
        print()


# ---------- 两种入口 ----------

def run_interactive():
    print("复利计算器 (直接回车可使用默认值)\n")
    principal = ask("请输入本金(元)", float)
    rate = parse_rate(ask("请输入年利率, 如 3.5 或 3.5% 或 0.035", str))
    years = ask("请输入投资年限(年, 可为小数)", float)
    periods = ask("每年复利次数 (1=年, 12=月, 365=日)", int, default=1)

    if principal < 0 or rate < 0 or years < 0:
        print("错误: 本金、利率、年限均不能为负数。")
        sys.exit(1)

    print_result(principal, rate, years, periods)


def run_args():
    parser = argparse.ArgumentParser(description="复利计算器")
    parser.add_argument("principal", type=float, help="本金(元), 如 10000")
    parser.add_argument("rate", type=str, help="年利率, 如 3.5 / 3.5%% / 0.035")
    parser.add_argument("years", type=float, help="投资年限(年, 可为小数)")
    parser.add_argument("-n", "--periods", type=int, default=1,
                        help="每年复利次数: 1=年复利(默认), 12=月复利, 365=日复利")
    args = parser.parse_args()

    if args.principal < 0 or args.years < 0 or args.periods <= 0:
        parser.error("本金/年限不能为负, 复利次数必须为正整数")

    rate = parse_rate(args.rate)
    print_result(args.principal, rate, args.years, args.periods)


if __name__ == "__main__":
    # 带命令行参数时走参数模式, 否则进入交互式
    if len(sys.argv) > 1:
        run_args()
    else:
        run_interactive()

