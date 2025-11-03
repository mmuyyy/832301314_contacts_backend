后端代码风格规范



参考标准



• Python：遵循 PEP 8 规范



命名规则



1\. 文件名：小写字母+下划线（如 app.py、contacts.py）



2\. 目录名：小写字母+下划线（如 src/controller）



3\. 函数名：小写字母+下划线（如 add\_contact、get\_contacts、delete\_contact、update\_contact、get\_db\_connection）



4\. 变量名：小写字母+下划线（如 db\_config、contact\_id、name、phone、db、cursor、data）



5\. 常量名：大写字母+下划线（本项目暂未使用）



注释要求



1\. 接口函数必须添加文档字符串（docstring），明确说明接口功能、请求方式、参数、返回格式



2\. 数据库操作相关代码需添加注释，说明 SQL 执行目的



3\. 异常处理逻辑需添加注释，说明处理的异常场景



4\. 关键配置（如数据库连接信息、接口路径）需添加注释说明



5\. 复杂逻辑块（如数据校验、事务处理）需添加步骤注释



格式规范



1\. 代码缩进使用 4 个空格（禁止使用制表符）



2\. 函数定义之间保留 2 个空行，函数内部逻辑块之间保留 1 个空行



3\. 一行代码长度不超过 80 字符，超长时合理换行（如 SQL 语句、长参数列表）



4\. SQL 语句关键字统一大写（如 SELECT、INSERT、UPDATE、DELETE、WHERE、SET）



5\. 数据库连接、游标等资源操作，必须用 try...finally 确保资源关闭，避免内存泄漏



6\. 接口返回格式统一为 JSON 结构，包含状态码（code）、提示信息（message），数据按需放入 data 字段



7\. 导入模块时，按“标准库→第三方库→自定义模块”的顺序排列，不同类别之间保留 1 个空行



代码示例



数据库连接函数示例

def get\_db\_connection():

&nbsp;   """

&nbsp;   建立并返回 MySQL 数据库连接

&nbsp;   配置说明：连接本地 MySQL 数据库，数据库名为 contacts\_db

&nbsp;   依赖配置：host=localhost, user=root, password=mxy137059., database=contacts\_db

&nbsp;   返回值：mysql.connector 连接对象，供后续数据库操作使用

&nbsp;   """

&nbsp;   db = mysql.connector.connect(\*\*db\_config)

&nbsp;   return db

新增联系人接口示例

def add\_contact():

&nbsp;   """

&nbsp;   新增联系人接口

&nbsp;   请求方式：POST

&nbsp;   请求路径：/add\_contact

&nbsp;   请求体参数：

&nbsp;       - name: 联系人姓名（字符串类型，必填，非空）

&nbsp;       - phone: 联系人电话（字符串类型，必填，非空）

&nbsp;   返回格式：

&nbsp;       - 成功：{"code": 200, "message": "联系人添加成功"}

&nbsp;       - 失败：{"code": 400, "message": "姓名和电话不能为空"}

&nbsp;       - 服务器错误：{"code": 500, "message": "添加失败：错误详情"}

&nbsp;   """

&nbsp;   db = None

&nbsp;   cursor = None

&nbsp;   try:

&nbsp;       # 获取前端传递的请求体数据

&nbsp;       data = request.json

&nbsp;       name = data.get('name')

&nbsp;       phone = data.get('phone')



&nbsp;       # 数据校验：姓名和电话为必填项

&nbsp;       if not name or not phone:

&nbsp;           return jsonify({"code": 400, "message": "姓名和电话不能为空"})



&nbsp;       # 建立数据库连接，执行新增操作

&nbsp;       db = get\_db\_connection()

&nbsp;       cursor = db.cursor()

&nbsp;       sql = "INSERT INTO contacts (name, phone) VALUES (%s, %s)"

&nbsp;       values = (name, phone)

&nbsp;       cursor.execute(sql, values)

&nbsp;       db.commit()  # 提交事务，确保数据写入数据库



&nbsp;       return jsonify({"code": 200, "message": "联系人添加成功"})

&nbsp;   except Exception as e:

&nbsp;       # 异常时回滚事务，避免数据不一致

&nbsp;       if db:

&nbsp;           db.rollback()

&nbsp;       return jsonify({"code": 500, "message": f"添加失败：{str(e)}"})

&nbsp;   finally:

&nbsp;       # 确保游标和数据库连接关闭，释放资源

&nbsp;       if cursor:

&nbsp;           cursor.close()

&nbsp;       if db:

&nbsp;           db.close()

查询所有联系人接口示例

def get\_contacts():

&nbsp;   """

&nbsp;   查询所有联系人接口

&nbsp;   请求方式：GET

&nbsp;   请求路径：/get\_contacts

&nbsp;   请求参数：无

&nbsp;   返回格式：

&nbsp;       - 成功：{"code": 200, "data": \[{"id": 1, "name": "xxx", "phone": "xxx"}, ...], "message": "查询成功"}

&nbsp;       - 无数据：{"code": 200, "data": \[], "message": "查询成功"}

&nbsp;       - 服务器错误：{"code": 500, "message": "查询失败：错误详情"}

&nbsp;   """

&nbsp;   db = None

&nbsp;   cursor = None

&nbsp;   try:

&nbsp;       db = get\_db\_connection()

&nbsp;       cursor = db.cursor(dictionary=True)  # 让返回结果以字典形式呈现，便于前端处理

&nbsp;       sql = "SELECT id, name, phone FROM contacts"

&nbsp;       cursor.execute(sql)

&nbsp;       contacts = cursor.fetchall()  # 获取所有查询结果



&nbsp;       return jsonify({

&nbsp;           "code": 200,

&nbsp;           "data": contacts,

&nbsp;           "message": "查询成功"

&nbsp;       })

&nbsp;   except Exception as e:

&nbsp;       return jsonify({"code": 500, "message": f"查询失败：{str(e)}"})

&nbsp;   finally:

&nbsp;       if cursor:

&nbsp;           cursor.close()

&nbsp;       if db:

&nbsp;           db.close()

修改联系人接口示例

def update\_contact(contact\_id):

&nbsp;   """

&nbsp;   修改联系人接口

&nbsp;   请求方式：PUT

&nbsp;   请求路径：/update\_contact/{contact\_id}

&nbsp;   请求参数：

&nbsp;       - 路径参数：contact\_id（整数类型，联系人唯一ID）

&nbsp;       - 请求体参数：name（新姓名）、phone（新电话），均为必填

&nbsp;   返回格式：

&nbsp;       - 成功：{"code": 200, "message": "联系人修改成功"}

&nbsp;       - 失败：{"code": 400, "message": "姓名和电话不能为空"} 或 {"code": 404, "message": "联系人不存在，修改失败"}

&nbsp;       - 服务器错误：{"code": 500, "message": "修改失败：错误详情"}

&nbsp;   """

&nbsp;   db = None

&nbsp;   cursor = None

&nbsp;   try:

&nbsp;       db = get\_db\_connection()

&nbsp;       cursor = db.cursor()

&nbsp;       data = request.json

&nbsp;       name = data.get('name')

&nbsp;       phone = data.get('phone')



&nbsp;       # 数据校验：姓名和电话不能为空

&nbsp;       if not name or not phone:

&nbsp;           return jsonify({"code": 400, "message": "姓名和电话不能为空"})



&nbsp;       # 先查询联系人是否存在，避免修改不存在的数据

&nbsp;       cursor.execute("SELECT id FROM contacts WHERE id = %s", (contact\_id,))

&nbsp;       if not cursor.fetchone():

&nbsp;           return jsonify({"code": 404, "message": "联系人不存在，修改失败"})



&nbsp;       # 执行更新操作

&nbsp;       sql = "UPDATE contacts SET name = %s, phone = %s WHERE id = %s"

&nbsp;       values = (name, phone, contact\_id)

&nbsp;       cursor.execute(sql, values)

&nbsp;       db.commit()



&nbsp;       return jsonify({"code": 200, "message": "联系人修改成功"})

&nbsp;   except Exception as e:

&nbsp;       if db:

&nbsp;           db.rollback()

&nbsp;       return jsonify({"code": 500, "message": f"修改失败：{str(e)}"})

&nbsp;   finally:

&nbsp;       if cursor:

&nbsp;           cursor.close()

&nbsp;       if db:

&nbsp;           db.close()

删除联系人接口示例

def delete\_contact(contact\_id):

&nbsp;   """

&nbsp;   删除联系人接口

&nbsp;   请求方式：DELETE

&nbsp;   请求路径：/delete\_contact/{contact\_id}

&nbsp;   请求参数：路径参数 contact\_id（整数类型，联系人唯一ID）

&nbsp;   返回格式：

&nbsp;       - 成功：{"code": 200, "message": "联系人删除成功！"}

&nbsp;       - 失败：{"code": 404, "message": "联系人不存在"}

&nbsp;       - 服务器错误：{"code": 500, "message": "删除失败：错误详情"}

&nbsp;   """

&nbsp;   db = None

&nbsp;   cursor = None

&nbsp;   try:

&nbsp;       db = get\_db\_connection()

&nbsp;       cursor = db.cursor()



&nbsp;       # 验证联系人是否存在

&nbsp;       cursor.execute("SELECT id FROM contacts WHERE id = %s", (contact\_id,))

&nbsp;       if not cursor.fetchone():

&nbsp;           return jsonify({"code": 404, "message": "联系人不存在"})



&nbsp;       # 执行删除操作

&nbsp;       sql = "DELETE FROM contacts WHERE id = %s"

&nbsp;       cursor.execute(sql, (contact\_id,))

&nbsp;       db.commit()



&nbsp;       return jsonify({"code": 200, "message": "联系人删除成功！"})

&nbsp;   except Exception as e:

&nbsp;       if db:

&nbsp;           db.rollback()

&nbsp;       return jsonify({"code": 500, "message": f"删除失败：{str(e)}"})

&nbsp;   finally:

&nbsp;       if cursor:

&nbsp;           cursor.close()

&nbsp;       if db:

&nbsp;           db.close()

