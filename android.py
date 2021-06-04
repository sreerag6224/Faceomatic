from flask import Flask, request
from DBConnection import Db
import demjson
import datetime
import face_recognition
import os
import cv2
import random
import smtplib
from email.mime.text import MIMEText
kk = []
student_ids = []

app = Flask(__name__)

path1="E:\\face\\static\\"
path2="E:/face"
sub_alloc_ids=""
cb=""
_image_counter=""
QtGui=""
QImage=""


@app.route('/login',methods=['post'])
def login():
    u=request.form['username']
    p=request.form['password']
    db=Db()
    qry=db.selectOne("select * from login where username='"+u+"' and password='"+str(p)+"'")
    res={}
    if qry is not None:
        res['status']="ok"
        res['lid']=qry['loginid']
        res['utype']=qry['usertype']
        if qry['usertype']=='staff':
            rr=db.selectOne("select * from staff where staff_id='"+str(qry['loginid'])+"'")
            res['uimage'] =rr['s_images']
            res['uname']=rr['s_name']
            res['uemail']=rr['s_email']
        elif qry['usertype']=='student':
            rr=db.selectOne("select * from student where student_id='"+str(qry['loginid'])+"'")
            res['uimage'] =rr['student_photo']
            res['uname']=rr['student_name']
            res['uemail']=rr['student_email']
        elif qry['usertype']=='parent':
            rr=db.selectOne("select * from parent where parent_id='"+str(qry['loginid'])+"'")
            res['uimage'] =rr['parent_photo']
            res['uname']=rr['parent_name']
            res['uemail']=rr['parent_email']
        elif qry['usertype']=='security':
            rr=db.selectOne("select * from security where security_id='"+str(qry['loginid'])+"'")
            res['uimage'] =rr['security_photo']
            res['uname']=rr['security_name']
            res['uemail']=rr['security_email']
    else:
        res['status']="none"
    return demjson.encode(res)
@app.route('/forgot',methods=['post'])
def forgot():
    u=request.form['username']
    db=Db()
    qry=db.selectOne("select * from login where username='"+u+"'")

    res={}
    if qry is None:
        res['status'] = "none"
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
            res['status']="ok"
        # res['data']=qry
        else:
            res['status']="none"
    return demjson.encode(res)

@app.route('/view_profile',methods=['post'])
def view_profile():
    u=request.form['lid']
    db=Db()
    qry=db.selectOne("select * from staff,dept where staff.s_dept_id=dept.dept_id and  staff_id='"+str(u)+"'")
    res={}
    if qry is not None:
        res['status']="ok"
        res['data']=qry


    else:
        res['status']="none"
    return demjson.encode(res)


@app.route('/view_student',methods=['post'])
def view_student():
    u=request.form['lid']
    print(u,"***")
    db = Db()
    qry = db.select("select * from course where dept_id=(select s_dept_id from staff where staff_id='" + str(u) + "')")
    print(qry)
    res={}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/view_student2',methods=['post'])
def view_student2():
    a=request.form['lid']
    b=request.form['course']
    c= request.form['sem']
    d = request.form['year']
    print(a,b,c,d)
    db=Db()
    qry=db.select("select * from student where s_course_id='"+str(b)+"' and student_semester='"+str(c)+"' and year='"+str(d)+"'")
    res = {}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/view_subject',methods=['post'])
def view_subject():
    u=request.form['lid']
    db = Db()
    #qry = db.select("select * from course where dept_id=(select s_dept_id from staff where staff_id='"+str(u)+"')")
    qry=db.select("select * from course  where course_id in(select course_subject.course_id from course_subject where cs_id in (select course_sub_id from sub_alloc_staff where staff_id='"+str(u)+"')) ")
    res={}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/view_subject2',methods=['post'])
def view_subject2():
    a=request.form['lid']
    b=request.form['course']
    c= request.form['sem']
    print(a,b,c)
    db=Db()
    #qry=db.select("select * from course_subject,subject,sub_alloc_staff where course_subject.subject_id=subject.subject_id and subject.semester='"+str(c)+"' and subject.course_id='"+str(b)+"'and sub_alloc_staff.course_sub_id=course_subject.cs_id and sub_alloc_staff.staff_id='"+str(a)+"'")
    qry=db.select("select * from subject where semester='"+str(c)+"' and subject_id in(select subject_id from course_subject where cs_id in (select course_sub_id from sub_alloc_staff where staff_id='"+str(a)+"') and course_id='"+str(b)+"')")
    print(qry)
    res = {}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/view_meeting',methods=['post'])
def view_meeting():
    u=request.form['lid']
    print(u)
    db = Db()
    #qry = db.select("select * from course where dept_id=(select s_dept_id from staff where staff_id='"+str(u)+"')")
    qry=db.select("select * from meeting where hodid=(select hod_id from hod where dept_id=(select s_dept_id from staff where staff_id='"+str(u)+"'))")
    print(qry)
    res={}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/view_student_profile',methods=['post'])
def view_student_profile():
    u=request.form['lid']
    db=Db()
    qry=db.selectOne("select * from student,course where course.course_id=student.s_course_id and student_id='"+str(u)+"'")
    res={}
    if qry is not None:
        res['status']="ok"
        res['data']=qry


    else:
        res['status']="none"
    return demjson.encode(res)


@app.route('/view_student_subject',methods=['post'])
def view_student_subject():
    u=request.form['lid']
    db = Db()
    #qry = db.select("select * from course where dept_id=(select s_dept_id from staff where staff_id='"+str(u)+"')")
    qry=db.select("select * from student,subject where subject.semester=student.student_semester and subject.course_id=student.s_course_id and student.student_id='"+str(u)+"' ")
    res={}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)

@app.route('/view_note',methods=['post'])
def view_note():
    u=request.form['lid']
    db = Db()
    #qry = db.select("select * from course where dept_id=(select s_dept_id from staff where staff_id='"+str(u)+"')")
    qry=db.select("select * from student,subject where subject.semester=student.student_semester and subject.course_id=student.s_course_id and student.student_id='"+str(u)+"' ")
    res={}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)


@app.route('/view_note2',methods=['post'])
def view_note2():
    sid=request.form['sub_id']
    print(sid)
    db = Db()
    #qry = db.select("select * from course where dept_id=(select s_dept_id from staff where staff_id='"+str(u)+"')")
    qry=db.select("select distinct * from subject,course_subject,sub_alloc_staff,notes where course_subject.course_id=subject.course_id and course_subject.subject_id='"+str(sid)+"' and sub_alloc_staff.course_sub_id=course_subject.cs_id and notes.sub_alloc_staff_id=sub_alloc_staff.sac_id group by nid")
    print(qry)
    res={}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)

@app.route('/view_StudentMark',methods=['post'])
def StudentMark():
    u = request.form['lid']
    db = Db()
    # qry = db.select("select * from course where dept_id=(select s_dept_id from staff where staff_id='"+str(u)+"')")
    qry = db.select(
        "select * from student,subject where subject.semester=student.student_semester and subject.course_id=student.s_course_id and student.student_id='" + str(
            u) + "' ")
    res = {}
    print(qry)
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)

@app.route('/StudentMark2',methods=['post'])
def StudentMark2():
    sid = request.form['sub_id']
    u = request.form['lid']
    print(sid)
    db = Db()
    # qry = db.select("select * from course where dept_id=(select s_dept_id from staff where staff_id='"+str(u)+"')")
    qry = db.select("select distinct * from subject,course_subject,sub_alloc_staff,mark where course_subject.course_id=subject.course_id and course_subject.subject_id=subject.subject_id and subject.subject_id='" + str( sid) + "'and mark.st_id='"+str(u)+"' and sub_alloc_staff.course_sub_id=course_subject.cs_id and mark.sub_alloc_staff_id=sub_alloc_staff.sac_id group by mid")
    print(qry)
    res = {}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/send_feedback1',methods=['post'])
def send_feedback1():
    u = request.form['lid']
    db = Db()
    # qry = db.select("select * from course where dept_id=(select s_dept_id from staff where staff_id='"+str(u)+"')")
    qry = db.select("select * from course,staff,student where staff.s_dept_id=course.dept_id and course.course_id=student.s_course_id and student.student_id='" + str(u) + "' ")
    res = {}
    print(qry)
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/send_feedback2',methods=['post'])
def send_feedback2():
    u=request.form['lid']
    su = request.form['staff']
    fb = request.form['fdb']
    db = Db()
    qry = db.insert("insert into feedback(feedback,fdate,user_id,staff_id) values('"+fb+"',now(),'"+u+"','"+su+"')")
    res = {}
    if qry is not None:
        res['status'] = "ok"

    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/view_notification',methods=['post'])
def view_notification():

    db = Db()
    qry = db.select(
        "select * from notification order by date_time desc")
    print(qry)
    res = {}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/view_Attendence',methods=['post'])
def view_Attendence():
    sid = request.form['sub_id']
    lid = request.form['lid']
    fd = request.form['fd']
    td = request.form['td']
    print(sid,lid,fd,td)
    db = Db()
    qry = db.select("select distinct * from attendence,course_subject,student,sub_alloc_staff where attendence.sub_alloc_staff_id=sub_alloc_staff.sac_id and sub_alloc_staff.course_sub_id=course_subject.cs_id and course_subject.subject_id='"+sid+"' and course_subject.course_id=student.s_course_id and attendence.stud_id='"+lid+"' and student.student_id='"+lid+"'and attendence.dates  between '"+fd+"' and '"+td+"' group by aid")
    print(qry)
    res = {}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/view_student_leave_status',methods=['post'])
def view_student_leave_status():
    u=request.form['lid']
    db = Db()
    qry = db.select("select * from stuleave where stu_id ='"+u+"' order by ldate desc")
    res={}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/student_apply_leave',methods=['post'])
def student_apply_leave():
    lid = request.form['lid']
    date = request.form['date']
    days= request.form['days']
    print(lid,date,days)
    db = Db()
    qry = db.insert("insert into stuleave(stu_id,ldate,no_of_days,status) values('"+lid+"','"+date+"','"+days+"','p')")
    print(qry)
    res = {}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
# @app.route('/attendence',methods=['post'])
# def attendence():
#     # lid = request.form['lid']
#     # date = request.form['date']
#     # days= request.form['days']
#     img=request.files['pic']
#     data = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#     img.save(path1 + "uploaded_img\\" + data + ".jpeg")
#     # print(lid)
#     db=Db();
#     results=db.select("select student_photo,student_id from student ")
#     known_faces = []
#     userids = []
#     if results is not None:
#         for result in results:
#             img = path2 + result['student_photo'].rstrip()
#             # img = "C:/aswathi/mpmd/mpmd/MPMD/static/userreg/nazriya@gmail.com.jpg"
#             print(img)
#             b_img = face_recognition.load_image_file(img, 'RGB')
#             b_imgs = face_recognition.face_encodings(b_img)#[0]
#             known_faces.append(b_imgs)
#             userids.append(result['student_id'])
#             print(img + "done")
#
#     print(path2 + "uploaded_img\\" + data + ".jpeg")
#     unknown_image = face_recognition.load_image_file(path2 + "/uploaded_img/" + data + ".jpeg")
#
#     try:
#         m = len(face_recognition.face_encodings(unknown_image))
#         facelocations = face_recognition.face_locations(unknown_image)
#
#         for a in range(m):
#             unknown_face_encoding = face_recognition.face_encodings(unknown_image)[a]
#             results = face_recognition.compare_faces(known_faces, unknown_face_encoding, tolerance=0.5)
#             for i in range(len(results)):
#                 if results[i] == True:
#
#                     print("============true")
#                     # ukimg = Image.open(path)
#                     # spic = Image.open(path)
#                     # top, right, bot, lef = facelocations[a]
#                     # flox = str(lef) + "," + str(top) + "," + str(right) + "," + str(bot)
#                     # s = "select max(notid) from tbl_notification"
#                     # c = conn()
#                     # mid = c.mid(s)
#                     # qry = "insert into tbl_notification (uid,postid,status,date,floc)values('" + str(
#                     #     userids[i]) + "','" + str(mxid) + "','pending',curdate(),'" + flox + "')"
#                     #
#                     # c.nonreturn(qry)
#                     # box = (lef, top, right, bot)
#                     # print("boxx")
#                     # cropped_image = ukimg.crop(box)
#                     # pth = rtpth + "static/notif/" + str(mid) + ".jpg"
#                     # cropped_image.save(pth)
#                     #
#                     # dr = ImageDraw.Draw(spic)
#                     # dr.rectangle(box, fill=(0, 0, 0))
#                     # spic.save(path)
#                     # img.show()
#
#                     # db = Db()
#     # qry = db.insert("insert into stuleave(stu_id,ldate,no_of_days,status) values('"+lid+"','"+date+"','"+days+"','p')")
#     # print(qry)
#     except Exception as e:
#         print(e)
#     res = {}
#     # # if qry is not None:
#     res['status'] = "ok"
#     # #     res['data'] = qry
#     # # else:
#     # #     res['status'] = "none"
#     return demjson.encode(res)


@app.route('/attendence',methods=['post'])
def attendence():
    res={}
    j=0
    _image_counter = 0
    lid = request.form['lid']
    crs = request.form['crs']
    sem= request.form['sem']
    sub= request.form['sub']
    print(lid,"++",crs,"==",sem,"////",sub)
    img=request.files['pic']
    data = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    img.save(path1 + "uploaded_img\\" + data + ".jpeg")
    # print(lid)
    db=Db();
    name=path1+"uploaded_img\\"+data+".jpeg"
    # name=path1+"uploaded_img\\aa.jpg"
    face_picture1 = face_recognition.load_image_file(name)
    # Detect faces
    face_locations = face_recognition.face_locations(face_picture1)
    print("aaa=",len(face_locations))
    # Encode faces
    face_encodings = face_recognition.face_encodings(face_picture1, face_locations)
    # ----------------------------------------------------------------

    db = Db()

    kc = 4
    selected_sem =5
    # res = db.select("select * from student where s_course_id='" + str(kc) + "' and student_semester='" + str(selected_sem) + "'")
    res = db.select("select * from student where s_course_id='" + str(crs) + "' and student_semester='" + str(sem) + "'")
    for rin in res:
        try:
            std_pic = rin['student_photo']
            kn = std_pic.split('/')
            std_pic = kn[len(kn) - 1]
            std_pic_path = path2 + std_pic
            face_picture = face_recognition.load_image_file(path2 +"/"+  rin['student_photo'])
            # Detect faces
            kn_face_locations = face_recognition.face_locations(face_picture)
            # Encode faces
            kn_face_encodings = face_recognition.face_encodings(face_picture, kn_face_locations)
            kk.append(kn_face_encodings)
        except Exception as e:
            print("error")
        student_ids.append(rin["student_id"])
    # --------------------------------------------------------------
    present_students = []
    qr=db.selectOne("select sac_id from sub_alloc_staff where course_sub_id=(select cs_id from course_subject where course_id='"+crs+"' and subject_id='"+sub+"' ) and staff_id='"+lid+"'")
    suballoc = qr['sac_id']
    print(suballoc,"...123...")
    print("fa",len(face_encodings))
    for face_encoding in face_encodings:
        print("===============++++++++++++++++")
        for i in range(0, len(student_ids)):
            try:
                matches = face_recognition.compare_faces(kk[i], face_encoding,tolerance=0.45)
                for x in matches:
                    if x == True:
                        j=j+1
                        print("Face matched...",)
                        present_students.append(student_ids[i])
                        print(present_students)
            except Exception as e:
                print(str(e))
    print("completed...")
    print(j)
    print(present_students)
    print(student_ids)
    for std in student_ids:
        if std in present_students:
            print(std,"p")
            res=db.selectOne("select * from attendence where dates=curdate() and stud_id='"+str(std)+"' and sub_alloc_staff_id='" + str(suballoc) + "'")
            if res is None:
                db.insert("insert into attendence VALUES(NULL,'" + str(suballoc) + "','" + str(std) + "',curdate(),curtime(),'p')")
        else:
            print(std,'pp')
            res = db.selectOne("select * from attendence where dates=curdate() and stud_id='" + str(
                std) + "' and sub_alloc_staff_id='" + str(suballoc) + "'")
            if res is None:
                db.insert("insert into attendence VALUES(NULL,'" + str(suballoc) + "','" + str(std) + "',curdate(),curtime(),'a')")


    _image_counter += 1
    print(_image_counter,"**")
    return "ok"


# def displayImage(self, img, window=True):
#     qformat = QtGui.QImage.Format_Indexed8
#     if len(img.shape) == 3:
#         if img.shape[2] == 4:
#             qformat = QtGui.QImage.Format_RGBA8888
#         else:
#             qformat = QImage.Format_RGB888
#     outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
#     outImage = outImage.rgbSwapped()

@app.route('/student_complaint1',methods=['post'])
def student_complaint1():
    lid = request.form['lid']
    comp = request.form['c']
    print(lid,comp)
    db = Db()
    qry = db.insert("insert into students_complaints(complaint,c_date,c_uid,reply) values('"+comp+"',now(),'"+lid+"','pending')")
    print(qry)
    res = {}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/view_stu_complaint',methods=['post'])
def view_stu_complaint():
    u=request.form['lid']
    db = Db()
    qry = db.select("select * from students_complaints where c_uid ='"+u+"' order by c_date desc")
    res={}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/parent_complaint1',methods=['post'])
def parent_complaint1():
    lid = request.form['lid']
    comp = request.form['c']
    print(lid,comp)
    db = Db()
    qry = db.insert("insert into parent_complaints(complaint,c_date,c_uid,reply) values('"+comp+"',now(),'"+lid+"','pending')")
    print(qry)
    res = {}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)

@app.route('/view_parent_complaint',methods=['post'])
def view_parent_complaint():
    u=request.form['lid']
    db = Db()
    qry = db.select("select * from parent_complaints where c_uid ='"+u+"' order by c_date desc")
    res={}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/child_mark',methods=['post'])
def child_mark():
    u=request.form['child']
    db = Db()
    qry = db.select("select sum(mark)as sum,avg(mark)as avg,sub_alloc_staff_id,st_id,subject_name as sub from mark,subject where st_id='"+u+"' and sub_alloc_staff_id in(select sac_id from sub_alloc_staff where course_sub_id in(select cs_id from  course_subject where course_id=(select s_course_id from student where student_id='"+u+"') and subject_id in(select subject_id from subject where semester =(select student_semester from student where student_id='"+u+"' )))) group by st_id,sub_alloc_staff_id ")
    print(qry)
    res={}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)

@app.route('/view_profile_security',methods=['post'])
def view_profile_security():
    u=request.form['lid']
    db=Db()
    qry=db.selectOne("select * from security where security_id='"+str(u)+"'")
    res={}
    if qry is not None:
        res['status']="ok"
        res['data']=qry


    else:
        res['status']="none"
    return demjson.encode(res)

@app.route('/security_complaint1',methods=['post'])
def security_complaint1():
    lid = request.form['lid']
    comp = request.form['c']
    print(lid,comp)
    db = Db()
    qry = db.insert("insert into security_complaints(complaint,c_date,c_uid,reply) values('"+comp+"',now(),'"+lid+"','pending')")
    print(qry)
    res = {}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)

@app.route('/view_security_complaint',methods=['post'])
def view_security_complaint():
    u=request.form['lid']
    db = Db()
    qry = db.select("select * from security_complaints where c_uid ='"+u+"' order by c_date desc")
    res={}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/view_security_leave_status',methods=['post'])
def view_security_leave_status():
    u=request.form['lid']
    db = Db()
    qry = db.select("select * from staffleave where l_staff_id ='"+u+"' order by l_date desc ")
    res={}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/security_apply_leave',methods=['post'])
def security_apply_leave():
    lid = request.form['lid']
    date = request.form['date']
    days= request.form['days']
    print(lid,date,days)
    db = Db()
    qry = db.insert("insert into staffleave(l_staff_id,l_date,l_no_of_days,status) values('"+lid+"','"+date+"','"+days+"','p')")
    print(qry)
    res = {}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)

@app.route('/view_child',methods=['post'])
def view_child():
    u=request.form['lid']
    db = Db()

    qry = db.selectOne("select student_idp from parent where parent_id='"+u+"'")
    ids=qry['student_idp']
    # print(ids,"**")
    # sidd=[]


    pid=ids.split(',')
    # print(pid)
    # print(qry.values(),"!!!!!!!!!!")

    r=[]
    for i in pid:
        print(i,"...")
        re={}
        qry2 = db.selectOne("select student.student_id,student.student_name,student.s_course_id,student.student_dob,student.student_semester,course.course_id,course.course_name,student.student_photo from course,student where course.course_id=student.s_course_id and student_id= ('" +i + "')")
        print(qry2)
        re['student_id']=qry2['student_id']
        print(re)
        re['student_name']=qry2['student_name']
        re['student_semester']=qry2['student_semester']
        re['course_name']=qry2['course_name']
        re['student_dob']=qry2['student_dob']
        re['student_photo']=qry2['student_photo']


        r.append(re)
        print(r)

    # print(sidd,"*****+++++++")
    res={}
    if re is not None:
        res['status'] = "ok"
        res['data'] = r
    else:
        res['status'] = "none"
    return demjson.encode(res)

@app.route('/child_sub',methods=['post'])
def child_sub():
    u=request.form['cid']
    db = Db()
    qry = db.select("select subject.subject_id,subject_name from subject,student,course_subject where subject.subject_id=course_subject.subject_id and course_subject.course_id=student.s_course_id and subject.semester=student.student_semester and student.student_id='"+u+"' ")
    res={}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/child_attendence',methods=['post'])
def child_attendence():
    sid = request.form['subid']
    lid = request.form['stu_id']
    print(sid,lid,)
    db = Db()
    qry = db.select("select distinct * from attendence,course_subject,student,sub_alloc_staff where attendence.sub_alloc_staff_id=sub_alloc_staff.sac_id and sub_alloc_staff.course_sub_id=course_subject.cs_id and course_subject.subject_id='"+sid+"' and course_subject.course_id=student.s_course_id and attendence.stud_id='"+lid+"' and student.student_id='"+lid+"' group by aid")
    print(qry)
    res = {}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
@app.route('/child_late',methods=['post'])
def child_late():
    sid = request.form['stu_id']
    print(sid)
    db = Db()
    qry=db.select("select e_date,e_time from late,rfid where late.rfid_id='"+sid+"' and e_time>='09:00:59'")
    print(qry)
    res = {}
    if qry is not None:
        res['status'] = "ok"
        res['data'] = qry
    else:
        res['status'] = "none"
    return demjson.encode(res)
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
