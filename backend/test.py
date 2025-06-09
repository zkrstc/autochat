from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.exceptions import BadRequest, NotFound

from werkzeug.security import check_password_hash

import os

import openai
#openai.api_key = "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"

app = Flask(__name__)
CORS(app)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/autochat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
# 放在 Flask app 和 db 初始化之后，main 启动之前
with app.app_context():
    db.create_all()

# 定义模型
class Requirement(db.Model):
    __tablename__ = 'requirements'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'version': self.version,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
        }
with app.app_context():
    db.create_all()

# 登录接口
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Login successful', 'user_id': user.id}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


from werkzeug.security import generate_password_hash

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 409

    new_user = User(
        username=username,
        password_hash=generate_password_hash(password)
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Register successful'}), 201


@app.route('/api/requirements',methods=['GET'])
def get_requirements():
    requirements = Requirement.query.all()
    return jsonify([requirement.to_dict() for requirement in requirements])

@app.route('/api/requirements', methods=['POST'])
def create_requirement():
    data = request.get_json()
    required_fields = ['user_id', 'name', 'version', 'content']

    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    new_requirement = Requirement(
        user_id=data['user_id'],
        name=data['name'],
        version=data['version'],
        content=data['content']
    )
    db.session.add(new_requirement)
    db.session.commit()

    return jsonify({'message': 'Requirement created', 'id': new_requirement.id}), 201

@app.route('/api/requirements/<int:id>', methods=['PUT'])
def update_requirement(id):
    try:
        # 获取要求记录
        requirement = Requirement.query.get_or_404(id)
        
        # 获取JSON数据
        data = request.get_json()
        
        if not data:
            raise BadRequest('No input data provided')
            print('3')
        # 验证必要字段
        if 'content' not in data:
            raise BadRequest('Missing required field: content')
            
        # 更新内容
        requirement.content = data['content']
        
        # 提交到数据库
        db.session.commit()
        
        return jsonify({
            'message': 'Requirement updated successfully',
            'id': id,
            'new_content': data['content']
        }), 200
        
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except NotFound:
        return jsonify({'error': 'Requirement not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500



@app.route('/api/requirements/list', methods=['GET'])
def get_requirements_list():
    requirements = Requirement.query.all()
    return jsonify([{'id': r.id, 'name': r.name, 'version': r.version} for r in requirements])

@app.route('/api/modules/generate', methods=['POST'])
def generate_modules():
    data = request.get_json()
    requirement_id = data.get('requirement_id')

    requirement = Requirement.query.get(requirement_id)
    if not requirement:
        return jsonify({'error': 'Requirement not found'}), 404

    prompt = f"""
你是一个资深的软件架构师。请根据以下软件需求描述为我生成3个模块，并给出模块名和相应Python代码：
需求内容如下：
{requirement.content}

请以如下 JSON 格式返回：
[
  {{ "name": "模块名称", "code": "对应代码（多行字符串）" }},
  ...
]
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "你是一个擅长软件模块划分与代码生成的专家。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        text_response = response['choices'][0]['message']['content']

        # 安全地将字符串 JSON 转换为对象
        import json
        modules = json.loads(text_response)
        return jsonify(modules)
    except Exception as e:
        return jsonify({'error': str(e)}), 500







if __name__ == '__main__':
    app.run(debug=True)
