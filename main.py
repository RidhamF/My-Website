#TODO  : Importing the Modules

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from forms import Register, Login
from flask_bootstrap import Bootstrap4


#TODO : Creating the APP

app = Flask(__name__)
app.secret_key = "this-is-a-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
bootstrap = Bootstrap4()
bootstrap.init_app(app)
#TODO : Establishing a login system:
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


class Base(DeclarativeBase):
    pass

#TODO : Creating the DATABASE
db = SQLAlchemy(model_class=Base)
db.init_app(app)


#TODO : Creating the Users Table
class User(db.Model,UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()

with app.app_context():
    db.create_all()

#TODO : Defining the Routes
logged_in = False

#Home Route
@app.route("/")
def home():
    return render_template("index.html",logged_in=logged_in)

#Login Route
@app.route("/login",methods=["GET",'POST'])
def login():
    global logged_in
    form = Login()
    if form.validate_on_submit():
        emails = [user.email for user in db.session.execute(db.select(User)).scalars().all()]
        usernames = [user.username for user in db.session.execute(db.select(User)).scalars().all()]
        if form.email.data not in emails and form.email.data not in usernames:
            flash("No such user exists")
            return redirect(url_for('login'))
        else:
            user  = db.session.execute(db.select(User).where(User.email==form.email.data)).scalar()
            if not user:
                user = db.session.execute(db.select(User).where(User.username == form.email.data)).scalar()
            if check_password_hash(user.password,form.password.data):
                logged_in = True
                return redirect(url_for("home"))
            else:
                flash("The password is incorrect")
                return redirect(url_for('login'))

    return render_template("login.html",form=form,logged_in=logged_in)

#Register Route
@app.route("/register",methods=['GET','POST'])
def register():
    global logged_in
    form = Register()
    if form.validate_on_submit():
        emails = [user.email for user in db.session.execute(db.select(User)).scalars().all()]
        if form.email.data in emails:
            flash("Email already registered")
            return redirect(url_for('register'))
        else:
            pass_hash = generate_password_hash(form.password.data,salt_length=8)
            user = User(username=form.username.data,password=pass_hash,email=form.email.data)
            with app.app_context():
                db.session.add(user)
                db.session.commit()
                logged_in = True
            return redirect(url_for("home"))

    return render_template("register.html",form=form,logged_in=logged_in)

#Contact ME Route
@app.route("/contact-me")
def contact():
    return render_template("contact.html",logged_in=logged_in)

#About Route
@app.route("/about")
def about():
    return render_template("about.html",logged_in=logged_in)

#Logout Route
@login_required
@app.route("/logout")
def logout():
    global logged_in
    logged_in=False
    return redirect(url_for('home'))





if __name__=="__main__":
    app.run(debug=True,port=6969)