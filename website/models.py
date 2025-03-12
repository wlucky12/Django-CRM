from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_id=models.AutoField(primary_key=True,verbose_name="客户ID")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name=models.CharField(max_length=50,verbose_name="姓名")
    email=models.EmailField(max_length=100,verbose_name="邮箱")
    phone_number=models.CharField(max_length=50,verbose_name="电话号码")
    address=models.TextField(max_length=100,verbose_name="地址")

    def __str__(self):
        return(f"{self.name}")
    
    class Meta:
        verbose_name="客户"
        verbose_name_plural="客户"

class Account(models.Model):
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="客户ID")
    account_number = models.CharField(max_length=50, unique=True, verbose_name="账号")
    TYPE_CHOICES = [
        (1, '活期'),
        (2, '定期'),
    ]
    account_type = models.SmallIntegerField(
        choices=TYPE_CHOICES,
        default=1,
        verbose_name='账户类型',
    )
    account_balance = models.IntegerField(verbose_name="账户余额", default=10000)
    
    def __str__(self):
        return f"{self.account_number}"

    def get_customer_name(self):
        return self.customer.name if self.customer else "无客户"

    class Meta:
        verbose_name = "账户"
        verbose_name_plural = "账户"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', '存款'),
        ('withdrawal', '取款'),
        ('transfer', '转账'),
    ]
    
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    account = models.ForeignKey(Account, related_name='transactions', on_delete=models.CASCADE, null=True, blank=True)
    target_account = models.ForeignKey(Account, related_name='received_transactions', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} on {self.date}"
    
    class Meta:
        verbose_name="交易"
        verbose_name_plural="交易"