import json
from hospitalApp import app, db
from hospitalApp.models import Category, Product, User
import hashlib

def load_category():
    # with open(f'{app.root_path}/data/category.json', encoding="UTF-8") as f:
    #     return json.load(f)
    return Category.query.all()

def load_product(category_id = None, kw = None, page=1):
    # with open(f'{app.root_path}/data/product.json', encoding="UTF-8") as f:
    #     product = json.load(f)
    # if category_id:
    #     product = [p for p in product if p['category_id'] == int(category_id)]
    #
    # if kw:
    #     product = [p for p in product if p['name'].lower().find(kw.lower()) >= 0]

    # return product

    products = Product.query.filter(Product.active.__eq__(True))
    if category_id:
        products = Product.query.filter(Product.category_id.__eq__(category_id))

    if kw:
        products = Product.query.filter(Product.name.contains(kw))

    # page_size = app.config['PAGE_SIZE']
    # start = (page-1) * page_size
    # end = start+page_size

    return products.all()

def count_product():
    return Product.query.filter(Product.active.__eq__(True)).count()


def get_product_by_id(product_id):
    return Product.query.get(product_id)
    # with open(f'{app.root_path}/data/product.json', encoding="UTF-8") as f:
    #     product = json.load(f)
    #
    # for p in product:
    #     if p["id"] == product_id:
    #         return p;

def register(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email = kwargs.get('email'),
                avatar = kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()

def auth_user(username, password, role):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password),
                             User.user_role.contains(role)).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)


def count_products_id():
    return Product.query.filter(Product.category_id.contains(1)).count()

def count_user_date():
    return User.query.filter(User.joined_date.contains("2022-11-25 00:00:00")).count()