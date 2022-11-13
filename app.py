import os

from flask import render_template, request, redirect, url_for, session, g, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import app, db, Users, Employee


port = int(os.environ.get('PORT', 5000))


@app.teardown_appcontext
def close_database(error):
    if hasattr(g, 'employeeapplication'):
        g.employeeapplication.close()


@app.before_first_request
def create_tables():
    db.create_all()


def get_current_user():
    user = None
    if 'user' in session:
        user = session['user']
        user_cur = Users.query.filter_by(name=user)
        user = user_cur.first()
    return user


def check_admin():
    isAdmin = False
    if 'user' in session:
        isAdmin = session['isAdmin']
    return isAdmin


@app.route('/')
def index():
    user = get_current_user()
    max_projects = Employee.query.order_by(Employee.total_projects.desc()).first()
    max_testcase = Employee.query.order_by(Employee.total_test_case.desc()).first()
    max_bughunter = Employee.query.order_by(Employee.total_defect_found.desc()).first()

    return render_template('index.html', user=user, max_projects=max_projects, max_testcase=max_testcase,
                           max_bughunter=max_bughunter)


@app.route('/register', methods=["POST", "GET"])
def register():
    user = get_current_user()

    if request.method == 'POST':
        name = request.form['name']
        password1 = request.form['password1']
        password2 = request.form['password2']
        if password1 != password2:
            return render_template('register.html', registererror="Confirm Password Correctly!")

        # hashing the password using generate_password_hash() method before saving to database
        hashed_password = generate_password_hash(password1)
        existing_user = Users.query.filter_by(name=name).first()

        # if same user id exits before showing username that already exists
        if existing_user:
            return render_template('register.html', registererror="Username already taken, try different username")

        new_user = Users(name=name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('register.html', user=user)


@app.route('/login', methods=["POST", "GET"])
def login():
    user = get_current_user()
    error = None

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user_cursor = Users.query.filter_by(name=name)
        user = user_cursor.first()

        if user:
            if check_password_hash(user.password, password):
                session['user'] = user.name
                session['isAdmin'] = user.admin
                return redirect(url_for('dashboard'))
            else:
                error = "Username or Password did not match"

        else:
            error = "Please register first"
    return render_template('login.html', loginerror=error, user=user)


@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    all_emp = Employee.query.all()
    return render_template('dashboard.html', user=user, all_emp=all_emp)


@app.route('/addnewemp', methods=["POST", "GET"])
def addnewemp():
    user = get_current_user()
    is_admin = check_admin()
    if not is_admin:
        return render_template('addNewEmployee.html', user=user,error="You don't have admin permission")
    if request.method == "POST":
        name = request.form['name']
        name = name.strip()
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        new_emp = Employee(name=name, email=email, phone=phone, address=address)
        db.session.add(new_emp)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('addNewEmployee.html', user=user)


@app.route('/singleemp/<int:empid>')
def singleemp(empid):
    user = get_current_user()
    emp_cur = Employee.query.filter_by(empid=empid)
    single_emp = emp_cur.first()
    return render_template('singleEmployeeProfile.html', user=user, single_emp=single_emp)


@app.route('/fetchone/<int:empid>')
def fetchone(empid):
    user = get_current_user()
    is_admin = check_admin()
    if not is_admin:
        return render_template('updateEmployee.html', user=user, error="You don't have update permission")
    else:
        emp_cur = Employee.query.filter_by(empid=empid)
        single_emp = emp_cur.first()
        return render_template('updateEmployee.html', user=user, single_emp=single_emp)


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

        current_emp = Employee.query.filter_by(empid=empid).first()

        current_emp.name = name.strip()
        current_emp.email = email
        current_emp.phone = phone
        current_emp.address = address
        current_emp.total_projects = total_projects
        current_emp.total_test_case = total_test_case
        current_emp.total_defect_found = total_defect_found
        current_emp.total_defects_pending = total_defects_pending

        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('updateEmployee.html', user=user)


@app.route('/deleteemp/<int:empid>', methods=["GET", "POST"])
def deleteemp(empid):
    user = get_current_user()
    is_admin = check_admin()

    if request.method == "GET":
        if not is_admin:
            print("You don't have admin permission")
            return render_template('dashboard.html', error="You don't have admin permission")
        else:
            data = Employee.query.get(empid)
            db.session.delete(data)
            db.session.commit()
            return redirect(url_for('dashboard'))
    return render_template('dashboard.html', user=user)


@app.route('/logout')
def logout():
    # session.pop('user', None)
    session.clear()
    return render_template('index.html', user=None)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
