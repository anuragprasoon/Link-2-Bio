from flask import Flask , render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "hello"
SQLALCHEMY_DATABASE_URI = "URI"
#app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_DATABASE_URI"] = "URI"
#app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
cloudinary.config(cloud_name = "USERNAME", api_key = "API KEY", api_secret = "API SECRET")
db = SQLAlchemy(app)

class users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.Text, unique=True)
    password = db.Column(db.String(50))
    about = db.Column(db.String(200))
    fb = db.Column(db.String(100))
    ig = db.Column(db.String(100))
    yt = db.Column(db.Text)
    tw = db.Column(db.String(100))
    dp = db.Column(db.Text)

 
class links(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    title = db.Column(db.String(100))
    link = db.Column(db.Text)


@app.route("/")
def home():
    if 'username' in session:
        return  redirect(url_for('profile'))
    else:
        return render_template("index.html")

@app.route("/old")
def old():
    return render_template("index1.html")
    

@app.route("/create", methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        a = request.form['username']
        me = users.query.filter_by(username=a).first()
        db.session.commit()
        if me == None:
            session['newusername'] = a
            return redirect(url_for("signup"))
        else:
            return render_template("create.html", msg="This Username is already registered")
    return render_template("create.html",msg="")

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if 'newusername' in session:
        a = session['newusername']
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            emailcheck=users.query.filter_by(email=email).first()
            if emailcheck == None:
                newuser = users(username=a, email=email, password=password)
                db.session.add(newuser)
                db.session.commit()
                session['username']=a
                return redirect(url_for('setup'))
            else:
                return render_template('signup.html', a=a, msg="An Account already exist with this Email ID.")
        return render_template("signup.html", msg="", a=a)
    else:
        return redirect(url_for('create'))


@app.route('/setup', methods=['POST', 'GET'])
def setup():
    if 'username' in session:
        u = session['username']
        if request.method == 'POST':
            a = request.form['about']
            f = request.form['fb']
            i = request.form['ig']
            t = request.form['tw']
            y = request.form['yt']
            dp= request.files['dp']
            set1 = users.query.filter_by(username=u).first()
            set1.about = a
            set1.fb = f
            set1.ig = i
            set1.tw = t
            set1.yt = y
            if dp.filename!="":
                profilepic = cloudinary.uploader.upload(request.files['dp'])
                set1.dp = profilepic['url']   
            db.session.commit()
            return redirect(url_for('profile'))
        else:
            info = users.query.filter_by(username=u).first()
            db.session.commit()
            return render_template('setup.html', info=info)
        

@app.route('/editprofile', methods=['POST', 'GET'])
def editprofile():
    if 'username' in session:
        u = session['username']
        if request.method == 'POST':
            a = request.form['about']
            f = request.form['fb']
            i = request.form['ig']
            t = request.form['tw']
            y = request.form['yt']
            dp= request.files['dp']
            set1 = users.query.filter_by(username=u).first()
            set1.about = a
            set1.fb = f
            set1.ig = i
            set1.tw = t
            set1.yt = y
            if dp.filename!="":
                profilepic = cloudinary.uploader.upload(request.files['dp'])
                set1.dp = profilepic['url']   
            db.session.commit()
            return redirect(url_for('profile'))
        else:
            info = users.query.filter_by(username=u).first()
            db.session.commit()
            return render_template('editprofile.html', user=info)

@app.route('/setting', methods=['POST', 'GET'])
def setting():
    if 'username' in session:
        u = session['username']
        if request.method == 'POST':
            f = request.form['fb']
            i = request.form['ig']
            t = request.form['tw']
            y = request.form['yt']
            set1 = users.query.filter_by(username=u).first()
            set1.fb = f
            set1.ig = i
            set1.tw = t
            set1.yt = y
            db.session.commit()
            return redirect(url_for('profile'))
        else:
            info = users.query.filter_by(username=u).first()
            db.session.commit()
            return render_template('setting.html', user=info)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return redirect(url_for('profile'))
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        check = users.query.filter_by(email=email).first()
        db.session.commit()
        if check.password == password:
            session['username'] = check.username
            return redirect(url_for('profile'))
        else:
            return render_template("login.html", msg="E-mail or Password is incorrect")
    else:
        return render_template("login.html", msg="")

@app.route("/profile", methods=['POST', 'GET'])
def profile():
    if 'username' in session:
        u = session['username']
        info = users.query.filter_by(username=u).first()
        lnk = links.query.filter_by(username=u).all()
        db.session.commit()
        return render_template("profile.html", user=info, link=lnk)
    else:
        return redirect(url_for('login'))
    
@app.route("/delete/<url>")
def delink(url):
    if 'username' in session:
        u = session['username']
        deletelink = links.query.filter(links.username == u).filter(links.id == url).first()
        db.session.delete(deletelink)
        db.session.commit()
        return redirect(url_for("profile"))


@app.route("/update/<url>", methods=['POST', 'GET'])
def updatelink(url):
    if 'username' in session:
        u = session['username']
        if request.method == 'POST':
            t = request.form['title']
            ul = request.form['link']
            upd = links.query.filter(links.username == u).filter(links.id == url).first()
            upd.title = t
            upd.link = ul
            db.session.commit()
            return redirect(url_for("profile"))
        else:
            ulink = links.query.filter(links.username == u).filter(links.id == url).first()
            db.session.commit()
            return render_template("updatelink.html", link=ulink)

    
@app.route("/addlink", methods=['POST', 'GET'])
def addlink():
    if 'username' in session:
        u = session['username']
        if request.method == 'POST':
            title1 = request.form['title']
            urlink = request.form['link']
            newlink = links(username=u, title=title1, link=urlink)
            db.session.add(newlink)
            db.session.commit()
            return redirect(url_for('profile'))
        else:
            return render_template("addlink.html")
    else:
        return redirect(url_for('login'))


@app.route("/<username>")
def template(username):
    userinfo = users.query.filter_by(username=username).first()
    link = links.query.filter_by(username=username).all()
    db.session.commit()
    return render_template("biolinktemplate.html", user=userinfo, link=link)


@app.route("/old/<username>")
def oldtemplate(username):
    return render_template("biolinktemplate1.html",user=username)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
