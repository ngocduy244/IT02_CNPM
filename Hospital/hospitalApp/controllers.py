from datetime import datetime, date
import math
from flask import render_template, request, redirect, url_for, session, jsonify
from hospitalApp import app, dao, login, utils, models, controllers
from hospitalApp.admin import *
from flask_login import login_user, logout_user
import cloudinary.uploader
from hospitalApp.models import Rule



def index():
    return render_template('index.html')


def user_details(user_id):
    user = dao.get_user_by_id(user_id)
    return render_template('CurriculumVitae_detail.html', user=user)


def login_admin():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    user = dao.auth_user(username=username, password=password, role=role)
    if user:
        login_user(user=user)

    return redirect('/admin')


def register_PKB():
    return render_template('registerMC.html')



def add_to_cart():
    data = request.json
    print(data)


    key = app.config["CART_KEY"]
    cart = session[key] if key in session else {}


    id = str(data['id'])
    name = data['name']
    kind = data['kind']
    unit = data['unit']
    price = data['price']


    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "kind":  kind,
            "unit": unit,
            "price": price,
            "quantity": 1
        }

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


def update_cart(medicine_id):
    key = app.config["CART_KEY"]

    cart = session.get(key)
    if cart and medicine_id in cart:
        cart[medicine_id]['quantity'] = int(request.json['quantity'])

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


def delete_cart(medicine_id):
    key = app.config["CART_KEY"]

    cart = session.get(key)
    if cart and medicine_id in cart:
        del cart[medicine_id]

    session[key] = cart

    return jsonify(utils.cart_stats(cart))

def create_prescription():
    disease = request.json["disease"]
    symptom = request.json["symptom"]
    user_id = int(request.json["userID"])
    date_today = date.today()

    key = app.config["CART_KEY"]
    cart = session.get(key)

    if dao.check_prescription_by_id_date(userID=user_id, created_date=date_today):
        del session[key]
        return jsonify({'status': 204})
    else:
        try:
            dao.add_prescription(cart=cart, disease_name=disease, user_id=user_id, symptom=symptom)
        except:
            return jsonify({'status': 500})
        else:
            del session[key]
            return jsonify({'status': 200})







def save_receipt():
    err_msg = ""
    prescription_id = int(request.json['prescriptionId'])
    user_id = int(request.json['userID'])
    total = int(request.json['totalPrice'])

    if dao.check_receipt(prescription_id=prescription_id):
       return  jsonify({'status': 204})

    else:
        try:
            if dao.load_medical_record_by_user_id(user_id):
                dao.create_MedicalRecord_have(user_id=user_id, prescription_id=prescription_id, total=total)
            else:
                dao.create_MedicalRecord(user_id=user_id, prescription_id=prescription_id, total=total)
        except:
            return jsonify({'status': 500})
        else:
            return jsonify({'status': 200})


def save_PKB():
    examines_date = request.json["date"]
    user_id = int(request.json["userID"])
    count = dao.count_mc_date(examines_date)
    rule = dao.get_rule_by_id(1)
    amount = int(rule.amount)

    if (count == rule.amount):
        return jsonify({
            'status': 206,
             'amount': amount
        })

    else:
        if dao.load_medicalCertificate_By_date_id(date=examines_date, user_id=int(user_id)):
            return jsonify({'status': 204})
        else:
            try:
                dao.registerMC(examines_date=examines_date, user_id=user_id)
            except:
                return jsonify({'status': 500})
            else:
                return jsonify({'status': 200})


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
                if(current_user.user_role == UserRole.ADMIN or current_user.user_role == UserRole.NURSE or current_user.user_role == UserRole.EMPLOYEE or current_user.user_role == UserRole.DOCTOR):
                    return redirect('/admin')
                return redirect(url_for('index'))
            else:
                err_msg="User name hoac passwork khong chinh xac"

    return render_template('login.html', err_msg=err_msg)


def logout_my_user():
    logout_user()
    return redirect(url_for('login_my_user'))


def register():
    name = request.json["name"]
    username = request.json["user_name"]
    password = request.json["password"]
    confirm = request.json["confirm"]
    birthday = request.json['birthday']
    address = request.json['address']
    phone = request.json['phone']
    gender = request.json['gender']
    identity_card = request.json['identity_card']
    avatar_path = ''

    try:
        if password.strip().__eq__(confirm.strip()):
            avatar = request.json["avatar"]
            if avatar:
                res= cloudinary.uploader.upload(avatar)
                avatar_path=res['secure_url']


            dao.register(name=name, username=username, password=password, avatar=avatar_path, phone=phone,
                                birthday=birthday, address=address, gender=gender, identity_card=identity_card)


    except:
        return jsonify({'status': 500})
    else:
        return jsonify({'status': 200})




