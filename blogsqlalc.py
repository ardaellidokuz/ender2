from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from passlib.hash import sha256_crypt
from wtforms import Form,StringField,TextAreaField,validators,PasswordField,BooleanField,RadioField
from datetime import datetime
app = Flask(__name__)
app.secret_key="eellidokuz"
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/arda/Desktop/blog/blog.db'
db = SQLAlchemy(app)


class hastalar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cinsiyet = db.Column(db.String(5))
    yas = db.Column(db.Integer)
    risk= db.Column(db.Float)
    tarih = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,)




class hastaform(Form):
    yas=StringField("Yaşınızı Girin",validators=(validators.DataRequired(),))
    cinsiyet=RadioField("Cinsiyetinizi Seçin", choices=["Kadın","Erkek"],validators=(validators.DataRequired(),))
    alkol=BooleanField('Alkol Kullanıyorum')
    kahve=BooleanField('Kahve Kullanıyorum')
    sut=BooleanField('Süt ve Süt Ürünleri Tüketiyorum')
    mvit=BooleanField('Multivitamin Takviyesi Alıyorum')
    lif=BooleanField('Lifli Gıdaları Bol Tüketiyorum')
    balik=BooleanField('Balık Tüketiyorum')
    et=BooleanField('İşlenmiş Et (sucuk,sosis) Tüketiyorum')
    diyabet=BooleanField('Diyabet Hastasıyım')
    demir=BooleanField('Demir İçeren (yumurta,kuru üzüm,kırmızı et) Maddeler Tüketiyorum')
    zinco=BooleanField('Çinko Takviyesi Alıyorum')
    sigara=BooleanField('Sigara İçiyorum')
@app.route("/hakkımda")
def hakkımnda():
    return render_template("hakkımda.html")
@app.route("/")
def index():
    return render_template("anasayfa.html")
@app.route("/iletisim")
def iletisim():
    return render_template("iletisim.html")
@app.route("/akademik")
def akademik():
    return render_template("akademik.html")
@app.route("/tarama_testi",methods=["GET","POST"])
def tarama_testi():
    form=hastaform(request.form)
    if request.method=="POST" and form.validate():
        a=0
        c=0
        yas=int(form.yas.data)
        cinsiyet=form.cinsiyet.data
        if form.alkol.data:
            a+=1.36
            c+=1
        if form.kahve.data:
            a+=0.95
            c+=1
        if form.sut.data:
            a+=0.4
            c+=1
        if form.mvit.data:
            a+=0.7
            c+=1
        if form.lif.data:
            a+=0.53
            c+=1
        if form.balik.data:
            a+=0.69
            c+=1
        if form.et.data:
            a+=1.24
            c+=1
        if form.diyabet.data:
            a+=1.38
            c+=1
        if form.demir.data:
            a+=0.24
            c+=1
        if form.zinco.data:
            a+=0.4
            c+=1
        if form.sigara.data:
            a+=1.18
            c+=1
        if form.cinsiyet.data=="Kadın":
            if a+c==0:
                b=(4/100)*1
            else:
                b=(4/100)*(a/c)
        if form.cinsiyet.data=="Erkek":
            if a+c==0:
                b=(4.3/100)*1
            else:
                b=(4.3/100)*(a/c)
        mydb=hastalar(cinsiyet=cinsiyet,yas=yas,risk=b)
        db.session.add(mydb)
        db.session.commit()
        flash("Risk Değeriniz:  "+str(round(b,4)*100)+"%","success")
        return redirect(url_for("index"))
    else:
        return render_template("tarama.html",form=form)
if __name__ =="__main__":
    db.create_all()
    app.run(debug=True)

