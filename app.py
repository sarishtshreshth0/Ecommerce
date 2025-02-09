from flask import Flask, render_template, request ,session , redirect , url_for
from flask_mail import Mail, Message
import random
from datetime import date
today = date.today().strftime("%Y-%m-%d")
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template, request ,session , redirect
from flask_mail import Mail, Message
import random
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
uri = "mongodb+srv://sarishtshreshth:openforall@cluster0.sf3lhpf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
app = Flask(__name__)
app.secret_key = "securemore"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'saristhshreshth12@gmail.com'
app.config['MAIL_PASSWORD'] = "emyx zmzd afjf keqh"
app.config['MAIL_DEFAULT_SENDER'] = 'saristhshreshth12@gmail.com'
mail = Mail(app)

db = client['ecommerce']
db_user = db['user']
db_otp = db['otp']
db_contact = db['contact']
db_product = db['product']

@app.route('/login',methods = ['GET', 'POST'])
def login():
    if request.method == "POST" :
        email = request.form['email']
        password = request.form['password']
        if email and password:
            check = db_user.find_one({"email":email, "password":password})
            if check:
                session['username'] = email
                return redirect("/")
            else:
                return redirect("/login")
        else:
            return redirect("/login")
    else:
        return render_template("login.html")
@app.route('/signup',methods = ['GET', 'POST'])
def signup():
    if request.method == "POST" :
        first = request.form['first']
        session['name'] = first
        last = request.form['last']
        m_number = request.form['m_number']
        email = request.form['email']
        session['email'] = email
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if email and password and first and last and confirm_password:
            db_user.insert_one({"first": first, "last": last, "m_number" :m_number , "email":email, "password":password, "confirm_password":confirm_password})
            return redirect("/verify")
        else:
            return redirect("/signup")
    else:
        return render_template("signup.html")


@app.route('/logout',methods = ['GET', 'POST'])
def logout():
    session.pop("username", None)
    return redirect("/login")

def send_otp():
    random_number = random.randint(1000, 9999)
    session['otp'] = str(random_number)
    db_otp.insert_one({"otp": str(random_number)})
    send_mail(random_number)
    return random_number

def send_mail(stored_otp):
    msg = Message(
        subject="Ecommerce Project",
        recipients=[session['email']],
        body= "your otp is " + str(stored_otp)
    )
    mail.send(msg)
    return "Mail sent!"

@app.route("/verify", methods=['GET', 'POST'])
def verify():
    if request.method == "POST":
        v1 = request.form.get('v1', '')
        v2 = request.form.get('v2', '')
        v3 = request.form.get('v3', '')
        v4 = request.form.get('v4', '')

        entered_otp = int(v1 + v2 + v3 + v4)
        stored_otp = int(session.get('otp', 0))

        print("Stored OTP:", stored_otp)
        print("Entered OTP:", entered_otp)
        if entered_otp == stored_otp:
            return redirect("/login")
        else:
            return redirect("/signup")

    result = send_otp()
    print("Generated OTP:", result)
    return render_template("verify_otp.html")

@app.route("/reset-password", methods=['GET', 'POST'])
def reset_password():
    return render_template("reset_password.html")

@app.route("/",methods = ['GET', 'POST'])
def home():
    name = db_user.find_one({"email":session.get('username')})
    if name:
        name = name["first"].title()
    else:
        name = "Login"
    session['name'] = name
    return render_template("index.html",name = name)

@app.route("/contact",methods = ['GET', 'POST'])
def contact():
    if request.method == "POST":
        message = request.form['message']
        msg = Message(
            subject="Ecommerce Project",
            recipients=[session['username']],
            body= message
        )
        mail.send(msg)
        db_contact.insert_one({"Id": session['username'],"issue": message ,"status": 'Pending', "raiseBy":session.get('name') , 'date' : today})
        return redirect("/ticketraise")
    name = session.get('name', 'Login')
    email = session.get('username', "Login")
    return render_template("contact_us.html",name = name , email = email)

@app.route("/ticketraise",methods = ['GET', 'POST'])
def ticket():
    Id = db_contact.count_documents({})
    return render_template("ticket_raised.html" , Id = Id)

@app.route("/raisedlist",methods = ['GET', 'POST'])
def listraised():
    list_raised = [i for i in db_contact.find({"Id":session.get('username')})]
    return render_template("show_raised.html" , raised = list_raised)

@app.route("/address",methods = ['GET', 'POST'])
def address():
    return render_template("manage_address.html")

@app.route("/setting", methods=['GET', 'POST'])
def setting():
    if session.get('username') is None:
        return redirect("/login")

    email = session.get('username')
    data = db_user.find_one({"email": email})

    if request.method == "POST" and "edit_mode" in request.form:
        return render_template(
            "Profile_setting.html",
            first=data["first"].title(),
            last=data["last"].title(),
            gender=data.get("gender", ""),
            email=email,
            m_number=data["m_number"],
            edit_mode=True
        )


    if request.method == "POST" and "save_mode" in request.form:
        new_first = request.form['first_name'].strip().title()
        new_last = request.form['last_name'].strip().title()
        new_m_number = request.form['m_number'].strip()
        new_gender = request.form.get('gender', '')
        # Update database
        db_user.update_one(
            {"email": email},
            {"$set": {
                "first": new_first,
                "last": new_last,
                "m_number": new_m_number,
                "gender": new_gender
            }}
        )

        return redirect("/setting")

    return render_template(
        "Profile_setting.html",
        first=data["first"].title(),
        last=data["last"].title(),
        gender=data.get("gender", ""),
        email=email,
        m_number=data["m_number"],
        edit_mode=False
    )

@app.route("/order",methods = ['GET', 'POST'])
def order():

    return render_template("orderpage.html")

@app.route("/mobile",methods = ['GET', 'POST'])
def product_list():
    product = [i for i in db_product.find()]
    return render_template("product_list_phone.html", products = product)

if __name__ == '__main__':
    app.run(debug=True)
