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



        k1 = Kind(name="Thuốc hạ sốt")
        k2 = Kind(name="Thuốc ho")
        k3 = Kind(name="Thuốc nhỏ mắt")

        db.session.add_all([k1,k2,k3])
        db.session.commit()

        unit1 = Unit(name="Viên")
        unit2 = Unit(name="Chai")
        unit3 = Unit(name="Vĩ")

        db.session.add_all([unit1, unit2, unit3])
        db.session.commit()

        m1 = Medicine(name="Aspirin", price=1400, unit_id=1, kind_id=1)
        m2 = Medicine(name="Paracetamol", price=10000, unit_id=3, kind_id=1)
        m3 = Medicine(name="Prospan", price=45000, unit_id=2, kind_id=2)
        m4 = Medicine(name="Rohto Vita", price=30000, unit_id=2, kind_id=3)

        db.session.add_all([m1, m2, m3, m4])
        db.session.commit()

        r1 = Rule(name="Số lượng bệnh nhân", amount=30)
        r2 = Rule(name="Số tiền khám", amount=150000)

        db.session.add_all([r1, r2])
        db.session.commit()

        import hashlib
        password = str(hashlib.md5('1'.encode('utf-8')).hexdigest())
        u1 = User(name='Lý Nguyễn Ngọc Duy', username='admin', password=password, birthday = date(1994,7,22),user_role=UserRole.ADMIN, address='371 Nguyễn Kiệm, Gò Vấp', phone='2214124',gender="Nam",
                identity_card='205105201900',
                  avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')

        u2 = User(name='Đào Minh Phố', username='doctor', password=password, birthday=date(1985, 5, 2), user_role=UserRole.DOCTOR,
                  address='371 Nguyễn Kiệm, Gò Vấp', phone='2214124', gender="Nam",
                  identity_card='208146851234',
                  avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')

        u3 = User(name='Nguyễn Phạm Ngọc Phú', username='nurse', password=password, birthday=date(2000, 2, 24), user_role=UserRole.NURSE,
                  address='371 Nguyễn Kiệm, Gò Vấp', phone='2214124', gender="Nữ",
                  identity_card='208145977234',
                  avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')

        u4 = User(name='Trấn Quang Khánh', username='employee', password=password, birthday=date(1999, 3, 6), user_role=UserRole.EMPLOYEE,
                  address='371 Nguyễn Kiệm, Gò Vấp', phone='2214124', gender="Nam",
                  identity_card='208141551234',
                  avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')

        u5 = User(name='user', username='user', password=password, birthday=date(2001, 2, 2), user_role=UserRole.USER,
                  address='371 Nguyễn Kiệm, Gò Vấp', phone='2214124', gender="Nữ",
                  identity_card='208146251234',
                  avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')

        u6 = User(name='user', username='user1', password=password, birthday=date(2001, 6, 27), user_role=UserRole.USER,
                  address='371 Nguyễn Kiệm, Gò Vấp', phone='2214124', gender="Nam",
                  identity_card='208142451234',
                  avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')

        u7 = User(name='user', username='user2', password=password, birthday=date(2000, 5, 12), user_role=UserRole.USER,
                  address='371 Nguyễn Kiệm, Gò Vấp', phone='2214124', gender="Nam",
                  identity_card='208142371234',
                  avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')

        u8 = User(name='user', username='user3', password=password, birthday=date(2002, 7, 12), user_role=UserRole.USER,
                  address='371 Nguyễn Kiệm, Gò Vấp', phone='2214124', gender="Nữ",
                  identity_card='208185851234',
                  avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')

        u9 = User(name='user', username='user4', password=password, birthday=date(2005, 7, 21), user_role=UserRole.USER,
                  address='371 Nguyễn Kiệm, Gò Vấp', phone='2214124', gender="Nam",
                  identity_card='208145854134',
                  avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')

        u10 = User(name='user', username='user5', password=password, birthday=date(2001, 12, 22), user_role=UserRole.USER,
                  address='371 Nguyễn Kiệm, Gò Vấp', phone='2214124', gender="Nữ",
                  identity_card='208125751234',
                  avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')


        db.session.add_all([u1,u2,u3,u4,u5,u6,u7,u8,u9,u10])
        db.session.commit()





        # pass
        # db.session.commit()
#