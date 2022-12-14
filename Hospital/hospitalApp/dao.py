import json
from hospitalApp import app, db
from hospitalApp.models import  User, MedicalCertificate, Rule, Medicine, Prescription, PrescriptionDetails, MedicalRecords, Receipt
import hashlib
from sqlalchemy import func, extract, and_
from datetime import datetime
from flask_login import current_user


# def load_category():
#     # with open(f'{app.root_path}/data/category.json', encoding="UTF-8") as f:
#     #     return json.load(f)
#     return Category.query.all()

# def load_product(category_id = None, kw = None, page=1):
#     # with open(f'{app.root_path}/data/product.json', encoding="UTF-8") as f:
#     #     product = json.load(f)
#     # if category_id:
#     #     product = [p for p in product if p['category_id'] == int(category_id)]
#     #
#     # if kw:
#     #     product = [p for p in product if p['name'].lower().find(kw.lower()) >= 0]
#
#     # return product
#
#     products = Product.query.filter(Product.active.__eq__(True))
#     if category_id:
#         products = Product.query.filter(Product.category_id.__eq__(category_id))
#
#     if kw:
#         products = Product.query.filter(Product.name.contains(kw))
#
#     # page_size = app.config['PAGE_SIZE']
#     # start = (page-1) * page_size
#     # end = start+page_size
#
#     return products.all()

def load_Medicine(kw=None):
    if kw:
        return Medicine.query.filter(Medicine.name.contains(kw))
    return Medicine.query.all()




# def count_product():
#     return Product.query.filter(Product.active.__eq__(True)).count()


def get_rule_by_id(rule_id):
    return Rule.query.get(rule_id)


# def get_product_by_id(product_id):
#     return Product.query.get(product_id)
    # with open(f'{app.root_path}/data/product.json', encoding="UTF-8") as f:
    #     product = json.load(f)
    #
    # for p in product:
    #     if p["id"] == product_id:
    #         return p;

def register(name, username, password, phone, birthday, identity_card, address, gender, avatar):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                phone=phone,
                birthday=birthday,
                identity_card=identity_card,
                address=address,
                gender=gender,
                avatar = avatar)

    db.session.add(user)
    db.session.commit()


def load_medical_record_by_user_id(user_id):
    return MedicalRecords.query.filter(MedicalRecords.user_id.__eq__(user_id)).first()

def load_MC_by_user_id(user_id=None):
    return MedicalCertificate.query.filter(MedicalCertificate.user_id.__eq__(user_id)).first()


def create_MedicalRecord(user_id, prescription_id, total):
    medical_record = MedicalRecords(user_id=user_id)
    db.session.add(medical_record)

    receipt = Receipt(user_id=user_id, prescription_id=prescription_id, total_price=total, medicalRecords=medical_record)
    db.session.add(receipt)

    db.session.commit()

def create_MedicalRecord_have(user_id, prescription_id, total):
    receipt = Receipt(user_id=user_id, prescription_id=prescription_id, total_price=total, medicalRecords=load_medical_record_by_user_id(user_id))
    db.session.add(receipt)

    db.session.commit()


def check_receipt(prescription_id=None):
    return Receipt.query.filter(Receipt.prescription_id.__eq__(prescription_id)).first()


def auth_user(username, password, role):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password),
                             User.user_role.contains(role)).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def load_user_by_id(user_id):
    return User.query.filter(User.id.__eq__(user_id)).first()


def load_user(user_id = None,user_identity_card=None):
    if user_id:
        return User.query.filter(User.id.__eq__(user_id)).first()
    if user_identity_card:
        return User.query.filter(User.identity_card.__eq__(user_identity_card)).first()


def load_medicalCertificate(date=None):
    if date:
        return MedicalCertificate.query.filter(MedicalCertificate.examines_date.contains(date))
    return MedicalCertificate.query.all()





def load_medicalCertificate_By_date_id(date=None, user_id=None):
    if date and user_id:
        return MedicalCertificate.query.filter(MedicalCertificate.examines_date.contains(date),
                                               MedicalCertificate.user_id.__eq__(user_id)).first()


# def count_products_id():
#     return Product.query.filter(Product.category_id.contains(1)).count()

# def count_user_date():
#     return User.query.filter(User.joined_date.contains("2022-11-25")).count()


def check_prescription_by_id_date(userID, created_date):
    if userID and created_date:
        return Prescription.query.filter(Prescription.created_date.contains(created_date),
                                     Prescription.user_id.__eq__(userID)).first()

def count_mc_date(date):
    return MedicalCertificate.query.filter(MedicalCertificate.examines_date.contains(date)).count()


def registerMC(examines_date, user_id):
    mc = MedicalCertificate(user_id=user_id, examines_date=examines_date)
    db.session.add(mc)
    db.session.commit()


def add_prescription(cart, disease_name, user_id, symptom):
    if cart:
        p = Prescription(disease_name=disease_name, user_id=user_id, symptom=symptom)
        db.session.add(p)


        for m in cart.values():
            d = PrescriptionDetails(quantity=m['quantity'], price=m['price'],
                                    prescription=p, medicine_id=m['id'])
            db.session.add(d)

        try:
            db.session.commit()
        except:
            return False

        else:
            return True


def get_prescription_by_id(id):
    return Prescription.query.get(id)


def medicine_total_price(id):
    total_price = 0
    if id:
        pre = get_prescription_by_id(id)
        for pd in pre.prescription_details:
            total_price += int(pd.price) * int(pd.quantity)
    return total_price



# def count_product_by_cate():
#     return db.session.query(Category.id, Category.name, func.count(Product.id)) \
#         .join(Product, Product.category_id.__eq__(Category.id), isouter=True) \
#         .group_by(Category.id).order_by(-Category.name).all()


def stats_revenue(kw=None, from_date=None, to_date=None):
    query = db.session.query(Medicine.id, Medicine.name, func.sum(PrescriptionDetails.quantity * PrescriptionDetails.price)) \
        .join(PrescriptionDetails, PrescriptionDetails.medicine_id.__eq__(Medicine.id)) \
        .join(Receipt, PrescriptionDetails.prescription_id.__eq__(Receipt.prescription_id))

    if kw:
        query = query.filter(Medicine.name.contains(kw))

    if from_date:
        query = query.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(Receipt.created_date.__le__(to_date))


    return query.group_by(Medicine.id).all()


def stats_revenue_month(from_month=None, to_month=None):
    data = db.session.query(func.month(Receipt.created_date),
                            func.sum(Receipt.total_price )) \
        .group_by(func.month(Receipt.created_date)).order_by(func.month(Receipt.created_date))

    if from_month and to_month:
        data = data.filter(and_(extract('month', Receipt.created_date) >= extract('month', from_month),
                                extract('month', Receipt.created_date) <= extract('month', to_month)))

    return data.all()

def statistic_medicine_using_frequency_month(from_month=None, to_month=None, keyword=None):
    data = db.session.query(func.month(Receipt.created_date),
                            func.sum(PrescriptionDetails.quantity)) \
        .join(Receipt, Receipt.prescription_id.__eq__(PrescriptionDetails.prescription_id)) \
        .join(Prescription, Prescription.id.__eq__(PrescriptionDetails.prescription_id)) \
        .join(Medicine, Medicine.id == PrescriptionDetails.medicine_id) \
        .group_by(func.month(Receipt.created_date)) \
        .order_by(func.month(Receipt.created_date))


    if keyword:
        data = data.filter(Medicine.name.__eq__(keyword))


    if from_month and to_month:
        data = data.filter(and_(extract('month', Prescription.created_date) >= extract('month', from_month),
                                extract('month', Prescription.created_date) <= extract('month', to_month)))


    return data.all()


def statistic_medical_examination_month(from_month=None, to_month=None):
    data = db.session.query(func.month(Receipt.created_date),
                            func.count(Prescription.id)) \
        .join(Receipt, Receipt.prescription_id.__eq__(Prescription.id)) \
        .group_by(func.month(Receipt.created_date)) \
        .order_by(func.month(Receipt.created_date))


    if from_month and to_month:
        data = data.filter(and_(extract('month', Prescription.created_date) >= extract('month', from_month),
                                extract('month', Prescription.created_date) <= extract('month', to_month)))


    return data.all()



if __name__ == '__main__':
    from hospitalApp import app

    with app.app_context():
        print(statistic_medical_examination_month())