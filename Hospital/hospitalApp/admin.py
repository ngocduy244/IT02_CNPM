from hospitalApp import admin, db, app, dao
from hospitalApp.models import  User, UserRole, Medicine, Rule, Kind, Unit
from flask_admin import Admin, BaseView, expose , AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, render_template, request, jsonify
from flask_login import logout_user, current_user
from datetime import datetime, date


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


# class ProductView(AuthenticatedModelView):
#     column_searchable_list = ['name', 'description']
#     column_filters = ['name', 'price']
#     can_view_details = True
#     column_exclude_list = ['image', 'description']
#     can_export = True
#     column_export_list = ['id', 'name', 'description', 'price']
#     column_labels = {
#         'name': 'Tên sản phẩm',
#         'description': 'Mô tả',
#         'price': 'Gía'
#     }
#     page_size = 5


class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        stats = dao.stats_revenue_month(from_month=request.args.get('from_month'), to_month=request.args.get('to_month'))
        return self.render('admin/stats.html', stats=stats)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class StatsMedicineView(AuthenticatedView):
    @expose('/')
    def index(self):
        stats = dao.statistic_medicine_using_frequency_month(from_month=(request.args.get('from_month')), to_month=(request.args.get('to_month')), keyword=request.args.get('kw'))
        return self.render('admin/stats_medicine.html', stats=stats)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class StatsPatientView(AuthenticatedView):
    @expose('/')
    def index(self):
        stats = dao.statistic_medical_examination_month(from_month=(request.args.get('from_month')),
                                                        to_month=(request.args.get('to_month')))
        return self.render('admin/stats_patient_amount.html', stats=stats)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN




class ExamineView(AuthenticatedView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        date_today = date.today()
        mc = dao.load_medicalCertificate(date_today)
        medicine = dao.load_Medicine()
        medicine_by_name = dao.load_Medicine(kw=request.args.get('keyword'))
        return self.render('admin/examine.html', mc=mc, date_today=date_today, medicine=medicine, medicine_by_name=medicine_by_name)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.DOCTOR




class registerMedicalCertificateView(AuthenticatedView):
    @expose('/')
    def index(self):
        date_today = date.today()
        mc = dao.load_medicalCertificate(date_today)
        user_id = (request.args.get('user_id'))
        user = dao.load_user(user_identity_card=request.args.get('identity_card'), user_id=user_id)
        return self.render('admin/register_medical_certificate.html', mc=mc, date_today=date_today, user=user)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.NURSE


class registerAccountView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/register_account.html')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.NURSE

class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')



class MyView(BaseView):
    def __init__(self, *args, **kwargs):
        self._default_view = True
        super(MyView, self).__init__(*args, **kwargs)
        self.admin = Admin()
@app.route('/medical-record/<int:user_id>')
def medical_record(user_id):
    medicalRecord = dao.load_medical_record_by_user_id(user_id)
    return MyView().render('/admin/medical_record.html', medicalRecord=medicalRecord)

class AdminView(AdminIndexView):
    def is_visible(self):
        return  current_user.is_authenticated
    @expose('/')
    def index(self):
        return self.render('admin/index.html')



class receiptView(AuthenticatedView):
    @expose('/', methods=['POST', 'GET'])
    def index(self):
        err_msg = ""
        date_today = date.today()
        prescription_id = request.args.get('prescription_id')
        prescription = dao.get_prescription_by_id(id=prescription_id)
        if prescription_id:
            if prescription:
                total_price = dao.medicine_total_price(id=prescription_id)
                rule = dao.get_rule_by_id(rule_id=2)
                total = total_price + rule.amount
                return self.render('admin/receipt.html', prescription=prescription, prescription_id=prescription_id,
                                       total_price=total_price, rule=rule, total=total, date_today=date_today)
            else:
                err_msg = "Toa thuốc này không tồn tại"
        return self.render('admin/receipt.html', err_msg=err_msg)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.EMPLOYEE



admin = Admin(app=app, name='Quản trị Phòng khám', template_mode='bootstrap4', index_view=AdminView())
admin.add_view(AuthenticatedModelView(User, db.session, name="Người dùng"))
admin.add_view(AuthenticatedModelView(Medicine, db.session, name="Thuốc"))
admin.add_view(AuthenticatedModelView(Kind, db.session, name="Loại"))
admin.add_view(AuthenticatedModelView(Unit, db.session, name="Đơn vị"))
admin.add_view(AuthenticatedModelView(Rule, db.session, name="Quy định"))
admin.add_view(registerAccountView(name="Đang kí người dùng"))
admin.add_view(registerMedicalCertificateView(name="Đang kí phiếu khám bệnh"))
admin.add_view(ExamineView(name="Khám bệnh"))
admin.add_view(receiptView(name="Thanh toán hóa đơn"))
admin.add_view(StatsPatientView(name='Thống kê bệnh nhân'))
admin.add_view(StatsMedicineView(name='Thống kê Thuốc'))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))
