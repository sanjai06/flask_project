from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Admin, Blog
from . import db
from .utils import ai_text, send_email
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        admin = Admin.query.filter_by(email=email).first()
        if admin:
            if check_password_hash(admin.password, password):
                if admin.username == username:
                    login_user(admin, remember=True)
                    send_email(Body="AI Blog ADMIN PANEL Login Success", 
                               Subject="You successfully login into AI Blog ADMIN PANEL")
                    return redirect(url_for('auth.admin'))
                else:
                    flash('username invalide', category='error')
            else:
                flash('password invalide', category='error')
        else:
            flash('email not exist', category='error')
    return render_template("login.html")

@auth.route('/logout',  methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/fun_admin', methods=['GET', 'POST'])
@login_required
def admin():
    admin_user = current_user.username
    admin_email = current_user.email
    blog_all = Blog.query.all()
    return render_template('admin.html', admin_user=admin_user, admin_email=admin_email, blog_all=blog_all)

@auth.route('/detail_blog')
@login_required
def detail_blog():
    div_id = request.args.get('id')
    admin_user = current_user.username
    admin_email = current_user.email
    detail_blog = Blog.query.filter_by(id=div_id).first()
    return render_template('details_blog.html',detail_blog=detail_blog, admin_user=admin_user, admin_email=admin_email)


@auth.route('/signin', methods=['GET', 'POST'])
@login_required
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        new_user = Admin(email=email, password=generate_password_hash(password, method='sha256'), username=username)
        db.session.add(new_user)
        db.session.commit()
        flash('Account Created!', category='success')
        return redirect(url_for('auth.admin'))
    return render_template('login.html')

@auth.route('/create_blog', methods=['GET', 'POST'])
@login_required
def create_blog():
    admin_user = current_user.username
    if request.method == 'POST':
        title_aiblog = request.form.get('title_aiblog')
        print(title_aiblog)
    if request.method == 'POST':
        title = request.form.get('title')
        patagraph = request.form.get('patagraph')
        displayValue = request.form.get('displayValue')
        if displayValue != '':
            blog_db = Blog(title=title, paragraph=patagraph, catagry=displayValue, show_para=True)
            db.session.add(blog_db)
            db.session.commit()
            send_email(
                Body='New blog post is created click agree to post a Blog /n Admin Access Required', 
                Subject='Blog Post created'
                )
    return render_template('manualblog.html', admin_user=admin_user)