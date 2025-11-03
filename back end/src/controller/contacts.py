from flask import request, jsonify
import mysql.connector

# 数据库配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mxy137059.', 
    'database': 'contacts_db'
}

# 数据库连接函数
def get_db_connection():
    db = mysql.connector.connect(**db_config)
    return db

# 1. 新增联系人
def add_contact():
    db = get_db_connection()
    cursor = db.cursor()
    data = request.json
    name = data.get('name')
    phone = data.get('phone')

    # 数据校验
    if not name or not phone:
        return jsonify({"code": 400, "message": "姓名和电话不能为空"})

    sql = "INSERT INTO contacts (name, phone) VALUES (%s, %s)"
    values = (name, phone)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"code": 200, "message": "联系人添加成功"})

# 2. 查询所有联系人
def get_contacts():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id, name, phone FROM contacts")
    contacts = cursor.fetchall()
    contact_list = []
    for contact in contacts:
        contact_list.append({
            'id': contact[0],
            'name': contact[1],
            'phone': contact[2]
        })
    cursor.close()
    db.close()
    return jsonify(contact_list)
# 3. 删除联系人
def delete_contact(contact_id):
    db = get_db_connection()
    cursor = db.cursor()
    # 先查询是否存在该联系人
    cursor.execute("SELECT id FROM contacts WHERE id = %s", (contact_id,))
    if not cursor.fetchone():
        cursor.close()
        db.close()
        return jsonify({"code": 404, "message": "联系人不存在"})
    
    # 执行删除
    cursor.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"code": 200, "message": "联系人删除成功！"})

# 4.根据ID查询单个联系人
def get_contact_by_id(contact_id):
    db = get_db_connection()
    cursor = db.cursor()
    # 查询指定ID的联系人
    cursor.execute("SELECT id, name, phone FROM contacts WHERE id = %s", (contact_id,))
    contact = cursor.fetchone()  # 获取单个结果
    cursor.close()
    db.close()

    if contact:
        # 转成前端能使用的字典格式
        return jsonify({
            "code": 200,
            "data": {
                'id': contact[0],
                'name': contact[1],
                'phone': contact[2]
            }
        })
    else:
        return jsonify({"code": 404, "message": "联系人不存在"})

# 5.修改联系人
def update_contact(contact_id):
    db = get_db_connection()
    cursor = db.cursor()
    data = request.json
    name = data.get('name')
    phone = data.get('phone')

    # 数据校验：姓名和电话不能为空
    if not name or not phone:
        cursor.close()
        db.close()
        return jsonify({"code": 400, "message": "姓名和电话不能为空"})

    # 先查询是否存在该联系人
    cursor.execute("SELECT id FROM contacts WHERE id = %s", (contact_id,))
    if not cursor.fetchone():
        cursor.close()
        db.close()
        return jsonify({"code": 404, "message": "联系人不存在，修改失败"})
    
    # 执行更新操作
    sql = "UPDATE contacts SET name = %s, phone = %s WHERE id = %s"
    values = (name, phone, contact_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"code": 200, "message": "联系人修改成功"})

# 路由注册函数
def register_routes(app):
    app.route('/add_contact', methods=['POST'])(add_contact)
    app.route('/get_contacts', methods=['GET'])(get_contacts)
    app.route('/delete_contact/<int:contact_id>', methods=['DELETE'])(delete_contact)
    app.route('/get_contact/<int:contact_id>', methods=['GET'])(get_contact_by_id)  # 新增查询单个接口
    app.route('/update_contact/<int:contact_id>', methods=['PUT'])(update_contact)  # 新增修改接口
