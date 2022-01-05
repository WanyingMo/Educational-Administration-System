# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 15:03:16 2020

@author: rommel
"""

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.messagebox
import sqlite3
from time import sleep
import socket
import shutil
import sys


class ftpclient(object):

    def   __init__(self,client):
        self.client = client

    def dolist(self):
        #Send request to server, receive message from server
        self.client.send(b'L')
        data = self.client.recv(1024).decode('UTF-8')
        if data == 'OK':
            while True:
                filename = self.client.recv(1024).decode('UTF-8')
                if filename == '##':
                    break
                print('\033[32m'+filename+'\033[0m')
        else:
            print(data)

    def doget(self,filename):
        message = 'G ' + filename
        self.client.send(message.encode())
        data = self.client.recv(1024).decode()
        if data == 'OK':
            f = open(filename,'w',encoding='UTF-8')
            while True:
                data = self.client.recv(1024)
                if data == b'##':
                    break
                f.write(data)
            f.close()
            print('%s download finished' % filename)
        else:
            print(data)
            

    def doput(self,filename):
        filename2 = filename.split('/')[-1]
        try:
            f = open(filename,'r',encoding='UTF-8')
        except:
            print('no such file')
            return

        self.client.send(('P '+filename2).encode('UTF-8'))
        data = self.client.recv(1024)
        if data == b'OK':
            while True:
                data = f.read(1024)
                if not data:
                    import time
                    time.sleep(0.1)
                    self.client.send(b'##')
                    break
                self.client.send(data)
            f.close()
            print('%s upload finished' % filename2)

    def doexit(self):
        self.client.send(b'Q')
        sys.exit('Thanks for using!')
        
address = ('127.0.0.1',8888)
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   
try:
        client.connect(address)
except Exception as e:
        print("Server connection failed！",e)
clientobj = ftpclient(client)
clientobj.doget("teach.db")

db = sqlite3.connect('teach.db')

db.execute ('''CREATE TABLE IF NOT EXISTS Student(
   ID             INTEGER    PRIMARY KEY   AUTOINCREMENT,
   NAME           TEXT      NOT NULL,
   Password       TEXT       NOT NULL,
   Gender         TEXT      NOT NULL,
   Age            TEXT       NOT NULL,
   Class          TEXT       MOT NULL,
   Phone          TEXT       NOT NULL,
   Address        TEXT      NOT NULL);''')


db.execute ('''CREATE TABLE IF NOT EXISTS Teacher(
   ID             INTEGER    PRIMARY KEY   AUTOINCREMENT,
   NAME           TEXT      NOT NULL,
   Password       TEXT       NOT NULL,
   Gender         TEXT      NOT NULL,
   Age            TEXT       NOT NULL,
   Class          TEXT       MOT NULL,
   Phone          TEXT       NOT NULL,
   Address        TEXT      NOT NULL);''')


db.execute ('''CREATE TABLE IF NOT EXISTS Administrators(
   ID             INTEGER    PRIMARY KEY   AUTOINCREMENT,
   NAME           TEXT      NOT NULL,
   Password       TEXT       NOT NULL,
   Age            TEXT       NOT NULL,
   Phone          TEXT       NOT NULL,
   Address        TEXT      NOT NULL);''')


db.execute ('''CREATE TABLE IF NOT EXISTS Course(
   ID             INTEGER       PRIMARY KEY   AUTOINCREMENT,
   Name           TEXT          NOT NULL,
   Credit         TEXT           NOT NULL,
   Teacherid      INT           NOT NULL,
   Cost           TEXT           NOT NULL,
   Upper_limit    INT     NOT NULL,
   Number         INT     NOT NULL);''')


db.execute ('''CREATE TABLE IF NOT EXISTS Course_selection(
   Studentid         INTEGER PRIMARY KEY   AUTOINCREMENT,
   CourseId          INT         NOT NULL,
   Teacherid         INT         NOT NULL,
   Record            INT         NOT NULL);''')


def select():
   window = tk.Tk()
   window.title('Teaching Affair Management System')
   window.geometry('500x300')
   l = tk.Label(window, text='Please choose your identity：')
   l.pack()
   def selected():
       window.destroy()
       GUI(var.get())
   var = tk.IntVar()
   r1 = tk.Radiobutton(window, text='student',variable=var, value=1,command=selected)
   r1.pack()
   r2 = tk.Radiobutton(window, text='teacher',variable=var, value=2,command=selected)
   r2.pack()
   r3 = tk.Radiobutton(window, text='administrator',variable=var, value=3,command=selected)
   r3.pack()
   window.mainloop()

def GUI(judge):
   root = Tk()
   root.title("Teaching Affair Management System")
   root.geometry("500x300")
   root.configure(background="black")
   class Example(Frame):
       def __init__(self, master, *pargs):
           Frame.__init__(self, master, *pargs)
           self.image = Image.open("C:\\Users\\rommel\\Desktop\\python\\teach_system\\client\\background.png")
           self.img_copy= self.image.copy()
           self.background_image = ImageTk.PhotoImage(self.image)
           self.background = Label(self, image=self.background_image)
           self.background.pack(fill=BOTH, expand=YES)
           self.background.bind('<Configure>', self._resize_image)
       def _resize_image(self,event):
           new_width = event.width
           new_height = event.height
           self.image = self.img_copy.resize((new_width, new_height))
           self.background_image = ImageTk.PhotoImage(self.image)
           self.background.configure(image =  self.background_image)

   e = Example(root)
   e.pack(fill=BOTH, expand=YES)
   
   tk.Label(root,text='User:').place(x=150,y=50)
   tk.Label(root,text='Password:').place(x=150,y=90)
   var_name=tk.IntVar()
   entry_name=tk.Entry(root,textvariable=var_name)
   entry_name.place(x=200,y=50)
   var_pwd=tk.StringVar()
   entry_pwd=tk.Entry(root,textvariable=var_pwd,show='*')
   entry_pwd.place(x=200,y=90)
   
   def sign_up():#1 is student, 2 is teacher, 3 is administrator
       if judge==1:
            root_sign_up=tk.Toplevel(root)
            root_sign_up.geometry('400x400')
            root_sign_up.title('Student information registration')
            new_id=tk.IntVar()
            tk.Label(root_sign_up,text='Student ID：').place(x=10,y=10)
            tk.Entry(root_sign_up,textvariable=new_id).place(x=150,y=10)
            new_name=tk.StringVar()
            tk.Label(root_sign_up,text='Name：').place(x=10,y=50)
            tk.Entry(root_sign_up,textvariable=new_name).place(x=150,y=50)    
            new_pwd=tk.StringVar()
            tk.Label(root_sign_up,text='Password：').place(x=10,y=90)
            tk.Entry(root_sign_up,textvariable=new_pwd,show='*').place(x=150,y=90)
            new_gender=tk.StringVar()
            tk.Label(root_sign_up,text='Gender：').place(x=10,y=130)
            tk.Entry(root_sign_up,textvariable=new_gender).place(x=150,y=130)
            new_age=tk.StringVar()
            tk.Label(root_sign_up,text='Age：').place(x=10,y=170)
            tk.Entry(root_sign_up,textvariable=new_age).place(x=150,y=170)
            new_class=tk.StringVar()
            tk.Label(root_sign_up,text='Class：').place(x=10,y=210)
            tk.Entry(root_sign_up,textvariable=new_class).place(x=150,y=210)
            new_phone=tk.StringVar()
            tk.Label(root_sign_up,text='Phone：').place(x=10,y=250)
            tk.Entry(root_sign_up,textvariable=new_phone).place(x=150,y=250)
            new_address=tk.StringVar()
            tk.Label(root_sign_up,text='Address').place(x=10,y=290)
            tk.Entry(root_sign_up,textvariable=new_address).place(x=150,y=290)
            def input():
                sql_input="SELECT ID from Student where ID = '%d';"%new_id.get()
                cu = db.cursor()
                cu.execute(sql_input)#If this ID exists
                row = cu.fetchone()
                if row:
                   tk.messagebox.askokcancel('Warning','ID already exists!')
                else:
                   sql = "INSERT INTO Student(ID,NAME,Password,Gender,Age,Class,Phone,Address)"
                   sql += " VALUES('%d','%s','%s','%s','%s','%s','%s','%s');"%(new_id.get(),new_name.get(),new_pwd.get(),new_gender.get(),new_age.get(),new_class.get(),new_phone.get(),new_address.get())
                   cu.execute(sql)
                   db.commit()
                   tk.messagebox.askokcancel('Warning','Information uploaded successfully!')
            tk.Button(root_sign_up,text='Registration confirm',command=input).place(x=150,y=350)
       elif judge==2:
            root_sign_up=tk.Toplevel(root)
            root_sign_up.geometry('400x400')
            root_sign_up.title('Teacher information registration')
            new_id=tk.IntVar()
            tk.Label(root_sign_up,text='Teacher ID：').place(x=10,y=10)
            tk.Entry(root_sign_up,textvariable=new_id).place(x=150,y=10)
            new_name=tk.StringVar()
            tk.Label(root_sign_up,text='Name：').place(x=10,y=50)
            tk.Entry(root_sign_up,textvariable=new_name).place(x=150,y=50)    
            new_pwd=tk.StringVar()
            tk.Label(root_sign_up,text='Password：').place(x=10,y=90)
            tk.Entry(root_sign_up,textvariable=new_pwd,show='*').place(x=150,y=90)
            new_gender=tk.StringVar()
            tk.Label(root_sign_up,text='Gender：').place(x=10,y=130)
            tk.Entry(root_sign_up,textvariable=new_gender).place(x=150,y=130)
            new_age=tk.StringVar()
            tk.Label(root_sign_up,text='Age：').place(x=10,y=170)
            tk.Entry(root_sign_up,textvariable=new_age).place(x=150,y=170)
            new_class=tk.StringVar()
            tk.Label(root_sign_up,text='Class：').place(x=10,y=210)
            tk.Entry(root_sign_up,textvariable=new_class).place(x=150,y=210)
            new_phone=tk.StringVar()
            tk.Label(root_sign_up,text='Phone：').place(x=10,y=250)
            tk.Entry(root_sign_up,textvariable=new_phone).place(x=150,y=250)
            new_address=tk.StringVar()
            tk.Label(root_sign_up,text='Address').place(x=10,y=290)
            tk.Entry(root_sign_up,textvariable=new_address).place(x=150,y=290)
            def input():
                sql_input = "SELECT ID from Teacher where ID = '%d';" % new_id.get()
                cu = db.cursor()
                cu.execute(sql_input)
                row = cu.fetchone()
                if row:
                   tk.messagebox.askokcancel('Warning','ID already exists!')
                else:
                   sql = "INSERT INTO Teacher(ID,NAME,Password,Gender,Age,Class,Phone,Address)"
                   sql += " VALUES('%d','%s','%s','%s','%s','%s','%s','%s');"%(new_id.get(),new_name.get(),new_pwd.get(),new_gender.get(),new_age.get(),new_class.get(),new_phone.get(),new_address.get())
                   cu.execute(sql)
                   db.commit()
                   tk.messagebox.askokcancel('Warning','Information uploaded successfully!')
            tk.Button(root_sign_up,text='Registration confirm',command=input).place(x=150,y=350)
       else:
            root_sign_up=tk.Toplevel(root)
            root_sign_up.geometry('400x300')
            root_sign_up.title('Administrator information registration')
            new_id=tk.IntVar()
            tk.Label(root_sign_up,text='ID：').place(x=10,y=10)
            tk.Entry(root_sign_up,textvariable=new_id).place(x=150,y=10)
            new_name=tk.StringVar()
            tk.Label(root_sign_up,text='Name：').place(x=10,y=50)
            tk.Entry(root_sign_up,textvariable=new_name).place(x=150,y=50)    
            new_pwd=tk.StringVar()
            tk.Label(root_sign_up,text='Password：').place(x=10,y=90)
            tk.Entry(root_sign_up,textvariable=new_pwd,show='*').place(x=150,y=90)
            new_age=tk.StringVar()
            tk.Label(root_sign_up,text='Age：').place(x=10,y=130)
            tk.Entry(root_sign_up,textvariable=new_age).place(x=150,y=130)
            new_phone=tk.StringVar()
            tk.Label(root_sign_up,text='Phone：').place(x=10,y=170)
            tk.Entry(root_sign_up,textvariable=new_phone).place(x=150,y=170)
            new_address=tk.StringVar()
            tk.Label(root_sign_up,text='Address').place(x=10,y=210)
            tk.Entry(root_sign_up,textvariable=new_address).place(x=150,y=210)
            def input():
                sql_input = "SELECT ID from Administrators where ID = '%d';" % new_id.get()
                cu = db.cursor()
                cu.execute(sql_input)
                row = cu.fetchone()
                if row:
                   tk.messagebox.askokcancel('Warning','ID already exists!')
                else:
                   sql = "INSERT INTO Administrators(ID,NAME,Password,Age,Phone,Address)"
                   sql += " VALUES('%d','%s','%s','%s','%s','%s');"%(new_id.get(),new_name.get(),new_pwd.get(),new_age.get(),new_phone.get(),new_address.get())
                   cu.execute(sql)
                   db.commit()
                   tk.messagebox.askokcancel('Warning','Information uploaded successfully!')
            tk.Button(root_sign_up,text='Registration confirm',command=input).place(x=150,y=250)
   def log_in():
       if judge==1:#Student server functions
           def identity():#Check Student Identity information
               def student_search():
                   sql_identity=db.cursor()
                   sql_identity.execute("SELECT ID,NAME,Password,Gender,Age,Class,Phone,Address from Student where ID='%d';"%var_name.get())
                   identity_row=sql_identity.fetchone()
                   tk.messagebox.askokcancel('Information',"Student ID：'%d'\nName：'%s'\nPassword：'%s'\nGender：'%s'\nAge：'%s'\nClass：'%s'\nPhone：'%s'\nAddress：'%s'\n"%(identity_row[0],identity_row[1],identity_row[2],identity_row[3],identity_row[4],identity_row[5],identity_row[6],identity_row[7]))
               def modify():
                   def confirm_modify():
                       tk.messagebox.askokcancel('Warning','New password is：%s'%(modify_pwd.get()))
                       sql_modify=db.cursor()
                       sql_modify.execute("UPDATE Student SET Password='%s' WHERE ID ='%d';"%(modify_pwd.get(),var_name.get()))
                       db.commit()
                   tk_modify=tk.Toplevel(root)
                   tk_modify.geometry('200x200')
                   tk_modify.title('Change Password')
                   modify_pwd=tk.StringVar()
                   tk.Label(tk_modify,text='New password：').place(x=10,y=50)
                   tk.Entry(tk_modify,textvariable=modify_pwd,show='*').place(x=150,y=50)  
                   tk.Button(tk_modify,text='Change confirm',command=confirm_modify).place(x=100,y=100)
               tk_identity=tk.Toplevel(root)
               tk_identity.geometry('200x200')
               tk_identity.title('Student server')
               tk.Button(tk_identity,text='Check personal information',command=student_search).place(x=50,y=50)
               tk.Button(tk_identity,text='Change password',command=modify).place(x=50,y=100)
           def curriculum():#Check course information
               def Course_selection():
                   def comfir_selection():
                       sea=db.cursor()
                       sea.execute("SELECT Teacherid,Upper_limit,Number from Course where ID= '%d';"%(selection_ID.get()))
                       db.commit()
                       sea_row=sea.fetchone()
                       if sea_row[1]>=sea_row[2]+1:
                           temp=sea_row[2]
                           temp=temp+1
                           tk.messagebox.askokcancel('Warning','Select course successfully')
                           sql_add_number=db.cursor()
                           sql_add_number.execute("UPDATE Course SET Number='%d' WHERE ID ='%d';"%(temp,selection_ID.get))#Population +1
                           db.commit()
                           init_record=0
                           sql_Course_selection=db.cursor()
                           sql_Course_selection.execute("INSERT INTO Course_selection(Studentid,CourseId,Teacherid,Record) VALUES('%d','%d','%d','%d');"%(var_name.get(),selection_ID.get(),sea_row[0],init_record))
                           db.commit()
                       else:
                           tk.messagebox.askokcancel('Warning','This course is full')
                   tk_selection=tk.Toplevel(root)
                   tk_selection.geometry('200x200')
                   tk_selection.title('Select course')
                   selection_ID=tk.IntVar()
                   tk.Label(tk_selection,text=('Please enter course ID：').place(x=10,y=50)
                   tk.Entry(tk_selection,textvariable=selection_ID).place(x=150,y=50)  
                   tk.Button(tk_selection,text='Course selection confirm',command=comfir_selection).place(x=100,y=100)
               def Drop_out():
                   def comfir_delete():
                       tk.messagebox.askokcancel('Warning','Drop course successfully')
                       sql_number=db.cursor()
                       sql_number.execute("SELECT Number from Course where ID= '%d';"%(Drop_out_ID.get()))
                       sql_number_row=sql_number.fetchone()
                       temp=sql_number_row[0]
                       temp=temp-1
                       sql_number_reduce=db.cursor()
                       sql_number_reduce.execute("UPDATE Course SET Number='%d' WHERE ID ='%d';"%(temp,Drop_out_ID.get()))#Population -1
                       db.commit()
                       sql_delete=db.cursor()
                       sql_delete.execute("DELETE FROM Course_selection WHERE CourseId='%d' and Studentid='%d';"%(Drop_out_ID.get(),var_name.get()))
                       db.commit()
                   tk_Drop_out=tk.Toplevel(root)
                   tk_Drop_out.geometry('200x200')
                   tk_Drop_out.title('Delete Course')
                   Drop_out_ID=tk.IntVar()
                   tk.Label(tk_Drop_out,text='Please enter the Course ID：').place(x=10,y=50)
                   tk.Entry(tk_Drop_out,textvariable=Drop_out_ID).place(x=150,y=50)  
                   tk.Button(tk_Drop_out,text='Delete course confirm',command=comfir_delete).place(x=100,y=100)
               def curriculum_seacher():
                   def curriculum_seacher_dis():
                       sql_curriculum=db.cursor()
                       sql_curriculum.execute("SELECT ID,Name,Credit,Teacherid,Cost,Upper_limit,Number from Course where ID= '%d';"%(curriculum_seacher_ID.get()))
                       curriculum_row=sql_curriculum.fetchone()
                       tk.messagebox.askokcancel('Information',"Course ID:'%d'\nCourse Name：'%s'\nCredit：'%s'\nTeacher ID：'%d'\nFee：'%s'\nPopulation limit：'%d'\nPopulation：'%d'\n"%(curriculum_row[0],curriculum_row[1],curriculum_row[2],curriculum_row[3],curriculum_row[4],curriculum_row[5],curriculum_row[6]))
                   tk_curriculum_seacher=tk.Toplevel(root)
                   tk_curriculum_seacher.geometry('200x200')
                   tk_curriculum_seacher.title('Check course information')
                   curriculum_seacher_ID=tk.IntVar()
                   tk.Label(tk_curriculum_seacher,text='Please enter course ID：').place(x=10,y=50)
                   tk.Entry(tk_curriculum_seacher,textvariable=curriculum_seacher_ID).place(x=150,y=50)  
                   tk.Button(tk_curriculum_seacher,text='Confirm',command=curriculum_seacher_dis).place(x=100,y=100)
               tk_curriculum=tk.Toplevel(root)
               tk_curriculum.geometry('200x200')
               tk_curriculum.title('Check course information')
               tk.Button(tk_curriculum,text='Select course',command=Course_selection).place(x=50,y=50)
               tk.Button(tk_curriculum,text='Drop course',command=Drop_out).place(x=50,y=100)
               tk.Button(tk_curriculum,text='Check course information',command=curriculum_seacher).place(x=50,y=150)
           def achievement():#Check grade
               def record_search():
                   def record_dis():
                       sql_record_dis=db.cursor()
                       sql_record_dis.execute("SELECT Record from Course_selection where Studentid= '%d' and CourseId='%d';"%(var_name.get(),record_search_ID.get()))
                       sql_record_row=sql_record_dis.fetchone()
                       tk.messagebox.askokcancel('Grade checking result','The grade for this course is：%d'%(sql_record_row[0]))
                   tk_record_search=tk.Toplevel(root)
                   tk_record_search.geometry('200x200')
                   tk_record_search.title('Check grade')
                   record_search_ID=tk.IntVar()
                   tk.Label(tk_record_search,text='Please enter course ID：').place(x=10,y=50)
                   tk.Entry(tk_record_search,textvariable=record_search_ID).place(x=150,y=50)  
                   tk.Button(tk_record_search,text='Confirm',command=record_dis).place(x=100,y=100)
               tk_achievement=tk.Toplevel(root)
               tk_achievement.geometry('100x100')
               tk_achievement.title('Check grade')
               tk.Button(tk_achievement,text='Check grade',command=record_search).place(x=50,y=50)
           cu = db.cursor()
           cu.execute("SELECT ID,Password from Student where ID = '%d' and Password='%s';"%(var_name.get(),var_pwd.get()))
           row = cu.fetchone()
           if row:
               student=tk.Toplevel(root)
               student.geometry('200x200')
               student.title('Student server')
               tk.Button(student,text='Check personal identity information',command=identity).place(x=50,y=50)
               tk.Button(student,text='Check course information',command=curriculum).place(x=50,y=100)
               tk.Button(student,text='Check grade',command=achievement).place(x=50,y=150)
           else:
               tk.messagebox.askokcancel('Warning','User or password is wrong')
               root.destroy()
               GUI(1)
       elif judge==2:#Teacher
           cu = db.cursor()
           cu.execute("SELECT ID,Password from Teacher where ID = '%d' and Password='%s';"%(var_name.get(),var_pwd.get()))
           row = cu.fetchone()
           if row:
               def teacher_course():
                    def teacher_search_course():
                        def search_course():
                            sql_search_course=db.cursor()
                            sql_search_course.execute("SELECT ID,Teacherid from Course where ID= '%d' and Teacherid='%d';"%(tk_teacher_search_course_ID.get(),var_name.get()))
                            search_course_row = sql_search_course.fetchone()
                            if search_course_row:
                                sql_search_course1=db.cursor()
                                sql_search_course1.execute("SELECT ID,NAME,Credit,Teacherid,Cost,Upper_limit,Number from Course where ID = '%d' and Teacherid='%d';"%(tk_teacher_search_course_ID.get(),var_name.get()))
                                sql_search_course1_row=sql_search_course1.fetchone()
                                tk.messagebox.askokcancel('Information',"Course ID：'%d'\nCourse Name：'%s'\nCredit：'%s'\nTeacher ID：'%d'\nFee：'%s'\nPopulation limit：'%d'\nPopulation：'%d'"%(sql_search_course1_row[0],sql_search_course1_row[1],sql_search_course1_row[2],sql_search_course1_row[3],sql_search_course1_row[4],sql_search_course1_row[5],sql_search_course1_row[6]))
                            else:
                                tk.messagebox.askokcancel('Warning','You have no checking rights or the course ID is wrong')
                        tk_teacher_search_course=tk.Toplevel(root)
                        tk_teacher_search_course.geometry('200x200')
                        tk_teacher_search_course.title('Teacher server')
                        tk_teacher_search_course_ID=tk.IntVar()
                        tk.Label(tk_teacher_search_course,text='Please enter course ID：').place(x=10,y=50)
                        tk.Entry(tk_teacher_search_course,textvariable=tk_teacher_search_course_ID).place(x=150,y=50)  
                        tk.Button(tk_teacher_search_course,text='Check',command=search_course).place(x=150,y=100)
                    def start_course():
                        def add_course():
                            sql_add_course=db.cursor()
                            sql_add_course.execute("INSERT INTO Course(ID,NAME,Credit,Teacherid,Cost,Upper_limit,Number) VALUES('%d','%s','%s','%s','%s','%d','%d');"%(start_course_ID.get(),start_course_NAME.get(),start_course_Credit.get(),start_course_Teacherid.get(),start_course_Cost.get(),start_course_Upper_limit.get(),start_course_Number))
                            db.commit()
                            tk.messagebox.askokcancel('Warning','Added successfully')
                        tk_start_course=tk.Toplevel(root)
                        tk_start_course.geometry('400x400')
                        tk_start_course.title('Set up course')
                        start_course_ID=tk.IntVar()
                        tk.Label(tk_start_course,text='Please enter course ID：').place(x=10,y=50)
                        tk.Entry(tk_start_course,textvariable=start_course_ID).place(x=150,y=50)  
                        start_course_NAME=tk.StringVar()
                        tk.Label(tk_start_course,text='Please enter course name：').place(x=10,y=100)
                        tk.Entry(tk_start_course,textvariable=start_course_NAME).place(x=150,y=100)  
                        start_course_Credit=tk.StringVar()
                        tk.Label(tk_start_course,text='Please enter course credit：').place(x=10,y=150)
                        tk.Entry(tk_start_course,textvariable=start_course_Credit).place(x=150,y=150)  
                        start_course_Teacherid=var_name
                        start_course_Cost=tk.StringVar()
                        tk.Label(tk_start_course,text='Please enter course fee：').place(x=10,y=200)
                        tk.Entry(tk_start_course,textvariable=start_course_Cost).place(x=150,y=200)  
                        start_course_Upper_limit=tk.IntVar()
                        tk.Label(tk_start_course,text='Please enter course population limit：').place(x=10,y=250)
                        tk.Entry(tk_start_course,textvariable=start_course_Upper_limit).place(x=150,y=250)  
                        start_course_Number=0#initialize the population as 0
                        tk.Button(tk_start_course,text='Set up confirm',command=add_course).place(x=100,y=300)
                    def end_course():
                        def delete_course():
                            sql_delete=db.cursor()
                            sql_delete.execute("delete from  Course where ID='%d' and Teacherid='%d';"%(end_course_ID.get(),var_name.get()))
                            db.commit()
                            delete_course_row=sql_delete.fetchone()
                            if delete_course_row:
                                tk.messagebox.askokcancel('Warning','Successfully!')
                            else:
                                tk.messagebox.askokcancel('Warning','You have no delete rights or the course ID is wrong')
                        tk_end_course=tk.Toplevel(root)
                        tk_end_course.geometry('300x300')
                        tk_end_course.title('End course')
                        end_course_ID=tk.IntVar()
                        tk.Label(tk_end_course,text='Please enter course ID：').place(x=10,y=50)
                        tk.Entry(tk_end_course,textvariable=end_course_ID).place(x=150,y=50)  
                        tk.Button(tk_end_course,text='End course confirm',command=delete_course).place(x=100,y=150)
                    tk_teacher_course=tk.Toplevel(root)
                    tk_teacher_course.geometry('200x200')
                    tk_teacher_course.title('Teacher server')
                    tk.Button(tk_teacher_course,text='Check course',command=teacher_search_course).place(x=50,y=50)
                    tk.Button(tk_teacher_course,text='Set up course',command=start_course).place(x=50,y=100)
                    tk.Button(tk_teacher_course,text='End course',command=end_course).place(x=50,y=150)
               def teacher_student_seacher():
                   def teacher_search_student():
                        sql_teacher_search_student=db.cursor()
                        sql_teacher_search_student.execute("SELECT ID,NAME,Password,Gender,Age,Class,Phone,Address from Student where ID= '%d';"%(teacher_student_seacher_ID.get()))
                        search_student_row=sql_teacher_search_student.fetchone()
                        tk.messagebox.askokcancel('Information','Student ID：%d\nName：%s\nPassword：%s\nGender：%s\nAge：%s\nClass：%s\nPhone：%s\n住址：%s\n'%(search_student_row[0],search_student_row[1],search_student_row[2],search_student_row[3],search_student_row[4],search_student_row[5],search_student_row[6],search_student_row[7]))
                   def Performance_evaluation():
                       def comfir_Performance_evaluation():
                            sql_comfir_Performance_evaluation=db.cursor()
                            sql_comfir_Performance_evaluation.execute("INSERT INTO Course_selection(Studentid,CourseId,Teacherid,Record) VALUES('%d','%d','%d','%d');"%(teacher_student_seacher_ID.get(),Performance_evaluation_ID.get(),var_name.get(),Performance_evaluation_Credit.get()))
                            db.commit()
                            tk.messagebox.askokcancel('Warning','Graded successfully')
                       Performance_evaluation=tk.Toplevel(root)
                       Performance_evaluation.geometry('200x200')
                       Performance_evaluation.title('Grading')
                       Performance_evaluation_ID=tk.IntVar()
                       tk.Label(Performance_evaluation,text='Please enter course ID：').place(x=10,y=50)
                       tk.Entry(Performance_evaluation,textvariable=Performance_evaluation_ID).place(x=150,y=50)  
                       Performance_evaluation_Credit=tk.IntVar()
                       tk.Label(Performance_evaluation,text='Please enter grade：').place(x=10,y=100)
                       tk.Entry(Performance_evaluation,textvariable=Performance_evaluation_Credit).place(x=150,y=100)  
                       tk.Button(Performance_evaluation,text='Confirm',command=comfir_Performance_evaluation).place(x=100,y=150)
                   teacher_student_seacher=tk.Toplevel(root)
                   teacher_student_seacher.geometry('200x200')
                   teacher_student_seacher.title('Teacher server')
                   teacher_student_seacher_ID=tk.IntVar()
                   tk.Label(teacher_student_seacher,text='Please enter student ID：').place(x=10,y=50)
                   tk.Entry(teacher_student_seacher,textvariable=teacher_student_seacher_ID).place(x=150,y=50)  
                   tk.Button(teacher_student_seacher,text='Check confirm',command=teacher_search_student).place(x=50,y=100)
                   tk.Button(teacher_student_seacher,text='Grading',command=Performance_evaluation).place(x=50,y=150)
               def teacher_identity():
                   def teacher_search():
                       teacher_search=db.cursor()
                       teacher_search.execute("SELECT ID,NAME,Password,Gender,Age,Class,Phone,Address from Teacher where ID= %d;"%(var_name.get()))
                       teacher_search_row=teacher_search.fetchone()
                       tk.messagebox.askokcancel('Information',"Teacher ID：'%d'\nName：'%s'\nPassword：'%s'\nGender：'%s'\nAge：'%s'\nClass：'%s'\nPhone：'%s'\nAddress：'%s'\n"%(teacher_search_row[0],teacher_search_row[1],teacher_search_row[2],teacher_search_row[3],teacher_search_row[4],teacher_search_row[5],teacher_search_row[6],teacher_search_row[7]))
                   def modify_teacher():
                       def modify_teacher_ID():
                            def modify_ID():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_modify_teacher_ID=db.cursor()
                               sql_modify_teacher_ID.execute("UPDATE Teacher SET ID='%d' WHERE ID ='%d';"%(teacher_ID.get(),var_name.get()))
                               db.commit()
                            tk_modify_teacher_ID=tk.Toplevel(root)
                            tk_modify_teacher_ID.geometry('200x200')
                            tk_modify_teacher_ID.title('Change teacher ID')
                            teacher_ID=tk.IntVar()
                            tk.Label(tk_modify_teacher_ID,text='Please enter new teacher ID：').place(x=10,y=50)
                            tk.Entry(tk_modify_teacher_ID,textvariable=teacher_ID).place(x=150,y=50)  
                            tk.Button(tk_modify_teacher_ID,text='Change confirm',command=modify_ID).place(x=100,y=100)
                       def modify_teacher_NAME():
                            def modify_NAME():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_modify_teacher_NAME=db.cursor()
                               sql_modify_teacher_NAME.execute("UPDATE Teacher SET NAME='%s' WHERE ID ='%d';"%(teacher_NAME.get(),var_name.get()))
                               db.commit()
                            tk_modify_teacher_NAME=tk.Toplevel(root)
                            tk_modify_teacher_NAME.geometry('200x200')
                            tk_modify_teacher_NAME.title('Change name')
                            teacher_NAME=tk.StringVar()
                            tk.Label(tk_modify_teacher_NAME,text='Please enter new name：').place(x=10,y=50)
                            tk.Entry(tk_modify_teacher_NAME,textvariable=teacher_NAME).place(x=150,y=50)  
                            tk.Button(tk_modify_teacher_NAME,text='Change confirm',command=modify_NAME).place(x=100,y=100)
                       def modify_teacher_Password(): 
                            def modify_Password():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_modify_teacher_Password=db.cursor()
                               sql_modify_teacher_Password.execute("UPDATE Teacher SET Password='%s' WHERE ID ='%d';"%(teacher_Password.get(),var_name.get()))
                               db.commit()
                            tk_modify_teacher_Password=tk.Toplevel(root)
                            tk_modify_teacher_Password.geometry('200x200')
                            tk_modify_teacher_Password.title('Change password')
                            teacher_Password=tk.StringVar()
                            tk.Label(tk_modify_teacher_Password,text='Please enter new password：').place(x=10,y=50)
                            tk.Entry(tk_modify_teacher_Password,textvariable=teacher_Password).place(x=150,y=50)  
                            tk.Button(tk_modify_teacher_Password,text='Change confirm',command=modify_Password).place(x=100,y=100)
                       def modify_teacher_Gender():   
                            def modify_Gender():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_modify_teacher_Gender=db.cursor()
                               sql_modify_teacher_Gender.execute("UPDATE Teacher SET Gender='%s' WHERE ID ='%d';"%(teacher_Gender.get(),var_name.get()))
                               db.commit()
                            tk_modify_teacher_Gender=tk.Toplevel(root)
                            tk_modify_teacher_Gender.geometry('200x200')
                            tk_modify_teacher_Gender.title('Change gender')
                            teacher_Gender=tk.StringVar()
                            tk.Label(tk_modify_teacher_Gender,text='Please enter gender：').place(x=10,y=50)
                            tk.Entry(tk_modify_teacher_Gender,textvariable=teacher_Gender).place(x=150,y=50)  
                            tk.Button(tk_modify_teacher_Gender,text='Change confirm',command=modify_Gender).place(x=100,y=100)
                       def modify_teacher_Age(): 
                            def modify_Age():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_modify_teacher_Age=db.cursor()
                               sql_modify_teacher_Age.execute("UPDATE Teacher SET Age='%s' WHERE ID ='%d';"%(teacher_Age.get(),var_name.get()))
                               db.commit()
                            tk_modify_teacher_Age=tk.Toplevel(root)
                            tk_modify_teacher_Age.geometry('200x200')
                            tk_modify_teacher_Age.title('Change age')
                            teacher_Age=tk.StringVar()
                            tk.Label(tk_modify_teacher_Age,text='Please enter new age：').place(x=10,y=50)
                            tk.Entry(tk_modify_teacher_Age,textvariable=teacher_Age).place(x=150,y=50)  
                            tk.Button(tk_modify_teacher_Age,text='Change confirm',command=modify_Age).place(x=100,y=100)
                       def modify_teacher_Class(): 
                            def modify_Class():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_modify_teacher_Class=db.cursor()
                               sql_modify_teacher_Class.execute("UPDATE Teacher SET Class='%s' WHERE ID ='%d';"%(teacher_Class.get(),var_name.get()))
                               db.commit()
                            tk_modify_teacher_Class=tk.Toplevel(root)
                            tk_modify_teacher_Class.geometry('200x200')
                            tk_modify_teacher_Class.title('Change class')
                            teacher_Class=tk.StringVar()
                            tk.Label(tk_modify_teacher_Class,text='Please enter new class：').place(x=10,y=50)
                            tk.Entry(tk_modify_teacher_Class,textvariable=teacher_Class).place(x=150,y=50)  
                            tk.Button(tk_modify_teacher_Class,text='Change confirm',command=modify_Class).place(x=100,y=100)
                       def modify_teacher_Phone():
                            def modify_Phone():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_modify_teacher_Phone=db.cursor()
                               sql_modify_teacher_Phone.execute("UPDATE Teacher SET Phone='%s' WHERE ID ='%d';"%(teacher_Phone.get(),var_name.get()))
                               db.commit()
                            tk_modify_teacher_Phone=tk.Toplevel(root)
                            tk_modify_teacher_Phone.geometry('200x200')
                            tk_modify_teacher_Phone.title('Change phone')
                            teacher_Phone=tk.StringVar()
                            tk.Label(tk_modify_teacher_Phone,text='Please enter new phone：').place(x=10,y=50)
                            tk.Entry(tk_modify_teacher_Phone,textvariable=teacher_Phone).place(x=150,y=50)  
                            tk.Button(tk_modify_teacher_Phone,text='Change confirm',command=modify_Phone).place(x=100,y=100)
                       def modify_teacher_Address():
                            def modify_Address():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_modify_teacher_Address=db.cursor()
                               sql_modify_teacher_Address.execute("UPDATE Teacher SET Address='%s' WHERE ID ='%d';"%(teacher_Address.get(),var_name.get()))
                               db.commit()
                            tk_modify_teacher_Address=tk.Toplevel(root)
                            tk_modify_teacher_Address.geometry('200x200')
                            tk_modify_teacher_Address.title('Change address')
                            teacher_Address=tk.StringVar()
                            tk.Label(tk_modify_teacher_Address,text='Please enter new address：').place(x=10,y=50)
                            tk.Entry(tk_modify_teacher_Address,textvariable=teacher_Address).place(x=150,y=50)  
                            tk.Button(tk_modify_teacher_Address,text='Change confirm',command=modify_Address).place(x=100,y=100)
                       modify_teacher=tk.Toplevel(root)
                       modify_teacher.geometry('200x500')
                       modify_teacher.title('Change information')
                       tk.Button(modify_teacher,text='Change teacher ID',command=modify_teacher_ID).place(x=50,y=50)
                       tk.Button(modify_teacher,text='Change name',command=modify_teacher_NAME).place(x=50,y=100)
                       tk.Button(modify_teacher,text='Change password',command=modify_teacher_Password).place(x=50,y=150)
                       tk.Button(modify_teacher,text='Change gender',command=modify_teacher_Gender).place(x=50,y=200)
                       tk.Button(modify_teacher,text='Change age',command=modify_teacher_Age).place(x=50,y=250)
                       tk.Button(modify_teacher,text='Change class',command=modify_teacher_Class).place(x=50,y=300)
                       tk.Button(modify_teacher,text='Change phone',command=modify_teacher_Phone).place(x=50,y=350)
                       tk.Button(modify_teacher,text='Change address',command=modify_teacher_Address).place(x=50,y=400)
                   teacher_identity=tk.Toplevel(root)
                   teacher_identity.geometry('200x200')
                   teacher_identity.title('teacher server')
                   tk.Button(teacher_identity,text='Check identity information',command=teacher_search).place(x=50,y=50)
                   tk.Button(teacher_identity,text='Change identity information',command=modify_teacher).place(x=50,y=100)
               tk_teacher=tk.Toplevel(root)
               tk_teacher.geometry('200x250')
               tk_teacher.title('teacher server')
               tk.Button(tk_teacher,text='Check identity information',command=teacher_identity).place(x=50,y=50)
               tk.Button(tk_teacher,text='Check course information',command=teacher_course).place(x=50,y=100)
               tk.Button(tk_teacher,text='Check student information',command=teacher_student_seacher).place(x=50,y=150)
           else:
               tk.messagebox.askokcancel('Warning','User or password is wrong')
               root.destroy()
               GUI(2)
       else:
           cu = db.cursor()
           cu.execute("SELECT ID,Password from Administrators where ID = '%d' and Password='%s';"%(var_name.get(),var_pwd.get()))
           row = cu.fetchone()
           if row:
               def administrators_search_student():
                   def comfir_search_student():
                       sql_comfir_search_student=db.cursor()
                       sql_comfir_search_student.execute("SELECT ID,NAME,Password,Gender,Age,Class,Phone,Address from Student where ID= %d;"%(administrators_search_student_ID.get()))
                       comfir_search_student_row=sql_comfir_search_student.fetchone()
                       tk.messagebox.askokcancel('Information',"Student ID：'%d'\nName：'%s'\nPassword：'%s'\nGender：'%s'\nAge：'%s'\nClass：'%s'\nPhone：'%s'\nAddress：'%s'\n"%(comfir_search_student_row[0],comfir_search_student_row[1],comfir_search_student_row[2],comfir_search_student_row[3],comfir_search_student_row[4],comfir_search_student_row[5],comfir_search_student_row[6],comfir_search_student_row[7]))
                   def administrators_modify_student():
                       def administrators_modify_student_ID():
                            def ad_modify_student_ID():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_student_ID=db.cursor()
                               sql_ad_modify_student_ID.execute("UPDATE Student SET ID='%s' WHERE ID ='%d';"%(modify_student_ID.get(),administrators_search_student_ID.get()))
                               db.commit()
                            tk_administrators_modify_student_ID=tk.Toplevel(root)
                            tk_administrators_modify_student_ID.geometry('200x200')
                            tk_administrators_modify_student_ID.title('Change student ID')
                            modify_student_ID=tk.IntVar()
                            tk.Label(tk_administrators_modify_student_ID,text='Please enter new Student ID：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_student_ID,textvariable=modify_student_ID).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_student_ID,text='Change confirm',command=ad_modify_student_ID).place(x=100,y=100)
                       def administrators_modify_student_NAME():
                            def ad_modify_student_NAME():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_student_NAME=db.cursor()
                               sql_ad_modify_student_NAME.execute("UPDATE Student SET NAME='%s' WHERE ID ='%d';"%(modify_student_NAME.get(),administrators_search_student_ID.get()))
                               db.commit()
                            tk_administrators_modify_student_NAME=tk.Toplevel(root)
                            tk_administrators_modify_student_NAME.geometry('200x200')
                            tk_administrators_modify_student_NAME.title('Change name')
                            modify_student_NAME=tk.StringVar()
                            tk.Label(tk_administrators_modify_student_NAME,text='Please enter new name：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_student_NAME,textvariable=modify_student_NAME).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_student_NAME,text='Change confirm',command=ad_modify_student_NAME).place(x=100,y=100)
                       def administrators_modify_student_Password():
                            def ad_modify_student_Password():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_student_Password=db.cursor()
                               sql_ad_modify_student_Password.execute("UPDATE Student SET Password='%s' WHERE ID ='%d';"%(modify_student_Password.get(),administrators_search_student_ID.get()))
                               db.commit()
                            tk_administrators_modify_student_Password=tk.Toplevel(root)
                            tk_administrators_modify_student_Password.geometry('200x200')
                            tk_administrators_modify_student_Password.title('Change password')
                            modify_student_Password=tk.StringVar()
                            tk.Label(tk_administrators_modify_student_Password,text='Please enter new code：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_student_Password,textvariable=modify_student_Password).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_student_Password,text='Change confirm',command=ad_modify_student_Password).place(x=100,y=100)
                       def administrators_modify_student_Gender():
                            def ad_modify_student_Gender():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_student_Gender=db.cursor()
                               sql_ad_modify_student_Gender.execute("UPDATE Student SET Gender='%s' WHERE ID ='%d';"%(modify_student_Gender.get(),administrators_search_student_ID.get()))
                               db.commit()
                            tk_administrators_modify_student_Gender=tk.Toplevel(root)
                            tk_administrators_modify_student_Gender.geometry('200x200')
                            tk_administrators_modify_student_Gender.title('Change gender')
                            modify_student_Gender=tk.StringVar()
                            tk.Label(tk_administrators_modify_student_Gender,text='Please enter gender：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_student_Gender,textvariable=modify_student_Gender).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_student_Gender,text='Change confirm',command=ad_modify_student_Gender).place(x=100,y=100)
                       def administrators_modify_student_Age():
                            def ad_modify_student_Age():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_student_Age=db.cursor()
                               sql_ad_modify_student_Age.execute("UPDATE Student SET Age='%s' WHERE ID ='%d';"%(modify_student_Age.get(),administrators_search_student_ID.get()))
                               db.commit()
                            tk_administrators_modify_student_Age=tk.Toplevel(root)
                            tk_administrators_modify_student_Age.geometry('200x200')
                            tk_administrators_modify_student_Age.title('Change age')
                            modify_student_Age=tk.StringVar()
                            tk.Label(tk_administrators_modify_student_Age,text='Please enter new age：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_student_Age,textvariable=modify_student_Age).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_student_Age,text='Change confirm',command=ad_modify_student_Age).place(x=100,y=100)
                       def administrators_modify_student_Class():
                            def ad_modify_student_Class():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_student_Class=db.cursor()
                               sql_ad_modify_student_Class.execute("UPDATE Student SET Class='%s' WHERE ID ='%d';"%(modify_student_Class.get(),administrators_search_student_ID.get()))
                               db.commit()
                            tk_administrators_modify_student_Class=tk.Toplevel(root)
                            tk_administrators_modify_student_Class.geometry('200x200')
                            tk_administrators_modify_student_Class.title('Change class')
                            modify_student_Class=tk.StringVar()
                            tk.Label(tk_administrators_modify_student_Class,text='Please enter new class：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_student_Class,textvariable=modify_student_Class).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_student_Class,text='Change confirm',command=ad_modify_student_Class).place(x=100,y=100)
                       def administrators_modify_student_Phone():
                            def ad_modify_student_Phone():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_student_Class=db.cursor()
                               sql_ad_modify_student_Class.execute("UPDATE Student SET Phone='%s' WHERE ID ='%d';"%(modify_student_Phone.get(),administrators_search_student_ID.get()))
                               db.commit()
                            tk_administrators_modify_student_Phone=tk.Toplevel(root)
                            tk_administrators_modify_student_Phone.geometry('200x200')
                            tk_administrators_modify_student_Phone.title('Change class')
                            modify_student_Phone=tk.StringVar()
                            tk.Label(tk_administrators_modify_student_Phone,text='Please enter new class：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_student_Phone,textvariable=modify_student_Phone).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_student_Phone,text='Change confirm',command=ad_modify_student_Phone).place(x=100,y=100)
                       def administrators_modify_student_Address():
                            def ad_modify_student_Address():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_student_Address=db.cursor()
                               sql_ad_modify_student_Address.execute("UPDATE Student SET Address='%s' WHERE ID ='%d';"%(modify_student_Address.get(),administrators_search_student_ID.get()))
                               db.commit()
                            tk_administrators_modify_student_Address=tk.Toplevel(root)
                            tk_administrators_modify_student_Address.geometry('200x200')
                            tk_administrators_modify_student_Address.title('Change class')
                            modify_student_Address=tk.StringVar()
                            tk.Label(tk_administrators_modify_student_Address,text='Please enter new class：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_student_Address,textvariable=modify_student_Address).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_student_Address,text='Change confirm',command=ad_modify_student_Address).place(x=100,y=100)
                       tk_administrators_modify_student=tk.Toplevel(root)
                       tk_administrators_modify_student.geometry('200x500')
                       tk_administrators_modify_student.title('Change student information')
                       tk.Button(tk_administrators_modify_student,text='Change student ID',command=administrators_modify_student_ID).place(x=50,y=50)
                       tk.Button(tk_administrators_modify_student,text='Change name',command=administrators_modify_student_NAME).place(x=50,y=100)
                       tk.Button(tk_administrators_modify_student,text='Change password',command=administrators_modify_student_Password).place(x=50,y=150)
                       tk.Button(tk_administrators_modify_student,text='Change gender',command=administrators_modify_student_Gender).place(x=50,y=200)
                       tk.Button(tk_administrators_modify_student,text='Change age',command=administrators_modify_student_Age).place(x=50,y=250)
                       tk.Button(tk_administrators_modify_student,text='Change class',command=administrators_modify_student_Class).place(x=50,y=300)
                       tk.Button(tk_administrators_modify_student,text='Change phone',command=administrators_modify_student_Phone).place(x=50,y=350)
                       tk.Button(tk_administrators_modify_student,text='Change address',command=administrators_modify_student_Address).place(x=50,y=400)
                   tk_administrators_search_student=tk.Toplevel(root)
                   tk_administrators_search_student.geometry('200x200')
                   tk_administrators_search_student.title('Check student information')
                   administrators_search_student_ID=tk.IntVar()
                   tk.Label(tk_administrators_search_student,text='Please enter student ID').place(x=10,y=50)
                   tk.Entry(tk_administrators_search_student,textvariable=administrators_search_student_ID).place(x=150,y=50)  
                   tk.Button(tk_administrators_search_student,text='Check confirm',command=comfir_search_student).place(x=100,y=100)
                   tk.Button(tk_administrators_search_student,text='Change information',command=administrators_modify_student).place(x=100,y=150)
               def administrators_search_teacher():
                   def comfir_search_teacher():
                       sql_comfir_search_teacher=db.cursor()
                       sql_comfir_search_teacher.execute("SELECT ID,NAME,Password,Gender,Age,Class,Phone,Address from Teacher where ID= %d;"%(administrators_search_teacher_ID.get()))
                       comfir_search_teacher_row=sql_comfir_search_teacher.fetchone()
                       tk.messagebox.askokcancel('Information',"Teacher ID：'%d'\nName：'%s'\nPassword：'%s'\nGender：'%s'\nAge：'%s'\nClass：'%s'\nPhone：'%s'\nAddress：'%s'\n"%(comfir_search_teacher_row[0],comfir_search_teacher_row[1],comfir_search_teacher_row[2],comfir_search_teacher_row[3],comfir_search_teacher_row[4],comfir_search_teacher_row[5],comfir_search_teacher_row[6],comfir_search_teacher_row[7]))
                   def administrators_modify_teacher():
                       def administrators_modify_teacher_ID():
                            def ad_modify_teacher_ID():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_teacher_ID=db.cursor()
                               sql_ad_modify_teacher_ID.execute("UPDATE Teacher SET ID='%d' WHERE ID ='%d';"%(modify_teacher_ID.get(),administrators_search_teacher_ID.get()))
                               db.commit()
                            tk_administrators_modify_teacher_ID=tk.Toplevel(root)
                            tk_administrators_modify_teacher_ID.geometry('200x200')
                            tk_administrators_modify_teacher_ID.title('Change teacher ID')
                            modify_teacher_ID=tk.IntVar()
                            tk.Label(tk_administrators_modify_teacher_ID,text='Please enter new teacher ID：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_teacher_ID,textvariable=modify_teacher_ID).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_teacher_ID,text='Change confirm',command=ad_modify_teacher_ID).place(x=100,y=100)
                       def administrators_modify_teacher_NAME():
                            def ad_modify_teacher_NAME():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_teacher_NAME=db.cursor()
                               sql_ad_modify_teacher_NAME.execute("UPDATE Teacher SET NAME='%s' WHERE ID ='%d';"%(modify_teacher_NAME.get(),administrators_search_teacher_ID.get()))
                               db.commit()
                            tk_administrators_modify_teacher_NAME=tk.Toplevel(root)
                            tk_administrators_modify_teacher_NAME.geometry('200x200')
                            tk_administrators_modify_teacher_NAME.title('Change name')
                            modify_teacher_NAME=tk.StringVar()
                            tk.Label(tk_administrators_modify_teacher_NAME,text='Please enter new name：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_teacher_NAME,textvariable=modify_teacher_NAME).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_teacher_NAME,text='Change confirm',command=ad_modify_teacher_NAME).place(x=100,y=100)
                       def administrators_modify_teacher_Password():
                            def ad_modify_teacher_Password():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_teacher_Password=db.cursor()
                               sql_ad_modify_teacher_Password.execute("UPDATE Teacher SET Password='%s' WHERE ID ='%d';"%(modify_teacher_Password.get(),administrators_search_teacher_ID.get()))
                               db.commit()
                            tk_administrators_modify_teacher_Password=tk.Toplevel(root)
                            tk_administrators_modify_teacher_Password.geometry('200x200')
                            tk_administrators_modify_teacher_Password.title('Change password')
                            modify_teacher_Password=tk.StringVar()
                            tk.Label(tk_administrators_modify_teacher_Password,text='Please enter new password：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_teacher_Password,textvariable=modify_teacher_Password).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_teacher_Password,text='Change confirm',command=ad_modify_teacher_Password).place(x=100,y=100)
                       def administrators_modify_teacher_Gender():
                            def ad_modify_teacher_Gender():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_teacher_Gender=db.cursor()
                               sql_ad_modify_teacher_Gender.execute("UPDATE Teacher SET Gender='%s' WHERE ID ='%d';"%(modify_teacher_Gender.get(),administrators_search_teacher_ID.get()))
                               db.commit()
                            tk_administrators_modify_teacher_Gender=tk.Toplevel(root)
                            tk_administrators_modify_teacher_Gender.geometry('200x200')
                            tk_administrators_modify_teacher_Gender.title('Change gender')
                            modify_teacher_Gender=tk.StringVar()
                            tk.Label(tk_administrators_modify_teacher_Gender,text='Please enter gender：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_teacher_Gender,textvariable=modify_teacher_Gender).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_teacher_Gender,text='Change confirm',command=ad_modify_teacher_Gender).place(x=100,y=100)
                       def administrators_modify_teacher_Age():
                            def ad_modify_teacher_Age():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_teacher_Age=db.cursor()
                               sql_ad_modify_teacher_Age.execute("UPDATE Teacher SET Age='%s' WHERE ID ='%d';"%(modify_teacher_Age.get(),administrators_search_teacher_ID.get()))
                               db.commit()
                            tk_administrators_modify_teacher_Age=tk.Toplevel(root)
                            tk_administrators_modify_teacher_Age.geometry('200x200')
                            tk_administrators_modify_teacher_Age.title('Change age')
                            modify_teacher_Age=tk.StringVar()
                            tk.Label(tk_administrators_modify_teacher_Age,text='Please enter new age：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_teacher_Age,textvariable=modify_teacher_Age).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_teacher_Age,text='Change confirm',command=ad_modify_teacher_Age).place(x=100,y=100)
                       def administrators_modify_teacher_Class():
                            def ad_modify_teacher_Class():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_teacher_Class=db.cursor()
                               sql_ad_modify_teacher_Class.execute("UPDATE Teacher SET Class='%s' WHERE ID ='%d';"%(modify_teacher_Class.get(),administrators_search_teacher_ID.get()))
                               db.commit()
                            tk_administrators_modify_teacher_Class=tk.Toplevel(root)
                            tk_administrators_modify_teacher_Class.geometry('200x200')
                            tk_administrators_modify_teacher_Class.title('Change class')
                            modify_teacher_Class=tk.StringVar()
                            tk.Label(tk_administrators_modify_teacher_Class,text='Please enter new class：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_teacher_Class,textvariable=modify_teacher_Class).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_teacher_Class,text='Change confirm',command=ad_modify_teacher_Class).place(x=100,y=100)
                       def administrators_modify_teacher_Phone():
                            def ad_modify_teacher_Phone():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_teacher_Class=db.cursor()
                               sql_ad_modify_teacher_Class.execute("UPDATE Teacher SET Phone='%s' WHERE ID ='%d';"%(modify_teacher_Phone.get(),administrators_search_teacher_ID.get()))
                               db.commit()
                            tk_administrators_modify_teacher_Phone=tk.Toplevel(root)
                            tk_administrators_modify_teacher_Phone.geometry('200x200')
                            tk_administrators_modify_teacher_Phone.title('Change phone')
                            modify_teacher_Phone=tk.StringVar()
                            tk.Label(tk_administrators_modify_teacher_Phone,text='Please enter new phone：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_teacher_Phone,textvariable=modify_teacher_Phone).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_teacher_Phone,text='Change confirm',command=ad_modify_teacher_Phone).place(x=100,y=100)
                       def administrators_modify_teacher_Address():
                            def ad_modify_teacher_Address():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_teacher_Address=db.cursor()
                               sql_ad_modify_teacher_Address.execute("UPDATE Teacher SET Address='%s' WHERE ID ='%d';"%(modify_teacher_Address.get(),administrators_search_teacher_ID.get()))
                               db.commit()
                            tk_administrators_modify_teacher_Address=tk.Toplevel(root)
                            tk_administrators_modify_teacher_Address.geometry('200x200')
                            tk_administrators_modify_teacher_Address.title('Change address')
                            modify_teacher_Address=tk.StringVar()
                            tk.Label(tk_administrators_modify_teacher_Address,text='Please enter new address：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_teacher_Address,textvariable=modify_teacher_Address).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_teacher_Address,text='Change confirm',command=ad_modify_teacher_Address).place(x=100,y=100)
                       tk_administrators_modify_teacher=tk.Toplevel(root)
                       tk_administrators_modify_teacher.geometry('200x500')
                       tk_administrators_modify_teacher.title('Change teacher information')
                       tk.Button(tk_administrators_modify_teacher,text='Change teacher ID',command=administrators_modify_teacher_ID).place(x=50,y=50)
                       tk.Button(tk_administrators_modify_teacher,text='Change name',command=administrators_modify_teacher_NAME).place(x=50,y=100)
                       tk.Button(tk_administrators_modify_teacher,text='Change password',command=administrators_modify_teacher_Password).place(x=50,y=150)
                       tk.Button(tk_administrators_modify_teacher,text='Change gender',command=administrators_modify_teacher_Gender).place(x=50,y=200)
                       tk.Button(tk_administrators_modify_teacher,text='Change age',command=administrators_modify_teacher_Age).place(x=50,y=250)
                       tk.Button(tk_administrators_modify_teacher,text='Change class',command=administrators_modify_teacher_Class).place(x=50,y=300)
                       tk.Button(tk_administrators_modify_teacher,text='Change phone',command=administrators_modify_teacher_Phone).place(x=50,y=350)
                       tk.Button(tk_administrators_modify_teacher,text='Change address',command=administrators_modify_teacher_Address).place(x=50,y=400)
                   tk_administrators_search_teacher=tk.Toplevel(root)
                   tk_administrators_search_teacher.geometry('200x200')
                   tk_administrators_search_teacher.title('Check teacher information')
                   administrators_search_teacher_ID=tk.IntVar()
                   tk.Label(tk_administrators_search_teacher,text='Please enter teacher ID').place(x=10,y=50)
                   tk.Entry(tk_administrators_search_teacher,textvariable=administrators_search_teacher_ID).place(x=150,y=50)  
                   tk.Button(tk_administrators_search_teacher,text='Check confirm',command=comfir_search_teacher).place(x=100,y=100)
                   tk.Button(tk_administrators_search_teacher,text='Change information',command=administrators_modify_teacher).place(x=100,y=150)
               def administrators_search_course():
                   def comfir_search_course():
                       sql_comfir_search_course=db.cursor()
                       sql_comfir_search_course.execute("SELECT ID,NAME,Credit,Teacherid,Cost,Upper_limit,Number from Course where ID= '%d';"%(administrators_search_course_ID.get()))
                       comfir_search_course_row=sql_comfir_search_course.fetchone()
                       tk.messagebox.askokcancel('Information',"Course ID：'%d'\nCourse Name：'%s'\nCredit：'%s'\nTeacher ID：'%d'\nFee：'%s'\nPopulation Limit：'%d'\nPopulation：'%d'"%(comfir_search_course_row[0],comfir_search_course_row[1],comfir_search_course_row[2],comfir_search_course_row[3],comfir_search_course_row[4],comfir_search_course_row[5],comfir_search_course_row[6]))
                   def administrators_modify_course():
                       def administrators_modify_course_ID():
                            def ad_modify_course_ID():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_course_ID=db.cursor()
                               sql_ad_modify_course_ID.execute("UPDATE Course SET ID='%d' WHERE ID='%d';"%(modify_course_ID.get(),administrators_search_course_ID.get()))
                               db.commit()
                            tk_administrators_modify_course_ID=tk.Toplevel(root)
                            tk_administrators_modify_course_ID.geometry('200x200')
                            tk_administrators_modify_course_ID.title('Change course ID')
                            modify_course_ID=tk.IntVar()
                            tk.Label(tk_administrators_modify_course_ID,text='Please enter new course ID：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_course_ID,textvariable=modify_course_ID).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_course_ID,text='Change confirm',command=ad_modify_course_ID).place(x=100,y=100)
                       def administrators_modify_course_NAME(): 
                            def ad_modify_course_NAME():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_course_NAME=db.cursor()
                               sql_ad_modify_course_NAME.execute("UPDATE Course SET NAME='%s' WHERE ID ='%d';"%(modify_course_NAME.get(),administrators_search_course_ID.get()))
                               db.commit()
                            tk_administrators_modify_course_NAME=tk.Toplevel(root)
                            tk_administrators_modify_course_NAME.geometry('200x200')
                            tk_administrators_modify_course_NAME.title('Change course name')
                            modify_course_NAME=tk.StringVar()
                            tk.Label(tk_administrators_modify_course_NAME,text='Please enter new course name：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_course_NAME,textvariable=modify_course_NAME).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_course_NAME,text='Change confirm',command=ad_modify_course_NAME).place(x=100,y=100)
                       def administrators_modify_course_Credit(): 
                            def ad_modify_course_Credit():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_course_Credit=db.cursor()
                               sql_ad_modify_course_Credit.execute("UPDATE Course SET Credit='%s' WHERE ID ='%d';"%(modify_course_Credit.get(),administrators_search_course_ID.get()))
                               db.commit()
                            tk_administrators_modify_course_Credit=tk.Toplevel(root)
                            tk_administrators_modify_course_Credit.geometry('200x200')
                            tk_administrators_modify_course_Credit.title('Change credit')
                            modify_course_Credit=tk.StringVar()
                            tk.Label(tk_administrators_modify_course_Credit,text='Please enter new credit：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_course_Credit,textvariable=modify_course_Credit).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_course_Credit,text='Change confirm',command=ad_modify_course_Credit).place(x=100,y=100)
                       def administrators_modify_course_Teacherid(): 
                            def ad_modify_course_Teacherid():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_course_NAME=db.cursor()
                               sql_ad_modify_course_NAME.execute("UPDATE Course SET Teacherid='%d' WHERE ID ='%d';"%(modify_course_NAME.get(),administrators_search_course_ID.get()))
                               db.commit()
                            tk_administrators_modify_course_NAME=tk.Toplevel(root)
                            tk_administrators_modify_course_NAME.geometry('200x200')
                            tk_administrators_modify_course_NAME.title('Change teacher ID')
                            modify_course_NAME=tk.IntVar()
                            tk.Label(tk_administrators_modify_course_NAME,text='Please enter new teacher ID：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_course_NAME,textvariable=modify_course_NAME).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_course_NAME,text='Change confirm',command=ad_modify_course_Teacherid).place(x=100,y=100)
                       def administrators_modify_course_Cost(): 
                            def ad_modify_course_course_Cost():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_course_course_Cost=db.cursor()
                               sql_ad_modify_course_course_Cost.execute("UPDATE Course SET course_Cost='%s' WHERE ID ='%d';"%(modify_course_course_Cost.get(),administrators_search_course_ID.get()))
                               db.commit()
                            tk_administrators_modify_course_course_Cost=tk.Toplevel(root)
                            tk_administrators_modify_course_course_Cost.geometry('200x200')
                            tk_administrators_modify_course_course_Cost.title('Change course fee')
                            modify_course_course_Cost=tk.StringVar()
                            tk.Label(tk_administrators_modify_course_course_Cost,text='Please enter new fee：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_course_course_Cost,textvariable=modify_course_course_Cost).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_course_course_Cost,text='Change confirm',command=ad_modify_course_course_Cost).place(x=100,y=100)
                       def administrators_modify_course_Upper_limit():  
                            def ad_modify_course_Upper_limit():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_course_Upper_limit=db.cursor()
                               sql_ad_modify_course_Upper_limit.execute("UPDATE Course SET Upper_limit='%d' WHERE ID ='%d';"%(modify_course_Upper_limit.get(),administrators_search_course_ID.get()))
                               db.commit()
                            tk_administrators_modify_course_Upper_limit=tk.Toplevel(root)
                            tk_administrators_modify_course_Upper_limit.geometry('200x200')
                            tk_administrators_modify_course_Upper_limit.title('Change population limit')
                            modify_course_Upper_limit=tk.IntVar()
                            tk.Label(tk_administrators_modify_course_Upper_limit,text='Please enter new population limit：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_course_Upper_limit,textvariable=modify_course_Upper_limit).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_course_Upper_limit,text='Change confirm',command=ad_modify_course_Upper_limit).place(x=100,y=100)
                       def administrators_modify_course_Number(): 
                            def ad_modify_course_Number():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_course_Number=db.cursor()
                               sql_ad_modify_course_Number.execute("UPDATE Course SET Number='%d' WHERE ID ='%d';"%(modify_course_Number.get(),administrators_search_course_ID.get()))
                               db.commit()
                            tk_administrators_modify_course_Number=tk.Toplevel(root)
                            tk_administrators_modify_course_Number.geometry('200x200')
                            tk_administrators_modify_course_Number.title('Change population')
                            modify_course_Number=tk.IntVar()
                            tk.Label(tk_administrators_modify_course_Number,text='Please enter new population：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_course_Number,textvariable=modify_course_Number).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_course_Number,text='Change confirm',command=ad_modify_course_Number).place(x=100,y=100)
                       tk_administrators_modify_course=tk.Toplevel(root)
                       tk_administrators_modify_course.geometry('200x400')
                       tk_administrators_modify_course.title('Change student information')
                       tk.Button(tk_administrators_modify_course,text='Change course ID',command=administrators_modify_course_ID).place(x=50,y=50)
                       tk.Button(tk_administrators_modify_course,text='Change course name',command=administrators_modify_course_NAME).place(x=50,y=100)
                       tk.Button(tk_administrators_modify_course,text='Change credit',command=administrators_modify_course_Credit).place(x=50,y=150)
                       tk.Button(tk_administrators_modify_course,text='Change teacher ID',command=administrators_modify_course_Teacherid).place(x=50,y=200)
                       tk.Button(tk_administrators_modify_course,text='Change course fee',command=administrators_modify_course_Cost).place(x=50,y=250)
                       tk.Button(tk_administrators_modify_course,text='Change population limit',command=administrators_modify_course_Upper_limit).place(x=50,y=300)
                       tk.Button(tk_administrators_modify_course,text='Change population',command=administrators_modify_course_Number).place(x=50,y=350)
                   tk_administrators_search_course=tk.Toplevel(root)
                   tk_administrators_search_course.geometry('200x200')
                   tk_administrators_search_course.title('Check course information')
                   administrators_search_course_ID=tk.IntVar()
                   tk.Label(tk_administrators_search_course,text='Please enter course ID').place(x=10,y=50)
                   tk.Entry(tk_administrators_search_course,textvariable=administrators_search_course_ID).place(x=150,y=50)  
                   tk.Button(tk_administrators_search_course,text='Check confirm',command=comfir_search_course).place(x=100,y=100)
                   tk.Button(tk_administrators_search_course,text='Change information',command=administrators_modify_course).place(x=100,y=150)
               def administrators_search_personal():
                   def comfir_search_personal():
                       sql_comfir_search_personal=db.cursor()
                       sql_comfir_search_personal.execute("SELECT ID,NAME,Password,Age,Phone,Address from Administrators where ID='%s';"%(administrators_search_personal_ID.get()))
                       comfir_search_personal_row=sql_comfir_search_personal.fetchone()
                       tk.messagebox.askokcancel('Information',"teacher ID：'%d'\n name：'%s'\n password：'%s'\n age：'%s'\n phone：'%s'\n address：'%s'\n"%(comfir_search_personal_row[0],comfir_search_personal_row[1],comfir_search_personal_row[2],comfir_search_personal_row[3],comfir_search_personal_row[4],comfir_search_personal_row[5]))
                   def administrators_modify_personal():
                       def administrators_modify_personal_ID():
                            def ad_modify_personal_ID():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_personal_ID=db.cursor()
                               sql_ad_modify_personal_ID.execute("UPDATE Administrators SET ID='%d' WHERE ID ='%d';"%(modify_personal_ID.get(),administrators_search_personal_ID.get()))
                               db.commit()
                            tk_administrators_modify_personal_ID=tk.Toplevel(root)
                            tk_administrators_modify_personal_ID.geometry('200x200')
                            tk_administrators_modify_personal_ID.title('Change teacher ID')
                            modify_personal_ID=tk.IntVar()
                            tk.Label(tk_administrators_modify_personal_ID,text='Please enter new teacher ID：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_personal_ID,textvariable=modify_personal_ID).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_personal_ID,text='Change confirm',command=ad_modify_personal_ID).place(x=100,y=100)
                       def administrators_modify_personal_NAME():
                            def ad_modify_personal_NAME():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_personal_NAME=db.cursor()
                               sql_ad_modify_personal_NAME.execute("UPDATE Administrators SET NAME='%s' WHERE ID ='%d';"%(modify_personal_NAME.get(),administrators_search_personal_ID.get()))
                               db.commit()
                            tk_administrators_modify_personal_NAME=tk.Toplevel(root)
                            tk_administrators_modify_personal_NAME.geometry('200x200')
                            tk_administrators_modify_personal_NAME.title('Change name')
                            modify_personal_NAME=tk.StringVar()
                            tk.Label(tk_administrators_modify_personal_NAME,text='Please enter new name：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_personal_NAME,textvariable=modify_personal_NAME).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_personal_NAME,text='Change confirm',command=ad_modify_personal_NAME).place(x=100,y=100)
                       def administrators_modify_personal_Password():
                            def ad_modify_personal_Password():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_personal_Password=db.cursor()
                               sql_ad_modify_personal_Password.execute("UPDATE Administrators SET Password='%s' WHERE ID ='%d';"%(modify_personal_Password.get(),administrators_search_personal_ID.get()))
                               db.commit()
                            tk_administrators_modify_personal_Password=tk.Toplevel(root)
                            tk_administrators_modify_personal_Password.geometry('200x200')
                            tk_administrators_modify_personal_Password.title('Change password')
                            modify_personal_Password=tk.StringVar()
                            tk.Label(tk_administrators_modify_personal_Password,text='Please enter new password：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_personal_Password,textvariable=modify_personal_Password).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_personal_Password,text='Change confirm',command=ad_modify_personal_Password).place(x=100,y=100)
                       def administrators_modify_personal_Age():
                            def ad_modify_personal_Age():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_personal_Age=db.cursor()
                               sql_ad_modify_personal_Age.execute("UPDATE Administrators SET Age='%s' WHERE ID ='%d';"%(modify_personal_Age.get(),administrators_search_personal_ID.get()))
                               db.commit()
                            tk_administrators_modify_personal_Age=tk.Toplevel(root)
                            tk_administrators_modify_personal_Age.geometry('200x200')
                            tk_administrators_modify_personal_Age.title('Change age')
                            modify_personal_Age=tk.StringVar()
                            tk.Label(tk_administrators_modify_personal_Age,text='Please enter new age：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_personal_Age,textvariable=modify_personal_Age).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_personal_Age,text='Change confirm',command=ad_modify_personal_Age).place(x=100,y=100)
                       def administrators_modify_personal_Phone():
                            def ad_modify_personal_Phone():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_personal_Class=db.cursor()
                               sql_ad_modify_personal_Class.execute("UPDATE Administrators SET Phone='%s' WHERE ID ='%d';"%(modify_personal_Phone.get(),administrators_search_personal_ID.get()))
                               db.commit()
                            tk_administrators_modify_personal_Phone=tk.Toplevel(root)
                            tk_administrators_modify_personal_Phone.geometry('200x200')
                            tk_administrators_modify_personal_Phone.title('Change phone')
                            modify_personal_Phone=tk.StringVar()
                            tk.Label(tk_administrators_modify_personal_Phone,text='Please enter new phone：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_personal_Phone,textvariable=modify_personal_Phone).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_personal_Phone,text='Change confirm',command=ad_modify_personal_Phone).place(x=100,y=100)
                       def administrators_modify_personal_Address():
                            def ad_modify_personal_Address():
                               tk.messagebox.askokcancel('Warning','Change successfully')
                               sql_ad_modify_personal_Address=db.cursor()
                               sql_ad_modify_personal_Address.execute("UPDATE Administrators SET Address='%s' WHERE ID ='%d';"%(modify_personal_Address.get(),administrators_search_personal_ID.get()))
                               db.commit()
                            tk_administrators_modify_personal_Address=tk.Toplevel(root)
                            tk_administrators_modify_personal_Address.geometry('200x200')
                            tk_administrators_modify_personal_Address.title('Change address')
                            modify_personal_Address=tk.StringVar()
                            tk.Label(tk_administrators_modify_personal_Address,text='Please enter new address：').place(x=10,y=50)
                            tk.Entry(tk_administrators_modify_personal_Address,textvariable=modify_personal_Address).place(x=150,y=50)  
                            tk.Button(tk_administrators_modify_personal_Address,text='Change confirm',command=ad_modify_personal_Address).place(x=100,y=100)
                       tk_administrators_modify_personal=tk.Toplevel(root)
                       tk_administrators_modify_personal.geometry('200x400')
                       tk_administrators_modify_personal.title('Change administrator information')
                       tk.Button(tk_administrators_modify_personal,text='Change teacher ID',command=administrators_modify_personal_ID).place(x=50,y=50)
                       tk.Button(tk_administrators_modify_personal,text='Change name',command=administrators_modify_personal_NAME).place(x=50,y=100)
                       tk.Button(tk_administrators_modify_personal,text='Change password',command=administrators_modify_personal_Password).place(x=50,y=150)
                       tk.Button(tk_administrators_modify_personal,text='Change age',command=administrators_modify_personal_Age).place(x=50,y=200)
                       tk.Button(tk_administrators_modify_personal,text='Change phone',command=administrators_modify_personal_Phone).place(x=50,y=250)
                       tk.Button(tk_administrators_modify_personal,text='Change address',command=administrators_modify_personal_Address).place(x=50,y=300)
                   tk_administrators_search_personal=tk.Toplevel(root)
                   tk_administrators_search_personal.geometry('200x200')
                   tk_administrators_search_personal.title('Check administrator information')
                   administrators_search_personal_ID=tk.IntVar()
                   tk.Label(tk_administrators_search_personal,text='Please enter teacher ID').place(x=10,y=50)
                   tk.Entry(tk_administrators_search_personal,textvariable=administrators_search_personal_ID).place(x=150,y=50)  
                   tk.Button(tk_administrators_search_personal,text='Check confirm',command=comfir_search_personal).place(x=100,y=100)
                   tk.Button(tk_administrators_search_personal,text='Change information',command=administrators_modify_personal).place(x=100,y=150)
               tk_administrators=tk.Toplevel(root)
               tk_administrators.geometry('200x200')
               tk_administrators.title('Administrator')
               tk.Button(tk_administrators,text='Check student information',command=administrators_search_student).place(x=50,y=50)
               tk.Button(tk_administrators,text='Check teacher information',command=administrators_search_teacher).place(x=50,y=100)
               tk.Button(tk_administrators,text='Check course information',command=administrators_search_course).place(x=50,y=150)
               tk.Button(tk_administrators,text='Check personal information',command=administrators_search_personal).place(x=50,y=200)
           else:
               tk.messagebox.askokcancel('Warning','User or password is wrong')
               root.destroy()
               GUI(3)
   bt_login=tk.Button(root,text='Sign in',command=log_in)
   bt_login.place(x=200,y=130)
   bt_logup=tk.Button(root,text='Sign up',command=sign_up)
   bt_logup.place(x=260,y=130)
   root.mainloop()
select()
shutil.copy("C:\\Users\\rommel\\Desktop\\python\\teach_system\\client\\teach.db","C:\\Users\\rommel\\Desktop\\python\\teach_system\\client\\server_new.db")
clientobj.doput("server_new.db")
db.close()
