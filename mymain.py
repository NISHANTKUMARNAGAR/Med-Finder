from flask import Flask,render_template,request,redirect,url_for,session
from dep_in import *
from werkzeug.utils import secure_filename
import time
import os


app=Flask(__name__)
app.config['UPLOAD_FOLDER']='./static/photos'
app.secret_key="super secret key"


#public page templates
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/record",methods=["GET","POST"])
def record():
    if(request.method=="POST"):
        madicinename=request.form["t1"]
        cur=make_connection()
        sql="select * from medicine_medical_info where name='"+madicinename+"'"
        cur.execute(sql)
        result=cur.fetchall()
        return render_template("record.html",result=result,name=madicinename)
    else:
        return render_template("record.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if(request.method=="POST"):
        email=request.form["f1"]
        ps=request.form["f2"]
        cur=make_connection()
        sql="select * from logindata where email='"+email+"' AND password='"+ps+"'"
        cur.execute(sql)
        n=cur.rowcount
        if(n>0):
            #create cookie
            data=cur.fetchone()
            usertype=data[2]
            session["usertype"]=usertype
            session["email"]=email
            if(usertype=="admin"):
                return redirect(url_for("adminhome"))
            elif(usertype=="medical"):
                return redirect(url_for("medicalhome"))
            else:
                return render_template("lg.html",msg="invalid usertype,contact to admin")
        else:
            return render_template("lg.html",msg="either user id or password is incorrect")
    else:
        return render_template("lg.html")


@app.route("/adminhome",methods=["GET","POST"])
def adminhome():
    if("usertype" in session):
        usertype=session["usertype"]
        email=session["email"]
        if(usertype=="admin"):
            name=getadminname(email)
            return render_template("adminhome.html",name=name)
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


#admin photo upload
@app.route("/adminphotoupload",methods=["GET","POST"])
def adminphotoupload():
    if('usertype' in session):
        usertype = session["usertype"]
        email = session["email"]
        if(usertype == "admin"):
            if(request.method == "POST"):
                file = request.files["f1"]
                if(file):
                    path = os.path.basename(file.filename)
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time())) + "." + file_ext
                    filename = secure_filename(filename)
                    cur = make_connection()
                    sql = "insert into photodata values('" + email + "','" + filename + "')"
                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if(n == 1):
                            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                            return render_template("adminphotoupload.html", result="success")
                        else:
                            return render_template("adminphotoupload.html", result="failure")
                    except:
                        return render_template("adminphotoupload.html", result="duplicate")
            else:
                return render_template("adminphotoupload.html")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


#Admin Change photo
@app.route("/changeadminphoto")
def changeadminphoto():
    if("usertype" in session):
        usertype=session["usertype"]
        email=session["email"]
        if(usertype=="admin"):
            photo=checkphoto(email)
            cur=make_connection()
            sql="delete from photodata where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                os.remove("./static/photos/"+photo)
                return render_template("changeadminphoto.html",data="success")
            else:
                return render_template("changeadminphoto.html", data="failure")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route("/medicalform",methods=["GET","POST"])
def medicalform():
    if ("usertype" in session):
        usertype = session["usertype"]
        if (usertype == "admin"):
            if(request.method=="GET"):
                print("get method recognized")
                return render_template("medicalregistration.html")
            elif(request.method=="POST"):
                print("post method recognized")
                medname=request.form["f1"]
                owner=request.form["f2"]
                licno=request.form["f3"]
                address=request.form["f4"]
                contact=request.form["f5"]
                email=request.form["f6"]
                password=request.form["f7"]
                confpass=request.form["f8"]
                usertype="medical"
                s1="insert into medicaldata values('"+medname+"','"+owner+"','"+licno+"','"+address+"','"+contact+"','"+email+"')"
                s2="insert into logindata values('"+email+"','"+password+"','"+usertype+"')"
                cur=make_connection()
                m=cur.execute(s1)
                n=cur.execute(s2)
                if(n==1 and m==1):
                  s="medical and login data saved"
                elif(n==1):
                  s="only login data saved"
                elif(m==1):
                  s="only medical data saved"
                else:
                  s="error no data saved"
                return render_template("medicalregistration.html",msg=s)
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


@app.route("/editmedical",methods=["GET","POST"])
def editmedical():
    if ("usertype" in session):
        usertype = session["usertype"]
        if (usertype == "admin"):
            if(request.method=="POST"):
                email=request.form["h1"]
                sql="select * from medicaldata where email='"+email+"'"
                cur=make_connection()
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template("editmedical.html",info=data)
                else:
                    return render_template("editmedical.html",msg="error can't fetch data")
            else:
                return redirect(url_for("showm"))
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


@app.route("/editmedical1",methods=["GET","POST"])
def editmedical1():
    if ("usertype" in session):
        usertype = session["usertype"]
        if (usertype == "admin"):
            if(request.method=="POST"):
                medname = request.form["f1"]
                owner = request.form["f2"]
                licno = request.form["f3"]
                address = request.form["f4"]
                contact = request.form["f5"]
                email = request.form["f6"]
                sql = "update medicaldata set name='"+medname+"',owner='"+owner+"',lno='"+licno+"',address='"+address+"',contact='"+contact+"' where email='"+email+"' "
                cur = make_connection()
                m = cur.execute(sql)
                if (m == 1):
                    return render_template("editmedical1.html",msg="Data changes are saved successfully")
                else:
                    return render_template("editmedical.html",msg="Try again")
            else:
                return redirect(url_for("showm"))
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


@app.route("/deletemedical",methods=["GET","POST"])
def deletemedical():
    if ("usertype" in session):
        usertype = session["usertype"]
        if (usertype == "admin"):
            if(request.method=="POST"):
                email=request.form["h2"]
                s1="delete from medicaldata where email='"+email+"'"
                s2="delete from logindata where email='"+email+"'"
                cur=make_connection()
                m=cur.execute(s1)
                n=cur.execute(s2)
                if(n==1 and m==1):
                    s="data deleted from login and medical"
                elif(m==1):
                    s="data deleted from medical"
                elif(n==1):
                    s="data deleted from login"
                else:
                    s="data not deleted"
                return render_template("deletemedical.html", msg=s)
            else:
                return redirect(url_for("showm"))
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


@app.route("/adminpage",methods=["GET","POST"])
def adminpage():
    if("usertype" in session):
        usertype=session["usertype"]
        if(usertype=="admin"):
            if(request.method=="GET"):
                print("get method recognized")
                return render_template("adminregistration.html")
            elif(request.method=="POST"):
                print("post method recognized")
                #collect form data
                name=request.form["f1"]
                address=request.form["f2"]
                contact=request.form["f3"]
                email=request.form["f4"]
                password=request.form["f5"]
                confirmpassword=request.form["f6"]
                usertype="admin"

                #create valid sql command
                s1="insert into admindata values('"+name+"','"+address+"','"+contact+"','"+email+"')"
                s2="insert into logindata values('"+email+"','"+password+"','"+usertype+"')"

                #create cursor
                cur=make_connection()

                #send data to tables
                m=cur.execute(s1)
                n=cur.execute(s2)

                #check response of mysql
                if(m==1 and n==1):
                    s="data saved and login created"
                elif(n==1):
                    s="only data is saved"
                elif(m==1):
                    s="only login is created"
                else:
                    s="error no data saved"

                return render_template("adminregistration.html",msg=s)
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


#admin profile
@app.route("/adminprofile")
def adminprofile():
    if("usertype" in session):
        usertype=session["usertype"]
        if(usertype=="admin"):
            cur=make_connection()
            email=session["email"]
            sql="select * from admindata where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                photo=checkphoto(email)
                data=cur.fetchone()
                return render_template("adminprofile.html",info=data,photo=photo)
            else:
                return render_template("adminprofile.html",msg="no data found", photo="No")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


#admin profile 1 (edit)
@app.route("/adminprofile1",methods=["GET","POST"])
def adminprofile1():
    if("usertype" in session):
        usertype=session["usertype"]
        if(usertype=="admin"):
            if(request.method=="POST"):
                email=session["email"]
                cur=make_connection()
                sql="select * from admindata where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template("adminprofile1.html",info=data)
                else:
                    return render_template("adminprofile1.html",msg="Data Not Found")
            else:
                return redirect(url_for("adminprofile"))
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


@app.route("/adminprofile2",methods=["GET","POST"])
def adminprofile2():
    if("usertype" in session):
        usertype=session["usertype"]
        if(usertype=="admin"):
            if(request.method=="POST"):
                name=request.form["f1"]
                address=request.form["f2"]
                contact=request.form["f3"]
                email=session["email"]
                cur=make_connection()
                sql="update admindata set name='"+name+"',address='"+address+"',contact='"+contact+"' where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("adminprofile2.html",msg="Data Saved")
                else:
                    return render_template("adminprofile2.html",msg="Data Not Saved")
            else:
                return redirect(url_for("adminprofile"))
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


@app.route("/showm")
def showm():
    if("usertype" in session):
        usertype=session["usertype"]
        if(usertype=="admin"):
            sql="select * from medicaldata"
            cur=make_connection()
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchall()
                return render_template("showmedical.html",info=data)
            else:
                return render_template("showmedical.html",msg="no data found")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


#admin change passowrd
@app.route("/adminchangepass",methods=["GET","POST"])
def adminchangepass():
    if("usertype" in session):
        usertype=session["usertype"]
        if(usertype=="admin"):
            if(request.method=="POST"):
                email=session["email"]
                oldpass=request.form["f1"]
                newpass=request.form["f2"]
                cur=make_connection()
                sql="update logindata set password='"+newpass+"' where email='"+email+"' AND password='"+oldpass+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("adminchangepass.html",msg="Change Password")
                else:
                    return render_template("adminchangepass.html",msg="Password Not Changed")
            else:
                return render_template("adminchangepass.html")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


@app.route("/medicalhome",methods=["GET","POST"])
def medicalhome():
    if("usertype" in session):
        usertype=session["usertype"]
        email=session["email"]
        if(usertype=="medical"):
            name=getmedicalname(email)
            return render_template("medicalhome.html",name=name)
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


@app.route("/medicalphotoupload",methods=["GET","POST"])
def medicalphotoupload():
    if("usertype" in session):
        usertype=session["usertype"]
        email=session["email"]
        if(usertype=="medical"):
            if(request.method=="POST"):
                file=request.files["f1"]
                if(file):
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+"."+file_ext
                    filename=secure_filename(filename)
                    cur=make_connection()
                    sql="insert into photodata values('"+email+"','"+filename+"')"
                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if(n==1):
                            file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
                            return render_template("medicalphotoupload.html",result="success")
                        else:
                            return render_template("medicalphotoupload.html",result="failure")
                    except:
                        return render_template("medicalphotoupload.html",result="duplicate")
            else:
                return render_template("medicalphotoupload.html")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


@app.route("/changemedicalphoto")
def changemedicalphoto():
    if("usertype" in session):
        usertype=session["usertype"]
        email=session["email"]
        if(usertype=="medical"):
            photo=checkphoto(email)
            cur=make_connection()
            sql="delete from photodata where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                os.remove("./static/photos/"+photo)
                return render_template("changemedicalphoto.html",data="success")
            else:
                return render_template("changemedicalphoto.html",data="failure")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("autherror"))


@app.route("/medicineinfo",methods=["GET","POST"])
def medicineinfo():
    if("usertype" in session):
        usertype=session["usertype"]
        email=session["email"]
        if(usertype=="medical"):
            if(request.method=="GET"):
                print("Get method invoked")
                return render_template("medicinedata.html")
            elif(request.method=="POST"):
                print("Post method invoked")
                name=request.form["f1"]
                comp=request.form["f2"]
                price=request.form["f3"]
                sql="insert into medicine values(0,'"+name+"','"+comp+"',"+price+",'"+email+"')"
                cur=make_connection()
                n=cur.execute(sql)
                if(n==1):
                    s="medicine data saved"
                else:
                    s="no data saved"
                return render_template("medicinedata.html",msg=s)
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


@app.route("/showmedicineinfo")
def showmedicineinfo():
    if("usertype" in session):
        usertype=session["usertype"]
        email=session["email"]
        if(usertype=="medical"):
            sql="select * from medicine where storeid='"+email+"'"
            cur=make_connection()
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchall()
                return render_template("showmed.html",info=data)
            else:
                return render_template("showmed.html",msg="no data found")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


@app.route("/editmedicineinfo",methods=["GET","POST"])
def editmedicineinfo():
    if ("usertype" in session):
        usertype = session["usertype"]
        if (usertype == "medical"):
            if(request.method=="POST"):
                name=request.form["h1"]
                sql="select * from medicine where name='"+name+"'"
                cur=make_connection()
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template("editmedicineinfo.html",info=data)
                else:
                    return render_template("editmedicineinfo.html",msg="error can't fetch data")
            else:
                return redirect(url_for("showmedicineinfo"))
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


@app.route("/editmedicineinfo1",methods=["GET","POST"])
def editmedicineinfo1():
    if ("usertype" in session):
        usertype = session["usertype"]
        if (usertype == "medical"):
            if(request.method=="POST"):
                name=request.form["f1"]
                comp=request.form["f2"]
                price=request.form["f3"]
                sql="update medicine set company='"+comp+"',price="+price+" where name='"+name+"'"
                cur=make_connection()
                m=cur.execute(sql)
                if(m==1):
                    return render_template("editmedicineinfo1.html",msg="Data changes are saved")
                else:
                    return render_template("editmedicineinfo1.html",msg="Try again")
            else:
                return redirect(url_for("showmedicineinfo"))
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


@app.route("/deletemedicineinfo",methods=["GET","POST"])
def deletemedicineinfo():
    if ("usertype" in session):
        usertype = session["usertype"]
        if (usertype == "medical"):
            if(request.method=="POST"):
                name=request.form["h2"]
                sql="delete from medicine where name='"+name+"'"
                cur=make_connection()
                m=cur.execute(sql)
                if(m==1):
                    s="data deleted from medicine"
                else:
                    s="data not deleted"
                return render_template("deletemedicineinfo.html",msg=s)
            else:
                return redirect(url_for("showmedicineinfo"))
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


#admin profile
@app.route("/medicalprofile")
def medicalprofile():
    if("usertype" in session):
        usertype=session["usertype"]
        if(usertype=="medical"):
            cur=make_connection()
            email=session["email"]
            sql="select * from medicaldata where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                photo=checkphoto(email)
                data=cur.fetchone()
                return render_template("medicalprofile.html",info=data,photo=photo)
            else:
                return render_template("medicalprofile.html",msg="No Data Found")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


@app.route("/medicalprofile1",methods=["GET","POST"])
def medicalprofile1():
    if("usertype" in session):
        usertype=session["usertype"]
        if(usertype=="medical"):
            if(request.method=="POST"):
                email=session["email"]
                cur=make_connection()
                sql="select * from medicaldata where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template("medicalprofile1.html",info=data)
                else:
                    return render_template("medicalprofile1.html",msg="No Data Found")
            else:
                return redirect(url_for("medicalprofile"))
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


@app.route("/medicalprofile2",methods=["GET","POST"])
def medicalprofile2():
    if("usertype" in session):
        usertype=session["usertype"]
        if(usertype=="medical"):
            if(request.method=="POST"):
                name=request.form["f1"]
                owner=request.form["f2"]
                licno=request.form["f3"]
                address=request.form["f4"]
                contact=request.form["f5"]
                email=session["email"]
                cur=make_connection()
                sql="update medicaldata set name='"+name+"',owner='"+owner+"',lno='"+licno+"',address='"+address+"',contact='"+contact+"' where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("medicalprofile2.html",msg="Data Saved")
                else:
                    return render_template("medicalprofile2.html",msg="Data Not Saved")
            else:
                return redirect(url_for("medicalprofile"))
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


#medical change password
@app.route("/medicalchangepass",methods=["GET","POST"])
def medicalchangepass():
    if("usertype" in session):
        usertype=session["usertype"]
        if(usertype=="medical"):
            if(request.method=="POST"):
                email=session["email"]
                oldpass=request.form["f1"]
                newpass=request.form["f2"]
                cur=make_connection()
                sql="update logindata set password='"+newpass+"' where email='"+email+"' AND password='"+oldpass+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("medicalchangepass.html",msg="Password Changed")
                else:
                    return render_template("medicalchangepass.html",msg="Password Not Changed")
            else:
                return render_template("medicalchangepass.html")
        else:
            return redirect(url_for("autherror"))
    else:
        return redirect(url_for("autherror"))


@app.route("/logout",methods=["GET","POST"])
def logout():
    if("usertype" in session):
        session.pop("usertype",None)
        session.pop("email",None)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


@app.route("/autherror")
def autherror():
    if("usertype" in session):
        return render_template("autherror.html")
    else:
        return redirect(url_for("autherror"))


#main function
if(__name__=="__main__"):
    app.run(debug=True)
