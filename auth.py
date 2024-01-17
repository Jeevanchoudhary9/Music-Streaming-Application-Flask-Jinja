from app import app
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
from models import Rating, db, User, Profile
from sqlalchemy.exc import SQLAlchemyError

# authentication decorators
def auth_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return inner

def admin_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue')
            return redirect(url_for('login'))
        if User.query.filter_by(userid=session['user_id']).first().role!="admin":
            flash('You are not authorized to access this page as you are not an admin')
            return redirect(url_for('user_dashboard'))
        return func(*args, **kwargs)
    return inner

def creator_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue')
            return redirect(url_for('login'))
        if User.query.filter_by(userid=session['user_id']).first().role!="creator":
            flash('You are not authorized to access this page as you are not a creator')
            return redirect(url_for('user_dashboard'))
        return func(*args, **kwargs)
    return inner

# user login page
@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect(url_for('user_dashboard'))
    return render_template('login_register/login.html',nav="login")

# user login post
@app.route('/login', methods=["POST"])
def login_post():
    username=request.form.get('username')
    password=request.form.get('password')

    if username=='' or password=='':
        flash('Please fill the required fields')
        return redirect(url_for('login'))
    
    user=User.query.filter_by(uname=username).first()
    if not user:
        flash('Please check your username and try again.')
        return redirect(url_for('login'))
    if not user.check_password(password):
        flash('Please check your password and try again.')
        return redirect(url_for('login'))
    #after successful login   
    session['user_id']=user.userid
    return redirect(url_for('user_dashboard'))

# Admin login page
@app.route('/login_admin')
def login_admin():
    return render_template('login_register/login_admin.html',nav="admin_login")

# Admin login post
@app.route('/login_admin', methods=["POST"])
def login_admin_post():
    username=request.form.get('username')
    password=request.form.get('password')

    if username is None or password is None:
        flash('Please fill the required fields')
        return redirect(url_for('login_admin'))
    
    user=User.query.filter_by(uname=username).first()
    
    if not user or User.query.filter_by(uname=username).first().role!="admin":
        flash('Please check your username and try again or go to User login.')
        return redirect(url_for('login_admin'))
    if not user.check_password(password):
        flash('Please check your password and try again.')
        return redirect(url_for('login_admin'))
    if user and User.query.filter_by(uname=username).first().role=="admin":
        #after successful login   
        session['user_id']=user.userid
        return redirect(url_for('admin_dashboard'))
    
    return redirect(url_for('login_admin'))


@app.route('/logout')
def logout():
    session.pop('user_id',None)
    return redirect(url_for('login'))


# new user registration page
@app.route('/register')
def register():
    return render_template('login_register/register.html',nav="register")


# new user registration post
@app.route('/register',methods=["POST"])
def register_post():
    username=request.form.get('username')
    password=request.form.get('password')
    firstname=request.form.get('firstname')
    lastname=request.form.get('lastname')
    email=request.form.get('email')
    phone=request.form.get('phone')
    address=request.form.get('address')

    if username is None or password is None or email is None :
        flash('Please fill the required fields')
        return redirect(url_for('register'))
    if len(phone)!=10:
        flash('Please check your phone number')
        return redirect(url_for('register'))
    
    if User.query.filter_by(uname=username).first():
        flash('Username already exists')
        return redirect(url_for('register'))
    
    try:
        def user(username, password, role="user",Profileid=None):
            return User(uname=username,password=password,profileid=Profileid,role=role)
    
        profile = Profile(firstname=firstname, lastname=lastname, email=email, phone=phone, address=address)
        db.session.add(profile)
        db.session.commit()

        pid = Profile.query.filter_by(firstname=firstname, lastname=lastname, email=email, phone=phone, address=address).first().profileid

        user=user(username,password,Profileid=pid)
        db.session.add(user)
        db.session.commit()

        flash(['You have successfully registered','success'])

    except SQLAlchemyError as e:
        db.session.rollback()
        flash('Registration failed. Please try again.', 'error')
    
    return redirect(url_for('login'))



