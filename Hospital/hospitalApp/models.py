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


    def __str__(self):
        return self.name


class MedicalRecords(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receipt = relationship('Receipt', backref='medicalRecords', lazy=True)

class MedicalCertificate(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=date.today())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    examines_date = Column(DateTime, default=date.today())


class Unit(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(12),nullable=False, unique=True)
    medicine = relationship('Medicine', backref='unit', lazy=True)

    def __str__(self):
        return self.name

class Kind(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20),nullable=False, unique=True)
    medicine = relationship('Medicine', backref='kind', lazy=True)

    def __str__(self):
        return self.name



class Medicine(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    unit_id = Column(Integer, ForeignKey(Unit.id), nullable=False)
    kind_id = Column(Integer, ForeignKey(Kind.id), nullable=False)
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
    MedicalRecords_id = Column(Integer, ForeignKey(MedicalRecords.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()

        #
        import hashlib
        password = str(hashlib.md5('1'.encode('utf-8')).hexdigest())
        u = User(name='user', username='user', password=password, birthday = date(2002,2,24),user_role=UserRole.USER, address='fff', phone='2214124',gender="Nữ",
                 identity_card='208145851234', avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        db.session.add(u)
        db.session.commit()



        # pass
        # db.session.commit()
#