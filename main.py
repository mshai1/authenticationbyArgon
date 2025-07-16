from flask import Flask, session, render_template, url_for, redirect, flash, request
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer


app = Flask(__name__)
app.config['SECRET_KEY'] = '4dvJnwNDfE84irUv0934ioRnj'

ph = PasswordHasher()
user_list = []

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users-list.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Users(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    useremail: Mapped[String] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[String] = mapped_column(String(256), nullable=False)
    fullname: Mapped[String] = mapped_column(String(80), nullable=False)
    phone: Mapped[Integer] = mapped_column(Integer, nullable=False)
    address: Mapped[String] = mapped_column(String(80), nullable=False)


    #Optional, allows searching by user email address
    def __repr__(self):
        return f'<User {self.useremail}>'

with app.app_context():
    db.create_all()


class SignUpForm(FlaskForm):
    full_name = StringField("Enter your full name", validators= [InputRequired()])
    phone = StringField("Enter your phone number", validators=[InputRequired()])
    address = StringField("Enter your address", validators=[InputRequired()])
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
        raw_password = form.user_password.data
        print(user_email)
        print(raw_password)

        user = Users.query.filter_by(useremail=user_email).first()

        if not user:
            flash("Email not found", "danger")

        else:
            try:
                ph.verify(user.password, raw_password)
                session['user_email'] = user.useremail
                flash("Login Successful!", "success")
                return redirect(url_for('profile'))
            except VerifyMismatchError:
                flash("Incorrect password", "danger")

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        signupname = form.full_name.data
        signupphone = form.phone.data
        signupaddress = form.address.data
        signupemail = form.email.data
        signuppassword = form.password.data
        print(signupemail)
        print(signuppassword)

        existing_user =  Users.query.filter_by(useremail=signupemail).first()
        if existing_user:
            flash("User already exists. Please try logging in", "danger")

        else:
            hashed_password = ph.hash(signuppassword)

            new_user = Users(
                fullname=signupname,
                phone=signupphone,
                address=signupaddress,
                useremail= signupemail,
                password= hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            flash("User signed up successfully!", "success")
            return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/profile')
def profile():
    if 'user_email' not in session:
        flash("Please log in to access the profile page.", "warning")
        return redirect(url_for('login'))

    user = Users.query.filter_by(useremail=session['user_email']).first()

    return render_template('profile.html', user=user)


@app.route('/update-profile', methods=['POST'])
def update_profile():
    user_email = session.get('user_email')
    if not user_email:
        return redirect(url_for('login'))

    user = Users.query.filter_by(useremail=session['user_email']).first()
    if not user:
        return redirect(url_for('login'))

    # Get updated values from form
    user.fullname = request.form.get('fullname')
    user.phone = request.form.get('phone')
    user.address = request.form.get('address')
    db.session.commit()

    flash("Profile updated successfully!", "success")
    return redirect(url_for('profile'))


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)