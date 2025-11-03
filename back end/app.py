from flask import Flask
from flask_cors import CORS
from src.controller.contacts import register_routes

# 创建Flask实例
app = Flask(__name__)
CORS(app, resources=r"/*")
register_routes(app)

# 启动服务
if __name__ == '__main__':
    app.run(debug=True)
