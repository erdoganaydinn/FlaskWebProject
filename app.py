from functools import wraps
from matplotlib.pyplot import connect
from requests import Session
from sympy import false, not_empty_in
from flask import Flask,render_template,redirect,url_for,request,url_for,session,flash,make_response
import hashlib
from werkzeug.utils import secure_filename
import os
import random
from connectmysql import connectMysql,Functions

app = Flask(__name__)


func = Functions()

loadingFile = "./static/"
app.config['UPLOAD_FOLDER'] = loadingFile
app.config["SECRET_KEY"] = "SBAKJFBDASKJFKJAFDKJSDABFKJ"

mysql = connectMysql(database = "flaskProje")
results =mysql.selectValue(table = "cars",whereColumns=["isReady"],whereValues=[2])

def splitCarsForAdminPage():

    mysql = connectMysql(database = "flaskProje")
    result =mysql.selectValue(table = "cars")
    cars0 = []
    cars1 = []
    cars2 = [] 
    cars3 = []
    for i in result:
        if i[11] == 0:
            cars0.append(i)
        elif i[11] == 1 :
            cars1.append(i)
        elif i[11] == 2:
            cars2.append(i)
        else:
            cars3.append(i)
    return cars0,cars1,cars2,cars3

def getUsersForAdminPage():

    mysql = connectMysql(database = "flaskProje")
    result = mysql.selectValue(table="USERS",
                               whereColumns=["isAdmin"],
                               whereValues=[0])
    
    return result


###########         Decoraters         ###########

def signin(func):
    @wraps(func)
    def decorator(*args,**kwargs):
        if session["id"] != "":
            return func(*args,**kwargs)
        return render_template("mainPage.html",
                               content = "Lütfen önce giriş yapınız...",
                               type = "danger",
                               results = results)       
    return decorator


def signout(func):
    @wraps(func)
    def decorator(*args,**kwargs):
        if session["id"] != "":
            return render_template("mainPage.html",
                                   content="Lütfen önce çıkış yapınız...",
                                   type="danger",
                                   results = results)
        return func(*args,**kwargs)
    
    return decorator


def isAdmin(func):
    @wraps(func)
    def decorator(*args,**kwargs):
        if session["isAdmin"] != True:
            return render_template("mainPage.html",
                                   content="Bu sayfayı ziyaret etmek için admin olmalısınız...",
                                   type="danger",
                                   results = results)
        return func(*args,**kwargs)
    
    return decorator



@app.route("/")
def mainPage():
    mysql = connectMysql(database="flaskProje")
    results =mysql.selectValue(table = "cars",whereColumns=["isReady"],whereValues=[2])
    return render_template("mainPage.html",results = results)


@app.route("/register",methods = ["GET","POST"])
@signout
def register():
    if request.method == "POST":
        name =request.form["name"]
        surName =request.form["surName"]
        email =request.form["email"]
        nickName = request.form["nickName"]
        password =request.form["password"]
        mysql = connectMysql(database="flaskProje")
        result = mysql.selectValue(table="USERS",whereColumns=["email"],whereValues=[email])
        
        if len(result)>0:
            return render_template("signIn.html",type="warning",content = "Girdiğiniz bilgilerde bir kullanıcı bulundu. Lütfen giriş yapınız.")
        else:
            mysql = connectMysql(database="flaskProje")
            mysql.insertValue(columns = ["name","surName","nickName","email","password","isAdmin"],values = [name,surName,nickName,email,func.passwordEncrypt(password),0],table="USERS")
            return render_template("signIn.html",type = "success",content = "Başarı ile kayıt oldunuz.Lütfen giriş yapınız.")      
    else:
        return render_template("register.html")


@app.route("/signin",methods = ["GET","POST"])
@signout
def signIn():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        mysql = connectMysql(database="flaskProje")
        result =mysql.selectValue(table = "USERS",
                                  columns = ["id","nickName","isAdmin"],
                                  whereColumns=["email","password"],
                                  whereSigns=["=","="],
                                  whereValues=[email,func.passwordEncrypt(password)])
        if len(result)>0:
            session["id"] = result[0][0]
            session["nickName"] = result[0][1]

            if int(result[0][2]) == 1 :
                session["isAdmin"] = True
            mysql = connectMysql(database = "flaskProje")
            results =mysql.selectValue(table = "cars",whereColumns=["isReady"],whereValues=[2])
            return render_template("mainPage.html",type = "success",content = "Başarı ile giriş yaptınız..",results = results)
        else:
            return render_template("signIn.html",type = "danger",content = "Böyle bir kullanıcı bulunamadı.Lütfen tekrar deneyiniz.")
    else:
        return render_template("signIn.html")

@app.route("/account",methods = ["GET","POST"])
@signin
def account():
    if request.method == "POST":
        name =request.form["name"]
        surName =request.form["surName"]
        email =request.form["email"]
        nickName = request.form["nickName"]
        password =request.form["password"]
        mysql = connectMysql(database = "flaskProje")
        mysql.updateValue(table = "USERS",changeColumnsName=["name","surName","nickName","email","password"],
        changeValuesName=[name,surName,nickName,email,password],columns=["id"],values =[session["id"]])
        mysql2 = connectMysql(database="flaskProje")
        value = mysql2.selectValue(table = "USERS",whereColumns=["id"],whereValues=[session["id"]])
        return render_template("account.html",type = "success",content = "Bilgiler Başarıyla güncellendi.",value = value[0])
    else:
        mysql = connectMysql(database="flaskProje")
        value = mysql.selectValue(table = "USERS",whereColumns=["id"],whereValues=[session["id"]])
        return render_template("account.html",value =value[0])


@app.route("/mycar",methods =["GET","POST"])
@signin
def myCar():
    if request.method == "POST":

        mysql = connectMysql(database = "flaskProje")
        result = mysql.selectValue(table ="cars",whereColumns=["userId"],whereValues = [session["id"]])
        brand = request.form["brand"]
        model = request.form["model"]
        year = request.form["year"]
        km = request.form["km"]
        damageRecord = request.form["damageRecord"]
        usageTime = request.form["usageTime"]
        explanation = request.form["explanation"]
        photo = request.files["photo"]
        price = request.form["price"]
        filename = secure_filename(photo.filename)
        filename = func.changeName(file = filename,name = session["id"],number = 1)
        photo.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
        picture = app.config["UPLOAD_FOLDER"]+filename
        if len(result) == 0:
            mysql = connectMysql(database = "flaskProje")
            mysql.insertValue(columns=["userId","brand","model","year","km","damageRecord","explanation","usageTime","photo","price"],
                         values=[session["id"],brand,model,year,km,damageRecord,explanation,usageTime,picture,price],
                         table = "cars")
        else:
            mysql = connectMysql(database = "flaskProje")
            mysql.updateValue(changeColumnsName=["brand","model","year","km","damageRecord","explanation","usageTime","photo","price"],
                              changeValuesName=[brand,model,year,km,damageRecord,explanation,usageTime,picture,price],
                              columns = ["userId"],
                              values=[session["id"]],
                              table = "cars")
        return redirect(url_for("myCar"))
            
    else :
        mysql =connectMysql(database = "flaskProje")
        result = mysql.selectValue(table = "cars",
                                   whereColumns=["userId"],
                                   whereValues=[session["id"]])
        if len(result) !=0:
            mysql= connectMysql(database = "flaskProje")
            result = mysql.selectValue(table ="cars",
                                    columns = ["*"],
                                    whereColumns=["userId"],
                                    whereValues=[session["id"]])

            if result[0][11] == 1 :
                return render_template("mycar.html",result= result[0],type="warning",content ="Araç satış işleminiz henüz onaylanmadı...")
            elif result[0][11] == 2 :
                return render_template("mycar.html",result= result[0],type="success",content ="Aracınız satışa çıkarıldı...")
            else:
                return render_template("mycar.html",result= result[0])
        else:
            return render_template("mycar.html")


@app.route("/sellcar",methods = ["GET","POST"])
@signin
def sellCar():

    if request.method == "POST":
        mysql = connectMysql(database ="flaskProje")
        mysql.updateValue(changeColumnsName=["isReady"],
                          changeValuesName=[1],
                          columns=["userId"],
                          values = [session["id"]],
                          table = "cars")
        return redirect(url_for("myCar"))
    
    else:
        return render_template("sellCar.html")

@app.route("/cancelcarsale",methods = ["GET","POST"])
@signin
def cancelCarSale():
    if request.method == "POST":
        mysql = connectMysql(database ="flaskProje")
        mysql.updateValue(changeColumnsName=["isReady"],
                          changeValuesName=[0],
                          columns=["userId"],
                          values = [session["id"]],
                          table = "cars")
        return redirect(url_for("myCar"))
    else:
        return render_template("cancelCarSale.html")

@app.route("/soldcarproccess",methods = ["GET","POST"])
@signin
def soldCarProccess():
    if request.method == "POST":
        mysql = connectMysql(database ="flaskProje")
        mysql.updateValue(changeColumnsName=["isReady"],
                          changeValuesName=[3],
                          columns=["userId"],
                          values = [session["id"]],
                          table = "cars")
        return redirect(url_for("myCar"))
    
    else:
        return render_template("soldCarProccess.html")

@app.route("/car/<string:id>")
def car(id):
    mysql = connectMysql(database = "flaskProje")
    result = mysql.selectValue(table = "cars",
                               whereColumns=["id"],
                               whereValues=[id])
    return render_template("car.html",result = result[0])


@app.route("/cancel")
@signin
def cancel():
    return redirect(url_for("myCar"))


@app.route("/soldcars")
def soldCars():
    mysql = connectMysql(database="flaskProje")
    results =mysql.selectValue(table = "cars",whereColumns=["isReady"],whereValues=[3])
    return render_template("soldcars.html",results = results)

@app.route("/newest")
def newest():
    mysql = connectMysql(database = "flaskProje")
    results = mysql.selectValue(table="cars",
                               whereColumns=["CURRENT_DATE-date","isReady"],
                               whereSigns=["<","="],
                               whereValues=[30,2])

    return render_template("newest.html",results = results)



###########   Changing Password Functions   ###########

@app.route("/changingpasswordOne",methods = ["GET","POST"])
@signout
def changePassword():
    if request.method == "POST":
        email = request.form["email"]
        mysql = connectMysql(database = "flaskProje")
        result = mysql.selectValue(table = "USERS",
                                   whereColumns=["email"],
                                   whereValues=[email])
        if len(result)>0:
            attributes = ["Ad","Soyad","Kullanıcı adı"]
            values = [result[0][1],result[0][2],result[0][3]]
            value = round(random.random()*2)
            return render_template("changingPasswordTwo.html",attribute = attributes[value],value = values[value])
        else:
            return render_template("changingPasswordOne.html",
                                   type = "warning",
                                   content = "Girilen email adresi bulunamadı . Lütfen geçerli bir email giriniz...")
    else:
        return render_template("changingPasswordOne.html")


@app.route("/changingpasswordTwo",methods = ["GET","POST"])
@signout
def changePasswordTwo():
    if request.method == "POST":
        result = request.form["result"]
        attribute = request.form["attribute"]
        value = request.form["value"]
        if result == value:
            return render_template("changingPasswordThree.html",attribute = attribute,value = value)
        else:
            return render_template("changingPasswordOne.html",
                                    type = "warning",
                                    content = "Girdiğiniz "+ attribute+" değeri bulunamadı .Lütfen tekrar deneyiniz")
    else:
        return render_template("changingPasswordTwo.html")

@app.route("/changingPasswordThree",methods = ["GET","POST"])
@signout
def changingPasswordThree():
    if request.method == "POST":
        attribute = request.form["attribute"]
        value = request.form["value"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if password == password2:
            attributes = ["Ad","Soyad","Kullanıcı adı"]
            values = ["name","surName","nickName"]
            for i in range(len(attributes)-1):
                if attributes[i] == attribute:
                    attribute = values[i]
            mysql = connectMysql(database = "flaskProje")    
            mysql.updateValue(table = "USERS",
                              changeColumnsName = ["password"],
                              changeValuesName = [func.passwordEncrypt(password)],
                              columns = [attribute],
                              values = [value])
            
            return render_template("signIn.html",
                                   type = "success",
                                   content = "Şifreniz başarıyla değiştirildi . Lütfen giriş yapınız ...")
        else:
            return render_template("changingPasswordOne.html",
                                   type = "warning",
                                   content = "Girdiğiniz şifreler uyuşmuyor . Lütfen tekrar deneyiniz...")
    else:
        return render_template("changingPasswordThree.html")


@app.route("/changedpassword",methods = ["GET","POST"])
@signin
def changedPassword():

    mysql= connectMysql(database = "flaskProje")
    result = mysql.selectValue(table ="cars",
                               columns = ["*"],
                               whereColumns=["userId"],
                               whereValues=[session["id"]])

    if request.method == "POST":
        password = request.form["password"]
        password2 = request.form["password2"]     
        if password == password2:
            
            mysql = connectMysql(database = "flaskProje")
            if(mysql.updateValue(table = "USERS",
                                changeColumnsName=["password"],
                                changeValuesName=[func.passwordEncrypt(password)],
                                columns=["id"],
                               values = [session["id"]])):
                mysql = connectMysql(database="flaskProje")
                value = mysql.selectValue(table = "USERS",
                                          whereColumns=["id"],
                                          whereValues=[session["id"]])

                return render_template("account.html",
                                       value = value[0],
                                       type = "success",
                                       content ="Şifreniz başarıyla değiştirildi")
            
            else:
                mysql = connectMysql(database="flaskProje")
                value = mysql.selectValue(table = "USERS",
                                          whereColumns=["id"],
                                          whereValues=[session["id"]])
                
                return render_template("account.html",
                                       value = value[0],
                                       type = "danger",
                                       content ="Şifreniz değiştirilemedi . Lütfen tekrar deneyiniz...")
        else:
            mysql = connectMysql(database="flaskProje")
            value = mysql.selectValue(table = "USERS",
                                      whereColumns=["id"],
                                      whereValues=[session["id"]])

            return render_template("account.html",
                                       value = value[0],
                                       type = "danger",
                                       content ="Girdiğiniz şifreler uyuşmuyor . Lütfen tekrar deneyiniz...")
    else:    
        return render_template("changedPassword.html")

@app.route("/admin")
@isAdmin
def admin():

    cars0,cars1,cars2,cars3 = splitCarsForAdminPage()
    users = getUsersForAdminPage()
    return render_template("admin.html",cars0 = cars0,cars1 = cars1,cars2 = cars2,cars3 = cars3,users = users)

@app.route("/admincarproccess<string:id>",methods = ["GET","POST"])
@isAdmin
def adminCarProccess(id):
    if request.method == "POST":
        pass
    else:
        mysql = connectMysql(database = "flaskProje")
        mysql.selectValue(table = "cars",
                          whereColumns=["id"],
                          whereValues=[id])
        
        return render_template("adminCarProccess.html")


@app.route("/admin/car/<string:id>")
@isAdmin
def adminCarDetail(id):
    mysql = connectMysql(database = "flaskProje")
    result = mysql.selectValue(table = "cars",
                               whereColumns=["id"],
                               whereValues=[id])
    return render_template("adminCar.html",result = result[0])


@app.route("/goesOnSale/<string:id>",methods = ["GET","POST"])
@isAdmin
def goesOnSale(id):
    mysql = connectMysql(database = "flaskProje")
    mysql.updateValue(table = "cars",
                      changeColumnsName=["isReady"],
                      changeValuesName= [2],
                      columns= ["id"],
                      values =  [id])
    
    cars0,cars1,cars2,cars3 = splitCarsForAdminPage()
    users = getUsersForAdminPage()
    return render_template("admin.html",
                           cars0 = cars0,
                           cars1 = cars1,
                           cars2 = cars2,
                           cars3 = cars3,
                           users = users,
                           type = "success",
                           content = "Araç satış onayı başarıyla gerçekleşti")


@app.route("/revokeOnSale/<string:id>",methods = ["GET","POST"])
@isAdmin
def revokeOnSale(id):
    mysql = connectMysql(database = "flaskProje")
    mysql.updateValue(table = "cars",
                      changeColumnsName=["isReady"],
                      changeValuesName= [1],
                      columns= ["id"],
                      values =  [id])
    cars0,cars1,cars2,cars3 = splitCarsForAdminPage()
    users = getUsersForAdminPage()
    return render_template("admin.html",
                           cars0 = cars0,
                           cars1 = cars1,
                           cars2 = cars2,
                           cars3 = cars3,
                           users = users,
                           type = "success",
                           content = "Araç satış iptal onayı başarıyla gerçekleşti")


@app.route("/admin/getusers/<string:id>",methods = ["GET","POST"])
@isAdmin
def getUsers(id):
    if request.method == "POST":
        print(id)
        mysql = connectMysql(database = "flaskProje")
        mysql2 = connectMysql(database = "flaskProje")
        
        mysql.deleteValue(table = "cars",
                          params = ["userId"],
                          values =[id])
        
        mysql2.deleteValue(table = "USERS",
                          params=["id"],
                          values=[id])
        
        cars0,cars1,cars2,cars3 = splitCarsForAdminPage()
        users = getUsersForAdminPage()
        return render_template("admin.html",
                            cars0 = cars0,
                            cars1 = cars1,
                            cars2 = cars2,
                            cars3 = cars3,
                            users = users,
                            type = "success",
                            content = "Kullanıcı silme işlemi başarıyla gerçekleşti ...")
    else:
        mysql = connectMysql(database = "flaskProje")
        result =mysql.selectValue(table = "USERS",
                                  whereColumns=["id"],
                                  whereValues=[id])
        return render_template("adminUsers.html",user =result[0])


@app.route("/logout")
@signin
def logOut():
    session["id"] = ""
    session["nickName"] = ""
    session["isAdmin"] = False 
    return render_template("mainPage.html",results = results)



@app.errorhandler(Exception)
def handle_exception(e):
    return render_template("error.html",
                           type="danger",
                           content = "Beklenmeyen bir hata oluştu . Lütfen tekrar deneyiniz...")


if __name__ == "__main__":
    app.run(debug=True)
