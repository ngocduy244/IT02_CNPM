from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from hospitalApp import db, app
from datetime import datetime
from enum import Enum as userEnum
from  flask_login import UserMixin

class UserRole(userEnum):
    ADMIN = 1
    USER = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.date(datetime.today()))
    avatar = Column(String(100))
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name


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
        # c1 = Category(name="Dien Thoai")
        # c2 = Category(name="May tính bảng")
        # c3 = Category(name="Phu kien")
        # db.session.add(c1)
        # db.session.add(c2)
        # db.session.add(c3)

        # import hashlib
        # password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u = User(name='Huu', username='Huu', password=password, user_role=UserRole.ADMIN,
        #          avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        # db.session.add(u)
        # db.session.commit()


        pass
        # db.session.commit()
