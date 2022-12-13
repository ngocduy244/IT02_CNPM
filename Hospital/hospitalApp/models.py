from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from hospitalApp import db, app
from datetime import datetime, date
from enum import Enum as userEnum
from  flask_login import UserMixin

class UserRole(userEnum):
    ADMIN = 1
    USER = 2
    NURSE = 3
    DOCTOR = 4
    EMPLOYEE = 5



class Unit(userEnum):
    vien = 1;
    chai = 2;
    vy = 3;


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    birthday = Column(DateTime, default=date.today())
    identity_card = Column(String(12), unique=True, nullable=False)
    address = Column(String(100))
    phone = Column(String(12))
    gender = Column(String(10), nullable=False)
    qualification = Column(String(100))
    joined_date = Column(DateTime, default=date.today())
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    avatar = Column(String(100))
    medicalRecords = relationship('MedicalRecords', backref='user', uselist=False, lazy=True)
    medicalCertificate = relationship('MedicalCertificate', backref='user', lazy=True)
    receipt = relationship('Receipt', backref='user', lazy=True)
    prescription = relationship('Prescription', backref='user', lazy=True)
    is_active = Column(Boolean, default=True)


    def __str__(self):
        return self.name


class Rule(db.Model):
    __tablename__ = 'rule'


    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    amount = Column(Integer, nullable=False)
    # calendar = relationship('Calendar', backref='rule', lazy=True)
    # receipt = relationship('Receipt', backref='rule', lazy=True)
    # medicalCertificate = relationship('MedicalCertificate', backref='rule', lazy=True)


    def __str__(self):
        return self.name


# class Calendar(db.Model):
#     __tablename__ = 'calendar'
#
#     name = Column(String(50), nullable=False)
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     created_date = Column(DateTime,default=datetime.date(datetime.today()), unique=True)
#     rule_id = Column(Integer, ForeignKey(Rule.id), nullable=False)
#     medicalCertificate = relationship('MedicalCertificate', backref='calendar', lazy=True)
#
#
#     def __str__(self):
#         return self.name


class MedicalRecords(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receipt = relationship('Receipt', backref='medicalRecords', lazy=True)

class MedicalCertificate(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=date.today())
    # Symptom = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    # calendar_date = Column(DateTime, ForeignKey(Calendar.created_date), nullable=False)
    # rule_id = Column(Integer, ForeignKey(Rule.id), default=1,nullable=False)
    examines_date = Column(DateTime, default=date.today())


class Medicine(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    kind = Column(String(50), nullable=False)
    unit = Column(Enum(Unit), nullable=False)
    price = Column(Integer, nullable=False)
    prescription_details = relationship('PrescriptionDetails', backref='medicine', lazy=True)




class Prescription(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=date.today())
    disease_name = Column(String(50), nullable=False)
    symptom = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receipt = relationship('Receipt', backref='prescription', lazy=True, uselist=False)
    prescription_details = relationship('PrescriptionDetails', backref='prescription', lazy=True)



class PrescriptionDetails(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, default=0)
    price = Column(Integer, default=0)
    prescription_id = Column(Integer, ForeignKey(Prescription.id), nullable=False)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    total_price = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    prescription_id = Column(Integer, ForeignKey(Prescription.id), nullable=False)
    # rule_id = Column(Integer, ForeignKey(Rule.id), default=2)
    MedicalRecords_id = Column(Integer, ForeignKey(MedicalRecords.id), nullable=False)


# class Category(BaseModel):
#     __tablename__ = 'category'
#
#
#     name = Column(String(20), nullable=False)
#     products = relationship('Product', backref='category', lazy=True)
#
#
#     def __str__(self):
#         return self.name


# class Product(BaseModel):
#     __tablename__ = 'product'
#
#
#     name = Column(String(50), nullable=False)
#     description = Column(String(255))
#     price = Column(Float, default=0)
#     image = Column(String(100))
#     active = Column(Boolean, default = True)
#     created_date = Column(DateTime, default=datetime.now())
#     category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
#     # Nếu khóa ngoại tham chiếu đến khóa chính được tạo sau thì dùng "tablename.[foreignKey]"
#
#
#     def __str__(self):
#         return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # c1 = Category(name="Điện thoại")
        # c2 = Category(name="May tính bảng")
        # c3 = Category(name="Phu kien")
        # db.session.add(c1)
        # db.session.add(c2)
        # db.session.add(c3)

        import hashlib
        password = str(hashlib.md5('1'.encode('utf-8')).hexdigest())
        u = User(name='employee', username='employee', password=password, birthday = date(2002,2,24),user_role=UserRole.EMPLOYEE, address='fff', phone='2214124',gender="Nam",
                 identity_card='205105201234', avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        db.session.add(u)
        db.session.commit()
        # p1 = Product(name='Galaxy S22 Pro', description='Samsung, 128GB', price=25000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #              category_id=1)
        # p2 = Product(name='Galaxy Fold 4', description='Samsung, 128GB', price=38000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg',
        #              category_id=1)
        # p3 = Product(name='Apple Watch S5', description='Apple, 32GB', price=18000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #              category_id=3)
        # p4 = Product(name='Galaxy Tab S8', description='Samsung, 128GB', price=22000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #              category_id=2)
        # p5 = Product(name='iPhone 14', description='Apple, 128GB', price=27000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #              category_id=1)
        # p6 = Product(name='iPad Pro 2022', description='Apple, 256GB', price=38000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg',
        #              category_id=2)
        # p7 = Product(name='Galaxy Z Fold 5', description='Samsung, 128GB', price=24000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #              category_id=2)
        # db.session.add_all([p1, p2, p3, p4, p5, p6, p7])
        # db.session.commit()


        # pass
        # db.session.commit()
#