from flask import Blueprint, jsonify, request
from .models import User
from . import db

bp = Blueprint('api', __name__)

@bp.route('/api/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', 10, type=int)
    pagination = User.query.paginate(page=page, per_page=per_page)
    users = [user.to_dict() for user in pagination.items]
    return jsonify({
        'code': 0,
        'msg': 'success',
        'count': pagination.total,
        'data': users
    })

@bp.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'code': 0, 'msg': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': '删除失败'}), 500
