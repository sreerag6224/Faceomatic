from flask import Flask, render_template, request, redirect,url_for,session,abort
from DBConnection import Db
import datetime,random
from datetime import timedelta
from email.mime import image



import os
import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail
app = Flask(__name__)
app.secret_key="fr"
path1="E:\\face\\static\\"

@app.route('/')
def start():
    return render_template("login2.html")
    # return render_template("login2.html")
@app.route('/loginpost',methods=['post'])
def loginpost():
    uname=request.form['textfield']
    passwd = request.form['textfield2']
    db=Db()
    qry=db.selectOne("select * from login where username='"+uname+"' and password='"+passwd+"'")

    if qry is not None:
        type=qry['usertype']
        session['u']=type
        session['lin']='lin'
        if type=='admin':
            return redirect('/admin_home')
        elif type=='hod':
            session['hod_id']=qry['loginid']
            return redirect('/hod_homepage')
        elif type=='staff':
            session['staff_id']=qry['loginid']
            return redirect('/staff_home_page')
        else:
            return "<script>alert('User does not exsist........');window.location='/'</script>"
    else:
        return "<script>alert('User does not exist........');window.location='/'</script>"


@app.route('/admin_home')
def admin_home():
    if session['lin']=='lin':
        if session['u'] != 'admin':
            abort(403)
        # return render_template("Admin/Admin_homepage.html")
        session['username']='Admin'
        return render_template("Admin/Admin_Home.html")
    else:
        return redirect('/')

# ==================================================================================
@app.route('/add_dept')
def add_dept():
    if session['lin'] == 'lin':
        return render_template("Admin/add_department.html")
    else:
        return redirect('/')
@app.route('/dep_post',methods=['post'])
def dep_post():
    if session['lin'] == 'lin':
        db=Db()
        department=request.form['textfield']
        qry=db.insert("insert into dept(dept_name) VALUES('"+department+"')")
        return add_dept()
    else:
        return redirect('/')
@app.route('/view_dept')
def view_dept():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from dept")
        return render_template("Admin/view_department.html",value=qry)
    else:
        return redirect('/')
@app.route('/delete_dept/<i>')
def delete_dept(i):
    db=Db()
    qry=db.delete("delete from dept where dept_id='"+i+"'")
    return view_dept()

# =====================================================================================
@app.route('/add_course')
def add_course():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from dept")
        return render_template("Admin/add_course.html",value=qry)
    else:
        return redirect('/')
@app.route('/course_post',methods=['post'])
def course_post():
    if session['lin'] == 'lin':
        db=Db()
        dept=request.form['select']
        crs=request.form['textfield']
        qry=db.insert("insert into course(dept_id,course_name) values('"+dept+"','"+crs+"')")
        return add_course()
    else:
        return redirect('/')
@app.route('/view_course')
def view_course():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from course,dept where course.dept_id=dept.dept_id")
        return render_template("Admin/view_course.html",value=qry)
    else:
        return redirect('/')
@app.route('/delete_course/<i>')
def delete_course(i):
    if session['lin'] == 'lin':
        db=Db()
        qry=db.delete("delete from course where course_id='"+i+"'")
        return view_course()
    else:
        return redirect('/')
#======================================================================================
@app.route('/add_staff')
def add_staff():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from dept")
        return render_template("Admin/add_staff.html",value=qry)
    else:
        return redirect('/')
@app.route('/staff_post',methods=['post'])
def staff_post():
    if session['lin'] == 'lin':
        db=Db()
        n1=request.form['textfield']
        n2=request.form['textfield2']
        n3=request.form['textfield3']
        n4=request.form['textfield4']
        n5=request.form['textfield5']
        n6=request.form['textfield6']
        n7=request.form['textfield7']
        n8=request.form['textfield8']
        n9=request.form['textfield9']
        img=request.files['fileField']
        dept=request.form['select']
        data = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        img.save(path1+"Staff\\"+data+".jpeg")
        path="/static/Staff/"+data+".jpeg"
        pwd=random.randint(0000,9999)
        print(pwd)
        qry2=db.selectOne("select * from login where username='"+n7+"'")
        if qry2 is None:

            qry=db.insert("insert into login(username,password,usertype) values('"+n7+"','"+str(pwd)+"','staff')")
            print(qry)
            qry1=db.insert("insert into staff(staff_id,s_dept_id,s_name,s_age,s_hname,s_place,s_post,s_pin,s_email,s_phone,qualification,s_images) values('"+str(qry)+"','"+dept+"','"+n1+"','"+n2+"','"+n3+"','"+n4+"','"+n5+"','"+n6+"','"+n7+"','"+n8+"','"+n9+"','"+path+"')")
            try:
                gmail = smtplib.SMTP('smtp.gmail.com', 587)

                gmail.ehlo()

                gmail.starttls()

                gmail.login('facerecognition103@gmail.com', 'kl13an6958')

            except Exception as e:
                print("Couldn't setup email!!" + str(e))

            msg = MIMEText("Your Password is " + str(pwd))

            msg['Subject'] = 'Verification'

            msg['To'] = n7

            msg['From'] = 'facerecognition103@gmail.com'

            try:

                gmail.send_message(msg)

            except Exception as e:

                print("COULDN'T SEND EMAIL", str(e))
            return add_staff()
        else:
            return "ok"
    else:
        return redirect('/')

@app.route('/view_staff')
def view_staff():
    if session['lin'] == 'lin':
        db = Db()
        qry = db.select("select * from staff,dept where staff.s_dept_id=dept.dept_id")
        print(qry)
        id = []
        for i in qry:
            id.append((i['s_dept_id']))
        qry1 = db.select("select * from dept ")
        print(qry1)
        print(id)
        return render_template("Admin/view_staff.html", value1=qry, value2=id, value3=qry1)
    else:
        return redirect('/')
@app.route('/view_staff1/<i>')
def view_staff1(i):
    db=Db()
    qry=db.select("select * from dept,staff where dept.dept_id=staff.s_dept_id and staff.s_dept_id='"+i+"'")

    return render_template("Admin/ajax_staff.html",value1=qry)
@app.route('/update_staff/<id>')
def update_staff(id):
    if session['lin'] == 'lin':
        db=Db()
        qry=db.selectOne("select * from staff where staff_id='"+id+"'")
        qry1=db.select("select * from dept")
        return render_template("Admin/update_staff.html",value1=qry,value2=qry1)
    else:
        return redirect('/')
@app.route('/update_staff_post/<id>',methods=['post'])
def update_staff_post(id):
    if session['lin'] == 'lin':
        db = Db()
        n1 = request.form['textfield']
        n2 = request.form['textfield2']
        n3 = request.form['textfield3']
        n4 = request.form['textfield4']
        n5 = request.form['textfield5']
        n6 = request.form['textfield6']
        n7 = request.form['textfield7']
        n8 = request.form['textfield8']
        n9 = request.form['textfield9']
        pht = request.files['fileField']
        dept = request.form['select']
        if request.files is not None:
            if pht.filename !="":
                data = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                pht.save(path1 + "\\Staff\\" + data + ".jpeg")
                path = "/static/Staff/" + data + ".jpeg"
                qry=db.update("update staff set s_dept_id='"+dept+"',s_name='"+n1+"',s_age='"+n2+"',s_hname='"+n3+"',s_place='"+n4+"',s_post='"+n5+"',s_pin='"+n6+"',s_email='"+n7+"',s_phone='"+n8+"',qualification='"+n9+"',s_images='"+path+"' where staff_id='"+id+"'")
                return view_staff()
            else:
                qry = db.update("update staff set s_dept_id='" + dept + "',s_name='" + n1 + "',s_age='" + n2 + "',s_hname='" + n3 + "',s_place='" + n4 + "',s_post='" + n5 + "',s_pin='" + n6 + "',s_email='" + n7 + "',s_phone='" + n8 + "',qualification='" + n9 + "' where staff_id='" + id + "'")
                return view_staff()
        else:
            qry = db.update("update staff set s_dept_id='" + dept + "',s_name='" + n1 + "',s_age='" + n2 + "',s_hname='" + n3 + "',s_place='" + n4 + "',s_post='" + n5 + "',s_pin='" + n6 + "',s_email='" + n7 + "',s_phone='" + n8 + "',qualification='" + n9 + "' where staff_id='" + id + "'")
            return view_staff()
    else:
        return redirect('/')


@app.route('/delete_staff/<id>')
def delete_staff(id):
    if session['lin'] == 'lin':
        db=Db()
        qry=db.delete("delete from staff where staff_id='"+id+"'")
        remove_user(id)
        print("**")
        return view_staff()
    else:
        return redirect('/')
#=====================================================================================
@app.route('/add_sub')
def add_sub():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from course")
        return render_template("Admin/add_subject.html",value=qry)
    else:
        return redirect('/')
@app.route('/sub_post',methods=['post'])
def sub_post():
    if session['lin'] == 'lin':
        db=Db()
        n1=request.form['textfield2']
        n2=request.files['fileField']
        n3=request.form['textfield3']
        data = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        n2.save(path1+"subject\\"+data+".pdf")
        path="/static/subject/"+data+".pdf"
        crs=request.form['select']
        qry=db.insert("insert into subject(course_id,subject_name,subject_details_mod,subject_text) values('"+crs+"','"+n1+"','"+path+"','"+n3+"')")
        return add_sub()
    else:
        return redirect('/')
@app.route('/view_subject')
def view_subject():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from course")
        qry1=db.select("select * from subject")
        return render_template("Admin/view_subject.html",value=qry)
    else:
        return redirect('/')
@app.route('/view_subject1/<id>')
def view_subject1(id):
    db=Db()
    qry=db.select("select * from course,subject where course.course_id=subject.course_id and subject.course_id='"+id+"'")
    return render_template("Admin/ajax_subject.html",value1=qry)
@app.route('/update_subject/<id>')
def update_subject(id):
    if session['lin'] == 'lin':
        db=Db()
        qry=db.selectOne("select * from subject where subject_id='"+id+"'")
        qry1=db.select("select * from course")
        return render_template("Admin/Update_subject.html",value=qry,value1=qry1)
    else:
        return redirect('/')
@app.route('/update_subject_post/<id>',methods=['post'])
def update_subject_post(id):
    if session['lin'] == 'lin':
        db=Db()
        n1 = request.form['textfield']
        n2 = request.files['fileField']
        n3 = request.form['textfield3']
        crs = request.form['select']
        data = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        n2.save(path1 + "subject\\" + data + ".pdf")
        path = "/static/subject/" + data + ".pdf"
        qry=db.update("update subject set course_id='"+crs+"',subject_name='"+n1+"',subject_details_mod='"+path+"',subject_text='"+n3+"' where subject_id='"+id+"'")
        return view_subject()
    else:
        return redirect('/')
@app.route('/delete_subject/<id>')
def delete_subject(id):
    if session['lin'] == 'lin':
        db=Db()
        qry=db.delete("delete from subject where subject_id='"+id+"'")
        return view_subject()
    else:
        return redirect('/')
#=====================================================================================
@app.route('/select_hod')
def select_hod():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from dept")
        return render_template("Admin/select_hod.html",value=qry)
    else:
        return redirect('/')
@app.route('/select_hod1/<i>')
def select_hod1(i):
    db=Db()
    qry=db.select("select * from staff where s_dept_id='"+i+"'")
    print(qry)
    return render_template('Admin/ajax_select_hod.html',value=qry)
@app.route('/select_hodpost',methods=['post'])
def select_hodpost():
    if session['lin'] == 'lin':
        db=Db()
        sid=request.form['select2']
        qry=db.selectOne("select s_dept_id from staff where staff_id='"+sid+"'")
        did=qry['s_dept_id']
        print(did)
        qry2=db.selectOne("select * from hod where dept_id='"+str(did)+"'")
        print(qry2['hod_id'],"***")
        if qry2 is None:
            qry1=db.insert("insert into hod(dept_id,h_staff_id) values('"+str(did)+"','"+sid+"')")
            qry3=db.update("update login set usertype='hod' where loginid='"+sid+"'")
        else:
            return render_template("Admin/select_hod_validate.html",value=qry2['hod_id'],value2=sid)
        return select_hod()
    else:
        return redirect('/')
@app.route('/hod_overwrite/<hid>/<sid>')
def hod_overwrite(hid,sid):
    if session['lin'] == 'lin':
        db=Db()
        qry2=db.update("update login set usertype='staff' where loginid=(select h_staff_id from hod where hod_id='"+hid+"')")
        qry=db.update("update hod set h_staff_id='"+sid+"' where hod_id='"+hid+"'")
        qry1=db.update("update login set usertype='hod' where loginid='"+sid+"'")
        return select_hod()
    else:
        return redirect('/')

#=====================================================================================
@app.route('/send_notification')
def send_notification():
    if session['lin'] == 'lin':
        return render_template("Admin/send_notification.html")
    else:
        return redirect('/')

@app.route('/notification_post',methods=['post'])
def notification_post():
    if session['lin'] == 'lin':
        db=Db()
        msg=request.form['textarea']
        qry=db.insert("insert into notification(notification_msg,date_time) values ('"+msg+"',now())")
        return send_notification()
    else:
        return redirect('/')
#=====================================================================================
@app.route('/add_student')
def add_student():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from course")
        return render_template("Admin/add_student.html",value=qry)
    else:
        return redirect('/')
@app.route('/post_student',methods=['post','get'])
def post_student():
    if session['lin'] == 'lin':
        db=Db()
        n1 = request.form['textfield']
        n2 = request.form['textfield2']
        n3 = request.form['textfield3']
        n4 = request.form['textfield4']
        n5 = request.form['textfield5']
        n6 = request.form['textfield6']
        n7 = request.form['textfield7']
        n8 = request.form['textfield8']
        n9 = request.form['textfield9']
        n10=request.form['textfield10']
        n11=request.form['textfield11']
        n12=request.form['select2']
        n13=request.form['textfield13']
        n14=request.form['textfield14']
        crs=request.form['select']
        pht=request.files['fileField']
        data = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        pht.save(path1+"student\\" + data + ".jpeg")
        path = "/static/student/" + data + ".jpeg"
        pwd = random.randint(0000, 9999)
        print(pwd)
        qry2 = db.selectOne("select * from login where username='" + n10 + "'")
        if qry2 is None:

            qry = db.insert("insert into login(username,password,usertype) values('" + n10 + "','" + str(pwd) + "','student')")
            print(qry)
            qry1 = db.insert("insert into student(student_id,student_name,s_course_id,student_dob,student_mname,student_fname,student_hname,student_place,student_post,student_pin,student_district,student_email,student_phone_number,student_semester,year,student_photo) values('"+str(qry)+"','"+n1+"','"+crs+"','"+n2+"','"+n3+"','"+n4+"','"+n5+"','"+n6+"','"+n7+"','"+n8+"','"+n9+"','"+n10+"','"+n11+"','"+n12+"','"+n13+"','"+path+"')")
            qry2=db.insert("insert into rfid(rfid_id,key) values('"+str(qry)+"','"+n14+"')")
            try:
                gmail = smtplib.SMTP('smtp.gmail.com', 587)

                gmail.ehlo()

                gmail.starttls()

                gmail.login('facerecognition103@gmail.com', 'kl13an6958')

            except Exception as e:
                print("Couldn't setup email!!" + str(e))

            msg = MIMEText("Your Password is " + str(pwd))

            msg['Subject'] = 'Verification'

            msg['To'] = n10

            msg['From'] = 'facerecognition103@gmail.com'

            try:

                gmail.send_message(msg)

            except Exception as e:

                print("COULDN'T SEND EMAIL", str(e))
            return  redirect(url_for('add_parent',i=qry))

        else:
            return "<script type=text/javascript>alert('User already exits');</script>"
        #return redirect('/add_parent/'"+qry+"'')
    else:
        return redirect('/')
@app.route('/view_student')
def view_student():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from course")
        return render_template("Admin/view_student.html",value=qry)
    else:
        return redirect('/')
@app.route('/view_student1/<i>')
def ajax_view_student1(i):
    db=Db()
    qry=db.select("select * from student where s_course_id='"+i+"'")
    return render_template('Admin/ajax_view_student.html',value=qry)
@app.route("/update_student/<id>")
def update_student(id):
    db=Db()
    qry=db.selectOne("select * from student where student_id='"+id+"'")
    qry1=db.select("select * from course")
    return render_template("Admin/update_student.html",value2=qry,value1=qry1,s=str(qry['student_semester']))
@app.route('/update_student_post/<id>',methods=['post'])
def update_student_post(id):
    if session['lin'] == 'lin':
        db=Db()
        n1 = request.form['textfield']
        n2 = request.form['textfield2']
        n3 = request.form['textfield3']
        n4 = request.form['textfield4']
        n5 = request.form['textfield5']
        n6 = request.form['textfield6']
        n7 = request.form['textfield7']
        n8 = request.form['textfield8']
        n9 = request.form['textfield9']
        n11 = request.form['textfield11']
        n12 = request.form['select2']
        n13 = request.form['textfield13']
        crs = request.form['select']
        pht = request.files['fileField']
        if request.files is not None:
            if pht.filename != "":
                data = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                pht.save(path1 +"student\\"+ data + ".jpeg")
                path = "/static/student/" + data + ".jpeg"
                qry1 = db.update("update student set student_name='" + n1 + "',s_course_id='" + crs + "',student_dob='" + n2 + "',student_mname='" + n3 + "',student_fname='" + n4 + "',student_hname='" + n5 + "',student_place='" + n6 + "',student_post='" + n7 + "',student_pin='" + n8 + "',student_district='" + n9+ "',student_phone_number='" + n11 + "',student_photo='" + path + "',student_semester='" + n12 + "',year='" + n13 + "' where student_id='" + id + "'")
                return view_student()
            else:
                qry1=db.update("update student set student_name='" + n1 + "',s_course_id='" + crs + "',student_dob='" + n2 + "',student_mname='" + n3 + "',student_fname='" + n4 + "',student_hname='" + n5 + "',student_place='" + n6 + "',student_post='" + n7 + "',student_pin='" + n8 + "',student_district='" + n9+ "',student_phone_number='" + n11 + "',student_semester='" + n12 + "',year='" + n13 + "' where student_id='" + id + "'")
                #qry1 = db.update("update student set student_name='"+n1+"',s_course_id='"+crs+"',student_dob='"+n2+"',student_mname='"+n3+"',student_fname='"+n3+"',student_hname='"+n4+"',student_place='"+n5+"',student_post='"+n6+"',student_pin='"+n7+"',student_district='"+n8+"',student_phone_number='"+n9+"',student_semester='"+n12+"',year='"+n13+"' where student_id='"+id+"'")
                return view_student()
        else:
            qry1 = db.update("update student set student_name='" + n1 + "',s_course_id='" + crs + "',student_dob='" + n2 + "',student_mname='" + n3 + "',student_fname='" + n4 + "',student_hname='" + n5 + "',student_place='" + n6 + "',student_post='" + n7 + "',student_pin='" + n8 + "',student_district='" + n9 + "',student_phone_number='" + n11 + "',student_semester='" + n12 + "',year='" + n13 + "' where student_id='" + id + "'")

            #qry1 = db.update("update student set student_name='" + n1 + "',s_course_id='" + crs + "',student_dob='" + n2 + "',student_mname='" + n3 + "',student_fname='" + n3 + "',student_hname='" + n4 + "',student_place='" + n5 + "',student_post='" + n6 + "',student_pin='" + n7 + "',student_district='" + n8 + "',student_phone_number='" + n9 + "',student_semester='" + n12 + "',year='" + n13 + "' where student_id='" + id + "'")
            return view_student()
    else:
        return redirect('/')
@app.route('/delete_student/<id>')
def delete_student(id):
    db=Db()
    p=get_parent(id)
    pid=p['parent_id']
    print(pid)
    s=removechild(pid,id)
    print(s)
    # s=s.strip()
    if len(s)==0:
        qry=db.delete("delete from parent where parent_id='"+str(pid)+"'")
        remove_user(pid)
    else:
        print("*----------------")
        qry2 = db.update("update parent set student_idp='"+ s +"' where parent_id='" + str(pid) + "'")

    qry=db.delete("delete from student where student_id='"+id+"'")
    remove_user(id)
    return view_student()
#=====================================================================================
#=====================================================================================
@app.route('/sel_dept')
def sel_dept():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from dept")
        return render_template("Admin/ajax_sel_dep.html",value=qry)
    else:
        return redirect('/')
@app.route('/sel_course/<id>')
def sel_course(id):
    db=Db()
    session['dept']=id
    qry=db.select("select * from course where dept_id='"+id+"'")
    return render_template("Admin/ajax_sel_course.html",value1=qry)
# @app.route('/sel_sem/<id>')
# def sel_sem(id):
#     db=Db()
#     qry=db.select("select * from subject where semester=" )
@app.route('/select_sem/<id>')
def view_student_leave_late(id):
    db=Db()
    session['cid']=id
    # qry=db.select("select sum(no_of_days),stu_id from stuleave GROUP by stu_id having stu_id IN (select student_id from student where s_course_id='"+id+"')")
    # print(qry)

    return render_template("Admin/semester.html")
    #return render_template("Admin/view_student_leave_late.html")
@app.route('/select_year/<id>')
def select_year(id):
    session['semid'] = id
    return render_template('Admin/year.html')
@app.route('/select_op/<id>')
def select_op(id):
    session['year']=id
    return render_template('Admin/leave_late1.html')
@app.route('/select_sub_leave/<id>')
def select_sub_leave(id):
    db=Db()
    qry=db.select("select count(aid) as a,student.student_name as s from attendence,student where attendence.stud_id=student.student_id and attendence.status='a' and student.student_semester='"+session['semid']+"' and s_course_id='"+session['cid']+"' and student.year='"+id+"' group by attendence.stud_id")
    print(qry)

    return render_template("Admin/view_student_leave_late.html",data=qry)
#=====================================================================================
@app.route('/view_late')
def select_late():
    if session['lin'] == 'lin':
        db = Db()
        qry = db.select("select * from dept")
        return render_template('Admin/view_student_late.html',value=qry)
    else:
        return redirect('/')
@app.route('/view_late1',methods=['post'])
def view_late1():
    db=Db()
    dep=request.form['select']
    crs=request.form['s']
    semster=request.form['sem']
    fromd=request.form['fdate']
    tod=request.form['todate']
    # qry=db.select("select student.student_name as nam,(TIME_TO_SEC((timediff(late.e_time,'9:00:00'))))/3600 as s,late.rfid_id,late.e_date,student.student_id,student.student_semester,student.s_course_id,course.course_id,course.dept_id from late,student,course,rfid where late.rfid_id=rfid.rfid_id and rfid.rfid_id=student.student_id and student.s_course_id=course.course_id and student.student_semester='"+semster+"'  and student.s_course_id='"+crs+"' and course.dept_id='"+dep+"' and late.e_date between  '"+fromd+"' and '"+tod+"' group by student_id,e_date having s>=0.0000")
    qry=db.select("select student.student_name as nam,SEC_TO_TIME((TIME_TO_SEC((timediff(late.e_time,'9:00:00'))))) as s,late.rfid_id,late.e_date,student.student_id,student.student_semester,student.s_course_id,course.course_id,course.dept_id from late,student,course,rfid where late.rfid_id=rfid.rfid_id and rfid.rfid_id=student.student_id and student.s_course_id=course.course_id and student.student_semester='"+semster+"'  and student.s_course_id='"+crs+"'and late.e_time>'09:00:00' and course.dept_id='"+dep+"' and late.e_date between  '"+fromd+"' and '"+tod+"' group by student_id,e_date having s>=0.0000 order by nam asc,e_date desc")
    print(qry)
    print(fromd,tod)
    return render_template("Admin/view_student_lateinfo.html",value=qry)
#=====================================================================================
#=====================================================================================
@app.route('/add_parent/<i>')
def add_parent(i):
    if session['lin'] == 'lin':
        db=Db()
        qry=db.selectOne("select * from student where student_id='"+i+"'")
        return render_template("Admin/add_parent.html",value1=qry)
    else:
        return redirect('/')
@app.route('/add_parent_post/<sid>',methods=['post'])
def add_parent_post(sid):
    if session['lin'] == 'lin':
        db=Db()
        n1 = request.form['textfield']
        n2 = request.form['textfield2']
        pht = request.files['fileField']
        data = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        pht.save(path1+"parent\\" + data + ".jpeg")
        path = "/static/parent/" + data + ".jpeg"
        pwd = random.randint(0000, 9999)
        print(pwd)
        qry2 = db.selectOne("select * from login where username='"+n2+"'")
        if qry2 is None:

            qry = db.insert("insert into login(username,password,usertype) values('" + n2 + "','" + str(pwd) + "','parent')")
            print(qry)
            qry1 = db.insert("insert into parent(parent_id,parent_name,parent_email,parent_photo,student_idp) values('"+str(qry)+"','"+n1+"','"+n2+"','"+path+"','"+sid+"')")
            try:
                gmail = smtplib.SMTP('smtp.gmail.com', 587)

                gmail.ehlo()

                gmail.starttls()

                gmail.login('facerecognition103@gmail.com', 'kl13an6958')

            except Exception as e:
                print("Couldn't setup email!!" + str(e))

            msg = MIMEText("Your Password is " + str(pwd))

            msg['Subject'] = 'Verification'

            msg['To'] = n2

            msg['From'] = 'facerecognition103@gmail.com'

            try:

                gmail.send_message(msg)

            except Exception as e:

                print("COULDN'T SEND EMAIL", str(e))

        else:
            print(qry2['loginid'])
            return render_template("Admin/parent2.html",value=qry2['loginid'],val=sid)
        return add_student()
    else:
        return redirect('/')
@app.route('/add_parent1/<sid>/<pid>')
def add_parent1(sid,pid):
    if session['lin'] == 'lin':
        db=Db()
        qry=db.selectOne("select * from parent where parent_id='"+pid+"'")
        s=str(qry['student_idp'])
        s=s+','+sid
        print(s)
        qry2=db.update("update parent set student_idp='"+s+"' where parent_id='"+pid+"'")
        print( qry2)
        return add_student()
    else:
        return redirect('/')
@app.route('/view_parent')
def view_parent():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from student,parent where parent.student_idp=student.student_id order by student_semester,student_name asc ")
        return render_template("Admin/view_parent.html",value=qry)
    else:
        return redirect('/')
@app.route('/update_parent/<id>')
def update_parent(id):
    db=Db()
    qry=db.selectOne("select * from parent where parent_id='"+id+"'")
    return render_template("Admin/Update_parent.html",value=qry)
@app.route('/update_parent_post/<id>',methods=['post'])
def update_parent_post(id):
    if session['lin'] == 'lin':
        db=Db()
        n1 = request.form['textfield']
        pht = request.files['fileField']
        if request.files is not None:
            if pht.filename != "":
                data = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                pht.save(path1+"\\parent\\" + data + ".jpeg")
                path = "/static/parent/" + data + ".jpeg"
                qry1 = db.update("update parent set parent_name='"+n1+"',parent_photo='"+path+"' where parent_id='"+id+"'")
                return view_parent()
            else:

                qry1 = db.update("update parent set parent_name='"+n1+"' where parent_id='"+id+"'")
                return view_parent()
        else:
            qry1 = db.update("update parent set parent_name='"+n1+"' where parent_id='"+id+"'")
            return view_parent()
    else:
        return redirect('/')
#=====================================================================================
@app.route('/view_feedback')
def view_feedback():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from student,staff,feedback where student.student_id=feedback.user_id and staff.staff_id=feedback.staff_id")
        return render_template("Admin/view_feedback.html",value=qry)
    else:
        return redirect('/')
#=====================================================================================
@app.route('/add_security')
def add_security():
    if session['lin'] == 'lin':
        return render_template("Admin/add_security.html")
    else:
        return redirect('/')

@app.route('/add_security_post',methods=['post'])
def add_security_post():
    if session['lin'] == 'lin':
        db=Db()
        n1=request.form['textfield']
        n2 = request.form['textfield2']
        n3 = request.form['textfield3']
        n4 = request.form['textfield4']
        pht = request.files['fileField']
        data = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        pht.save(path1+"\\security\\" + data + ".jpeg")
        path = "/static/security/" + data + ".jpeg"
        pwd = random.randint(0000, 9999)
        print(pwd)
        qry2 = db.selectOne("select * from login where username='"+n4+"'")
        if qry2 is None:

            qry = db.insert("insert into login(username,password,usertype) values('" + n4 + "','" + str(pwd) + "','security')")
            print(qry)
            qry1 = db.insert("insert into security(security_id,security_name,security_place,security_phone,security_email,security_photo) values('" + str(qry) + "','" + n1 + "','" + n2 + "','" + n3 + "','" + n4 + "','" + path + "')")
            try:
                gmail = smtplib.SMTP('smtp.gmail.com', 587)

                gmail.ehlo()

                gmail.starttls()

                gmail.login('facerecognition103@gmail.com', 'kl13an6958')

            except Exception as e:
                print("Couldn't setup email!!" + str(e))

            msg = MIMEText("Your Password is " + str(pwd))

            msg['Subject'] = 'Verification'

            msg['To'] = n4

            msg['From'] = 'facerecognition103@gmail.com'

            try:

                gmail.send_message(msg)

            except Exception as e:

                print("COULDN'T SEND EMAIL", str(e))

        else:
            return "ok"
        return add_security()
    else:
        return redirect('/')

@app.route('/view_security')
def view_security():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from security")
        return render_template("Admin/view_security.html",value=qry)
    else:
        return redirect('/')

@app.route('/delete_security/<id>')
def delete_security(id):
    if session['lin'] == 'lin':
        db=Db()
        qry=db.delete("Delete from security where security_id='"+id+"'")
        remove_user(id)
        return view_security()
    else:
        return redirect('/')

@app.route('/update_security/<id>')
def update_security(id):
    if session['lin'] == 'lin':
        db=Db()
        qry=db.selectOne("select * from security where security_id='"+id+"'")
        return render_template("Admin/update_security.html",value1=qry)
    else:
        return redirect('/')
@app.route('/update_security_post/<id>',methods=['post'])
def update_security_post(id):
    if session['lin'] == 'lin':
        db=Db()
        n1=request.form['textfield']
        n2=request.form['textfield2']
        n3=request.form['textfield3']
        pht=request.files['fileField']
        if request.files is not None:
            if pht.filename != "":
                data = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                pht.save(path1+"\\security\\" + data + ".jpeg")
                path ="/static/security/" + data + ".jpeg"
                qry1 = db.update("update security set security_name='"+n1+"',security_place='"+n2+"',security_phone='"+n3+"',security_photo='"+path+"' where security_id='"+id+"'")
                return view_security()
            else:

                qry1 = db.update("update security set security_name='"+n1+"',security_place='"+n2+"',security_phone='"+n3+"' where security_id='"+id+"'")
                return view_security()
        else:
            qry1 = db.update("update security set security_name='"+n1+"',security_place='"+n2+"',security_phone='"+n3+"' where security_id='"+id+"'")
            return view_security()
    else:
        return redirect('/')
#======================================================================================
@app.route('/view_staff_leave')
def view_staff_leave():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from staff ")
        qry1 = db.select("select * from security ")
        return render_template("Admin/view_staff_leave.html",value1=qry,value2=qry1)
    else:
        return redirect('/')
@app.route('/view_staff_leave2/<id>')
def view_staff_leave2(id):
    db=Db()
    qry1=db.select("select * from staffleave where l_staff_id='"+id+"'")
    print(qry1)
    return render_template("Admin/view_staff_leave1.html",value2=qry1)
@app.route('/approve_staff_leave/<id>')
def approve_staff_leave(id):
    if session['lin'] == 'lin':
        db=Db()
        qry=db.update("update staffleave set status='a' where leave_id='"+id+"'")
        return redirect("/view_staff_leave")
    else:
        return redirect('/')

@app.route('/reject_staff_leave/<id>')
def reject_staff_leave(id):
    if session['lin'] == 'lin':
        db=Db()
        qry=db.update("update staffleave set status='r' where leave_id='"+id+"'")
        return redirect("/view_staff_leave")
    else:
        return redirect('/')

#=====================================================================================

# @app.route('/approve_staff_leave')
# def approve_staff_leave():
#     return render_template("Admin/approve_staff_leave.html")

@app.route('/view_complaints')
def view_complaints():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select distinct usertype from login  where usertype!='admin'" )
        return render_template("Admin/view_complaints.html",value1=qry)
    else:
        return redirect('/')
@app.route('/view_complaints1/<utype>')
def view_complaints1(utype):
    db=Db()
    session['u_type']=utype
    if utype==('staff'):
        qry=db.select("select staff_complaints.c_id as cid,staff_complaints.complaint as c,staff_complaints.c_date as date,staff_complaints.rdate,staff_complaints.reply,staff_complaints.c_uid,staff.staff_id,staff.s_name as name from staff_complaints,staff where staff_complaints.c_id=staff.staff_id group by c_id ")
    elif utype==('student'):
        qry = db.select("select students_complaints.c_id as cid,students_complaints.complaint as c,students_complaints.c_date as date,students_complaints.rdate,students_complaints.reply,students_complaints.c_uid,student.student_id,student.student_name as name from students_complaints,student where students_complaints.c_uid=student.student_id ")
    elif utype==('parent'):
        qry = db.select("select parent_complaints.c_id as cid,parent_complaints.complaint as c ,parent_complaints.c_date as date,parent_complaints.rdate,parent_complaints.reply,parent_complaints.c_uid,parent.parent_id,parent.parent_name as name  from parent_complaints,parent where parent_complaints.c_uid=parent.parent_id group by c_id")
    elif utype==('security'):
        qry = db.select("select security_complaints.c_id as cid,security_complaints.complaint as c ,security_complaints.c_date as date,security_complaints.rdate,security_complaints.reply,security_complaints.c_uid,security.security_id,security.security_name as name from security_complaints,security where security_complaints.c_uid=security.security_id group by c_id")
    elif utype==('hod'):
        qry = db.select("select hod_complaints.c_id as cid,hod_complaints.complaint as c ,hod_complaints.c_date as date,hod_complaints.reply,hod_complaints.rdate,hod_complaints.c_uid,hod.hod_id,hod.h_staff_id,staff.staff_id,staff.s_name as name  from staff,hod_complaints,hod where hod_complaints.c_uid=hod.hod_id and hod.h_staff_id=staff.staff_id")


    return render_template("Admin/view_complaint1.html",value2=qry)

@app.route('/reply_complaints/<id>')
def reply_complaints(id):
    if session['lin'] == 'lin':
        db=Db()
        u=(session['u_type'])
        if u== 'staff':
            qry = db.selectOne("select * from staff_complaints where c_id='" + id + "'")
            print(qry)
        elif u=='hod':
            qry = db.selectOne("select * from hod_complaints where c_id='" + id + "'")
            print(qry)
        elif u=='parent':
            qry = db.selectOne("select * from parent_complaints where c_id='" + id + "'")
            print(qry)
        elif u=='student':
            qry = db.selectOne("select * from students_complaints where c_id='" + id + "'")
            print(qry)
        elif u=='security':
            qry = db.selectOne("select * from security_complaints where c_id='" + id + "'")
            print(qry)

        return render_template("Admin/reply_complaint.html",value1=qry)
    else:
        return redirect('/')

@app.route('/reply_complaint_post/<id>',methods=['post'])
def reply_complaints_post(id):
    if session['lin'] == 'lin':
        db = Db()
        rp=request.form['textfield']
        u = (session['u_type'])
        if u == 'staff':
            qry = db.update("update staff_complaints set reply='"+rp+"',rdate= now() where c_id='" + id + "'")
            print(qry)
        elif u == 'hod':
            qry = db.update("update hod_complaints set reply='" + rp + "',rdate= now() where c_id='" + id + "'")
            print(qry)
        elif u == 'parent':
            qry = db.update("update parent_complaints set reply='" + rp + "',rdate= now() where c_id='" + id + "'")
            print(qry)
        elif u == 'student':
            qry = db.update("update students_complaints set reply='" + rp + "',rdate= now() where c_id='" + id + "'")
            print(qry)
        elif u == 'security':
            qry = db.update("update security_complaints set reply='" + rp + "',rdate= now() where c_id='" + id + "'")
            print(qry)
        return view_complaints()
    else:
        return redirect('/')


#=====================================================================================
#=====================================================================================
#=====================================================================================

@app.route('/hod_homepage')
def hod_homepage():
    if session['lin']=='lin':
       # return render_template("Hod/hod_homepage.html")
       db = Db()
       qry = db.selectOne("select s_name from staff where staff_id='" + str(session['hod_id']) + "'")
       session['username']=qry['s_name']
       return  render_template("Hod/Hod_home.html")
    else:
        return redirect('/')
@app.route('/view_hod_profile')
def view_hod_profile():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.selectOne("select * from staff where staff_id='"+str(session['hod_id'])+"'")
        return render_template("Hod/view_hod_profile.html",value=qry)
    else:
        return redirect('/')

@app.route('/hod_view_staff')
def hod_view_staff():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from staff where s_dept_id=(select s_dept_id from staff where staff_id='"+str(session['hod_id'])+"') order by s_name asc")
        return render_template("Hod/view_staff.html",value1=qry)
    else:
        return redirect('/')

@app.route('/hod_view_student')
def hod_view_student():
    if session['lin'] == 'lin':
        db = Db()
        qry = db.select("select  * from course where dept_id=(select s_dept_id from staff where staff_id='"+str(session['hod_id'])+"') ")
        return render_template("Hod/view_student.html",value=qry)
    else:
        return redirect('/')
@app.route('/hod_view_student1/<i>')
def hod_ajax_view_student1(i):
    db=Db()
    qry=db.select("select * from student where s_course_id='"+i+"' order by student_name asc,student_semester desc")
    return render_template('Hod/ajax_view_student.html', value=qry)

@app.route('/view_notification')
def view_notification():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from notification")
        return render_template("Hod/view_notification.html",value=qry)
    else:
        return redirect('/')

@app.route('/hod_view_feedback')
def hod_view_feedback():
    if session['lin'] == 'lin':
        db = Db()
        qry = db.select("select * from student,staff,feedback where student.student_id=feedback.user_id and staff.staff_id=feedback.staff_id")
        return render_template("Hod/view_feedback.html", value=qry)
    else:
        return redirect('/')
@app.route('/hod_view_meeting')
def view_meeting():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from meeting where hodid=(select hod_id from hod where h_staff_id='"+str(session['hod_id'])+"')")
        return render_template("Hod/view_meeting.html",value=qry)
    else:
        return redirect('/')
@app.route('/hod_add_meeting')
def add_meeting():
    if session['lin'] == 'lin':
        return render_template("Hod/add_meeting.html")
    else:
        return redirect('/')

@app.route('/hod_add_meeting_post',methods=['post'])
def hod_add_meeting_post():
    if session['lin'] == 'lin':
        db=Db()
        n1=request.form['textfield']
        n2=request.form['textfield2']
        n3=request.form['textfield3']
        qry=db.insert("insert into meeting(hodid,meeting_content,mdate,mtime) values((select hod_id from hod where h_staff_id='"+str(session['hod_id'])+"'),'"+n1+"','"+n2+"','"+n3+"')")
        return add_meeting()
    else:
        return redirect('/')

@app.route('/hod_apply_leave')
def hod_apply_leave():
    if session['lin'] == 'lin':
        return render_template("Hod/apply_leave.html")
    else:
        return redirect('/')

@app.route('/hod_apply_leave_post',methods=['post'])
def hod_apply_leave_post():
    if session['lin'] == 'lin':
        db=Db()
        n1=request.form['textfield']
        n2 = request.form['textfield2']
        qry=db.insert("insert into staffleave(l_staff_id,l_date,l_no_of_days,status) values ('"+str(session['hod_id'])+"','"+n1+"','"+n2+"','p')")
        return hod_apply_leave()
    else:
        return redirect('/')

@app.route('/view_leave_status')
def view_leave_status():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from staffleave where l_staff_id='"+str(session['hod_id'])+"'")
        return render_template("Hod/view_leave_status.html",value=qry)
    else:
        return redirect('/')
@app.route('/delete_leave_apl/<id>')
def delete_leave_apl(id):
    if session['lin'] == 'lin':
        db=Db()
        qry=db.delete("delete from staffleave where leave_id='"+id+"'")
        return view_leave_status()
    else:
        return redirect('/')
#======================================================================================================================================
@app.route('/subjectallocation_course')
def subjectallocation_course():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from course where course.dept_id=(select dept_id from hod where h_staff_id='"+str(session['hod_id'])+"')")
        return render_template("Hod/subjectallocation_course.html",value1=qry)
    else:
        return redirect('/')
@app.route('/subjectallocation_course1/<id>')
def subjectallocation_course1(id):
    db=Db()
    qry1=db.select("select * from subject where course_id='"+id+"'")
    return render_template("Hod/sub_alloc_course1.html",value2=qry1)
@app.route('/course_sub_post',methods=['post'])
def course_sub_post():
    if session['lin'] == 'lin':
        db=Db()
        n1=request.form['select']
        n2=request.form['select1']
        qry=db.selectOne("select * from course_subject where course_id='"+str(n1)+"' and subject_id='"+str(n2)+"'")
        if qry is None:
            qry=db.insert("insert into course_subject(course_id,subject_id) values('"+n1+"','"+n2+"')")
        return subjectallocation_course()
    else:
        return redirect('/')
#===================================================================================================================================

@app.route('/subjectallocation_staff')
def subjectallocation_staff():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from course where dept_id=(select dept_id from hod where h_staff_id='"+str(session['hod_id'])+"')")
        print(qry)
        return render_template("Hod/subjectallocation_staff.html",value1=qry)
    else:
        return redirect('/')

@app.route('/subjectallocation_staff1/<id>')
def subjectallocation_staff1(id):
    db=Db()
    session['course_id']=id
    qry=db.select("select * from staff where s_dept_id=(select dept_id from hod where h_staff_id='"+str(session['hod_id'])+"')")
    print(qry)
    return render_template("Hod/subjectallocation_staff1.html",value2=qry)

@app.route('/subjectallocation_staff2/<id>')
def subjectallocation_staff2(id):
    db=Db()
    session['staff_id']=id
    qry=db.select("select * from subject where subject_id in(select  subject_id from course_subject where course_id='"+str(session['course_id'])+"')")
    print(qry)
    return render_template("Hod/subjectallocation_staff2.html",value3=qry)

@app.route('/suballoc_staff_post',methods=['post'])
def suballoc_staff_post():
    if session['lin'] == 'lin':
        n1=request.form['select2']
        n2 = request.form['select3']
        n3 = request.form['select4']
        db=Db()
        qry=db.selectOne("select cs_id from course_subject where course_id='"+n1+"' and subject_id='"+n3+"'")
        print(qry)
        qry1=db.selectOne("select * from sub_alloc_staff where course_sub_id='"+str(qry['cs_id'])+"' and staff_id='"+str(n2)+"'")
        if qry1 is None:
            qry2=db.selectOne("select * from sub_alloc_staff where course_sub_id='"+str(qry['cs_id'])+"' ")
            if qry2 is None:
                qry3=db.insert("insert into sub_alloc_staff(course_sub_id,staff_id) values('"+str(qry['cs_id'])+"','"+n2+"')")
            else:
                qry3=db.update("update sub_alloc_staff set staff_id='"+str(n2)+"' where course_sub_id='"+str(qry['cs_id'])+"'")
            return subjectallocation_staff()
        else:
            return subjectallocation_staff()
    else:
        return redirect('/')



@app.route('/hod_view_staff_late')
def hod_view_staff_late():
    if session['lin'] == 'lin':
        db=Db()
        # qry=db.select("select (TIME_TO_SEC((timediff(e_time,'9:00:00'))))/3600 as s,e_date,rfid_id,staff_id,s_name as nam from late,staff where rfid_id=staff_id and s_dept_id=(select dept_id from hod where h_staff_id='"+str(session['hod_id'])+"')having s>0.000 ")
        qry=db.select("select SEC_TO_TIME((TIME_TO_SEC((timediff(late.e_time,'9:00:00'))))) as s,e_date,rfid_id,staff_id,s_name as nam from late,staff where rfid_id=staff_id and s_dept_id=(select dept_id from hod where h_staff_id='"+str(session['hod_id'])+"') group by staff_id,e_date having s>0.000  order by nam asc,e_date desc ")
        return render_template("Hod/view_staff_late.html",value=qry)
    else:
        return redirect('/')

@app.route('/hod_view_staff_leave')
def hod_view_staff_leave():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from staffleave,staff where  l_staff_id=staff_id and s_dept_id=(select dept_id from hod where h_staff_id='"+str(session['hod_id'])+"') and status='a'")
        return render_template("Hod/view_staff_leave.html",value=qry)
    else:
        return redirect('/')

@app.route('/approve_student_leave')
def approve_student_leave():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from stuleave,student,course,hod where stuleave.stu_id=student.student_id and student.s_course_id=course.course_id and course.dept_id=hod.dept_id and h_staff_id='"+str(session['hod_id'])+"'")
        return render_template("Hod/approve_student_leave.html",value=qry)
    else:
        return redirect('/')
@app.route('/approve_student_leave_post1/<id>')
def approve_student_leave_post1(id):
    db=Db()
    qry=db.update("update stuleave set status='a' where sl_id='"+id+"'")
    return approve_student_leave()
@app.route('/approve_student_leave_post2/<id>')
def approve_student_leave_post2(id):
    db=Db()
    qry=db.update("update stuleave set status='r' where sl_id='"+id+"'")
    return approve_student_leave()

@app.route('/hod_view_student_leave1')
def hod_view_student_leave_late1():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.selectOne("select dept_id from hod where h_staff_id='"+str(session['hod_id'])+"'")
        print(qry)
        did=qry['dept_id']
        print(did)
        return redirect(url_for('sel_course1', id=did))
    else:
        return redirect('/')

@app.route('/sel_course1/<id>')
def sel_course1(id):
    if session['lin'] == 'lin':
        db=Db()
        session['dept']=id
        qry=db.select("select * from course where dept_id='"+id+"'")
        return render_template("Hod/hod_view_student_leave.html",value1=qry)
    else:
        return redirect('/')

# @app.route('/sel_sem/<id>')
# def sel_sem(id):
#     db=Db()
#     qry=db.select("select * from subject where semester=" )
@app.route('/select_sem1/<id>')
def view_student_leave_late1(id):
    db=Db()
    session['cid']=id
    # qry=db.select("select sum(no_of_days),stu_id from stuleave GROUP by stu_id having stu_id IN (select student_id from student where s_course_id='"+id+"')")
    # print(qry)

    return render_template("Admin/semester.html")
    #return render_template("Admin/view_student_leave_late.html")
@app.route('/select_year1/<id>')
def select_year1(id):
    session['semid'] = id
    return render_template('Admin/year.html')
@app.route('/select_op1/<id>')
def select_op1(id):
    session['year']=id
    return render_template('Admin/leave_late1.html')
@app.route('/select_sub_leave1/<id>')
def select_sub_leave1(id):
    db=Db()
    qry=db.select("select count(aid) as a,student.student_name as s from attendence,student where attendence.stud_id=student.student_id and attendence.status='a' and student.student_semester='"+session['semid']+"' and s_course_id='"+session['cid']+"' and student.year='"+id+"' group by attendence.stud_id order by s asc")
    print(qry)

    return render_template("Hod/Stud_leave.html",data=qry)

@app.route('/hod_send_complaint')
def hod_send_complaint():
    if session['lin'] == 'lin':
        return render_template("Hod/hod_send_complaints.html")
    else:
        return redirect('/')

@app.route('/hod_complaint_post',methods=['post'])
def hod_complaint_post():
    if session['lin'] == 'lin':
        db=Db()
        n1=request.form['textarea']
        qry=db.insert("insert into hod_complaints(complaint,c_date,c_uid,reply) values('"+n1+"',now(),(select hod_id from hod where h_staff_id='"+str(session['hod_id'])+"'),'pending')")
        return hod_send_complaint()
    else:
        return redirect('/')

@app.route('/hod_view_complaint')
def hod_view_complaint():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from hod_complaints where c_uid=(select hod_id from hod where h_staff_id='"+str(session['hod_id'])+"')")
        return render_template("Hod/hod_view_complaint.html",value=qry)
    else:
        return redirect('/')




#=====================================================================================
#=====================================================================================
#=====================================================================================
@app.route('/staff_home_page')
def staff_home_page():
    if session['lin']=='lin':
        db=Db()
        qry=db.selectOne("Select s_name from staff where staff_id='"+str(session['staff_id'])+"'")
        session['username']=qry['s_name']
        return render_template("Staff/Staff_Home.html")
    # return render_template("Staff/staff_hom_page.html")
    else:
        return redirect('/')
@app.route('/staff_view_profile')
def staff_view_profile_staff():
    if session['lin'] == 'lin':
        db = Db()
        qry = db.selectOne("select * from staff where staff_id='" + str(session['staff_id']) + "'")
        return render_template("Staff/view_profile.html", value=qry)
    else:
        return redirect('/')
@app.route('/staff_add_mark')
def staff_add_mark():
    if session['lin'] == 'lin':
        db=Db()
        # qry=db.select("select * from course_subject ,course ,subject where course_subject.course_id=course.course_id and subject.subject_id=course_subject.subject_id and course.dept_id=(select s_dept_id from staff where staff_id='"+str(session['staff_id'])+"') group by course_name")
        # qry=db.select("select * from course_subject ,course ,subject,sub_alloc_staff where course_subject.course_id=course.course_id and subject.subject_id=course_subject.subject_id and course.dept_id in(select course_sub_id from sub_alloc_staff where staff_id='"+str(session['staff_id'])+"') group by cs_id")
        qry=db.select("  select  course_subject.cs_id,course.course_id,course.course_name,subject.subject_id,course_subject.subject_id from course_subject ,course ,subject,sub_alloc_staff where course_subject.course_id=course.course_id and subject.subject_id=course_subject.subject_id and course_subject.cs_id in(select course_sub_id from sub_alloc_staff where staff_id='"+str(session['staff_id'])+"') group by course_id")
        return render_template("Staff/Add_mark.html",value=qry)
    else:
        return redirect('/')

@app.route('/staff_add_mark1/<id>')
def staff_add_mark1(id):
    if session['lin'] == 'lin':
        db=Db()
        session['csid']=id
        # qry=db.select("select * from course_subject,subject where subject.subject_id=course_subject.subject_id and course_subject.course_id='"+id+"'")
        qry=db.select("select * from course_subject,subject where subject.subject_id=course_subject.subject_id and course_subject.course_id='"+id+"' and course_subject.cs_id in(select course_sub_id from sub_alloc_staff where staff_id='"+str(session['staff_id'])+"')")
        return render_template("Staff/ajax_add_mark1.html",value=qry)
    else:
        return redirect('/')

@app.route('/staff_add_mark2/<id>')
def staff_add_mark2(id):
    db=Db()
    session['subsid'] = id
    qry=db.select("select * from student where s_course_id ='"+str(session['csid'])+"'")
    return render_template("Staff/ajax_add_mark2.html",value=qry)
@app.route('/staff_add_mark_post',methods=['post'])
def staff_add_mark_post():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.selectOne("select cs_id from course_subject where course_id='"+str(session['csid'])+"' and subject_id='"+str(session['subsid'])+"'")
        n3=qry['cs_id']
        print(n3)
        qry1=db.selectOne("select sac_id from sub_alloc_staff where course_sub_id='"+str(n3)+"' and staff_id='"+str(session['staff_id'])+"'")
        n4=qry1['sac_id']
        # print(n4)
        sid=request.form.getlist('name')
        mid= request.form.getlist('mark')
        # print(n1)
        # print(n2)
        for i in range(0,len(sid)):
            print(sid[i],"--",mid[i])
            qry2=db.insert("insert into mark(sub_alloc_staff_id,st_id,mark) values('"+str(n4)+"','"+str(sid[i])+"','"+mid[i]+"')")
            print(qry2)
        # return redirect('/staff_add_mark')
        return staff_add_mark()
    else:
        return redirect('/')

#-----------------------------------------------------------------------------------
@app.route('/staff_add_notes')
def staff_add_notes():
    if session['lin'] == 'lin':
        db = Db()
    # qry = db.select("select * from course_subject ,course ,subject where course_subject.course_id=course.course_id and subject.subject_id=course_subject.subject_id and course.dept_id=(select s_dept_id from staff where staff_id='" + str(session['staff_id']) + "') group by course_name")
        qry=db.select("  select * from course_subject ,course ,subject where course_subject.course_id=course.course_id and subject.subject_id=course_subject.subject_id and course_subject.cs_id in (select course_sub_id from sub_alloc_staff where staff_id='" + str(session['staff_id']) + "') group by course_name")
        return render_template("Staff/add_notes.html",value=qry)
    else:
        return redirect('/')

@app.route('/staff_add_notes1/<id>')
def staff_add_notes1(id):
    db = Db()
    qry = db.select("select * from course_subject,subject where subject.subject_id=course_subject.subject_id and course_subject.course_id='" + id + "'and course_subject.cs_id in(select course_sub_id from sub_alloc_staff where staff_id='"+str(session['staff_id'])+"')")
    return render_template("Staff/ajax_add_notes1.html",value=qry)
@app.route('/staff_note_post',methods=['post'])
def staff_note_post():
    if session['lin'] == 'lin':
        n1=request.form['select']
        n2=request.form['select2']
        db=Db()
        qry = db.selectOne( "select cs_id from course_subject where course_id='" + n1 + "' and subject_id='" +n2 + "'")
        print(qry)
        n3 = qry['cs_id']
        print(n3)
        qry1 = db.selectOne("select sac_id from sub_alloc_staff where course_sub_id='" + str(n3) + "' and staff_id='" + str( session['staff_id']) + "'")
        print(qry1)
        n4 = qry1['sac_id']
        print(n4)
        session['sub_aloc_staff']=n4
        nt=request.files['fileField']
        data = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nt.save(path1+"Notes\\"+data+".pdf")
        path="/static/Notes/"+data+".pdf"
        qry2=db.insert("insert into notes(sub_alloc_staff_id,notes,ndate)values('"+str(n4)+"','"+path+"',now())")
        return staff_add_notes()
    else:
        return redirect('/')
#---------------------------------------------------------------------------------------
@app.route('/staff_view_meeting')
def staff_view_meeting():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from meeting where hodid=(select hodid from hod where dept_id=(select s_dept_id from staff where staff_id='"+str(session['staff_id'])+"'))")
        return render_template("Staff/view_meeting.html",value=qry)
    else:
        return redirect('/')
@app.route('/staff_view_notes')
def staff_view_notes():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select course.course_id,course.course_name as cname,course_subject.cs_id,course_subject.course_id,sub_alloc_staff.sac_id,sub_alloc_staff.course_sub_id,notes.nid,notes.sub_alloc_staff_id,notes.notes as n,notes.ndate from course,course_subject,notes,sub_alloc_staff where notes.sub_alloc_staff_id=sub_alloc_staff.sac_id and sub_alloc_staff.staff_id='"+str(session['staff_id'])+"' and course_subject.cs_id=sub_alloc_staff.course_sub_id and course.course_id=course_subject.course_id")
        return render_template("Staff/View_notes.html",value=qry)
    else:
        return redirect('/')
@app.route('/delete_note/<id>')
def delete_note(id):
    if session['lin'] == 'lin':
        db=Db()
        qry=db.delete("delete from notes where nid='"+id+"'")
        return  staff_view_notes()
    else:
        return redirect('/')

# def staff_view_notification():
#      return render_template("Staff/view_notification.html")

    # return render_template("Staff/View_profile_staff.html")
@app.route('/staff_sub_alloc_staff')
def staff_sub_alloc_staff():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select(" select course.course_id,course.course_name, subject.subject_id,subject.subject_id,subject.subject_name,subject.subject_details_mod,sub_alloc_staff.course_sub_id from course,subject,sub_alloc_staff,course_subject where  course.course_id=course_subject.course_id and subject.subject_id=course_subject.subject_id and course_subject.cs_id in (select course_sub_id from sub_alloc_staff where staff_id='"+str(session['staff_id'])+"') group by (subject_name)")
        return render_template("Staff/view_sub_alloc_staff.html",value=qry)
    else:
        return redirect('/')

@app.route('/staff_view_student')
def staff_view_student():
    if session['lin'] == 'lin':
        db = Db()
        qry = db.select("select  * from course where dept_id=(select s_dept_id from staff where staff_id='"+str(session['staff_id'])+"')")
        return render_template("Staff/view_student.html",value=qry)
    else:
        return redirect('/')
@app.route('/staff_view_notification')
def staff_view_notification():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from notification")
        return render_template("Staff/view_notification.html",value=qry)
    else:
        return redirect('/')
@app.route('/staff_apply_leave')
def staff_apply_leave():
    if session['lin'] == 'lin':
        return render_template("Staff/apply_leave.html")
    else:
        return redirect('/')
@app.route('/staff_apply_leave_post',methods=['post'])
def staff_apply_leave_post():
    if session['lin'] == 'lin':
        db=Db()
        n1=request.form['textfield']
        n2 = request.form['textfield2']
        qry=db.insert("insert into staffleave(l_staff_id,l_date,l_no_of_days,status) values ('"+str(session['staff_id'])+"','"+n1+"','"+n2+"','p')")
        return staff_apply_leave()
    else:
        return redirect('/')

@app.route('/view_leave_status1')
def view_leave_status1():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from staffleave where l_staff_id='"+str(session['staff_id'])+"'")
        return render_template("Staff/view_leave_status.html",value=qry)
    else:
        return redirect('/')
@app.route('/delete_leave_ap2/<id>')
def delete_leave_ap2(id):
    if session['lin'] == 'lin':
        db=Db()
        qry=db.delete("delete from staffleave where leave_id='"+id+"'")
        return view_leave_status1()
    else:
        return redirect('/')
@app.route('/staff_send_complaint')
def staff_send_complaint():
    if session['lin'] == 'lin':
        return render_template("Staff/staff_send_complaints.html")
    else:
        return redirect('/')
@app.route('/staff_complaint_post',methods=['post'])
def staff_complaint_post():
    if session['lin'] == 'lin':
        db=Db()
        n1=request.form['textarea']
        qry=db.insert("insert into staff_complaints(complaint,c_date,c_uid,reply) values('"+n1+"',now(),'"+str(session['staff_id'])+"','pending')")
        return staff_send_complaint()
    else:
        return redirect('/')
@app.route('/staff_view_complaint')
def staff_view_complaint():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select * from staff_complaints where c_uid='"+str(session['staff_id'])+"'")
        return render_template("Staff/staff_view_complaint.html",value=qry)
    else:
        return redirect('/')
@app.route('/add_attendence')
def add_attendence():
    if session['lin'] == 'lin':
        db=Db()
        qry=db.select("select  course_subject.cs_id,course.course_id,course.course_name,subject.subject_id,course_subject.subject_id from course_subject ,course ,subject,sub_alloc_staff where course_subject.course_id=course.course_id and subject.subject_id=course_subject.subject_id and course_subject.cs_id in(select course_sub_id from sub_alloc_staff where staff_id='"+str(session['staff_id'])+"') group by course_id")
        return render_template("Staff/add_attendence.html",value=qry)
    else:
        return redirect('/')
@app.route('/add_attendence1/<id>')
def add_attendence1(id):
    db=Db()
    print(id)
    session['course_id']=id
    qry=db.select("select * from course_subject,subject where subject.subject_id=course_subject.subject_id and course_subject.course_id='"+id+"' and course_subject.cs_id in(select course_sub_id from sub_alloc_staff where staff_id='"+str(session['staff_id'])+"')")
    print(qry)
    return render_template("Staff/ajax_add_attendence1.html",value=qry)
@app.route('/add_attendence2/<id>')
def add_attendence2(id):
    db=Db()
    session['subsid']=id
    return render_template("Staff/ajax_add_attendence2.html")
@app.route('/add_attendence3/<id>')
def add_attendence3(id):
    db=Db()
    session['sem']=id
    return render_template("Staff/ajax_add_attendence3.html")
@app.route('/add_attendence4/<id>')
def add_attendence4(id):
    db=Db()
    session['year']=id
    qry=db.select("select student_id,student_name,s_course_id,student_semester,year from student where s_course_id='"+str(session['course_id'])+"' and student_semester='"+str(session['sem'])+"' and year='"+id+"'")
    print(qry)
    return render_template("Staff/ajax_add_attendence4.html",value=qry)
@app.route('/attendence_post',methods=['post'])
def attendence_post():
    if session['lin'] == 'lin':
        db=Db()
        plist=[]
        list1=request.form.getlist('att')
        print(plist)
        slist=[]
        qry=db.select("select student_id from student where s_course_id='"+str(session['course_id'])+"' and student_semester='"+str(session['sem'])+"' and year='"+str(session['year'])+"'")
        print(qry)
        for i in qry:
            slist.append(i['student_id'])
        print(slist)
        qry1=db.selectOne("select sac_id from sub_alloc_staff where staff_id='"+str(session['staff_id'])+"' and course_sub_id=(select cs_id from course_subject where course_id='"+str(session['course_id'])+"' and subject_id='"+str(session['subsid'])+"') ")
        sasid=qry1['sac_id']
        print(list1)
        for i in slist:

            if str(i) in list1:

                qry2=db.insert("insert into attendence(sub_alloc_staff_id,stud_id,dates,time,status) values('"+str(sasid)+"','"+str(i)+"',now(),now(),'p')")
            else:
                qry2=db.insert("insert into attendence(sub_alloc_staff_id,stud_id,dates,time,status) values('"+str(sasid)+"','"+str(i)+"',now(),now(),'a')")

        return add_attendence()
    else:
        return redirect('/')
#=====================================================================================
#=====================================================================================
@app.route('/reset')
def reset():
    return render_template("reset-password.html")

@app.route('/forgotpassword',methods=['post'])
def forgotpassword():
    u=request.form['username']
    db=Db()
    qry=db.selectOne("select * from login where username='"+u+"'")


    if qry is None:
        # return redirect('/')
        return "<script type='text/javascript'>alert('User Not found'); window.location.href='/';</script>"
    else:
        pwd = random.randint(0000, 9999)
        qry2 = db.update( "update login set password='"+str(pwd)+"' where username='"+u+"'")
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)

            gmail.ehlo()

            gmail.starttls()

            gmail.login('facerecognition103@gmail.com', 'kl13an6958')

        except Exception as e:
            print("Couldn't setup email!!" + str(e))

        msg = MIMEText("Your Password is " + str(pwd))

        msg['Subject'] = 'Verification'

        msg['To'] = u

        msg['From'] = 'facerecognition103@gmail.com'

        try:

            gmail.send_message(msg)

        except Exception as e:

            print("COULDN'T SEND EMAIL", str(e))

    if qry2 is not None:
        return redirect('/')
        # res['data']=qry


    else:
       return redirect('/')
    return redirect('/')

#=====================================================================================

def remove_user(id):
    db=Db()
    qry=db.delete("delete from login where loginid='"+str(id)+"'")
    return
#=====================================================================================
#=====================================================================================
@app.route('/logout')
def logout():
    session['lin']=''
    return redirect('/')
#=====================================================================================
#=====================================================================================
#=====================================================================================
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'),404
@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'),403
@app.errorhandler(400)
def bad_request_error(error):
    return render_template('400.html'),400
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'),500
@app.errorhandler(503)
def service_unavailable_error(error):
    return render_template('503.html'),503

#=====================================================================================

def get_parent(id):
    db=Db()
    qry=db.selectOne("select parent_id from parent where student_idp like '%,"+str(id)+",%' or student_idp like  '"+str(id)+",%' or student_idp like  '%,"+str(id)+"' or student_idp like '"+str(id)+"'")
    print(qry)
    return qry
def removechild(pid,cid):
    db = Db()

    qry = db.selectOne("select student_idp from parent where parent_id='" + str(pid) + "'")
    ids = qry['student_idp']
    pid = ids.split(',')

    r = []
    for i in pid:
        print(i, "...")
        print(type(i))
        if(i!=str(cid)):
            r.append(i);
    print(r)
    print(type(r))
    # s=str(r)
    # print("*",s,type(s))
    s=(",".join((map(str,r)))  )


    return s



if __name__ == '__main__':
    app.run(debug=True)

