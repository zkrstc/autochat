from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.exceptions import BadRequest, NotFound
app = Flask(__name__)
CORS(app)
# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/autochat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

@app.route('/api/requirements',methods=['GET'])
def get_requirements():
    requirements = Requirement.query.all()
    return jsonify([requirement.to_dict() for requirement in requirements])

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

if __name__ == '__main__':
    app.run(debug=True)
