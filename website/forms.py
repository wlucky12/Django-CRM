from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .utils.bootstrap import BootStrapModelForm
from .models import Customer, Transaction, Account

class SignUpForm(UserCreationForm):
    # email = forms.EmailField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}))
    # name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'}))
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#循环找到所有字段，并给每个字段插件添加css样式
		for name, field in self.fields.items():
			field.widget.attrs={'class': 'form-control','placeholder':name}

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
		
#通过继承BootStrapModelForm，实现自动添加css样式
class AddRecordForm(BootStrapModelForm):
    # name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Name", "class":"form-control"}), label="")
    # email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control"}), label="")
    # phone_number = forms.IntegerField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone Number", "class":"form-control"}), label="")
    # address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Address", "class":"form-control"}), label="")
    
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_number','address']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'account', 'target_account', 'amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.all()
        self.fields['target_account'].queryset = Account.objects.all()
        self.fields['target_account'].required = False

        # 为账户字段添加客户名
        self.fields['account'].label_from_instance = lambda obj: f"{obj.account_number} - {obj.get_customer_name()}"
        self.fields['target_account'].label_from_instance = lambda obj: f"{obj.account_number} - {obj.get_customer_name()}"

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        account = cleaned_data.get('account')
        target_account = cleaned_data.get('target_account')
        amount = cleaned_data.get('amount')

        if transaction_type == 'transfer' and not target_account:
            raise forms.ValidationError("转账交易必须指定目标账户。")

        if account and amount:
            if transaction_type == 'withdrawal' and account.account_balance < amount:
                raise forms.ValidationError("账户余额不足。")
            if transaction_type == 'transfer' and account.account_balance < amount:
                raise forms.ValidationError("账户余额不足，无法完成转账。")

        return cleaned_data