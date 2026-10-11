from flask import Flask,render_template,request,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)

#DB config

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key ='chamundinagar'


db=SQLAlchemy(app)


class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),unique=True,nullable=False)
    email =db.Column(db.String(100),nullable=False)
    age=db.Column(db.Integer,nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)


    def  __repr__(self):
        return f'<User {self.username}'


@app.route('/')
def start():
    return redirect(url_for('login'))
@app.route('/login',methods=["GET","POST"])
def login():
    if(request.method=="POST"):
        username=request.form.get('username')
        password=request.form.get('password')
        if(username == "huzaif" and password== "password"):
            session["user"] = username
            return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/home')
def home():
    users=Users.query.all() #OR SELECT * FROM users //stores everyrow in users
    return render_template('home.html',users=users,filtered_users=None)

@app.route('/add_user',methods=["GET","POST"])
def add_user():
    if(request.method == "POST"):
        username=request.form.get('username')
        email=request.form.get('email')
        age=request.form.get('age')
        new_user = Users(username=username,email=email,age=age)


        #add to database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('add_user.html')


@app.route('/update/<int:id>',methods=["GET","POST"])
def update(id):
    user=Users.query.get(id)
    if(request.method == "POST"):
        user.username=request.form.get('username')
        user.email=request.form.get('email')
        user.age=request.form.get('age')

        db.session.commit()
        return redirect(url_for('home'))
    return render_template('update_user.html',user=user)


@app.route('/delete/<int:id>',methods=["GET","POST"])
def delete(id):
    if(request.method == "POST"):
        user=Users.query.get(id)
        db.session.delete(user)
        db.session.commit()

        return redirect(url_for("home"))



@app.route('/filter',methods=["GET","POST"])
def filter():
    users=Users.query.all()
    if(request.method =="POST"):
        option=request.form.get('filter')
        print(option)
        if(option == "lessthan"):

            filtered_users=Users.query.filter(Users.age <18).all()

        elif (option == "greaterthan"):
            filtered_users=Users.query.filter(Users.age >=18).all()
        else:
            filtered_users=None
        return render_template('home.html',users=users,filtered_users=filtered_users)
    return render_template('home.html',filtered_users=None)


@app.route('/logout')
def logout():
    session.pop("user")
    return redirect(url_for('login'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)

    