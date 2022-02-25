from flask import Flask, render_template, request,redirect,url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, LoginManager, login_user, logout_user, current_user
from forms import Login, Participation
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///work.db"
app.config["SECRET_KEY"] = "MOLUTBA"
db = SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)


class Names(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    password = db.Column(db.Text,nullable=False)

    def __repr__(self):
        return f"{id}"

class Auto(db.Model,UserMixin):
    user_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text,nullable=False)
    cookies = db.Column(db.Text,nullable=False)
    proxy = db.Column(db.Text,nullable=True)
    UserAgent = db.Column(db.Text,nullable=True)



@login_manager.user_loader
def use(user_id):
    return Names.query.get(user_id)






@app.route('/control',methods=["POST","GET"])
@login_required
def cont():
    info = Auto.query.filter(Auto.name==current_user.name).first()
    if info:
        return render_template('control.html',user=info)

    else:
        return redirect(url_for('cont_rep'))



@app.route('/control-replace',methods=["POST","GET"])
@login_required
def cont_rep():
    part = Participation()
    info = Auto.query.filter(Auto.name==current_user.name).first()
    if info:
        print("fkkfjdkfodjsfsddssddf")
        if part.validate_on_submit():
            info.cookies = part.cookies.data
            info.proxy = part.proxy.data
            info.UserAgent = part.UserAgent.data
            db.session.commit()
            return redirect(url_for("cont"))

    else:
        if part.validate_on_submit():
            cookies = part.cookies.data
            proxy = part.proxy.data
            useragent = part.UserAgent.data
            new_data = Auto(name=current_user.name,cookies=cookies,proxy=proxy,UserAgent=useragent)
            db.session.add(new_data)
            db.session.commit()
            return redirect(url_for("cont"))
    return render_template('control-replace.html',part=part)





@app.route("/authorization",methods=["POST","GET"])
def auth():
    form = Login()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        user = Names.query.filter(Names.name==name,Names.password==password).first()
        if user:
            login_user(user)
            return redirect(url_for('cont'))
        else:
            flash("Такого пользователя нет!")



    return render_template("authorization.html",form=form,r="reg",name='Страница авторизации')


@app.route("/register",methods=["POST","GET"])
def reg():
    form = Login()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        if Names.query.filter(Names.name==name).first():
            flash("Такой пользователь уже есть!")
        else:
            new_user = Names(name=name,password=password)
            db.session.add(new_user)
            db.session.commit()
            user = Names.query.filter(Names.name==name,Names.password==password).first()
            login_user(user)
            return redirect(url_for("cont"))
    return render_template("authorization.html",form=form,r='auth',name="Страница регистрации")

@app.route('/logout')
def log():
    logout_user()
    return redirect(url_for('reg'))

@app.route("/")
def index():
    if current_user.is_anonymous:
        return redirect(url_for("auth"))
    else:
        return 'top'





app.run(debug=True)