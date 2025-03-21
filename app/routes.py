from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from . import db
from .forms import RegistrationForm
from pypinyin import pinyin, Style
import re
from . import auth
import string
import random
from flask import current_app

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return redirect(url_for('routes.register'))

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(random.choice(chars) for _ in range(length))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # 获取验证码文本和哈希值
        c_text = request.form.get('captcha_text')
        c_hash = request.form.get('captcha_id')
        
        # 将用户输入的验证码转换为大写（确保与生成时一致）
        c_text = c_text.upper()
        
        # 验证码验证
        if not current_app.captcha.verify(c_text, c_hash):
            flash('验证码错误，请重试', 'error')
            return redirect(url_for('routes.register'))
        
        # 获取原始用户名
        raw_username = form.username.data
        
        # 将中文转换为拼音
        if re.search('[\u4e00-\u9fff]', raw_username):  # 检查是否包含中文
            username = ''.join([item[0] for item in pinyin(raw_username, style=Style.NORMAL)])
        else:
            username = raw_username.lower()  # 非中文用户名转换为小写
            
        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('用户名已存在，请选择其他用户名。', 'error')
            print(f'用户名 {username} 重复注册')
            return redirect(url_for('routes.register'))
            
        # 检查邮箱是否已存在
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('该邮箱已被注册，请使用其他邮箱。', 'error')
            print(f'邮箱 {form.email.data} 重复注册')
            return redirect(url_for('routes.register'))
            
        # 生成随机密码
        initial_password = generate_password()
        
        # 创建新用户
        new_user = User(
            username=username,
            email=form.email.data,
            status='pending',
            initial_password=initial_password  # 假设 User 模型中有这个字段
        )
        
        db.session.add(new_user)
        db.session.commit()
        flash('注册成功！', 'success')
        return redirect(url_for('routes.index'))
    

    # 生成新的验证码，并确保其大小写与验证逻辑一致
    captcha_dict = current_app.captcha.create()
    captcha_dict['text'] = captcha_dict['text'].upper()  # 强制为大写
    return render_template('user_register.html', form=form, captcha=captcha_dict)

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/admin')
@auth.login_required
def admin_dashboard():
    pending_users = User.query.filter_by(approved=False).all()
    approved_users = User.query.filter_by(approved=True).all()
    print(f"待审批用户数量：{len(pending_users)}")  # 调试信息
    print(f"已审批用户数量：{len(approved_users)}")  # 调试信息
    return render_template('admin_dashboard.html', 
                         pending_users=pending_users,
                         approved_users=approved_users)

@bp.route('/approve/<int:user_id>')
def approve_user(user_id):
    user = User.query.get_or_404(user_id)
    user.approved = True
    db.session.commit()
    flash('用户已批准', 'success')
    return redirect(url_for('routes.admin_dashboard'))

@bp.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('用户已删除', 'success')
    return redirect(url_for('routes.admin_dashboard'))

@bp.route('/generate_command/<int:user_id>')
def generate_command(user_id):
    user = User.query.get_or_404(user_id)
    command = (f"sudo useradd -m -s /bin/bash {user.username} && "
               f"echo '{user.username}:{user.initial_password}' | sudo chpasswd")
    return command