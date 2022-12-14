from datetime import datetime, date
import math
from flask import render_template, request, redirect, url_for, session, jsonify
from hospitalApp import app, dao, login, utils, models, controllers
from hospitalApp.admin import *
from flask_login import login_user, logout_user
import cloudinary.uploader
from hospitalApp.models import Rule

app.add_url_rule('/', 'index', controllers.index)
app.add_url_rule('/CurriculumVitae/<int:user_id>', 'user_details', controllers.user_details)
app.add_url_rule('/login-admin', 'login_admin', controllers.login_admin, methods=['post'])
app.add_url_rule('/api/cart', 'add-cart', controllers.add_to_cart, methods=['post'])
app.add_url_rule('/api/cart/<medicine_id>', 'update-cart', controllers.update_cart,  methods=['put'])
app.add_url_rule('/api/cart/<medicine_id>', 'delete-cart', controllers.delete_cart,  methods=['delete'])
app.add_url_rule('/api/prescription', 'create-prescription', controllers.create_prescription,  methods=['post', 'get'])
app.add_url_rule('/api/receipt', 'save_receipt', controllers.save_receipt, methods=['post'])
app.add_url_rule('/api/medicalCertificate', 'save_PKB', controllers.save_PKB, methods=['post'])
app.add_url_rule('/login', 'login_my_user', controllers.login_my_user, methods=['get', 'post'])
app.add_url_rule('/logout', 'logout_my_user', controllers.logout_my_user)
app.add_url_rule('/api/account', 'register', controllers.register, methods=['post'])
app.add_url_rule('/registerMC', 'register_PKB', controllers.register_PKB)


@app.context_processor
def common_response():
    return {
        'cart': utils.cart_stats(session.get(app.config["CART_KEY"]))
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    app.run(debug=True)

