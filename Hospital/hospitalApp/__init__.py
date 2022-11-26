from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
import cloudinary



app = Flask(__name__)
app.secret_key="(J%*(#H#&@*H@**AS*FASBF*ASF&&***@"

app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:%s@localhost/labhospitaldb?charset=utf8mb4" % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config['PAGE_SIZE']=2


db = SQLAlchemy(app=app)


admin = Admin(app=app, name='Quản trị bán hàng online', template_mode='bootstrap4')

cloudinary.config(
        cloud_name="dxqeqad9d",
        api_key= "583547176434271",
        api_secret= "tf5rWXdaF5G-vPyLompiLN042NA"
)

login = LoginManager(app=app)