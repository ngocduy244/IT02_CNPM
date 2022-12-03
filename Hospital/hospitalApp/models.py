from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from hospitalApp import db, app
from datetime import datetime
from enum import Enum as userEnum
from  flask_login import UserMixin

class UserRole(userEnum):
    ADMIN = 1
    USER = 2
    NURSE = 3
    DOCTOR = 4
    EMPLOYEE = 5


class Gender(userEnum):
    Male = 1
    Female = 2


class Unit(userEnum):
    capsule = 1;
    bottle = 2;
    vy = 3;


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):

    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    birthday = Column(DateTime, default=datetime.date(datetime.today()))
    address = Column(String(100))
    phone = Column(String(12))
    gender = Column(Enum(Gender), nullable=False)
    qualification = Column(String(100))
    joined_date = Column(DateTime, default=datetime.date(datetime.today()))
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
    amount = Column(Float, nullable=False)
    # calendar = relationship('Calendar', backref='rule', lazy=True)
    receipt = relationship('Receipt', backref='rule', lazy=True)
    medicalCertificate = relationship('MedicalCertificate', backref='rule', lazy=True)


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
    prescription = relationship('Prescription', backref='medicalRecords', lazy=True)

class MedicalCertificate(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.date(datetime.today()))
    Symptom = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    # calendar_date = Column(DateTime, ForeignKey(Calendar.created_date), nullable=False)
    rule_id = Column(Integer, ForeignKey(Rule.id), default=1 ,nullable=False)
    examines_date = Column(DateTime, default=datetime.date(datetime.today()))


class Medicine(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    kind = Column(String(50), nullable=False)
    unit = Column(Enum(Unit), nullable=False)
    price = Column(Float, nullable=False)
    prescription_details = relationship('PrescriptionDetails', backref='medicine', lazy=True)




class Prescription(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.date(datetime.today()))
    disease_name = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    MedicalRecords_id = Column(Integer, ForeignKey(MedicalRecords.id), nullable=False)
    receipt = relationship('Receipt', backref='prescription', lazy=True, uselist=False)
    prescription_details = relationship('PrescriptionDetails', backref='prescription', lazy=True)



class PrescriptionDetails(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    usage = Column(String(50), nullable=False)
    prescription_id = Column(Integer, ForeignKey(Prescription.id), nullable=False)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.date(datetime.today()))
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    prescription_id = Column(Integer, ForeignKey(Prescription.id), nullable=False)
    rule_id = Column(Integer, ForeignKey(Rule.id), nullable=False)


class Category(BaseModel):
    __tablename__ = 'category'


    name = Column(String(20), nullable=False)
    products = relationship('Product', backref='category', lazy=True)


    def __str__(self):
        return self.name


class Product(BaseModel):
    __tablename__ = 'product'


    name = Column(String(50), nullable=False)
    description = Column(String(255))
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default = True)
    created_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    # Nếu khóa ngoại tham chiếu đến khóa chính được tạo sau thì dùng "tablename.[foreignKey]"


    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        # c1 = Category(id=6,name="XX222X")
        # c2 = Category(name="May tính bảng")
        # c3 = Category(name="Phu kien")
        # db.session.add(c1)
        # db.session.add(c2)
        # db.session.add(c3)

        import hashlib
        password = str(hashlib.md5('1'.encode('utf-8')).hexdigest())
        u = User(name='admin', username='admin', password=password, birthday = datetime(2002,2,24),user_role=UserRole.ADMIN,  address='fff', phone='2214124',gender=Gender.Male,
                 avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        db.session.add(u)
        db.session.commit()


        # pass
        # db.session.commit()
