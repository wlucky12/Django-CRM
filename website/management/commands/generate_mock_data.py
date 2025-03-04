from django.core.management.base import BaseCommand
from faker import Faker
import random
from website.models import Customer, Account

class Command(BaseCommand):
    help = 'Generate mock data for Customer and Account models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of mock customers to create',
        )

    def handle(self, *args, **kwargs):
        fake = Faker('zh_CN')  # 使用中文数据
        count = kwargs['count']

        for _ in range(count):
            # 创建客户
            customer = Customer.objects.create(
                name=fake.name(),
                email=fake.email(),
                phone_number=fake.phone_number(),
                address=fake.address()
            )

            # 创建账户
            account_number = fake.unique.bothify('##########')  # 10位随机数字
            Account.objects.create(
                customer=customer,
                account_number=account_number,
                account_type=random.choice([1, 2]),  # 随机选择账户类型
                account_balance=random.randint(1000, 100000)  # 随机余额
            )

        self.stdout.write(self.style.SUCCESS(f'成功创建 {count} 条客户和账户数据'))