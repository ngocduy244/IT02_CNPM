from datetime import datetime
import math
from flask import render_template, request, redirect, url_for
from hospitalApp import app, dao, login
from hospitalApp.admin import *
from flask_login import login_user, logout_user
import cloudinary.uploader
from hospitalApp.models import  Rule

@app.route('/')
def index():
    # page = request.args.get('page', 1)
    # counter = dao.count_product()

    # page = request.args.get('page', 1)

    product = dao.load_product(category_id=request.args.get('category_id'),
                               kw=request.args.get("keyword")
                                )
    # page=int(page)

    counter = dao.count_products_id()
    dem = dao.count_user_date()

    return render_template('index.html',
                           product=product,
                           pages = counter,
                           dem = dem)
                           # pages=math.ceil(counter/app.config['PAGE_SIZE'])


@app.route('/product/<int:product_id>')
def details(product_id):
    product = dao.get_product_by_id(product_id)
    return render_template('product_detail.html', product=product)


@app.route('/CurriculumVitae/<int:user_id>')
def user_details(user_id):
    user = dao.get_user_by_id(user_id)
    date = datetime.date(datetime.today())
    string = str(date)
    mc = dao.load_medicalCertificate(string)
    count = dao.count_mc_date(string)
    rule = dao.get_rule_by_id(1)
    return render_template('CurriculumVitae_detail.html', user=user,mc=mc,count=count, rule=rule)

@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/registerMC',methods=['get', 'post'])
def register_PKB():
    err_msg = ""
    if request.method.__eq__("POST"):
        date = request.form.get("date")
        symptom = request.form.get("symptom")
        user_id = request.form.get("user_id")
        count = dao.count_mc_date(date)
        rule = dao.get_rule_by_id(1)

        if(count == rule.amount):
            err_msg = "Số lường PKB đã vượt quá " + str(int(rule.amount)) + " người"
        else:
            dao.registerMC(date, symptom, user_id)
            return redirect('/login')
    return render_template('registerMC.html', err_msg=err_msg)

@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method.__eq__("POST"):
        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        avatar_path = ''

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get("avatar")
                if avatar:
                    res= cloudinary.uploader.upload(avatar)
                    avatar_path=res['secure_url']

                dao.register(name=name, username=username, password=password, email=email, avatar=avatar_path)


                return redirect('/login')
            else:
                err_msg="Mat khau khong dung"
        except Exception as ex:
            err_msg="He thong dang co loi" + str(ex)


    return render_template('register.html', err_msg=err_msg)

@app.route('/login', methods=['get', 'post'])
def login_my_user():
    err_msg=""
    if request.method.__eq__("POST"):
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        if role == "":
            err_msg = "Bạn phải chọn chức vụ"
        elif username == "":
            err_msg = "Bạn phải nhập tên đăng nhập"
        elif password == "":
            err_msg = "Bạn phải nhập mật khẩu"
        else:
            user = dao.auth_user(username,password, role)
            if user:
                login_user(user=user)
                if(current_user.user_role == UserRole.ADMIN):
                    return redirect('/admin')
                return redirect(url_for('index'))
            else:
                err_msg="User name hoac passwork khong chinh xac"

    return render_template('login.html', err_msg=err_msg)


@app.context_processor
def common_response():
    return {
        'category': dao.load_category()
    }

@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect(url_for('login_my_user'))

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)



if __name__ == '__main__':
    app.run(debug=True)

