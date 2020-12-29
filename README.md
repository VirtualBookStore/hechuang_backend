# hechuang_backend

## API文档

[自动生成的API文档](openapi-schema.yml)

*注意，所有价格单位精确到人民币分*


## how to run

### 安装python3

最好是3.9

### 安装依赖
```
pip install -r requirements.txt
```

### 切换到文件夹下
```
cd hechuang
```

### 启动
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

默认会是假设在`http://127.0.0.1:8000/`
的简单服务器
api文档在`http://127.0.0.1:8000/openapi/`
swagger可视化版本是`http://127.0.0.1:8000/swagger-ui/`
redoc可视化版本是`http://127.0.0.1:8000/redoc/`




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










### 使用 Docker 环境开发

**注意！**
- **不要滥用 sudo**
- 在本地开发分支中执行以下操作
- 所有对于 `catfood` 下文件的修改都与本地目录同步
- DB 的数据会持久化存储在 `.persistence` 下，删除请使用

    ```
    # sudo rm -rf .persistence #
    ```
#### 启动 Web 服务器

进入代码根目录，运行

```
USER_ID=`id -u` GROUP_ID=`id -g` MINIO_ADDRESS=<ip of a specific NIC on your host> docker-compose up
```

你可以手动查看自己网卡的 IP

```
ip addr
```

或者使用以下脚本匹配第一个可用网卡的 IP

```
alias myip="ip -4 addr | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | grep -v 127.0.0.1 | head -n 1"
```

```
USER_ID=`id -u` GROUP_ID=`id -g` MINIO_ADDRESS=`myip` docker-compose up
```

不要关闭终端，使用代码编辑器修改代码

在 `http://127.0.0.1:8000` 可以访问 Web API，本地文件保存时会自动刷新服务器

#### 在 Docker 中运行指令

找到 web 的容器

```
docker ps
```

打开交互 Shell

```
docker exec -it <container name or id> /bin/bash 
```

#### 关闭 Web 服务器

```
docker-compose down
```

了解其他配置可以阅读 `Dockerfile.web.dev` 和 `docker-compose.yml`
