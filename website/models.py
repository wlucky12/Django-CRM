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
    customer=models.ForeignKey(Customer,blank=True,null=True,on_delete=models.SET_NULL,verbose_name="客户ID")
    account_number=models.CharField(max_length=50,unique=True,verbose_name="账号")
    TYPE_CHOICES = [
        (1, '活期'),
        (2, '定期'),
    ]
    account_type = models.SmallIntegerField(
        choices=TYPE_CHOICES,
        default=1,
        verbose_name='账户类型',
    )
    account_balance=models.IntegerField(verbose_name="账户余额",default=10000)
    
    def __str__(self):
        return(f"{self.account_number}")

    class Meta:
        verbose_name="账户"
        verbose_name_plural="账户"

class Transaction(models.Model):
    account=models.ForeignKey(Account,blank=True,null=True,on_delete=models.SET_NULL,verbose_name="账户ID")
    TRANSACTION_CHOICES = [
        (1, 'deposit'),
        (2, 'withdraw'),
        (3, 'transfer'),
    ]
    account_type = models.SmallIntegerField(
        choices=TRANSACTION_CHOICES,
        default=1,
        verbose_name='交易类型',
    )
    transaction_amount=models.IntegerField(verbose_name="交易金额",default=0)
    transaction_date=models.DateTimeField(auto_now_add=True)
    transaction_description=models.TextField(max_length=100,default='',verbose_name="交易描述")

    def __str__(self):
        return(f"{self.transaction_type}")
    
    class Meta:
        verbose_name="交易"
        verbose_name_plural="交易"