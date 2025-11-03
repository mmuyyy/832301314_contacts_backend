\# 极简通讯录 - 后端项目

\## 项目介绍

本项目是第一次作业的后端部分，提供通讯录核心接口，实现数据持久化存储，支持前端的所有交互请求。



\## 技术栈

\- Python 3.x（开发语言）

\- Flask（Web框架）

\- MySQL（数据库，数据持久化）



\## 目录结构

src/

├── app.py           # 应用入口文件（启动服务）

└── controller/

└── contacts.py  # 核心逻辑（接口实现、数据库操作）

\## 依赖安装

1\. 确保电脑已安装 Python 3.x；

2\. 打开终端，执行以下命令安装依赖：

```bash

pip install flask mysql-connector-python python-dotenv

本地运行步骤



1\. 配置 MySQL 数据库：



◦ 新建数据库 contacts\_db；



◦ 新建表 contacts，执行 SQL 语句：

CREATE TABLE contacts (

&nbsp;   id INT AUTO\_INCREMENT PRIMARY KEY,

&nbsp;   name VARCHAR(255) NOT NULL,

&nbsp;   phone VARCHAR(20) NOT NULL

);

◦ 修改 contacts.py 中的 db\_config（确保数据库密码与你的本地 MySQL 密码一致）；



2\. 打开终端，进入项目的 src 目录（命令：cd 你的项目路径/src）；



3\. 启动后端服务：执行命令 python app.py；



4\. 服务启动后，接口地址为 http://127.0.0.1:5000。



接口文档

接口功能 请求方式 请求路径 请求体参数 返回格式 

新增联系人 POST /add\_contact name（姓名）、phone（电话） {"code": 200, "message": "联系人添加成功"} 

查询所有联系人 GET /get\_contacts 无 {"code": 200, "data": \[联系人列表], "message": "查询成功"} 

查询单个联系人 GET /get\_contact/{contact\_id} 无（路径参数传ID） {"code": 200, "data": 联系人信息} 

修改联系人 PUT /update\_contact/{contact\_id} name、phone {"code": 200, "message": "联系人修改成功"} 

删除联系人 DELETE /delete\_contact/{contact\_id} 无（路径参数传ID） {"code": 200, "message": "联系人删除成功！"} 



注意事项



1\. 启动服务前，需确保本地 MySQL 已启动，且数据库 contacts\_db 和表 contacts 已创建；



2\. 若修改数据库配置，需同步更新 contacts.py 中的 db\_config；



3\. 接口返回格式统一为 JSON，包含状态码 code、提示信息 message，数据放在 data 字段（按需返回）。

