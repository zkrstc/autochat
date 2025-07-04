from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.exceptions import BadRequest, NotFound
from flask import jsonify
from werkzeug.security import check_password_hash
from datetime import datetime
import os
import json
from openai import OpenAI
from config import API_CONFIG
from sqlalchemy.exc import SQLAlchemyError
app = Flask(__name__)
CORS(app)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/autochat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

client = OpenAI(
    api_key=API_CONFIG["api_key"],
    base_url=API_CONFIG["base_url"]
)



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

class Architecture(db.Model):
    __tablename__ = 'architectures'
    id = db.Column(db.Integer, primary_key=True)
    requirement_id = db.Column(db.Integer, db.ForeignKey('requirements.id'), nullable=False)
    architecture_json = db.Column(db.Text, nullable=False)
    generated_by = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DatabaseDesign(db.Model):
    __tablename__ = 'database_designs'
    id = db.Column(db.Integer, primary_key=True)
    requirement_id = db.Column(db.Integer, db.ForeignKey('requirements.id'), nullable=False)
    erd_diagram = db.Column(db.Text)
    sql_script = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ModuleCode(db.Model):
    __tablename__ = 'module_codes'
    id = db.Column(db.Integer, primary_key=True)
    architecture_id = db.Column(db.Integer, db.ForeignKey('architectures.id'), nullable=False)
    module_name = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(20), nullable=False)
    code = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DeploymentLog(db.Model):
    __tablename__ = 'deployment_logs'
    id = db.Column(db.Integer, primary_key=True)
    architecture_id = db.Column(db.Integer, db.ForeignKey('architectures.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    log_output = db.Column(db.Text)
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)

class TestCase(db.Model):
    __tablename__ = 'test_cases'
    id = db.Column(db.Integer, primary_key=True)
    requirement_id = db.Column(db.Integer, db.ForeignKey('requirements.id'), nullable=False)
    input_data = db.Column(db.Text, nullable=False)
    expected_output = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class VersionHistory(db.Model):
    __tablename__ = 'version_history'
    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(30), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)
    version = db.Column(db.Integer, nullable=False)
    data_snapshot = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    messages = data.get('messages', [])
    
    try:
        completion = client.chat.completions.create(
            model="deepseek-chat",  # 或 "gpt-4"
            messages=messages
        )
        reply = completion.choices[0].message.content
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'reply': f"后端出错: {str(e)}"}), 500
    

# 登录接口
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    print(username)
    print(password)
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Login successful', 'user_name':user.username }), 200
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




@app.route('/api/architectures/<int:requirement_id>', methods=['GET'])
def get_architecture(requirement_id):
    architecture = Architecture.query.filter_by(requirement_id=requirement_id).first()
    
    if not architecture:
        return jsonify({
            'error': 'Architecture not found',
            'status': 404
        }), 404
    
    import json

    try:
    # 确保返回的是可序列化的数据
        return jsonify({
            'status': 'success',
            'data': {
                'id': architecture.id,
                'requirement_id': architecture.requirement_id,
                'architecture_json': architecture.architecture_json,
                'generated_by': architecture.generated_by,
                'created_at': architecture.created_at.isoformat()
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500





@app.route('/api/architectures/generate', methods=['POST'])
def generate_architecture():
    # 获取请求数据
    data = request.get_json()
    requirement_id = data.get('requirement_id')
    user_name = data.get('user_name')  # 当前用户ID
    
    if not requirement_id or not user_name:
        return jsonify({'error': 'Missing requirement_id or user_id', 'status': 400}), 400
    
    # 获取需求文档内容
    requirement = Requirement.query.get(requirement_id)
    
    if not requirement:
        return jsonify({'error': 'Requirement not found', 'status': 404}), 404
    
    # 构建AI提示
    prompt = f"""
    你是一名资深软件架构师。请根据以下需求文档内容，设计一个合理的软件系统架构。

    ⚠️ 请严格遵循以下要求输出：
    1. **只输出 JSON 数据**，不要包含任何其他描述性语言；
    2. JSON 的结构必须完全符合下面给出的格式模板；
    3. 不允许在 JSON 外加任何解释、前缀或后缀文本。

    需求文档内容：
    {requirement.content}

    请按照以下 JSON 格式返回结果：

    {{
        "architectureDiagram": {{
            "description": "架构描述",
            "diagram": "ASCII架构图"(给出架构图，不要只写ASCII架构图几个字)
        }},
        "technologyStack": {{
            "frontend": "前端技术栈",
            "backend": "后端技术栈",
            "database": "数据库技术栈"
        }},
        "modules": [
            "模块1",
            "模块2",
            "..."
        ]
    }}
    """

    
    try:

        
        response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个资深的软件架构师，擅长设计清晰、可扩展的系统架构。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
        print(response)
            
        # 解析AI响应
        ai_response = response.choices[0].message.content
        
        print(ai_response)
        # 查询相同 requirement_id 的记录
        existing_architecture = Architecture.query.filter_by(requirement_id=requirement_id).first()

        if existing_architecture:
            # 只清空 architecture_json 字段
            existing_architecture.architecture_json = None  # 或者设为空字符串 ""
            db.session.commit()
        # 创建架构记录
        new_architecture = Architecture(
            requirement_id=requirement_id,
            architecture_json=ai_response,
            generated_by=user_name,
            created_at=datetime.utcnow()
        )
        
        db.session.add(new_architecture)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'data': {
                'id': new_architecture.id,
                'requirement_id': new_architecture.requirement_id,
                'architecture_json': new_architecture.architecture_json,
                'generated_by': new_architecture.generated_by,
                'created_at': new_architecture.created_at.isoformat()
            }
        })
        
    except Exception as e:
        db.session.rollback()
        # 打印详细的堆栈信息用于日志
        print("捕获到异常：", str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500



@app.route('/api/module_code', methods=['GET'])
def get_module_code():
    architecture_id = request.args.get('architecture_id')
    module_name = request.args.get('module_name')
    print(architecture_id)
    print(module_name)
    if not architecture_id or not module_name:
        return jsonify({'error': 'Missing parameters'}), 400
    
    # 查询所有匹配的记录而不仅仅是第一条
    module_codes = ModuleCode.query.filter_by(
        architecture_id=architecture_id,
        module_name=module_name
    ).all()
    
    if not module_codes:
        return jsonify({'error': 'Module code not found'}), 404
    
    # 将结果组合成一个列表返回
    result = [{
        'code': module.code,
        'language': module.language
    } for module in module_codes]
    
    return jsonify(result)

@app.route('/api/modules/generate', methods=['POST'])
def generate_modules():
    data = request.get_json()
    requirement_id = data.get('requirement_id')
    architecture_id= data.get('architecture_id')
    module_name = data.get('module_name')  # 用户选的模块名
    print(requirement_id)
    print(architecture_id)
    print(module_name)
    if not requirement_id or not module_name:
        return jsonify({'error': 'Missing required parameters'}), 400

    requirement = Requirement.query.get(requirement_id)
    architecture=Architecture.query.get(architecture_id)
    if not requirement:
        return jsonify({'error': 'Requirement not found'}), 404

    prompt = f"""
你是一个资深的软件架构师。请根据以下软件需求描述为我生成模块，并给出模块名和相应的代码。

**要求如下：**
- 每个模块代码前添加一行注释，说明所使用的编程语言，例如：“# Language: Python”
- 请按如下 JSON 格式返回：
⚠️ 请严格遵循以下要求输出：
    1. **只输出 JSON 数据**，不要包含任何其他描述性语言；
    2. JSON 的结构必须完全符合下面给出的格式模板；
    3. 不允许在 JSON 外加任何解释、前缀或后缀文本。
    4. 不要有任何多于的字符、空格、换行符。
    5. 模块名不能包含特殊字符。
    6. 只需要生成当前选择的模块的代码
当前只需生成关于名称是{module_name}的前端和后端代码。
不需要其他的任何代码,最好根据架构来设计前后端的代码,
代码必须都是一个名称，不需要什么加上什么前后缀（不需要User Module Frontend之类的，
直接使用User Module就好了）,你可以将该代码分成至多3个json数据
**JSON 模板：**
[
  {{
    "name": "模块名称",
    "code": "# Language: Python\\n代码内容..."
  }},
  ...
]

架构内容如下：
{architecture.architecture_json}
"""
    #如果需要关联各个代码可以在使用module_codes的查询记录
    import re

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个擅长软件模块划分与代码生成的专家。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2048
        )
        print(response)
        text_response = response.choices[0].message.content
        # text_response = re.sub(r'```json.*?```', '', text_response, flags=re.DOTALL)
        # import json
        modules = json.loads(text_response)
        
        for module in modules:
            code = module.get('code', '')
            
            # 处理转义字符
            code = code.replace('\\n', '\n')
            
            # 从注释中提取语言
            match = re.search(r'#\s*Language:\s*([^\n\\]+)', code)
            language = match.group(1).strip() if match else 'Unknown'

            code_entry = ModuleCode(
                architecture_id=architecture_id,
                module_name=module.get('name'),
                language=language,
                code=code,
                created_at=datetime.utcnow()
            )
            db.session.add(code_entry)

        db.session.commit()
        return jsonify({'status': 'success', 'modules': modules})
        
    except SQLAlchemyError as e:
        db.session.rollback()  # 发生错误时回滚事务
        print(f"数据库操作失败: {str(e)}")
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# @app.route('/api/modules/generate', methods=['POST'])
# def generate_modules():
#     data = request.get_json()
#     requirement_id = data.get('requirement_id')

#     requirement = Requirement.query.get(requirement_id)
#     if not requirement:
#         return jsonify({'error': 'Requirement not found'}), 404

#     prompt = f"""
# 你是一个资深的软件架构师。请根据以下软件需求描述为我生成3个模块，并给出模块名和相应Python代码：
# 需求内容如下：
# {requirement.content}

# 请以如下 JSON 格式返回：
# [
#   {{ "name": "模块名称", "code": "对应代码（多行字符串）" }},
#   ...
# ]
# """

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "你是一个擅长软件模块划分与代码生成的专家。"},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.7
#         )
#         text_response = response['choices'][0]['message']['content']

#         # 安全地将字符串 JSON 转换为对象
#         import json
#         modules = json.loads(text_response)
#         return jsonify(modules)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# 获取指定需求的数据库设计
@app.route('/api/database_designs', methods=['GET'])
def get_database_designs():
    requirement_id = request.args.get('requirement_id')
    if not requirement_id:
        return jsonify({'error': 'Missing requirement_id parameter'}), 400
    
    designs = DatabaseDesign.query.filter_by(requirement_id=requirement_id).order_by(DatabaseDesign.created_at.desc()).all()
    
    if not designs:
        return jsonify({'error': 'No database designs found for this requirement'}), 404
    
    result = [{
        'id': design.id,
        'requirement_id': design.requirement_id,
        'erd_diagram': design.erd_diagram,
        'sql_script': design.sql_script,
        'created_at': design.created_at.isoformat() if design.created_at else None
    } for design in designs]
    
    return jsonify(result)



@app.route('/api/database/generate', methods=['POST'])
def generate_database():
    data = request.get_json()
    requirement_id = data.get('requirement_id')

    if not requirement_id:
        return jsonify({'error': 'requirement_id is required'}), 400

    requirement = Requirement.query.get(requirement_id)
    print(requirement)
    if not requirement:
        return jsonify({'error': 'Requirement not found'}), 404

    prompt = f"""
你是一个专业的数据库架构师。请根据以下软件需求描述为我设计数据库，包括：

1. ER图（使用纯文本表示，格式如下示例）
2. SQL建表语句

⚠️ 请严格遵循以下要求输出：
    1. **只输出 JSON 数据**，不要包含任何其他描述性语言；
    2. JSON 的结构必须完全符合下面给出的格式模板；
    3. 不允许在 JSON 外加任何解释、前缀或后缀文本。
    4. 不要有任何多于的字符、空格、换行符。
**ER图格式示例：**
+-------------+       +-------------+       +-------------+
|    User     |       |  Product    |       |    Order    |
+-------------+       +-------------+       +-------------+
| id (PK)     |       | id (PK)     |       | id (PK)     |
| name        |       | shop_id (FK)|       | user_id (FK)|
| phone       |       | name        |       | shop_id (FK)|
| password    |       | price       |       | status      |
+-------------+       +-------------+       | total       |
      |                     |              | created_at  |
      |                     |              +-------------+
      |                     |                    |
      |                     +----------+         |
      |                                |         |
      v                                v         v
+--------------------------+-----------------------------+
|         OrderItem        |         Shop               |
+--------------------------+-----------------------------+
| order_id (PK,FK)         | id (PK)                    |
| product_id (PK,FK)       | name                       |
| quantity                 | address                    |
| price_at_order           +-----------------------------+
+--------------------------+

**SQL语句格式要求：**
- 使用标准SQL语法
- 包含主键、外键约束
- 包含适当的索引
- 包含必要的注释

请以如下JSON格式返回：
[
    {{
    "erd_diagram": "纯文本ER图",
    "sql_script": "完整的SQL建表语句"
    }}
]


需求内容如下：
{requirement.content}

"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个专业的数据库架构师，擅长设计关系型数据库。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2048
        )
        
        result = response.choices[0].message.content
        print(result)
        import re
        result = re.sub(r"^```json|```$", "", result).strip()
        # 解析 JSON 字符串
        db_design = json.loads(result)
        print(db_design)
        #保存到数据库
        design = DatabaseDesign(
            requirement_id=requirement_id,
            erd_diagram=db_design.get('erd_diagram'),
            sql_script=db_design.get('sql_script'),
            created_at=datetime.utcnow()
        )
        
        db.session.add(design)
        db.session.commit()
        
        return jsonify({
            'id': design.id,
            'erd_diagram': design.erd_diagram,
            'sql_script': design.sql_script,
            'created_at': design.created_at.isoformat()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



@app.route('/api/test_cases', methods=['GET'])
def get_test_cases():
    requirement_id = request.args.get('requirement_id', type=int)
    if requirement_id is None:
        return jsonify({'error': 'requirement_id is required'}), 400

    cases = TestCase.query.filter_by(requirement_id=requirement_id).all()
    print(cases)
    return jsonify({
    'data': [{
        'id': case.id,
        'input_data': case.input_data,
        'expected_output': case.expected_output,
        'type': case.type
    } for case in cases]
})


@app.route('/api/test_cases/<int:id>', methods=['PUT'])
def update_test_case(id):
    data = request.json
    case = TestCase.query.get_or_404(id)
    case.input_data = data.get('input_data', case.input_data)
    case.expected_output = data.get('expected_output', case.expected_output)
    db.session.commit()
    return jsonify({'message': '更新成功'})

@app.route('/api/test_cases/<int:id>', methods=['DELETE'])
def delete_test_case(id):
    case = TestCase.query.get_or_404(id)
    db.session.delete(case)
    db.session.commit()
    return jsonify({'message': '删除成功'})


@app.route('/api/test-cases/generate', methods=['POST'])
def generate_test_cases():
    data = request.get_json()
    requirement_id = data.get('requirement_id')
    architecture_id = data.get('architecture_id')

    if not requirement_id or not architecture_id:
        return jsonify({'error': 'requirement_id and architecture_id are required'}), 400

    requirement = Requirement.query.get(requirement_id)
    architecture = Architecture.query.get(architecture_id)
    
    if not requirement:
        return jsonify({'error': 'Requirement not found'}), 404
    if not architecture:
        return jsonify({'error': 'Architecture not found'}), 404
    # 解析架构JSON获取模块列表
    architecture_data = json.loads(architecture.architecture_json)
    modules = architecture_data.get('modules', [])
    print(modules)
    print(architecture_data)
    prompt = f"""
            你是一个专业的测试工程师。请根据以下信息生成全面的测试用例：

            1. 系统架构模块：
            {', '.join(modules) if modules else '无明确模块划分'}

            2. 技术栈：
            前端: {architecture_data.get('technologyStack', {}).get('frontend', '未知')}
            后端: {architecture_data.get('technologyStack', {}).get('backend', '未知')}
            数据库: {architecture_data.get('technologyStack', {}).get('database', '未知')}

            3. 架构内容：
            {architecture.architecture_json}

            要求：
            1. 为每个主要模块生成测试用例
            2. 包含正常情况和异常情况的测试用例
            3. 每个测试用例包含：
            - 测试类型（单元测试/集成测试/系统测试）
            - 具体输入数据
            - 预期输出结果
            4. 使用如下JSON格式返回：

            ⚠️ 请严格遵循以下要求输出：
            1. **只输出 JSON 数据**，不要包含任何其他描述性语言；
            2. JSON 的结构必须完全符合下面给出的格式模板；
            3. 不允许在 JSON 外加任何解释、前缀或后缀文本。
            4. 不要有任何多于的字符、空格、换行符。
            5.测试用例不超过8个
            [
            {{
                "type": "User Module",
                "input_data": "注册用户：用户名 'alice'，手机号 '1234567890'，密码 '123456'",
                "expected_output": "注册成功，返回用户ID"
            }},
            ...
            ]
        """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个专业的测试工程师，擅长编写各种类型的测试用例。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2048
        )
        result = response.choices[0].message.content
        print(result)

        import re
        # result = re.sub(r"^```json|```$", "", result).strip()
        # 解析 JSON 字符串
        result = re.sub(r'```json.*?```', '', result, flags=re.DOTALL)
        test_cases = json.loads(result)
        saved_cases = []

        for case in test_cases:
            new_case = TestCase(
                requirement_id=requirement_id,
                input_data=case.get('input_data', ''),
                expected_output=case.get('expected_output', ''),
                type=case.get('type', '单元测试'),
                created_at=datetime.utcnow()
            )
            db.session.add(new_case)
            db.session.flush()  # 获取生成的ID
            saved_cases.append({
                'id': new_case.id,
                'type': new_case.type,
                'input_data': new_case.input_data,
                'expected_output': new_case.expected_output,
                'created_at': new_case.created_at.isoformat()
            })

        db.session.commit()

        return jsonify(saved_cases)

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    


if __name__ == '__main__':
    app.run(debug=True)
