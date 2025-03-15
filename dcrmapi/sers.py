# 序列化器
from rest_framework import serializers
from website.models import Customer,Account,Transaction

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()  # 自定义字段，返回客户名字

    class Meta:
        model = Account
        fields = '__all__'
    def get_customer_name(self, obj):
        return obj.customer.name if obj.customer else "无客户"

class TransactionSerializer(serializers.ModelSerializer):
    account_customer_name = serializers.SerializerMethodField()  # 自定义字段，返回账户客户名字
    target_account_customer_name = serializers.SerializerMethodField()  # 自定义字段，返回目标账户客户名字

    class Meta:
        model = Transaction
        fields = '__all__'
    def get_account_customer_name(self, obj):
        return obj.account.customer.name if obj.account and obj.account.customer else "无客户"

    def get_target_account_customer_name(self, obj):
        return obj.target_account.customer.name if obj.target_account and obj.target_account.customer else "无客户"
