from flask import Flask, render_template, request, redirect, url_for, session, g
from database import get_database
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


@app.teardown_appcontext
def close_database(error):
    if hasattr(g, 'employeeapplication'):
        g.employeeapplication.close()


def get_current_user():
    user = None
    if 'user' in session:
        user = session['user']
        db = get_database()
        user_cur = db.execute('select * from users where name = ?', [user])
        user = user_cur.fetchone()
    return user


@app.route('/')
def index():
    user = get_current_user()
    return render_template('index.html', user=user)


@app.route('/login', methods=["POST", "GET"])
def login():
    user = get_current_user()
    error = None
    db = get_database()

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user_cursor = db.execute('select * from users where name = ?', [name])
        user = user_cursor.fetchone()

        if user:
            if check_password_hash(user['password'], password):
                session['user'] = user['name']
                return redirect(url_for('dashboard'))
            else:
                error = "Username or Password did not match"

        else:
            error = "Please register first"
    return render_template('login.html', loginerror=error, user=user)


@app.route('/register', methods=["POST", "GET"])
def register():
    user = get_current_user()
    db = get_database()

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        registered_users = db.execute('select * from users where name = ?', [name])
        existing_user = registered_users.fetchone()

        if existing_user:
            return render_template('register.html', registererror="Username already taken, try different username")

        db.execute('insert into users (name,password) values (?,?)', [name, hashed_password])
        db.commit()
        return redirect(url_for('index'))

    return render_template('register.html', user=user)


@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    db = get_database()
    emp_cursor = db.execute('select * from emp')
    all_emp = emp_cursor.fetchall()
    return render_template('dashboard.html', user=user, all_emp=all_emp)


@app.route('/addnewemp', methods=["POST", "GET"])
def addnewemp():
    user = get_current_user()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        db = get_database()
        db.execute('insert into emp(name,email,phone,address) values (?,?,?,?)', [name, email, phone, address])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('addnewemployee.html', user=user)


@app.route('/singleemp/<int:empid>')
def singleemp(empid):
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute("select * from emp where empid=?", [empid])
    single_emp = emp_cur.fetchone()
    return render_template('singleemployeeprofile.html', user=user, single_emp=single_emp)


@app.route('/fetchone/<int:empid>')
def fetchone(empid):
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute("select * from emp where empid=?", [empid])
    single_emp = emp_cur.fetchone()
    return render_template('updateemployee.html', user=user, single_emp=single_emp)


@app.route('/update', methods=["POST", "GET"])
def update():
    user = get_current_user()
    if request.method == "POST":
        empid = request.form['empid']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        total_projects = request.form['total_projects']
        total_test_case = request.form['total_test_case']
        total_defect_found = request.form['total_defect_found']
        total_defects_pending = request.form['total_defects_pending']
        db = get_database()
        db.execute('update emp set name=?,email=?,phone=?,address=?,total_projects=?,total_test_case=?,'
                   'total_defect_found=?,total_defects_pending=? where empid=?',
                   [name, email, phone, address, total_projects, total_test_case, total_defect_found, total_defects_pending, empid])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('updateemployee.html', user=user)


@app.route('/deleteemp/<int:empid>', methods=["GET", "POST"])
def deleteemp(empid):
    user = get_current_user()
    if request.method == "GET":
        db = get_database()
        emp_cursor = db.execute('delete from emp where empid = ?', [empid])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', user=user)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('index.html', user=None)


if __name__ == "__main__":
    app.run(debug=True)
