import datetime
from XiaoHei import xiaohei
# 我的债务
# 1. 杭州联合银行 50w 3.8% 每个月20号 每个月还1583.3元，开始日20230426-20260409
# 2. 中国信银行 30w 3.5% 每个月21号 每个月还875元，开始日20230428-结束日20240428


class Loan:
    def __init__(self, bank_name, amount, interest_rate, start_date, end_date, installment_day, monthly_payment):
        self.bank_name = bank_name
        self.amount = amount
        self.interest_rate = interest_rate
        self.start_date = start_date
        self.end_date = end_date
        self.installment_day = installment_day
        self.monthly_payment = monthly_payment

    # 是还款日
    def is_installment_day(self):
        today = datetime.date.today()
        return today.day == self.installment_day

    def check_last_three_months(self):
        remaining_months = (self.end_date - datetime.date.today()).days // 30
        if remaining_months <= 3:
            print(f"注意：{self.bank_name}的贷款即将到期，还剩下不到三个月的时间。请及时安排还款。")

    def print_installment_info(self):
        if self.is_installment_day():
            xiaohei.send_text(
                f"今天是{self.bank_name}的还款日！应还款金额为 {self.monthly_payment: .2f} 元。")
            self.check_last_three_months()
        else:
            pass


# 创建贷款对象
loan1 = Loan("杭州联合银行", 500000, 3.8, datetime.date(
    2023, 4, 26), datetime.date(2026, 4, 9), 25, 1583.3)
loan2 = Loan("中国信银行", 300000, 3.5, datetime.date(
    2023, 4, 28), datetime.date(2024, 4, 28), 25, 875)


def check_debt():
    # 判断是否是还款日并输出还款信息
    loan1.print_installment_info()
    loan2.print_installment_info()
