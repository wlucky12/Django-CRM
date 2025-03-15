from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from website.models import Customer

class Command(BaseCommand):
    help = 'Update passwords for all customers'

    def handle(self, *args, **kwargs):
        customers = Customer.objects.all()
        for customer in customers:
            if not customer.password.startswith('pbkdf2_sha256$'):  # 检查密码是否已哈希
                customer.password = make_password(customer.password)  # 哈希存储密码
                customer.save()
                self.stdout.write(self.style.SUCCESS(f'Updated password for {customer.name}')) 