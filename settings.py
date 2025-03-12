TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # 如果有全局模板目录
        'APP_DIRS': True,  # 自动查找每个应用的templates目录
        'OPTIONS': {
            'context_processors': [
                # ... 其他配置
            ],
        },
    },
] 