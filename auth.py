from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterFrom, LoginForm
from db import db, User
import smtplib
import os

auth_bp = Blueprint('auth_bp', __name__)


def load_user(user_id):
    return db.get_or_404(User, user_id)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterFrom()
    focus_on = None
    if form.validate_on_submit():
        data = form.data
        user = db.session.execute(db.select(User).where(User.email == data['email'])).scalar()
        if user:
            focus_on = "email"
            flash("email already registered.")
        elif data['password'] != data['conformPass']:
            focus_on = "conform_pass"
            flash("password not match, please conform password.")
        elif len(data['password']) < 8:
            focus_on = "password"
            flash("password length should be more-than 8 require.")
        else:
            new_user = User(
                name=data['name'],
                email=data['email'],
                password=generate_password_hash(data['password'], method='pbkdf2:sha1', salt_length=8)
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('blog_bp.get_all_posts'))
    return render_template(
        "register.html",
        form=form,
        focus_on=focus_on,
        user=current_user
    )


@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    focus_on = None
    if form.validate_on_submit():
        data = form.data
        user = db.session.execute(db.select(User).where(User.email == data['email'])).scalar()
        if user:
            if check_password_hash(user.password, data['password']):
                login_user(user)
                return redirect(url_for("blog_bp.get_all_posts"))
            else:
                focus_on = 'password'
                flash('wrong password')
        else:
            focus_on = 'email'
            flash('email not registered.')
    return render_template(
        "login.html",
        form=form,
        focus_on=focus_on,
        user=current_user
    )


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog_bp.get_all_posts'))


@auth_bp.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        data = request.form
        name = data['name']
        email = data['email']
        phone = data['phone']
        message = data['message']
        # sending mail
        send_msg = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nmessage: {message}"
        send_email = "nikhiltelase@gmail.com"
        result = send_mail(mail_id=send_email, user_msg=send_msg)

        # send a mail to uere for interection
        feedbaack_msg = "Thank You!\n\nThank you for reaching out. We'll get back to you as soon as possible!"
        send_mail(mail_id=email, user_msg=feedbaack_msg)

        return render_template("contact.html", user_feedback=result, user=current_user)
    else:
        return render_template("contact.html", user_feedback="Contact Me", user=current_user)


def send_mail(mail_id, user_msg):
    my_email = os.getenv("EMAIL")
    print(my_email)
    password = os.getenv("PASSWORD")
    print(password)
    message = f"Subject: Blog web \n\n{user_msg}"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()  # secure
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=[mail_id],
                                msg=message)
        return "Thanks For Contact Me"
    except Exception as error:
        print(error)
        return "Error, please try again"
