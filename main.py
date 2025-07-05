from flask import Flask, session, render_template, url_for
from argon2 import PasswordHasher
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer


app = Flask(__name__)
app.config['SECRET_KEY'] = '4dvJnwNDfE84irUv0934ioRnj'
# Bootstrap5(app)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users-list.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Users(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    useremail: Mapped[String] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[String] = mapped_column(String(256), nullable=False)

    #Optional, allows searching by user email address
    def __repr__(self):
        return f'<User {self.useremail}>'

# with app.app_context():
#     db.create_all()


class SignUpForm(FlaskForm):
    email = StringField("Enter your email address", validators=[InputRequired(), Email(message="Enter a valid email.")])
    password = PasswordField("Create a password", validators=[InputRequired(), Length(min=8)])
    re_password = PasswordField("Re-enter the password", validators=[InputRequired(),
                                                                     EqualTo('password', message='Password must match')])
    signup = SubmitField("Sign-Up")


class LoginInForm(FlaskForm):
    user_email = StringField("Enter your email address", validators=[InputRequired(), Email(message="Enter a valid email.")])
    user_password = PasswordField("Enter your password", validators=[InputRequired()])
    remember_me = SubmitField("Remember me")
    user_login = SubmitField("Login")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginInForm()
    if form.validate_on_submit():
        user_email = form.user_email.data
        password = form.user_password.data
        print(user_email)
        print(password)

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        signupemail = form.email.data
        signuppassword = form.password.data
        print(signupemail)
        print(signuppassword)
    return render_template('signup.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)