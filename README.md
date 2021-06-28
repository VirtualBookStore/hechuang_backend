# hechuang_backend

## API文档

[自动生成的API文档](openapi-schema.yml)

*注意，所有价格单位精确到人民币分*


## how to develop

### 安装python3

必须是python3.9，不然会报错

```bash
python -V
```


将默认的python版本也设置成3.9

### 使用virtualenv（可选）

```bash
python -m venv venv
source ./venv/bin/activate
```


### 安装依赖

```bash
pip install -r requirements.txt
```

### 切换到文件夹下
```bash
cd hechuang # manage.py 所在的目录
```

### 开发服务器
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver # 调试
```

默认会是假设在`http://127.0.0.1:8000/`
的简单服务器api文档在`http://127.0.0.1:8000/openapi/`
swagger可视化版本是`http://127.0.0.1:8000/swagger-ui/`
redoc可视化版本是`http://127.0.0.1:8000/redoc/`

### 使用gunicorn部署

```bash
cd hechuang # manage.py 所在的目录
pip install gunicorn
gunicorn -b=0.0.0.0:6629 -w=4 hechuang.wsgi # 以4个线程启动，在6629端口
```



### 一些内置数据
```

# 管理员
username='admin'
email='rand1925@tongji.edu.cn',
password='admin123'

# 顾客
username='rand1925'
email='rand1925@tongji.edu.cn'
password='rand1925'

# tag
1 教科书
2 软件工程
3 Java

# 书籍
isbn='7111548973',
title='软件工程',
escription='实践者的研究方法',
price=9900,
new_total=5,
tags = [1. 2]


isbn='7302244752'
title='Java程序设计'
description='Java程序设计'
price=3500
new_total=0
old_total=5
recommended=True
tags = [1, 3]


isbn='7115420114'
title='Java核心技术'
description='Core Java'
price=10900
new_total=10
old_total=10
recommended=False
tags = [3]

```
