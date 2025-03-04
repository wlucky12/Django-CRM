from django import forms

class BootStrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #循环找到所有字段，并给每个字段插件添加css样式
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = name
            else:
                field.widget.attrs={
                      'class': 'form-control',
                      'placeholder':name,
                    }