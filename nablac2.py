from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
import sqlite3 as sq
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as fct
from datetime import datetime
from calendar import monthrange
import webbrowser
import nabla_database_builder as ndb
import os

db_path = 'nabla_database.db'

# Check if the file exists
if os.path.exists(db_path):
    mydb = sq.connect("nabla_database.db")
    mycursor = mydb.cursor()
else:
    ndb.database_build()
    mydb = sq.connect('nabla_database.db')
    mycursor = mydb.cursor()

# Kullanıcı adı ve şifre
users = [
    ['admin','123456']
]

def login_win():

    def log():
        username = username_ent.get()
        password = password_ent.get()
        # Kullanici adi aramasi
        for user in users:
            if username == user[0] and password == user[1]:
                LOP.set(True)
                login_window.destroy()
        
        if LOP.get() == False :
            tk.messagebox.showerror(title="Hatalı Giriş!", message="Kullanıcı adı veya şifre yanlış!")
                



    def mouse_on1(e):
        username_ent.delete(0,'end')
    def mouse_on2(e):
        password_ent.delete(0,"end")
    def mouse_off1(e):
        text = username_ent.get()
        if text == '':
            username_ent.insert(0,"Kullanıcı Adı")
    def mouse_off2(e):
        text = password_ent.get()
        if text == '':
            password_ent.insert(0,"Şifre")



    login_window = tk.Tk()
    login_window.title("Nabla OBS Giriş Ekranı")

    icon = PhotoImage(file="images/a.png")
    login_window.iconphoto(False,icon)

    screen_h = login_window.winfo_screenheight()
    screen_w = login_window.winfo_screenwidth()

    app_w = int(screen_w/3)
    app_h = int(screen_h/1.25)

    login_window.geometry(f"{app_w}x{app_h}+{int(screen_w*(0.5))-int(app_w*(0.5))}+{int(screen_h*(0.5))-int(app_h*(0.5))}")
    login_window.minsize(width=app_w, height=app_h)
    login_window.configure(background="white")

    login_image = Image.open('images/yuzde50.png')
    login_image = login_image.resize((app_w-int(app_w/2),app_w-int(app_w/2)))
    login_image = ImageTk.PhotoImage(login_image)
    tk.Label(login_window,image=login_image,background="white").pack(pady=50)

    username_ent = tk.Entry(master=login_window,relief="flat",background="white",foreground="black",border=3,highlightcolor="purple",highlightthickness=1,width=30,
                            font=("Calibri",14),justify="center")
    username_ent.pack(padx=50,fill="x")
    #username_ent.insert(0,'enes')
    password_ent =  tk.Entry(master=login_window,relief="flat",background="white",foreground="black",border=1,highlightcolor="purple",highlightthickness=1,width=30,
                             font=("Calibri",14),show='\u25C9',justify="center")
    password_ent.pack(padx=50,pady=20,fill="x")
    #password_ent.insert(0,'Enes.4151')

    username_ent.bind('<FocusIn>',mouse_on1)
    password_ent.bind('<FocusIn>',mouse_on2)
    username_ent.bind('<FocusOut>',mouse_off1)
    password_ent.bind('<FocusOut>',mouse_off2)

    LOP = tk.BooleanVar(master=login_window)

    LogIn_button = tk.Button(master=login_window,text="Giriş Yap",border=0,foreground="white",background="#2ABDE1",font=("Calibri",14),relief="flat",command=log)
    LogIn_button.pack(pady=30,padx=50,fill="x")

    login_window.mainloop()
    return LOP.get()
    


def main_page():
    q = "select * from kurum"
    mycursor.execute(q)
    cam_set = mycursor.fetchall()

    if cam_set == []:
        
        def save_info():
            try:
                Kurumad = entryler[0].get()
                sahip = entryler[1].get()
                mudur = entryler[2].get()
                kap = entryler[3].get()

                q = f"insert into kurum (name, owner, mudur, capacity) values ('{Kurumad.lower()}','{sahip.lower()}','{mudur.lower()}','{kap.lower()}');"
                mycursor.execute(q)
                mydb.commit()

                main_page()
            except:
                tk.messagebox.showerror(title="Veri Hatası",text="Verileri düzgün biçimde doldurun!")


        righ_menu_panel = tk.Frame(master=main_window, background="white")
        righ_menu_panel.place(relx=0.1,y=0,relwidth=0.9,relheight=1.0)

        tk.Label(master=righ_menu_panel, text="Dikkat!",font=("Calibri",14,"bold"), foreground="red", anchor="center",background="white").pack(fill="x")

        text = "Nabla OBS'in verimli biçimde kullanılması adına kurumunuz hakkında bazı bilgilere ihtiyacı vardır. Aşağıda verileri doğru doldurduğunuzdan emin olun ve kaydedin."
        textwid = tk.Text(master=righ_menu_panel,background="white",highlightthickness=0,border=0,relief="flat",font=("Calibri",12),
                        height=3,wrap="word")
        textwid.pack(fill="x",padx=50)
        textwid.insert(INSERT,text)
        textwid.configure(state="disabled")


        bilgi_frame = tk.Frame(master=righ_menu_panel,highlightthickness=1,highlightcolor="red",background="white")
        bilgi_frame.pack(fill="both",padx=50,pady=50)

        bilgi_frame.columnconfigure(0,weight=1)
        bilgi_frame.columnconfigure(1,weight=1)

        bilgiler = ["Kurum Adı","Sahibi","Mudur","Kapasite"]
        entryler = []
        for i in range(len(bilgiler)):
            tk.Label(master=bilgi_frame,text=f"{bilgiler[i]} : ",background="white",font=("Calibri",12),foreground="black").grid(row=i,column=0,sticky="e")
            entryler.append(tk.Entry(master=bilgi_frame,relief="flat",border=1,highlightthickness=2,background="white"))
            entryler[-1].grid(row=i,column=1,sticky = "w")

        apply_btn = tk.Button(master=bilgi_frame,text="Kaydet",relief="flat",border=0,highlightthickness=0,background="green",
                              command=save_info,font=("Calibri",12,"bold"),foreground="white")
        
        apply_btn.grid(column=0,row=len(bilgiler)+1,columnspan=2,sticky="news")


    else:

        


        def get_saved_gider():
            q = f"select * from taxes"
            mycursor.execute(q)
            info = mycursor.fetchall()
            return len(info)

        def get_saved_student():
            q = f"select * from student"
            mycursor.execute(q)
            info = mycursor.fetchall()
            return len(info)
        
        def get_com_info():
            q = f"select * from kurum"
            mycursor.execute(q)
            info = mycursor.fetchall()

            return info[0]


        def taksit():
            date1 = datetime.now()
            today = datetime(date1.year,date1.month,date1.day)

            q = f"select * from paymet_student;"
            mycursor.execute(q)
            data = mycursor.fetchall()
            unpeyed = 0
            personal_id = ''
            personal_unpayed = 0
            final_data = []
            if data != []:
                for i in data:
                    personal_id = i[0]
                    student_date = datetime(today.year,i[3],i[1])
                    if today.month < i[3]:
                        student_date = datetime(today.year-1,i[3],i[1])
                    
                    date_diff = today.month - student_date.month

                    if student_date.day >= today.day:
                        date_diff = date_diff - 1

                    if date_diff > 0 :
                        for j in range(date_diff):
                            if i[4+j] != "ödendi":
                                unpeyed = unpeyed + 1
                                personal_unpayed = personal_unpayed + 1
                    if unpeyed != 0:
                        final_data.append([personal_id,personal_unpayed])
                    personal_id = ''
                    personal_unpayed = 0

                    

            return unpeyed, final_data

        def all_tax():
            alltax_panel = tk.Frame(master=righ_menu_panel,background="white",highlightthickness=1,highlightbackground="orange")
            alltax_panel.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.8)

            alltax_panel_topbar =  tk.Frame(master=alltax_panel,background="white",highlightthickness=0,highlightbackground="blue")
            alltax_panel_topbar.pack(fill="x")

            tk.Label(master=alltax_panel_topbar,background="white",font=("Calibri",12,"bold"),text="Zamanı gelmiş ve ödenmemiş taksitler: ").pack(side="left",padx=10)



            """
            selected_item = teacher_list.focus()
            selected_row = teacher_list.item(selected_item)
            selected_teacher = selected_row.get("values")


            for i in range(len(labels)):
                tk.Label(master=teacher_info_panelbase, background="white",font=("Calibri", 12), foreground="black",text=selected_teacher[i],anchor="w").grid(row=i,column=1,sticky="news")
                pass
            
            """

            close_button=tk.Button(master=alltax_panel_topbar,image=close_btn_image,command=lambda : alltax_panel.destroy(),background="white",border=0,highlightthickness=0,highlightbackground="white")
            close_button.pack(side="right",padx=10,pady=10)

            data = taksit()[1]

            alltaxes_tree = ttk.Treeview(alltax_panel)
            xscrollx = tk.Scrollbar(alltax_panel,orient="horizontal",command=alltaxes_tree.xview)
            xscrollx.pack(side="bottom",fill="x")
            yscrolly = tk.Scrollbar(alltax_panel,orient="vertical",command=alltaxes_tree.yview)
            yscrolly.pack(side="right",fill="y")

            alltaxes_tree.configure(yscrollcommand=yscrolly.set)
            alltaxes_tree.configure(xscrollcommand=xscrollx.set)

            alltaxes_tree['columns'] = ('Ad','Soyad','Veli Tel','One','Adet','Toplam')
            alltaxes_tree.column('#0',width=0,stretch=NO)
            for i in alltaxes_tree["columns"]:
                alltaxes_tree.column(i,width=10)

            alltaxes_tree.heading('Ad',text='Ad',anchor=W)
            alltaxes_tree.heading('Soyad',text='Soyad',anchor=W)
            alltaxes_tree.heading('Veli Tel',text='Veli Tel',anchor=W)
            alltaxes_tree.heading('One',text='1 Ödeme',anchor=W)
            alltaxes_tree.heading('Adet',text='Adet',anchor=W)
            alltaxes_tree.heading('Toplam',text='Total Borç',anchor=W)

            alltaxes_tree.pack(fill="both",expand="true")
            idcount=0
            for i in data:

                q = f"Select * from student where student_key like '{data[idcount][0]}';"
                q2 = f"Select * from paymet_student where student_key like '{data[idcount][0]}';"
                
                mycursor.execute(q)
                person = mycursor.fetchall()[0]
                mycursor.execute(q2)
                coast = mycursor.fetchall()[0]

                total = int(coast[2]) * int(data[idcount][1])

                #print(person)
                alltaxes_tree.insert(parent='',index="end",iid=idcount,values=(person[1],person[2],person[10],coast[2],data[idcount][1],total))
                idcount = idcount+1


        righ_menu_panel = tk.Frame(master=main_window, background="white")
        righ_menu_panel.place(relx=0.1,y=0,relwidth=0.9,relheight=1.0)
        tk.Label(master=righ_menu_panel, text="Ana Sayfa",font=("Calibri",14,"bold"), foreground="red", anchor="center",background="white").pack(fill="x")

        base = tk.Frame(master=righ_menu_panel,background="blue")
        base.pack(side="top",padx=50,pady=10,fill="both",expand=True)
        base_d = tk.Frame(master=righ_menu_panel,background="green")
        base_d.pack(side="bottom",padx=50,pady=20,fill="both",expand=True)
        base.pack_propagate(False)
        base_d.pack_propagate(False)

        # Yukarı line
        company_infoF = tk.Frame(master=base,background="white")
        company_infoF.pack(side="left",fill="both",expand=True)

        company_infoF2 = tk.Frame(master=base,background="white")
        company_infoF2.pack(side="left",fill="both",expand=True)

        company_infoF.pack_propagate(False)
        company_infoF2.pack_propagate(False)

        kurumdata = get_com_info()
        tk.Label(master=company_infoF,text=f"Kurum Adı: {kurumdata[1].upper()}",anchor="w",font=("Calibri",12),foreground="blue",background="white").pack(fill="x")
        tk.Label(master=company_infoF,text=f"Kurum Sahibi: {kurumdata[2].upper()}",anchor="w",font=("Calibri",12),foreground="blue",background="white").pack(fill="x")
        tk.Label(master=company_infoF,text=f"Kurum Müdürü: {kurumdata[3].upper()}",anchor="w",font=("Calibri",12),foreground="blue",background="white").pack(fill="x")
        tk.Label(master=company_infoF,text=f"Kurum Kapasitesi: {kurumdata[4].upper()}",anchor="w",font=("Calibri",12),foreground="blue",background="white").pack(fill="x")
        tk.Label(master=company_infoF,text="Nabla OBS Hakkında",anchor="center",font=("Calibri",12,"bold"),foreground="red",background="white").pack(fill="x",pady=10)
        tk.Label(master=company_infoF,text="Uygulama Sürümü: v1.0.0-beta",anchor="w",font=("Calibri",12),foreground="black",background="white").pack(fill="x")
        tk.Label(master=company_infoF,text="Üretici: Nabla BBS",anchor="w",font=("Calibri",12),foreground="black",background="white").pack(fill="x")
        tk.Label(master=company_infoF,text=f"Lisans Durumu: OK",anchor="w",font=("Calibri",12),foreground="black",background="white").pack(fill="x")
        tk.Label(master=company_infoF,text=f"Güncelleme Onayı: OK",anchor="w",font=("Calibri",12),foreground="black",background="white").pack(fill="x")
        
        aylar = ["OCAK","ŞUBAT","MART","NİSAN","MAYIS","HAZİRAN","TEMMUZ","AĞUSTOS","EYLÜL","EKİM","KASIM","ARALIK"]
        gunler = ["PAZARTESİ","SALI","ÇARŞAMBA","PERŞEMBE","CUMA","CUMARTESİ","PAZAR"]
        tk.Label(master=company_infoF2,text=f"{datetime.now().day}",anchor="center",font=("Calibri",60,"bold"),foreground="black",background="white").pack(fill="x")
        tk.Label(master=company_infoF2,text=f"{aylar[datetime.now().month-1]}",anchor="center",font=("Calibri",20,"bold"),foreground="orange",background="white").pack(fill="x")
        tk.Label(master=company_infoF2,text=f"{datetime.now().year}",anchor="center",font=("Calibri",20,"bold"),foreground="red",background="white").pack(fill="x")
        tk.Label(master=company_infoF2,text=f"{gunler[datetime.now().weekday()]}",anchor="center",font=("Calibri",20,"bold"),foreground="purple",background="white").pack(fill="x")
        

        # Alt Frame
        frame1=tk.Frame(master=base_d,background="blue")
        frame1.pack(side="left",fill="both",expand=True)
        frame1.pack_propagate(False)
        frame2=tk.Frame(master=base_d,background="orange")
        frame2.pack(side="left",fill="both",expand=True)
        frame3=tk.Frame(master=base_d,background="red")
        frame3.pack(side="left",fill="both",expand=True)
        frame2.pack_propagate(False)
        frame3.pack_propagate(False)

        tk.Label(master=frame1,text=f"{get_saved_student()}",background="blue",foreground="white",anchor="center",font=("Calibri",70,"bold")).pack(fill="both",expand=True)
        tk.Label(master=frame1,text="Kayıtlı Öğrenci\nBulunuyor.",background="blue",foreground="white",anchor="center",font=("Calibri",12,"bold")).pack(fill="both")

        tk.Label(master=frame2,text=f"{taksit()[0]}",background="orange",foreground="white",anchor="center",font=("Calibri",70,"bold")).pack(fill="both",expand=True)
        tk.Button(master=frame2,text="Ödenmemiş Taksitler.\nBuraya Tıkla!",background="orange",foreground="white",anchor="center",relief="flat",border=0,highlightthickness=0,font=("Calibri",12,"bold"),command=all_tax).pack(fill="both")

        tk.Label(master=frame3,text=f"{get_saved_gider()}",background="red",foreground="white",anchor="center",font=("Calibri",70,"bold")).pack(fill="both",expand=True)
        tk.Label(master=frame3,text="Ödenmiş Ek Gider\n(Tüm Zamanlar)",background="red",foreground="white",anchor="center",font=("Calibri",12,"bold")).pack(fill="both")
        """
        student_pay_btn = tk.Button(master=base, text=f"Gecikmiş taksitelerinizin sayısı\n{taksit()}",font=("Calibri",20,"bold"),
                                    background="red",foreground="white",relief="flat",border=0,highlightthickness=0)
        student_pay_btn.grid(row=1,column=0,sticky="news")
        
        """

        





def lesson_page():
    
    #variables
    students = []
    exams = []
    quizes = []

    def clear_frame():
        for widgets in frame_base.winfo_children():
            widgets.destroy()


    def efficient_page():
        
        clear_frame()

        verim_button.configure(foreground="#1664BC",background="white")
        special_button.configure(foreground="white",background="#1664BC")
        program_button.configure(foreground="white",background="#1664BC")
        classroom_button.configure(foreground="white",background="#1664BC")

        try:
            q = "select * from student"
            mycursor.execute(q)
            a = mycursor.fetchall()
            student = len(a[0])
            return ret
        except:
            print("Kayıtlı öğtenci yok.")
        
        
        try:
            q = "select * from quiz"
            mycursor.execute(q)
            a = mycursor.fetchall()
            ret = len(a[0])
            return ret
        except:
            print("Quiz bulamadık.")


        
        try :
            q = "select * from exam_class_one"
            mycursor.execute(q)
            a = mycursor.fetchall()
            ret = len(a)
        except: 
            ret = 0


        try:
            q = "select * from exam_class_two"
            mycursor.execute(q)
            a = mycursor.fetchall()
            ret = ret + len(a)
        except:
            ret = ret + 0

        try:
            q = "select * from exam_class_three"
            mycursor.execute(q)
            a = mycursor.fetchall()
            ret = ret + len(a)
        except:
            ret = ret + 0
    

    def special_page():
        # control parameter
        selected_teacher = []
        selected_student = []
               
        teacher_key = tk.StringVar()
        teacher_name = tk.StringVar()
        teacher_surname = tk.StringVar()
        student_key = tk.StringVar()
        student_name = tk.StringVar()
        student_surnaname = tk.StringVar()
        student_class = tk.StringVar()
        major = tk.StringVar()
        date = tk.StringVar()
        time = tk.StringVar()
        coat = tk.StringVar()


        def save_special_lesson():
            q = f"insert into special_lesson (teacher_key, teacher_name, teacher_surname, student_key, student_name, student_surname, major, date, time, cost) values ('{teacher_key.get()}','{teacher_name.get()}','{teacher_surname.get()}'"
            q = q + f",'{student_key.get()}','{student_name.get()}','{student_surnaname.get()}','{major.get()}','{day_ent.get()}','{saat_ent.get()}','{coast_ent.get()}');"

            mycursor.execute(q)
            mydb.commit()


        def bildirim(teacher_name,teacher_surname,major,student_name,student_surnaname,day,saat):

            rct = f"Özel Ders Randevusu : \n\n"
            rct = rct + f"{(student_name.get()).upper() +' '+ (student_surnaname.get().upper())} adlı öğrencimizin özel {(major.get()).upper()} dersi için {day} tarihinde {saat} saatli randevusu oluşturulmuştur.\nÖğretmen : {(teacher_name.get()).upper()} {(teacher_surname.get()).upper()}\n"
            rct = rct + f"Oluşturulan derslere zamanında katılım gösterilmesini rica ederiz.\nİyi günler."

            main_window.clipboard_clear()
            main_window.clipboard_append(rct)

        def clear_tree(wg):
            if len(wg.get_children()) != 0:
            
                for item in wg.get_children():
                    search_teacher_tree.delete(item)

        def control_student(a):
            op = 1-a

            if op == 1:
                
                add_ex_student_frame.pack(fill="x",pady=5,padx=20)


            elif op == 0:

                add_ex_student_frame.pack_forget()

            return op


        def control_teacher(a):
            op = 1-a

            if op == 1:
                
                add_ex_teacher_frame.pack(fill="x",pady=5,padx=20)


            elif op == 0:

                add_ex_teacher_frame.pack_forget()

            return op


        def func_search_teacher():

            clear_tree(search_teacher_tree)
            search_source = str(search_teacher_ent.get())
            q = f"select * from teacher where '{search_source}' IN (name, surname, personal_id, major, email, adres, tel, teacher_key, salary);"
            mycursor.execute(q)
            data = mycursor.fetchall()

            idcount = 0
            
            for i in data:
                selected_teacher.append(i)
                t_name = i[0] + ' ' + i[1]
                t_major = i[3]
                t_tel = i[6]

                search_teacher_tree.insert(parent='',index="end",iid=idcount,values=(t_name,t_major,t_tel))
                idcount = idcount + 1


        def func_search_student():

            clear_tree(search_student_tree)
            search_source = str(search_student_ent.get())
            q = f"select * from student where '{search_source}' IN (id, name, surname, personal_id, mother_name, father_name, class, school, email, adres, parent_tel, student_tel, student_key);"
            mycursor.execute(q)
            data = mycursor.fetchall()

            idcount = 0
            


            for i in data:
                selected_student.append(i)
                t_name = i[1] + ' ' + i[2]
                t_major = i[6]
                t_tel = i[10]

                search_student_tree.insert(parent='',index="end",iid=idcount,values=(t_name,t_major,t_tel))
                idcount = idcount + 1
        
        def take_student():

            if check_stvar.get() == 1:
                student_key.set('extra')
                student_name.set((external_studentname.get()).lower())
                student_surnaname.set((external_studentsurname.get()).lower())
                student_class.set((external_student_class.get()).lower())


            elif check_stvar.get() == 0 :
                selected_line =int(search_student_tree.focus())
                student_key.set(selected_student[selected_line][12])
                student_name.set(selected_student[selected_line][1])
                student_surnaname.set(selected_student[selected_line][2])
                student_class.set(selected_student[selected_line][6])

            student_lbl.configure(text=f"Öğrenci : {student_name.get()} {student_surnaname.get()}")


            image_drawer.create_image((194,20),image=tik)
            apply_teacher.configure(state="disabled")




        def take_teacher():

            if check_var.get() == 1:
                teacher_key.set('extra')
                teacher_name.set((external_teachername.get()).lower())
                teacher_surname.set((external_teachersurname.get()).lower())
                major.set((external_teacher_major.get()).lower())


            elif check_var.get() == 0 :
                selected_line =int(search_teacher_tree.focus())
                teacher_key.set(selected_teacher[selected_line][7])
                teacher_name.set(selected_teacher[selected_line][0])
                teacher_surname.set(selected_teacher[selected_line][1])
                major.set(selected_teacher[selected_line][3])


            teacher_lbl.configure(text=f"Öğretmen : {teacher_name.get()} {teacher_surname.get()}")
            major_lbl.configure(text=f"Ders : {major.get()}")


            image_drawer.create_image((20,20),image=tik)
            apply_teacher.configure(state="disabled")
            



        clear_frame()
        special_button.configure(foreground="#1664BC",background="white")
        verim_button.configure(foreground="white",background="#1664BC")
        program_button.configure(foreground="white",background="#1664BC")
        classroom_button.configure(foreground="white",background="#1664BC")


        sp_left_frame = tk.Frame(master=frame_base,background="white",border=0,highlightthickness=1,highlightbackground="#1664BC")
        sp_left_frame.pack(side="left",fill=BOTH,expand=True,padx=10,pady=10)

        
        sp_middle_frame = tk.Frame(master=frame_base,background="white",border=0,highlightthickness=1,highlightbackground="orange")
        sp_middle_frame.pack(side="left",fill=BOTH,padx=10,pady=10,expand=True)
        sp_middle_frame.pack_propagate(False)

        image_drawer = tk.Canvas(master=sp_middle_frame,width=int(image_for_special_lesson_pre.width),height=int(image_for_special_lesson_pre.height),background="white",border=0,highlightthickness=0)
        image_drawer.pack(padx=10,pady=10)
        image_drawer.create_image((149,71), image=image_for_special_lesson)

        sp_right_frame = tk.Frame(master=frame_base,background="white",border=0,highlightthickness=1,highlightbackground="#1664BC")
        sp_right_frame.pack(side="left",fill=BOTH,expand=True,padx=10,pady=10)


        #LeftPanel
        tk.Label(sp_left_frame,text="Öğretmen Seçimi",background="white",foreground="#1664BC", anchor="center").pack(pady=5,fill="x")

        search_teacher_frame = tk.Frame(master=sp_left_frame,background="white",border=0,highlightthickness=0)
        search_teacher_frame.pack(fill="x",pady=5,padx=20)

        search_teacher_frame.columnconfigure(0,weight=1)

        search_teacher_ent = tk.Entry(master=search_teacher_frame,background="white")
        search_teacher_ent.grid(row=0,column=0,sticky="news")

        search_teacher_button = tk.Button(master=search_teacher_frame, text="ARA", border=0, highlightthickness=0, width=5, background="green",foreground="white",command=func_search_teacher)
        search_teacher_button.grid(row=0, column=1,sticky="e")

        search_teacher_tree = ttk.Treeview(master=search_teacher_frame)
        search_teacher_tree.grid(row=1,column=0,columnspan=2,rowspan=5,sticky="news", pady=5)
        search_teacher_tree.grid_propagate(True)

        search_teacher_tree["column"] = ("name","major","phone")

        search_teacher_tree.column('#0', width=0, stretch="no")
        search_teacher_tree.column('name', width=10)
        search_teacher_tree.column('major',width=10)
        search_teacher_tree.column('phone', width=10)




        search_teacher_tree.heading('name', text='Ad Soyad')
        search_teacher_tree.heading('major', text="Branş")
        search_teacher_tree.heading('phone', text="Telefon")
        
        
        check_var = tk.IntVar()
        check_var.set(0)

        check_teacher = tk.Checkbutton(master=sp_left_frame,text="Kurum öğretmeni değil mi?",variable=check_var,onvalue=1,offvalue=0,background="white",border=0,highlightthickness=0,relief="flat")
        check_teacher.pack(fill="x",pady=5)

        check_teacher.bind("<Button-1>", lambda e: control_teacher(check_var.get()))

        add_ex_teacher_frame = tk.Frame(master=sp_left_frame,background="white",border=0,highlightthickness=1,highlightbackground="#1664BC")
        add_ex_teacher_frame.columnconfigure(1,weight=1)

        tk.Label(master=add_ex_teacher_frame,text="Öğretmen Adı:",background="white").grid(row=0,column=0,sticky="e")
        external_teachername = tk.Entry(master=add_ex_teacher_frame)
        external_teachername.grid(row=0,column=1,sticky="we")

        tk.Label(master=add_ex_teacher_frame,text="Öğretmen Soyadı:",background="white").grid(row=1,column=0,sticky="e")
        external_teachersurname = tk.Entry(master=add_ex_teacher_frame)
        external_teachersurname.grid(row=1,column=1,sticky="we")

        tk.Label(master=add_ex_teacher_frame,text="Öğretmen Tel:",background="white").grid(row=2,column=0,sticky="e")
        external_teachertel = tk.Entry(master=add_ex_teacher_frame)
        external_teachertel.grid(row=2,column=1,sticky="we")

        tk.Label(master=add_ex_teacher_frame,text="Branş :",background="white").grid(row=3,column=0,sticky="e")
        external_teacher_major = tk.Entry(master=add_ex_teacher_frame)
        external_teacher_major.grid(row=3,column=1,sticky="we")


        apply_teacher = tk.Button(master=sp_left_frame, text="Öğretmeni Onayla",font=("Calibri",12,"bold"),relief="flat",border=0,width=15,foreground="white",background="#1664BC",borderwidth=0,command=take_teacher)
        apply_teacher.pack(side="bottom",fill="x",padx=10,pady=10)

        sp_left_frame.pack_propagate(False)
        sp_right_frame.pack_propagate(False)



        
        # Right Frame

        tk.Label(sp_right_frame,text="Öğrenci Seçimi",background="white",foreground="#1664BC", anchor="center").pack(pady=5,fill="x")

        search_student_frame = tk.Frame(master=sp_right_frame,background="white",border=0,highlightthickness=0)
        search_student_frame.pack(fill="x",pady=5,padx=20)

        search_student_frame.columnconfigure(0,weight=1)
        search_student_ent = tk.Entry(master=search_student_frame,background="white")
        search_student_ent.grid(row=0,column=0,sticky="news")
        search_student_button = tk.Button(master=search_student_frame, text="ARA", border=0, highlightthickness=0, width=5, background="green",foreground="white",command=func_search_student)
        search_student_button.grid(row=0, column=1,sticky="e")
        search_student_tree = ttk.Treeview(master=search_student_frame)
        search_student_tree.grid(row=1,column=0,columnspan=2,rowspan=5,sticky="news", pady=5)
        search_student_tree.grid_propagate(True)
        search_student_tree["column"] = ("name","class","phone")
        search_student_tree.column('#0', width=0, stretch="no")
        search_student_tree.column('name', width=10)
        search_student_tree.column('class',width=10)
        search_student_tree.column('phone', width=10)
        search_student_tree.heading('name', text='Ad Soyad')
        search_student_tree.heading('class', text="Sınıf")
        search_student_tree.heading('phone', text="Telefon")
        
        
        check_stvar = tk.IntVar()
        check_stvar.set(0)

        check_student = tk.Checkbutton(master=sp_right_frame,text="Kurum öğrencisi değil mi?",variable=check_stvar,onvalue=1,offvalue=0,background="white",border=0,highlightthickness=0,relief="flat")
        check_student.pack(fill="x",pady=5)

        check_student.bind("<Button-1>", lambda e: control_student(check_stvar.get()))

        add_ex_student_frame = tk.Frame(master=sp_right_frame,background="white",border=0,highlightthickness=1,highlightbackground="#1664BC")
        add_ex_student_frame.columnconfigure(1,weight=1)

        tk.Label(master=add_ex_student_frame,text="Öğrenci Adı:",background="white").grid(row=0,column=0,sticky="e")
        external_studentname = tk.Entry(master=add_ex_student_frame)
        external_studentname.grid(row=0,column=1,sticky="we")

        tk.Label(master=add_ex_student_frame,text="Öğrenci Soyadı:",background="white").grid(row=1,column=0,sticky="e")
        external_studentsurname = tk.Entry(master=add_ex_student_frame)
        external_studentsurname.grid(row=1,column=1,sticky="we")

        tk.Label(master=add_ex_student_frame,text="Öğrenci Tel:",background="white").grid(row=2,column=0,sticky="e")
        external_studenttel = tk.Entry(master=add_ex_student_frame)
        external_studenttel.grid(row=2,column=1,sticky="we")

        tk.Label(master=add_ex_student_frame,text="Sınıf:",background="white").grid(row=3,column=0,sticky="e")
        external_student_class = tk.Entry(master=add_ex_student_frame)
        external_student_class.grid(row=3,column=1,sticky="we")


        apply_student = tk.Button(master=sp_right_frame, text="Öğrenciyi Onayla",font=("Calibri",12,"bold"),relief="flat",border=0,width=15,foreground="white",background="#1664BC",borderwidth=0,command=take_student)
        apply_student.pack(side="bottom",fill="x",padx=10,pady=10)

        sp_left_frame.pack_propagate(False)
        sp_right_frame.pack_propagate(False)
        



        ### Middle Frame ###

        # 1. Frame for information about student and teacher.
        info_frame = tk.Frame(master=sp_middle_frame,background='red',highlightthickness=0,border=0)
        info_frame.pack(fill='both',padx=5,pady=5)
        
        teacher_lbl = tk.Label(master=info_frame,background="white",text=f"Öğretmen : ",anchor="w")
        teacher_lbl.pack(fill="x")
        student_lbl = tk.Label(master=info_frame,background="white",text=f"Öğrenci : ",anchor="w")
        student_lbl.pack(fill="x")
        major_lbl = tk.Label(master=info_frame,background="white",text=f"Ders : ",anchor="w")
        major_lbl.pack(fill="x")

        date_frame = tk.Frame(master=info_frame,background='white',highlightthickness=0,border=0,highlightcolor="purple")
        date_frame.pack(fill="x",expand=True)

        date_frame.columnconfigure(1,weight=1)
        
        

        tk.Label(master=date_frame, text="Tarih (/): ",background="white").grid(row=0,column=0,sticky="e")
        day_ent = tk.Entry(master=date_frame,background="white",relief="flat",border=0,highlightthickness=1,highlightcolor="green")
        day_ent.grid(row=0,column=1,sticky="news")



        tk.Label(master=date_frame, text="Saat: ",background="white").grid(row=1,column=0,sticky="e")
        saat_ent = tk.Entry(master=date_frame,background="white",relief="flat",border=0,highlightthickness=1,highlightcolor="green")
        saat_ent.grid(row=1,column=1,sticky="news")


        tk.Label(master=date_frame, text="Tutar: ",background="white").grid(row=2,column=0,sticky="e")
        coast_ent = tk.Entry(master=date_frame,background="white",relief="flat",border=0,highlightthickness=1,highlightcolor="green")
        coast_ent.grid(row=2,column=1,sticky="news")



        
        notice_button = tk.Button(master=sp_middle_frame,text="Bildirim Mesajını Kopyala",background="yellow",border=0,highlightthickness=0,foreground="black",command= lambda : bildirim(teacher_name,teacher_surname,major,student_name,student_surnaname,day_ent.get(),saat_ent.get()))
        notice_button.pack(fill="x",padx=5,pady=5)


        notice_button = tk.Button(master=sp_middle_frame,text="Dersi Kaydet",font=("Calibri",12,"bold"),relief="flat",border=0,width=15,foreground="white",background="#1664BC",borderwidth=0,command= save_special_lesson)
        notice_button.pack(side="bottom",fill="x",padx=5,pady=5)



    def lessonprogram_page():
        clear_frame()
        program_button.configure(foreground="#1664BC",background="white")
        verim_button.configure(foreground="white",background="#1664BC")
        special_button.configure(foreground="white",background="#1664BC")
        classroom_button.configure(foreground="white",background="#1664BC")


    def classrooms_page():
        clear_frame()
        classroom_button.configure(foreground="#1664BC",background="white")
        verim_button.configure(foreground="white",background="#1664BC")
        special_button.configure(foreground="white",background="#1664BC")
        program_button.configure(foreground="white",background="#1664BC")




    righ_menu_panel = tk.Frame(master=main_window, background="white")
    righ_menu_panel.place(relx=0.1,y=0,relwidth=0.9,relheight=1.0)

    base =  tk.Frame(master=righ_menu_panel,background="white")
    base.pack(fill="both",expand=True,padx=50,pady=20) 

    #top button's line ok.
    tk.Frame(master=base,background="#1664BC").pack(fill="x")

    #left limit line
    tk.Frame(master=base,background="#1664BC").pack(side="left",fill="y")

    base_master = tk.Frame(master=base, background="white")
    base_master.pack(side="left",fill="both",expand=True)

    tk.Frame(master=base,background="#1664BC").pack(side="left",fill="y")

    button_bar_frame = tk.Frame(master=base_master,background="white")
    button_bar_frame.pack(fill="x")

    verim_button =  tk.Button(master=button_bar_frame, text="Ders Verimi",font=("Calibri",12,"bold"),relief="flat",border=0,width=15,foreground="white",background="#1664BC",borderwidth=0,command=efficient_page)
    #verim_button.pack(side="left")

    special_button =  tk.Button(master=button_bar_frame, text="Özel Ders",font=("Calibri",12,"bold"),relief="flat",border=0,width=15,foreground="white",background="#1664BC",borderwidth=0,command=special_page)
    special_button.pack(side="left")

    program_button =  tk.Button(master=button_bar_frame, text="Ders Programı",font=("Calibri",12,"bold"),relief="flat",border=0,width=15,foreground="white",background="#1664BC",borderwidth=0,command=lessonprogram_page)
    #program_button.pack(side="left")

    classroom_button =  tk.Button(master=button_bar_frame, text="Derslik Bilgisi",font=("Calibri",12,"bold"),relief="flat",border=0,width=15,foreground="white",background="#1664BC",borderwidth=0,command=classrooms_page)
    #classroom_button.pack(side="left")

    frame_base = tk.Frame(master=base_master, background="white")
    frame_base.pack(fill="both",expand=True)

    # open a grid to offer school statistics.
    special_page()
    



def class_page():

    def get_teacher():
        
        for item in teacher_list.get_children():
            teacher_list.delete(item)

        if search_ent.get() != '':
            search_source = (search_ent.get()).lower()
            #print(search_source)
            q = f"select * from teacher where '{search_source}' IN (name, surname, personal_id, major, email, adres, tel, teacher_key, salary);"
            mycursor.execute(q)
            data = mycursor.fetchall()
            idcount = 0
            for i in data:
                teacher_list.insert(parent='', index="end", iid=idcount, values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[8]))
                idcount = idcount + 1

        else:
            search_source = (search_ent.get()).lower()
            #print(search_source)
            q = f"select * from teacher;"
            mycursor.execute(q)
            data = mycursor.fetchall()
            idcount = 0
            for i in data:
                teacher_list.insert(parent='', index="end", iid=idcount, values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[8]))
                idcount = idcount + 1



    def teacher_info():
        
        teacher_info_panel = tk.Frame(master=righ_menu_panel,background="white",highlightthickness=1,highlightbackground="blue")
        teacher_info_panel.place(relx=0.33,y=20,relwidth=0.65,relheight=0.95)

        teacher_info_panel_topbar =  tk.Frame(master=teacher_info_panel,background="white",highlightthickness=0,highlightbackground="blue")
        teacher_info_panel_topbar.pack(fill="x")

        tk.Label(master=teacher_info_panel_topbar,background="white",font=("Calibri",12,"bold"),text="Öğretmen Profili").pack(side="left",padx=10)


        capsayici1 = tk.Frame(master=teacher_info_panel,background="white")
        capsayici1.pack(pady=50)

        tk.Label(master=capsayici1,image=teacherid_image,background="white").pack(fill="x",side="left",padx=50)
        teacher_info_panelbase = tk.Frame(master=capsayici1,background="white",highlightthickness=0,highlightbackground="blue")
        teacher_info_panelbase.pack(side="left",fill="x",expand=True)

        teacher_info_panelbase.columnconfigure(1, weight=1)

        # name, surname, personal_id, major, email, adres, tel, teacher_key, salary
        labels = ["Adı: ", "Soyadı: ", "TC: ", "Branş: ", "e-posta: ", "Adres: ", "Tel: ", "Ücret: "]
        for i in range(len(labels)):
            tk.Label(master=teacher_info_panelbase, background="white",font=("Calibri", 12), foreground="black",text=labels[i],anchor="e").grid(row=i,column=0,sticky="news")

        selected_item = teacher_list.focus()
        selected_row = teacher_list.item(selected_item)
        selected_teacher = selected_row.get("values")


        for i in range(len(labels)):
            tk.Label(master=teacher_info_panelbase, background="white",font=("Calibri", 12), foreground="black",text=selected_teacher[i],anchor="w").grid(row=i,column=1,sticky="news")
            pass

        close_button=tk.Button(master=teacher_info_panel_topbar,image=close_btn_image,command=lambda : teacher_info_panel.destroy(),background="white",border=0,highlightthickness=0,highlightbackground="white")
        close_button.pack(side="right",padx=10,pady=10)


    def save_teacher():
        try:
            teacher_key = ((Entrys[0].get())[0]).lower() + ((Entrys[1].get())[0]).lower() + Entrys[2].get()


            q = "insert into teacher (name, surname, personal_id, major, email, adres, tel, teacher_key, salary)"
            q = q + f" values ('{(Entrys[0].get().lower())}','{(Entrys[1].get().lower())}','{(Entrys[2].get()).lower()}','{(Entrys[3].get()).lower()}','{(Entrys[4].get()).lower()}','{(Entrys[5].get()).lower()}','{Entrys[7].get()}','{teacher_key}','{(Entrys[6].get()).lower()}')"

            #print(q)

            mycursor.execute(q)
            mydb.commit()
            tk.messagebox.showinfo(title=None, message="Öğretmen kaydedildi!")
        except:
            tk.messagebox.showerror(title=None, message="Öğretmen kaydedilemedi!")


    righ_menu_panel = tk.Frame(master=main_window, background="white")
    righ_menu_panel.place(relx=0.1,y=0,relwidth=0.9,relheight=1.0)

    add_teacher_panelbase = tk.Frame(master=righ_menu_panel,background="white",highlightthickness=1,highlightbackground="red")
    add_teacher_panelbase.place(x=20,y=20,relwidth=0.3,relheight=0.95)
    add_teacher_panelbase.pack_propagate(False)

    see_teacher_panelbase = tk.Frame(master=righ_menu_panel,background="white",highlightthickness=1,highlightbackground="blue")
    see_teacher_panelbase.place(relx=0.33,y=20,relwidth=0.65,relheight=0.95)
    see_teacher_panelbase.pack_propagate(False)

    tk.Label(add_teacher_panelbase,text="Öğretmen Kaydet", font=("Calibri",14,"bold"),background="white",foreground="red").pack(fill="x",padx=5,pady=5)
    tk.Label(see_teacher_panelbase,text="Araştır", font=("Calibri",14,"bold"),background="white",foreground="blue").pack(fill="x",padx=5,pady=5)


    add_teacher_panel = tk.Frame(master=add_teacher_panelbase,background="white",highlightthickness=0)
    add_teacher_panel.pack(fill="both",padx=20,pady=10)

    see_teacher_panel = tk.Frame(master=see_teacher_panelbase,background = "white",highlightthickness=0,highlightbackground="blue")
    see_teacher_panel.pack(fill="both",padx=10,pady=10)





    ############ Öğretmen Ekleme ekranı ################
    add_teacher_panel.columnconfigure(1,weight=1)

    # öğretmen ekleme entryleri ve labelleri.
    tk.Label(master=add_teacher_panel, text="Ad: ",anchor="e",font=("Calibri",12),background = "white").grid(row=0,column=0,sticky="news",pady=10) # connected to entrys 0
    tk.Label(master=add_teacher_panel, text="Soyad: ",anchor="e",font=("Calibri",12),background = "white").grid(row=1,column=0,sticky="news",pady=10) # connected to entrys 1
    tk.Label(master=add_teacher_panel, text="TC: ",anchor="e",font=("Calibri",12),background = "white").grid(row=2,column=0,sticky="news",pady=10) # connected to entrys 2
    tk.Label(master=add_teacher_panel, text="Branş: ",anchor="e",font=("Calibri",12),background = "white").grid(row=3,column=0,sticky="news",pady=10) # connected to entrys 3
    tk.Label(master=add_teacher_panel, text="e-posta: ",anchor="e",font=("Calibri",12),background = "white").grid(row=4,column=0,sticky="news",pady=10) # connected to entrys 4
    tk.Label(master=add_teacher_panel, text="Adres: ",anchor="e",font=("Calibri",12),background = "white").grid(row=5,column=0,sticky="news",pady=10) # connected to entrys 5
    tk.Label(master=add_teacher_panel, text="Ücret: ",anchor="e",font=("Calibri",12),background = "white").grid(row=6,column=0,sticky="news",pady=10) # connected to entrys 6
    tk.Label(master=add_teacher_panel, text="Tel: ",anchor="e",font=("Calibri",12),background = "white").grid(row=7,column=0,sticky="news",pady=10) # connected to entrys 6


    Entrys = []
    for i in range(8):
        Entrys.append(tk.Entry(master=add_teacher_panel,background="white",font=("Calibri",12,"bold"),highlightthickness=1,border=0,highlightcolor="red",highlightbackground="gray"))
        Entrys[i].grid(row=i,column=1,sticky="ew")


    save_button = tk.Button(master=add_teacher_panelbase,text="KAYDET",font=("Calibri",14,"bold"),background="red",foreground="white",border=0,highlightthickness=0,command=save_teacher)
    save_button.pack(fill="x",padx=20,pady=20,side="bottom")
        
    ########## Öğretmen izleme ekranı ###############
    see_teacher_panel.columnconfigure(0,weight=1)
    see_teacher_panel.rowconfigure(1,weight=1)
    search_ent = tk.Entry(master=see_teacher_panel,background="white",border=0,highlightthickness=1,highlightcolor="green",)
    search_ent.grid(row=0,column=0,sticky="news")
    search_btn = tk.Button(master=see_teacher_panel,text="ARA",border=0,highlightthickness=0,background="green",font=("Calibri",12,"bold"),foreground="white",command=get_teacher)
    search_btn.grid(row=0,column=1,ipadx=3,sticky="news")

    teacher_list = ttk.Treeview(master=see_teacher_panel,height=20)
    
    teacher_list["columns"] = ('name', 'surname', 'personal_id', 'major', 'email', 'adres', 'tel', 'salary')
    teacher_list_heading = ['İsim', 'Soyisim', 'TC', 'Branş', 'e-posta', 'Adres', 'Tel', 'Ücret']

    teacher_list.column('#0',width=0,stretch=NO)

    for i in teacher_list['columns']:
        teacher_list.column(f"{i}", width=10,anchor="center")

    for i in range(len(teacher_list_heading)):
        teacher_list.heading(f"{teacher_list['columns'][i]}", text=f"{teacher_list_heading[i]}",anchor="center")
        

    teacher_list.grid(row=1,column=0,columnspan=2,pady=20,sticky="news")


    show_button= tk.Button(master=see_teacher_panelbase,text="Verileri Getir",font=("Calibri",14,"bold"),background="blue",foreground="white",border=0,highlightthickness=0,command=teacher_info).pack(side="bottom",fill="x",padx=20,pady=20)
    get_teacher()



def student_page():
    righ_menu_panel = tk.Frame(master=main_window, background="white")
    righ_menu_panel.place(relx=0.1,y=0,relwidth=0.9,relheight=1.0)

    righ_menu_panel_title = Label(righ_menu_panel,text="ÖĞRENCİ SAYFASI",font=("Calibri",16,"bold"), foreground="#1664BC",background="white")
    righ_menu_panel_title.pack(fill="x")

    righ_menu_panel_metin = "\nÖğrenci Sorgulama ekranımıza hoş geldiniz! Bu ekran aracılığıyla öğrenci verilerini kolayca sorgulayabilir ve değerli bilgilere anında erişebilirsiniz."
    righ_menu_panel_metin = righ_menu_panel_metin + "Sistemimiz, öğrencilerin akademik performanslarını, devam durumlarını, notlarını ve diğer önemli bilgileri kapsamlı bir şekilde sunar. Öğrencilerimizin ilerlemelerini takip ederken, eğitimcilerin daha bilinçli ve veriye dayalı kararlar almasına yardımcı olmak bizim önceliğimizdir."
    righ_menu_panel_metin = righ_menu_panel_metin + "\n\nSorgulama ekranımız sayesinde, aşağıdaki bilgileri öğrenebilirsiniz:"
    righ_menu_panel_metin = righ_menu_panel_metin + "\n   1. Öğrencinin adı, soyadı ve kimlik numarası."
    righ_menu_panel_metin = righ_menu_panel_metin + "\n   2. Öğrencinin devam durumu ve katılım oranı."
    righ_menu_panel_metin = righ_menu_panel_metin + "\n   3. Akademik derslerdeki notları ve performansı."
    righ_menu_panel_metin = righ_menu_panel_metin + "\n   4. Öğrenci hakkındaki notlar ve özel durumlar."
    righ_menu_panel_metin = righ_menu_panel_metin + "\n\nBilgilerin güvenliği ve gizliliği, bizim için son derece önemlidir. Tüm öğrenci verileri şifrelenmiş ve güvenli bir şekilde saklanmaktadır. Sadece yetkili kullanıcılar, öğrenci bilgilerine erişim hakkına sahiptir ve bu bilgilerin korunmasını sağlamak için gerekli önlemler alınmıştır."
    righ_menu_panel_metin = righ_menu_panel_metin + "\nUygulamamızın kullanıcı dostu arayüzü sayesinde, istediğiniz öğrenci bilgilerine hızlıca ulaşabilirsiniz. Sorularınız veya yardıma ihtiyacınız olduğunda, destek ekibimiz her zaman size yardımcı olmak için hazırdır."
    righ_menu_panel_word = tk.Text(master=righ_menu_panel,highlightthickness=0 ,wrap="word",highlightcolor="blue",relief="flat",font=("Time New Roman",12),height=15)
    righ_menu_panel_word.insert(INSERT, "\t"+righ_menu_panel_metin)
    righ_menu_panel_word.pack(fill="x",padx=50)
    righ_menu_panel_word.config(state="disabled")

    tk.Frame(master=righ_menu_panel,background="#1664BC").pack(fill="x",padx=50,pady=20)

    save_ogr_button = tk.Button(righ_menu_panel,text="Öğrenci Kaydet",border=2,font=("Calibri",12,"bold"),relief="flat",highlightthickness=10, activebackground='#1664BC',activeforeground="white",highlightcolor="blue",command=save_student).pack(fill="x",side="top",padx=50,pady=5)
    see_ogr_button = tk.Button(righ_menu_panel,text="Öğrenci Gözlemle ve Veri Ekleme",border=2,font=("Calibri",12,"bold"),relief="flat",highlightthickness=10, activebackground='#1664BC',activeforeground="white",highlightcolor="blue",command=see_student).pack(fill="x",side="top",padx=50,pady=5)
    #delete_ogr_button = tk.Button(righ_menu_panel,text="Öğrenci Silme",border=2,font=("Calibri",12,"bold"), foreground="red",relief="flat",highlightthickness=10, activebackground='#1664BC',activeforeground="white",highlightcolor="blue",command=save_student).pack(fill="x",side="top",padx=50,pady=5)


def account_page():

    

    def clear_frame():
        for widgets in frame_base.winfo_children():
            widgets.destroy()

    def clear_choosen_frame(frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    def durum():

        def get_teacher_patment():
            teacher_count = 0
            payment_teacher_data = 0
            return_package = []
            q = "select * from teacher"
            mycursor.execute(q)
            data = mycursor.fetchall()

            for i in data:
                teacher_count = teacher_count + 1
                payment_teacher_data = payment_teacher_data + int(i[8])
            
            return_package.append(teacher_count)
            return_package.append(payment_teacher_data)

            return return_package
        
        
        def get_ogr_payment():

            # array for datas
            student_count = 0
            payment_student_data = 0
            return_package = []
            q = "select * from paymet_student"
            mycursor.execute(q)
            data = mycursor.fetchall()

            for i in data:
                student_count = student_count + 1
                payment_student_data = payment_student_data + int(i[2])
            
            return_package.append(student_count)
            return_package.append(payment_student_data)

            return return_package
        
        def get_special_payment():

            # array for datas
            student_count = 0
            payment_special_data = 0
            return_package = []
            q = "select * from special_lesson"
            mycursor.execute(q)
            data = mycursor.fetchall()

            for i in data:
                student_count = student_count + 1
                payment_special_data = payment_special_data + int(i[9])
            
            return_package.append(student_count)
            return_package.append(payment_special_data)

            return return_package
        
        
        def get_taxes():
            nowdate = datetime.now()
            this_month = nowdate.month
            this_year = nowdate.year
            query = "SELECT * FROM taxes WHERE month LIKE ? AND year LIKE ?"
            mycursor.execute(query, (f'%{this_month}%', f'%{this_year}%'))
            data = mycursor.fetchall()
            taxes = []
            type_fatura = [0,0,0,0,0]
            type_vergi = [0,0,0,0]
            type_borc = [0,0,0,0,0]
            type_jop = [0,0,0,0,0,0]

            for i in data:
                if i[3] == 'fatura':
                    if i[4] == 'elektrik':
                        type_fatura[0] = type_fatura[0] + int(i[5])
                    elif i[4] == 'su':
                        type_fatura[1] = type_fatura[1] + int(i[5])
                    elif i[4] == 'doğalgaz':
                        type_fatura[2] = type_fatura[2] + int(i[5])
                    elif i[4] == 'internet':
                        type_fatura[3] = type_fatura[3] + int(i[5])
                    elif i[4] == 'diğer':
                        type_fatura[4] = type_fatura[4] + int(i[5])

                elif i[3] == 'vergi':
                    if i[4] == 'kurum ödemesi':
                        type_vergi[0] = type_vergi[0] + int(i[5])
                    elif i[4] == 'çalışan ödemesi':
                        type_vergi[1] = type_vergi[1] + int(i[5])
                    elif i[4] == 'şirket ödemesi':
                        type_vergi[2] = type_vergi[2] + int(i[5])
                    elif i[4] == 'diğer':
                        type_vergi[4] = type_vergi[3] + int(i[5])

                elif i[3] == 'borç':
                    if i[4] == 'kırtasiye':
                        type_borc[0] = type_borc[0] + int(i[5])
                    elif i[4] == 'yayın':
                        type_borc[1] = type_borc[1] + int(i[5])
                    elif i[4] == 'ulaşım ve taşıma':
                        type_borc[2] = type_borc[2] + int(i[5])
                    elif i[4] == 'yapı':
                        type_borc[3] = type_borc[3] + int(i[5])   
                    elif i[4] == 'diğer':
                        type_borc[4] = type_borc[4] + int(i[5])

                elif i[3][0] == 'i':
                    if i[4] == 'öğretmen ödemesi':
                        type_jop[0] = type_jop[0] + int(i[5])
                    elif i[4] == 'müdür ödemesi':
                        type_jop[1] = type_jop[1] + int(i[5])
                    elif i[4] == 'yemek':
                        type_jop[2] = type_jop[2] + int(i[5])
                    elif i[4] == 'öğrenci taşımacılığı':
                        type_jop[3] = type_jop[3] + int(i[5])   
                    elif i[4] == 'iş yatırımı':
                        type_jop[4] = type_jop[4] + int(i[5]) 
                    elif i[4] == 'diğer':
                        type_jop[5] = type_jop[5] + int(i[5])

            taxes.append(type_fatura)
            taxes.append(type_vergi)
            taxes.append(type_borc)
            taxes.append(type_jop)
            return taxes

        student_pays = get_ogr_payment()
        special_lessons = get_special_payment()
        taks = get_taxes()
        faturalar = 0
        for i in taks[0]:
            faturalar = faturalar + i

        vergiler = 0
        for i in taks[1]:
            vergiler = vergiler + i

        borclar = 0
        for i in taks[2]:
            borclar = borclar + i

        joplar = 0
        for i in taks[3]:
            joplar = joplar + i


        #gider
        ogretmen_gider = get_teacher_patment()

        total_money = student_pays[1] + special_lessons[1]
        
        clear_frame()
        durum_button.configure(foreground="red",background="white")
        odeme_button.configure(foreground="white",background="red")
        gider_button.configure(foreground="white",background="red")


        base = tk.Frame(master=frame_base,background="white",border=0,highlightthickness=0)
        base.pack(fill="both",expand=True)

        base.columnconfigure(0,weight=1)

        fig = plt.figure(1)
        if student_pays[1] != 0 :    
            plt.subplot(121)
            plt.title(f"Toplam Kurum Geliri : {total_money}")
            plt.pie([student_pays[1]*20,special_lessons[1]*50],labels=["Öğrenci Taksidi","Özel Ders Geliri"],autopct='%1.1f%%')
        else:
            tk.messagebox.showwarning(title="Yetersiz Veri", message="Hesaplama bilgilerinin sunulabilmesi için daha fazla veriye ihtiyacımız var. Lütfen daha fazla veri ekleyin.")
        
        colors = ['#ff9999','#00FFFF','#FF0000','#33FF33']
        giderler = ["Faturalar", "Vergiler", "Borçlar", "İş Harcamaları"]
        giderlerpara=[faturalar,vergiler,borclar,joplar]
        total_gider = 0
        for i in giderlerpara:
            total_gider= total_gider + i

        if total_gider != 0:
            plt.subplot(122)
            plt.title(f"Toplam Kurum Gideri: {total_gider}")
            plt.pie(giderlerpara,labels=giderler,autopct='%1.1f%%',colors=colors)
        else:
            tk.messagebox.showwarning(title="Yetersiz Veri", message="Hesaplama bilgilerinin sunulabilmesi için daha fazla veriye ihtiyacımız var. Lütfen daha fazla veri ekleyin.")
            
        
        
        plot_floor = fct(fig,master=base)
        plot_floor.get_tk_widget().pack(fill="both",expand=True)
        plt.close('all')

           
    def gider():
        clear_frame()
        def type_selection(event):
            val = event.widget.get()
            
            if val == "Fatura":
                clear_choosen_frame(fatura_frame)
                tk.Label(master=fatura_frame,anchor="center",background="white",relief="flat",font=("Time New Roman",10),
                     text=f"\n\nTamam! gider tipi olarak {val} seçildi.\nŞimdi bunu detaylandıralım:",
                     foreground="blue").pack(fill="x")
                faturas()
            elif val == "Vergi":
                clear_choosen_frame(fatura_frame)
                tk.Label(master=fatura_frame,anchor="center",background="white",relief="flat",font=("Time New Roman",10),
                     text=f"\n\nTamam! gider tipi olarak {val} seçildi.\nŞimdi bunu detaylandıralım:",
                     foreground="blue").pack(fill="x")
                taxes()
            elif val == "Borç":
                clear_choosen_frame(fatura_frame)
                tk.Label(master=fatura_frame,anchor="center",background="white",relief="flat",font=("Time New Roman",10),
                     text=f"\n\nTamam! gider tipi olarak {val} seçildi.\nŞimdi bunu detaylandıralım:",
                     foreground="blue").pack(fill="x")
                payback()
            elif val == "İş Harcamaları":
                clear_choosen_frame(fatura_frame)
                tk.Label(master=fatura_frame,anchor="center",background="white",relief="flat",font=("Time New Roman",10),
                     text=f"\n\nTamam! gider tipi olarak {val} seçildi.\nŞimdi bunu detaylandıralım:",
                     foreground="blue").pack(fill="x")
                jop_payment()



        def fat_selection(event):

            def save_taxes():

                # taxes date information
                nowdate = datetime.now()
                this_month = nowdate.month
                this_year = nowdate.year

                query = f"insert into taxes (month, year, type, gider, coast, label) values('{this_month}','{this_year}','{val.lower()}','{val2.lower()}','{pay_ent.get()}','{(fat_ent.get().lower())}')"
                mycursor.execute(query)
                mydb.commit()

            
            global fat_select
            val = type_selector.get()
            val2= str(event.widget.get())
            fat_select = val

            fat_label = tk.Label(master=fatura_frame,text=f"\n\nGider: {val2} - {val} için bir etiket verin: ",background="white",foreground="blue",highlightbackground="gray").pack(fill="x")
            fat_ent = tk.Entry(master=fatura_frame,relief="flat",highlightthickness=1)
            fat_ent.pack(fill="x")
            
            pay_label = tk.Label(master=fatura_frame,text=f"\n\nGider: {val2} - {val} için ödenen tutarı girin: ",background="white",foreground="red").pack(fill="x")
            pay_ent = tk.Entry(master=fatura_frame,font=("Calibri",14,"bold"),relief="flat",foreground="red",highlightcolor="red",highlightbackground="red",highlightthickness=1)
            pay_ent.pack(fill="x")

            Buttons = tk.Button(master=fatura_frame,text="Gideri Kaydet",background="red",foreground="white",border=0,relief="flat",font=("Calibri",14),command=save_taxes)
            Buttons.pack(side="bottom",fill="x")



        def faturas():
            fat_type = ["Elektrik","Su","Doğalgaz","İnternet","Diğer"]
            fat_selector = ttk.Combobox(master=fatura_frame,state="readonly",values=fat_type)
            fat_selector.pack(fill="x")
            fat_selector.bind("<<ComboboxSelected>>",fat_selection)

        def taxes():
            fat_type = ["Kurum Ödemesi","Çalışan Ödemesi","Şirket Ödemesi","Diğer"]
            fat_selector = ttk.Combobox(master=fatura_frame,state="readonly",values=fat_type)
            fat_selector.pack(fill="x")
            fat_selector.bind("<<ComboboxSelected>>",fat_selection)

        def payback():
            fat_type = ["Kırtasiye","Yayın","Ulaşım ve Taşıma","Yapı","Diğer"]
            fat_selector = ttk.Combobox(master=fatura_frame,state="readonly",values=fat_type)
            fat_selector.pack(fill="x")
            fat_selector.bind("<<ComboboxSelected>>",fat_selection)

        def jop_payment():
            fat_type = ["Öğretmen Ödemesi","Müdür Ödemesi","Yemek","Öğrenci Taşımacılığı","İş Yatırımı","Diğer"]
            fat_selector = ttk.Combobox(master=fatura_frame,state="readonly",values=fat_type)
            fat_selector.pack(fill="x")
            fat_selector.bind("<<ComboboxSelected>>",fat_selection)


        #gider görme listesini doldur:
        def clear_all():
            for item in gider_tree.get_children():
                gider_tree.delete(item)

        def alltaxes():
            clear_all()

            def close():
                alltaxFrame.destroy()
                gider()
            # for name

            # Frame for all taxes
            alltaxFrame = tk.Frame(master=frame_base,background="orange")
            alltaxFrame.place(x=0,y=0,relwidth=1.0,relheight=1.0)

            alltaxFrame = tk.Frame(master=frame_base,background="orange")
            alltaxFrame.place(x=0,y=0,relwidth=1.0,relheight=1.0)

            alltaxFrameinfo =  tk.Frame(master=alltaxFrame,background="white",highlightthickness=0,highlightbackground="blue")
            alltaxFrameinfo.pack(fill="x")

            tk.Label(master=alltaxFrameinfo,background="white",font=("Calibri",12,"bold"),text="Tüm Giderler").pack(side="left",padx=10)
            close_button=tk.Button(master=alltaxFrameinfo,image=close_btn_image,command=close,background="white",border=0,highlightthickness=0,highlightbackground="white")
            close_button.pack(side="right",padx=10,pady=10)

            alltaxes_tree = ttk.Treeview(alltaxFrame)
            xscrollx = tk.Scrollbar(alltaxFrame,orient="horizontal",command=alltaxes_tree.xview)
            xscrollx.pack(side="bottom",fill="x")
            yscrolly = tk.Scrollbar(alltaxFrame,orient="vertical",command=alltaxes_tree.yview)
            yscrolly.pack(side="right",fill="y")

            alltaxes_tree.configure(yscrollcommand=yscrolly.set)
            alltaxes_tree.configure(xscrollcommand=xscrollx.set)

            alltaxes_tree['columns'] = ('month','year','type','tax','coast','label')
            alltaxes_tree.column('#0',width=0,stretch=NO)
            for i in alltaxes_tree["columns"]:
                alltaxes_tree.column(i,width=10)

            alltaxes_tree.heading('month',text='Ay',anchor=W)
            alltaxes_tree.heading('year',text='Yıl',anchor=W)
            alltaxes_tree.heading('type',text='Tip',anchor=W)
            alltaxes_tree.heading('tax',text='Fatura',anchor=W)
            alltaxes_tree.heading('coast',text='Tutar',anchor=W)
            alltaxes_tree.heading('label',text='Etiket',anchor=W)
            
            alltaxes_tree.pack(fill="both",expand=True)

            search_ogr_query = f"Select * from taxes;"
            mycursor.execute(search_ogr_query)
            finded_ogr = mycursor.fetchall()
            idcount = 0
            for i in finded_ogr:
                alltaxes_tree.insert(parent='',index="end",iid=idcount,values=(i[1:]))
                idcount = idcount+1

        def selected_gider():
            clear_all()
            nowdate = datetime.now()
            this_month = nowdate.month
            this_year = nowdate.year
            search_ogr_query= f"Select * from taxes where month like '{this_month}' and year like '{this_year}';"

            mycursor.execute(search_ogr_query)
            finded_ogr = mycursor.fetchall()
            idcount = 0
            for i in finded_ogr:
                gider_tree.insert(parent='',index="end",iid=idcount,values=(i[1:]))
                idcount = idcount+1

        gider_button.configure(foreground="red",background="white")
        odeme_button.configure(foreground="white",background="red")
        durum_button.configure(foreground="white",background="red")
        
        

        now = datetime.now()
        year = now.year
        mont = now.month

        left_base = tk.Frame(master=frame_base,background="blue")
        left_base.pack(side="left",fill="both",expand=True,padx=50,pady=50)
        tk.Label(master=left_base,text="Gider Görüntüleme Alanı",background="white",font=("Calibri",14,"bold"),foreground="green").pack(fill="x")
        textmetinl = "Gider görüntülemem alanına hoş geldiniz! Bu alanda varsayılan olarak bu ay eklenen giderler görüntülenir."
        textwl = tk.Text(master=left_base,highlightthickness=0 ,wrap="word",highlightcolor="blue",relief="flat",font=("Time New Roman",10),height=2,width=1)
        textwl.insert(INSERT, textmetinl)
        textwl.pack(fill="x")
        textwl.config(state="disabled")

        gider_tree = ttk.Treeview(left_base)
        gider_tree['columns'] = ('month','year','type','tax','coast','label')
        gider_tree.column('#0',width=0,stretch=NO)
        for i in gider_tree["columns"]:
            gider_tree.column(i,width=10)

        gider_tree.heading('month',text='Ay',anchor=W)
        gider_tree.heading('year',text='Yıl',anchor=W)
        gider_tree.heading('type',text='Tip',anchor=W)
        gider_tree.heading('tax',text='Fatura',anchor=W)
        gider_tree.heading('coast',text='Tutar',anchor=W)
        gider_tree.heading('label',text='Etiket',anchor=W)
        
        gider_tree.pack(fill="both",expand=True)

        selected_gider()
        btnFsearchall = tk.Button(master=left_base,text="Tümünü Göster",background="blue",foreground="white",border=0,relief="flat",font=("Calibri",14),command=alltaxes)
        btnFsearchall.pack(side="bottom",fill="x")
        btnFsearch = tk.Button(master=left_base,text="Yenile",background="green",foreground="white",border=0,relief="flat",font=("Calibri",14),command=selected_gider)
        btnFsearch.pack(side="bottom",fill="x")
        

        ######### Fatura Ekleme Alanı ######################
        tax_type = ["Fatura","Vergi","Borç","İş Harcamaları"]

        right_base = tk.Frame(master=frame_base,background="yellow")
        right_base.pack(side="left",fill="both",expand=True,padx=50,pady=50)
        right_base.columnconfigure(0,weight=1)

        left_base.pack_propagate(False)
        right_base.pack_propagate(False)
        tk.Label(master=right_base,text="Gider Ekleme Alanı",background="white",font=("Calibri",14,"bold"),foreground="blue").pack(fill="x")

        textmetin = "Gider ekleme alanına hoşgeldiniz. Nabla size daha detaylı raporlar sunabilmek adına ödemelerinizi detaylandırmanızı ister. Öncelikle bir gider tipi seçin:"
        textw = tk.Text(master=right_base,highlightthickness=0 ,wrap="word",highlightcolor="blue",relief="flat",font=("Time New Roman",10),height=2,width=1)
        textw.insert(INSERT, textmetin)
        textw.pack(fill="x")
        textw.config(state="disabled")

        type_selector = ttk.Combobox(master=right_base,state="readonly",values=tax_type)
        type_selector.pack(fill="x")
        type_selector.bind("<<ComboboxSelected>>",type_selection)

        
        fatura_frame = tk.Frame(master=right_base,background="white")
        fatura_frame.pack(fill="both",expand=True)

        

    def odeme():
        clear_frame()
        odeme_button.configure(foreground="red",background="white")
        gider_button.configure(foreground="white",background="red")
        durum_button.configure(foreground="white",background="red")



    righ_menu_panel = tk.Frame(master=main_window, background="white")
    righ_menu_panel.place(relx=0.1,y=0,relwidth=0.9,relheight=1.0)

    base =  tk.Frame(master=righ_menu_panel,background="white")
    base.pack(fill="both",expand=True,padx=50,pady=20) 

    #top button's line ok.
    tk.Frame(master=base,background="red").pack(fill="x")

    #left limit line
    tk.Frame(master=base,background="red").pack(side="left",fill="y")

    base_master = tk.Frame(master=base, background="white")
    base_master.pack(side="left",fill="both",expand=True)

    tk.Frame(master=base,background="red").pack(side="left",fill="y")

    button_bar_frame = tk.Frame(master=base_master,background="white")
    button_bar_frame.pack(fill="x")

    durum_button =  tk.Button(master=button_bar_frame, text="Kurum Durumu",font=("Calibri",12,"bold"),relief="flat",border=0,foreground="white",background="red",borderwidth=0,command=durum)
    durum_button.pack(side="left",fill="x",expand=True)

    odeme_button =  tk.Button(master=button_bar_frame, text="Ödeme Durumları",font=("Calibri",12,"bold"),relief="flat",border=0,foreground="white",background="red",borderwidth=0,command=odeme)
    #odeme_button.pack(side="left",fill="x",expand=True)

    gider_button =  tk.Button(master=button_bar_frame, text="Ek Giderler",font=("Calibri",12,"bold"),relief="flat",border=0,foreground="white",background="red",borderwidth=0,command=gider)
    gider_button.pack(side="left",fill="x",expand=True)

    frame_base = tk.Frame(master=base_master, background="white")
    frame_base.pack(fill="both",expand=True)
    
    gider()
    
def app_page():
    righ_menu_panel = tk.Frame(master=main_window, background="white")
    righ_menu_panel.place(relx=0.1,y=0,relwidth=0.9,relheight=1.0)

    righ_menu_panel_title = Label(righ_menu_panel,text="UYGULAMA HAKKINDA",font=("Calibri",16,"bold"), foreground="#1664BC",background="white")
    righ_menu_panel_title.pack(fill="x")

    righ_menu_panel_metin = "Uygulama Üreticisi : Enes YILDIRIM\nUygulama Sürümü : 1.0.0\n"
    righ_menu_panel_word = tk.Text(master=righ_menu_panel,highlightthickness=0 ,highlightcolor="blue",relief="flat",font=("Time New Roman",12),height=5)
    righ_menu_panel_word.insert(INSERT,righ_menu_panel_metin)
    righ_menu_panel_word.pack(fill="x",padx=50)
    righ_menu_panel_word.config(state="disabled")


def about_page():
    webbrowser.open_new(r"https://nablabbs.blogspot.com/p/nabla-bagmsz-bilisim-sistemleri-yaratc.html")


def anounce_page():
    webbrowser.open_new(r"https://nablabbs.blogspot.com/p/nabla-obs-duyurular.html")


def help_page():
    righ_menu_panel = tk.Frame(master=main_window, background="white")
    righ_menu_panel.place(relx=0.1,y=0,relwidth=0.9,relheight=1.0)

    righ_menu_panel_title = Label(righ_menu_panel,text="YARDIM SAYFASI",font=("Calibri",16,"bold"), foreground="red",background="white")
    righ_menu_panel_title.pack(fill="x")

    righ_menu_panel_metin = "\nMerhaba,"
    righ_menu_panel_metin = righ_menu_panel_metin + "\n\nYardım sayfamıza hoş geldiniz! Size uygulamamızı daha iyi anlamanız ve sorunsuz kullanmanız için buradayız. Aşağıda sıkça sorulan soruların cevaplarını ve temel kullanım talimatlarını bulabilirsiniz:"
    righ_menu_panel_metin = righ_menu_panel_metin + "\n\n1. Nasıl Öğrenci Sorgulama Yaparım?: "
    righ_menu_panel_metin = righ_menu_panel_metin + "Öğrenci sorgulama ekranına geçmek için ana menüdeki 'Sorgula' veya 'Öğrenci Sorgula' gibi bir bağlantıyı tıklayın. Ardından, istediğiniz öğrencinin adını, soyadını veya kimlik numarasını girerek sorgulama yapabilirsiniz."
    righ_menu_panel_metin = righ_menu_panel_metin + "\n\n2. Verilerimi Güvende Tutuyor musunuz?: "
    righ_menu_panel_metin = righ_menu_panel_metin + "Evet, öğrenci verilerinin güvenliği bizim için önceliklidir. Tüm veriler şifrelenir ve sadece yetkili kullanıcılar tarafından erişilebilir. Verilerinizin gizliliğini sağlamak için gerekli önlemleri aldığımızdan emin olabilirsiniz."
    righ_menu_panel_metin = righ_menu_panel_metin + "\n\n3. Şifremi Unuttum, Ne Yapmalıyım?: "
    righ_menu_panel_metin = righ_menu_panel_metin + "Şifrenizi unuttuysanız, 'Şifremi Unuttum' bağlantısını tıklayarak şifrenizi yenileme veya sıfırlama seçeneğine erişebilirsiniz. E-posta adresinizi veya diğer kimlik doğrulama bilgilerinizi kullanarak yeni bir şifre oluşturabilirsiniz."
    righ_menu_panel_metin = righ_menu_panel_metin + "\n\n4. Hala Yardıma İhtiyacım Var, Kime Başvurabilirim?: "
    righ_menu_panel_metin = righ_menu_panel_metin + "Herhangi bir soru, sorun veya yardım ihtiyacınız varsa, destek ekibimiz size yardımcı olmaktan mutluluk duyacaktır. İletişim veya Destek bölümünden bizimle iletişime geçebilirsiniz."
    righ_menu_panel_metin = righ_menu_panel_metin + "\n\n Eğer daha fazla bilgiye ihtiyacınız varsa veya başka bir konuda yardım talep etmek isterseniz, lütfen bize bildirin. Size en iyi şekilde yardımcı olmak için buradayız!"
    
    righ_menu_panel_word = tk.Text(master=righ_menu_panel,highlightthickness=0 ,highlightcolor="blue",relief="flat",font=("Time New Roman",12),height=20)
    righ_menu_panel_word.insert(INSERT, righ_menu_panel_metin)
    righ_menu_panel_word.pack(fill="x",padx=50,side="top")
    righ_menu_panel_word.config(state="disabled")


    help_button = tk.Button(righ_menu_panel,text="Kullanıcı Adımı Unuttum :(",command=lambda: print("Şifremi Unuttum!"),border=2,font=("Calibri",12,"bold"),relief="flat",highlightthickness=10, activebackground='#1664BC',activeforeground="white",highlightcolor="blue").pack(fill="x",side="top",padx=50,pady=5)


    help_button = tk.Button(righ_menu_panel,text="Şiremi Unuttum :(",command=lambda: print("Şifremi Unuttum!"),border=2,font=("Calibri",12,"bold"),relief="flat",highlightthickness=10, activebackground='#1664BC',activeforeground="white",highlightcolor="blue").pack(fill="x",side="top",padx=50,pady=5)

    help_button = tk.Button(righ_menu_panel,text="Yardım İste!",command=lambda: print("Yardım Talebi"),border=2,font=("Calibri",12,"bold"),relief="flat",highlightthickness=10, activebackground='#1664BC',activeforeground="white",highlightcolor="blue").pack(fill="x",side="top",padx=50,pady=5)


def save_student():

    def getdata():
        ogr_adi_str = (str(ogr_adi.get())).lower()
        ogr_soyadi_str = (str(ogr_soyadi.get())).lower()
        ogr_tc_str = int(ogr_tc.get())
        ogr_anne_str = (str(ogr_anne.get())).lower()
        ogr_baba_str = (str(ogr_baba.get())).lower()
        ogr_class_str = int(ogr_class.get())
        ogr_school_str = (str(ogr_school.get())).lower()
        ogr_email_str = (str(ogr_email.get())).lower()
        ogr_adres_str = (ent_ogr_adress.get("1.0","end-1c")).lower()
        ogr_parent_tel_str = (ogr_parent_tel.get())
        ogr_tel_str = (ogr_tel.get())
        

        # for payment

        
        ogr_key = f"{ogr_adi_str[0]}{ogr_soyadi_str[0]}{ogr_tc_str}"

        query = f"insert into student (name, surname, personal_id, mother_name, father_name, class, school, email, adres, parent_tel, student_tel, student_key)"
        query = query + f" values ('{ogr_adi_str}','{ogr_soyadi_str}','{ogr_tc_str}','{ogr_anne_str}','{ogr_baba_str}','{ogr_class_str}','{ogr_school_str}','{ogr_email_str}','{ogr_adres_str}','{ogr_parent_tel_str}','{ogr_tel_str}','{ogr_key}')"
        try:
            mycursor.execute(query)
            mydb.commit()

            # for payment
            # insert into paymet_student (student_key, payment_day, payment_coast, month1) values ('mybdsjdbfısdb', '15', '1500','yes')
            query = f"insert into paymet_student (student_key, payment_day, payment_coast, first_month) values ('{ogr_key}', {ent3_add_quiz.get()}, {ent2_add_quiz.get()},{ent1_add_quiz.get()})"
            
            mycursor.execute(query)
            mydb.commit()

        except :
            tk.messagebox.showerror(title=None, message="Öğrenci zaten kayıtlı!")



    ogr_adi = tk.StringVar()
    ogr_soyadi = tk.StringVar()
    ogr_tc = tk.IntVar()
    ogr_tc.set("")
    ogr_anne = tk.StringVar()
    ogr_baba = tk.StringVar()
    ogr_class = tk.IntVar()
    ogr_class.set("")
    ogr_school = tk.StringVar()
    ogr_email = tk.StringVar()
    ogr_adres = "naber"
    ogr_parent_tel = tk.StringVar()
    ogr_parent_tel.set("")
    ogr_tel = tk.StringVar()
    ogr_tel.set("")
    

    ogr_save_frame = tk.Frame(master=main_window, background="white")
    
    ogr_save_frame.place(relx=0.1,y=0,relwidth=0.9,relheight=1.0)


    ogr_save_frame_titlebar = tk.Frame(master=ogr_save_frame,background="white")
    ogr_save_frame_titlebar.pack(side="top",fill="x")

    ogr_save_frame_button = tk.Button(master=ogr_save_frame_titlebar, text="\u2190",font=("Calibri",20,"bold"),border=0,relief="flat",highlightthickness=0, activebackground='white',activeforeground="orange",highlightcolor="blue",foreground="orange",background="white",command=student_page)
    ogr_save_frame_button.pack(side="left",padx=10,pady=5)
    
    ogr_save_frame_title = Label(master=ogr_save_frame,text="Öğrenci Kaydetme Ekranı",font=("Calibri",16,"bold"), foreground="#1664BC",background="white")
    ogr_save_frame_title.pack(fill="x")

    ogr_save_frame_general = tk.Frame(master=ogr_save_frame, background="white")
    ogr_save_frame_general.pack(padx=50,side="left",fill="y")

    ogr_save_frame_general.columnconfigure(1,weight=1)



    lbl_ogr_adi = Label(ogr_save_frame_general, text="Öğrenci Adı",font=("Times New Roman",12), foreground="black",background="white").grid(row=0,column=0,sticky="wn",pady=10,padx=5)
    lbl_ogr_soyadi = Label(ogr_save_frame_general, text="Öğrenci Soyadı",font=("Times New Roman",12), foreground="black",background="white").grid(row=1,column=0,sticky="wn",pady=10,padx=5)
    lbl_ogr_tc = Label(ogr_save_frame_general, text="T.C. Kimlik No",font=("Times New Roman",12), foreground="black",background="white").grid(row=2,column=0,sticky="wn",pady=10,padx=5)
    lbl_ogr_anne = Label(ogr_save_frame_general, text="Anne Adı",font=("Times New Roman",12), foreground="black",background="white").grid(row=3,column=0,sticky="wn",pady=10,padx=5)
    lbl_ogr_baba = Label(ogr_save_frame_general, text="Baba Adı",font=("Times New Roman",12), foreground="black",background="white").grid(row=4,column=0,sticky="wn",pady=10,padx=5)
    lbl_ogr_class = Label(ogr_save_frame_general, text="Sınıf",font=("Times New Roman",12), foreground="black",background="white").grid(row=5,column=0,sticky="wn",pady=10,padx=5)
    lbl_ogr_School = Label(ogr_save_frame_general, text="Okulu",font=("Times New Roman",12), foreground="black",background="white").grid(row=6,column=0,sticky="wn",pady=10,padx=5)
    lbl_ogr_email = Label(ogr_save_frame_general, text="e-mail",font=("Times New Roman",12), foreground="black",background="white").grid(row=7,column=0,sticky="wn",pady=10,padx=5)
    lbl_ogr_adress = Label(ogr_save_frame_general, text="Adres",font=("Times New Roman",12), foreground="black",background="white").grid(row=8,column=0,sticky="nwn",pady=10,padx=5)
    lbl_ogr_parent_tel = Label(ogr_save_frame_general, text="Veli Tel. No",font=("Times New Roman",12), foreground="black",background="white").grid(row=9,column=0,sticky="nwn",pady=10,padx=5)
    lbl_ogr_tel = Label(ogr_save_frame_general, text="Öğrenci Tel. No",font=("Times New Roman",12), foreground="black",background="white").grid(row=10,column=0,sticky="nwn",pady=10,padx=5)

    ent_ogr_adi = tk.Entry(ogr_save_frame_general,font=("Times New Roman",12), foreground="#1664BC",background="white",textvariable=ogr_adi).grid(row=0,column=1,sticky="wn",pady=10,padx=5)
    ent_ogr_soyadi = tk.Entry(ogr_save_frame_general, font=("Times New Roman",12), foreground="#1664BC",background="white",textvariable=ogr_soyadi).grid(row=1,column=1,sticky="wn",pady=10,padx=5)
    ent_ogr_tc = tk.Entry(ogr_save_frame_general, font=("Times New Roman",12), foreground="#1664BC",background="white",textvariable=ogr_tc).grid(row=2,column=1,sticky="wn",pady=10,padx=5)
    ent_ogr_anne = tk.Entry(ogr_save_frame_general, font=("Times New Roman",12), foreground="#1664BC",background="white",textvariable=ogr_anne).grid(row=3,column=1,sticky="wn",pady=10,padx=5)
    ent_ogr_baba = tk.Entry(ogr_save_frame_general, font=("Times New Roman",12), foreground="#1664BC",background="white",textvariable=ogr_baba).grid(row=4,column=1,sticky="wn",pady=10,padx=5)
    ent_ogr_class = tk.Entry(ogr_save_frame_general, font=("Times New Roman",12), foreground="#1664BC",background="white",textvariable=ogr_class).grid(row=5,column=1,sticky="wn",pady=10,padx=5)
    ent_ogr_School = tk.Entry(ogr_save_frame_general, font=("Times New Roman",12), foreground="#1664BC",background="white",textvariable=ogr_school).grid(row=6,column=1,sticky="wn",pady=10,padx=5)
    ent_ogr_email = tk.Entry(ogr_save_frame_general, font=("Times New Roman",12), foreground="#1664BC",background="white",textvariable=ogr_email).grid(row=7,column=1,sticky="wn",pady=10,padx=5)
    ent_ogr_adress = tk.Text(ogr_save_frame_general, font=("Times New Roman",12),height=2,width=20,wrap="word", foreground="#1664BC",background="white")
    ent_ogr_adress.grid(row=8,column=1,sticky="wn",pady=10,padx=5)
    ent_ogr_parent_tel = tk.Entry(ogr_save_frame_general, font=("Times New Roman",12), foreground="#1664BC",background="white",textvariable=ogr_parent_tel).grid(row=9,column=1,sticky="wn",pady=10,padx=5)
    ent_ogr_tel = tk.Entry(ogr_save_frame_general, font=("Times New Roman",12), foreground="#1664BC",background="white",textvariable=ogr_tel).grid(row=10,column=1,sticky="wn",pady=10,padx=5)

    
    payment_frame = tk.Frame(master=ogr_save_frame, background="white")
    payment_frame.pack(padx=50,fill="both",expand=True,side="left")

    klavuz_text = "\nÖğrenci kaydetme ekranına hoşgeldiniz! Umarız ki verimli bir süreç olur.\n\n"
    klavuz_text = klavuz_text + f"\nBu ekranda öğrencinin verilerinin işlenebilmesi adına doğru bilgileri doldurmaya özen gösteriniz." 
    klavuz_text = klavuz_text +"\nKaydedilecek öğrenci için bir hesap kesim tarihi belirlenmesi ve taksit tutarlarının doğru girilmesi finansal açıdan sizin için önemlidir."
    
    klavuz_widget_word = tk.Text(master=payment_frame,highlightthickness=0 ,wrap="word",highlightcolor="blue",relief="flat",font=("Time New Roman",10),height=8)
    klavuz_widget_word.insert(INSERT, klavuz_text)
    klavuz_widget_word.pack(fill="x")
    klavuz_widget_word.config(state="disabled")

    payentframe = tk.Frame(master=payment_frame,highlightthickness=1,highlightbackground="red",background="white")
    payentframe.pack()

    #months2pay = ["Ocak", "Subat", "Mart", "Nisan", "Mayis", "Haziran", "Temmuz", "Agustos", "Eylül", "Ekim", "Kasim", "Aralik"]
    months2pay = [1,2,3,4,5,6,7,8,9,10,11,12]

    # Labels for adding quiz
    lb1_pay = tk.Label(master=payentframe, text="HESAP K.",background="white")
    lb1_pay.grid(row=0,column=0,sticky="we",padx=5)

    lb2_pay = tk.Label(master=payentframe, text="TUTAR",background="white")
    lb2_pay.grid(row=0,column=1,sticky="we",padx=5)

    lb3_pay = tk.Label(master=payentframe, text="İLK AY",background="white")
    lb3_pay.grid(row=0,column=2,sticky="we",padx=5)

    

    ent1_add_quiz = ttk.Combobox(master=payentframe,state="readonly", values=months2pay)
    ent1_add_quiz.grid(row=1,column=2,sticky="we",pady=5,padx=5)
    

    ent2_add_quiz = tk.Entry(master=payentframe,background="white")
    ent2_add_quiz.grid(row=1,column=1,sticky="we",pady=5,padx=5)
    
    ent3_add_quiz = tk.Entry(master=payentframe,background="white")
    ent3_add_quiz.grid(row=1,column=0,sticky="we",pady=5,padx=5)


    add_quiz_commit_button = tk.Button(master=payentframe, text="Uygula",font=("Calibri",12),relief="flat",border=0,width=10,foreground="white",background="red",borderwidth=0)
    add_quiz_commit_button.grid(row=2,column=0,columnspan=3,sticky="we")


    klavuz_text = "\n\n\nSon uyarılar :\n\n"
    klavuz_text = klavuz_text + f"\nÖğrenciniz burslu ise burs oranına göre aylık ücretini doğru biçimde yazmayı unutmayın." 
    klavuz_text = klavuz_text +"\nToplanan ücret bilgileri sadece programın kurulu olduğu şahsi bilgisayarda depolanır. Nabla bu verileri dışarı aktarmaz."
    
    klavuz_widget_word = tk.Text(master=payment_frame,highlightthickness=0 ,wrap="word",highlightcolor="blue",relief="flat",font=("Time New Roman",10),height=13,foreground="red")
    klavuz_widget_word.insert(INSERT, klavuz_text)
    klavuz_widget_word.pack(fill="x")
    klavuz_widget_word.config(state="disabled")

    btn_save_ogr = tk.Button(master=payment_frame, text="KAYDET",font=("Calibri",14),relief="flat",border=0,foreground="white",background="#6DF158",command=getdata).pack(fill="x")
    btn_clear_ogr = tk.Button(master=payment_frame, text="TEMİZLE",font=("Calibri",14),relief="flat",border=0,foreground="white",background="#3FB0F0").pack(fill="x")


def see_student():

    def get_ogr():
        selected_line = ogr_search_result_tree.focus()

        selected_row = ogr_search_result_tree.item(selected_line)
        selected_ogr = selected_row.get("values")

        ogr_profile_page(selected_ogr)

        


    def clear_all():
        for item in ogr_search_result_tree.get_children():
            ogr_search_result_tree.delete(item)

    def search_ogr():
        clear_all()

        search_source = ogr_search.get()

        # for name
        search_ogr_query = f"Select * from student where '{search_source}' IN (name, surname, personal_id, mother_name, father_name, class, school, email, adres, parent_tel, student_tel, student_key);"
        mycursor.execute(search_ogr_query)
        finded_ogr = mycursor.fetchall()
        idcount = 0
        for i in finded_ogr:
            ogr_search_result_tree.insert(parent='',index="end",iid=idcount,values=(i))
            idcount = idcount+1
        
    def del_ogr():
        search_source = ogr_search_result_tree.focus()
        search_values = ogr_search_result_tree.item(search_source).get('values')
        search_source = search_values[-1]

        search_ogr_query = f"delete from student where '{search_source}' IN (student_key);"
        mycursor.execute(search_ogr_query)
        search_ogr_query = f"delete from paymet_student where '{search_source}' IN (student_key);"
        mycursor.execute(search_ogr_query)
        mydb.commit()
        search_ogr()



    ogr_see_frame = tk.Frame(master=main_window, background="white")    
    ogr_see_frame.place(relx=0.1,y=0,relwidth=0.9,relheight=1.0)

    ogr_see_frame_titlebar = tk.Frame(master=ogr_see_frame,background="white")
    ogr_see_frame_titlebar.pack(side="top",fill="x")

    ogr_see_frame_button = tk.Button(master=ogr_see_frame_titlebar, text="\u2190",font=("Calibri",20,"bold"),border=0,relief="flat",highlightthickness=0, activebackground='white',activeforeground="orange",highlightcolor="blue",foreground="orange",background="white",command=student_page)
    ogr_see_frame_button.pack(side="left",padx=10,pady=5)


    ogr_see_frame_title = Label(master=ogr_see_frame,text="Gözlem ve Veri Ekleme Alanı",font=("Calibri",16,"bold"), foreground="#1664BC",background="white")
    ogr_see_frame_title.pack(fill="x")

    ogr_see_search_frame = tk.Frame(master=ogr_see_frame,background="white")
    ogr_see_search_frame.pack(fill="x",pady=10,padx=200)

    ogr_search = tk.StringVar(master=ogr_see_search_frame)
    ogr_see_search_frame_entry =  tk.Entry(ogr_see_search_frame, font=("Times New Roman",16), foreground="#1664BC",background="white",textvariable=ogr_search)
    ogr_see_search_frame_entry.pack(side="left",fill="both",expand=True)

    ogr_see_search_frame_btn_search = tk.Button(master=ogr_see_search_frame,width=10, text="ARA",font=("Calibri",16,"bold"),relief="flat",border=0,foreground="white",background="#6DF158",borderwidth=0,command=search_ogr)
    ogr_see_search_frame_btn_search.pack(fill="x",side="left", padx=5)


    
    ogr_search_result_tree = ttk.Treeview(ogr_see_frame)
    ogr_search_result_tree['columns'] = (
        'Database ID',
        'Ad',
        'Soyad',
        'TC',
        'Anne Adı',
        'Baba Adı',
        'Sınıf',
        'Okul',
        'Email',
        'Adres',
        'VTel',
        'OTel',
        'OGR_KEY'
        )

    ogr_search_result_tree.column('#0',width=0,stretch=NO)
    ogr_search_result_tree.column('Database ID',minwidth=100,width=100)
    ogr_search_result_tree.column('Ad',minwidth=100,width=100)
    ogr_search_result_tree.column('Soyad',minwidth=100,width=100)
    ogr_search_result_tree.column('TC',minwidth=100,width=100)
    ogr_search_result_tree.column('Anne Adı',minwidth=100,width=100)
    ogr_search_result_tree.column('Baba Adı',minwidth=100,width=100)
    ogr_search_result_tree.column('Sınıf',minwidth=100,width=100)
    ogr_search_result_tree.column('Okul',minwidth=100,width=100)
    ogr_search_result_tree.column('Email',minwidth=100,width=100)
    ogr_search_result_tree.column('Adres',minwidth=100,width=100)
    ogr_search_result_tree.column('VTel',minwidth=100,width=100)
    ogr_search_result_tree.column('OTel',minwidth=100,width=100)
    ogr_search_result_tree.column('OGR_KEY',minwidth=0,width=0,stretch=NO)

    ogr_search_result_tree.heading('Database ID',text="DBID",anchor=W)
    ogr_search_result_tree.heading('Ad',text="AD",anchor=W)
    ogr_search_result_tree.heading('Soyad',text="Soyad",anchor=W)
    ogr_search_result_tree.heading('TC',text="TC",anchor=W)
    ogr_search_result_tree.heading('Anne Adı',text="Anne Adı",anchor=W)
    ogr_search_result_tree.heading('Baba Adı',text="Baba Adı",anchor=W)
    ogr_search_result_tree.heading('Sınıf',text="Sınıf",anchor=W)
    ogr_search_result_tree.heading('Okul',text="Okul",anchor=W)
    ogr_search_result_tree.heading('Email',text="e-posta",anchor=W)
    ogr_search_result_tree.heading('Adres',text="Adres",anchor=W)
    ogr_search_result_tree.heading('VTel',text="Veli İletişim",anchor=W)
    ogr_search_result_tree.heading('OTel',text="Öğrenci İletişim",anchor=W)
    ogr_search_result_tree.heading('OGR_KEY',text="Öğrenci Anahtarı",anchor=W)
    
    


    ogr_search_result_tree.pack(pady=20,padx=50,fill="both",expand=True)

    ogr_see_search_frame_btn_getdata = tk.Button(master=ogr_see_frame, text="Verileri Getir",font=("Calibri",16,"bold"),relief="flat",border=0,foreground="white",background="#6DF158",borderwidth=0,command=get_ogr)
    ogr_see_search_frame_btn_deldata = tk.Button(master=ogr_see_frame, text="Öğrenci Verisini Sil",font=("Calibri",16,"bold"),relief="flat",border=0,foreground="white",background="red",borderwidth=0,command=del_ogr)
    ogr_see_search_frame_btn_getdata.pack(fill="x",padx=50,pady=5)
    ogr_see_search_frame_btn_deldata.pack(fill="x",padx=50,pady=10)

    """
    
    ogr_see_scroll_base = Frame(master=ogr_see_frame, background="green")
    ogr_see_scroll_base.pack(expand=True, fill="both",padx=50,pady=20)

    ogr_see_scroll_canvas = Canvas(master=ogr_see_scroll_base,bg="blue")
    ogr_see_scroll_canvas.pack(side="left",fill="both",expand=True)

    ogr_see_scrollbar = tk.Scrollbar(master=ogr_see_scroll_base,orient=VERTICAL,command=ogr_see_scroll_canvas.yview)
    ogr_see_scrollbar.pack(side="right",fill="y")

    ogr_see_scroll_canvas.configure(yscrollcommand=ogr_see_scrollbar.set)
    ogr_see_scroll_canvas.bind('<Configure>',lambda e: ogr_see_scroll_canvas.configure(scrollregion=ogr_see_scroll_canvas.bbox("all")))

    ogr_see_scroll_frame = tk.Frame(master=ogr_see_scroll_canvas, background="pink")
    ogr_see_scroll_frame.pack(expand=True,fill="both")
    ogr_see_scroll_frame.pack_propagate(False)
    
    ogr_see_scroll_canvas.create_window((0,0),window=ogr_see_scroll_frame)


    """


def ogr_profile_page(ogr):

    # define student values.
    ogr_dbid = ogr[0]
    ogr_adi = ogr[1]
    ogr_soyadi = ogr[2]
    ogr_tc = ogr[3]
    ogr_anne = ogr[4]
    ogr_baba = ogr[5]
    ogr_class = ogr[6]
    ogr_school = ogr[7]
    ogr_email = ogr[8]
    ogr_adres = ogr[9]
    ogr_parent_tel = ogr[10]
    ogr_tel = ogr[11]
    ogr_key = ogr[12]


    classes_dersler = []

    if ogr_class == 1 :

        classes_dersler.append("Matematik")
        classes_dersler.append("Türkçe")
        classes_dersler.append("Hayat Bilgisi")
        classes_dersler.append("Görsel Sanatlar")
        classes_dersler.append("Müzik")
        classes_dersler.append("Beden Eğitimi")

    elif ogr_class == 2 : 

        classes_dersler.append("Matematik")
        classes_dersler.append("Türkçe")
        classes_dersler.append("Hayat Bilgisi")
        classes_dersler.append("İngilizce")
        classes_dersler.append("Görsel Sanatlar")
        classes_dersler.append("Müzik")
        classes_dersler.append("Beden Eğitimi")

    elif ogr_class == 3 :

        classes_dersler.append("Matematik")
        classes_dersler.append("Türkçe")
        classes_dersler.append("Hayat Bilgisi")
        classes_dersler.append("Fen Bilgisi")
        classes_dersler.append("İngilizce")
        classes_dersler.append("Görsel Sanatlar")
        classes_dersler.append("Müzik")
        classes_dersler.append("Beden Eğitimi")

    elif ogr_class == 4:

        classes_dersler.append("Matematik")
        classes_dersler.append("Türkçe")
        classes_dersler.append("Fen Bilgisi")
        classes_dersler.append("Sosyal Bilgiler")
        classes_dersler.append("İngilizce")
        classes_dersler.append("Din Kültürü")
        classes_dersler.append("Görsel Sanatlar")
        classes_dersler.append("Müzik")
        classes_dersler.append("Beden Eğitimi")
        classes_dersler.append("Trafik")
        classes_dersler.append("Yurttaşlık ve Demokrasi")

    elif ogr_class == 5:

        classes_dersler.append("Matematik")
        classes_dersler.append("Türkçe")
        classes_dersler.append("Fen Bilgisi")
        classes_dersler.append("Sosyal Bilgiler")
        classes_dersler.append("İngilizce")
        classes_dersler.append("Din Kültürü")
        classes_dersler.append("Görsel Sanatlar")
        classes_dersler.append("Müzik")
        classes_dersler.append("Beden Eğitimi")
        classes_dersler.append("Bilişim Teknolojileri")

    elif ogr_class == 6:

        classes_dersler.append("Matematik")
        classes_dersler.append("Türkçe")
        classes_dersler.append("Fen Bilgisi")
        classes_dersler.append("Sosyal Bilgiler")
        classes_dersler.append("İngilizce")
        classes_dersler.append("Din Kültürü")
        classes_dersler.append("Görsel Sanatlar")
        classes_dersler.append("Müzik")
        classes_dersler.append("Beden Eğitimi")
        classes_dersler.append("Bilişim Teknolojileri")

    elif ogr_class == 7:

        classes_dersler.append("Matematik")
        classes_dersler.append("Türkçe")
        classes_dersler.append("Fen Bilgisi")
        classes_dersler.append("Sosyal Bilgiler")
        classes_dersler.append("İngilizce")
        classes_dersler.append("Din Kültürü")
        classes_dersler.append("Görsel Sanatlar")
        classes_dersler.append("Müzik")
        classes_dersler.append("Beden Eğitimi")
        classes_dersler.append("Teknoloji ve Tasarım")


    elif ogr_class == 8:

        classes_dersler.append("Matematik")
        classes_dersler.append("Türkçe")
        classes_dersler.append("Fen Bilgisi")
        classes_dersler.append("İnklap Tarihi")
        classes_dersler.append("İngilizce")
        classes_dersler.append("Din Kültürü")
        classes_dersler.append("Görsel Sanatlar")
        classes_dersler.append("Müzik")
        classes_dersler.append("Beden Eğitimi")
        classes_dersler.append("Teknoloji ve Tasarım")
        classes_dersler.append("Kariyer Planlama")

    elif ogr_class > 8 :
        classes_dersler.append("Türkçe")
        classes_dersler.append("Matematik")
        classes_dersler.append("Fizik")
        classes_dersler.append("Kimya")
        classes_dersler.append("Biyoloji")
        classes_dersler.append("Tarih")
        classes_dersler.append("Coğrafya")
        classes_dersler.append("İnkılap Tarihi ve Atatürkçülük")
        classes_dersler.append("Yabancı Dil (Genellikle İngilizce)")
        classes_dersler.append("Din Kültürü ve Ahlak Bilgisi")
        classes_dersler.append("Beden Eğitimi")
        classes_dersler.append("Görsel Sanatlar")
        classes_dersler.append("Müzik")
        classes_dersler.append("Rehberlik ve Psikolojik Danışmanlık")
        classes_dersler.append("Felsefe")
        classes_dersler.append("Mantık")
        classes_dersler.append("Edebiyat")
        classes_dersler.append("Dil ve Anlatım")
        classes_dersler.append("İş Sağlığı ve Güvenliği")
        classes_dersler.append("Trafik ve İlk Yardım")
        classes_dersler.append("Teknoloji Tasarımı")
        classes_dersler.append("Bilgisayar")
        classes_dersler.append("Bilişim Teknolojileri")


    classes_exam = []

    if ogr_class == 1 :

        classes_exam.append("Matematik")
        classes_exam.append("Türkçe")
        classes_exam.append("Hayat Bilgisi")


    elif ogr_class == 2 : 

        classes_exam.append("Matematik")
        classes_exam.append("Türkçe")
        classes_exam.append("Hayat Bilgisi")
        classes_exam.append("İngilizce")


    elif ogr_class == 3 :

        classes_exam.append("Matematik")
        classes_exam.append("Türkçe")
        classes_exam.append("Hayat Bilgisi")
        classes_exam.append("Fen Bilgisi")
        classes_exam.append("İngilizce")


    elif ogr_class == 4:

        classes_exam.append("Matematik")
        classes_exam.append("Türkçe")
        classes_exam.append("Fen Bilgisi")
        classes_exam.append("Sosyal Bilgiler")
        classes_exam.append("İngilizce")
        classes_exam.append("Din Kültürü")


    elif ogr_class == 5:

        classes_exam.append("Matematik")
        classes_exam.append("Türkçe")
        classes_exam.append("Fen Bilgisi")
        classes_exam.append("Sosyal Bilgiler")
        classes_exam.append("İngilizce")
        classes_exam.append("Din Kültürü")


    elif ogr_class == 6:

        classes_exam.append("Matematik")
        classes_exam.append("Türkçe")
        classes_exam.append("Fen Bilgisi")
        classes_exam.append("Sosyal Bilgiler")
        classes_exam.append("İngilizce")
        classes_exam.append("Din Kültürü")


    elif ogr_class == 7:

        classes_exam.append("Matematik")
        classes_exam.append("Türkçe")
        classes_exam.append("Fen Bilgisi")
        classes_exam.append("Sosyal Bilgiler")
        classes_exam.append("İngilizce")
        classes_exam.append("Din Kültürü")



    elif ogr_class == 8:

        classes_exam.append("Matematik")
        classes_exam.append("Türkçe")
        classes_exam.append("Fen Bilgisi")
        classes_exam.append("İnklap Tarihi")
        classes_exam.append("İngilizce")
        classes_exam.append("Din Kültürü")


    elif ogr_class > 8 :
        classes_exam.append("Türkçe")
        classes_exam.append("Matematik")
        classes_exam.append("Fizik")
        classes_exam.append("Kimya")
        classes_exam.append("Biyoloji")
        classes_exam.append("Tarih")
        classes_exam.append("Coğrafya")
        classes_exam.append("İnkılap Tarihi ve Atatürkçülük")
        classes_exam.append("Yabancı Dil (Genellikle İngilizce)")
        classes_exam.append("Din Kültürü ve Ahlak Bilgisi")
        classes_exam.append("Felsefe")
        classes_exam.append("Edebiyat")
        classes_exam.append("Dil ve Anlatım")





    def clear_frame():
        for widgets in frame_right_window_base.winfo_children():
            widgets.destroy()

    def profile_summary():
        clear_frame()



        summary_note_button.configure(background="white",foreground="#1664BC")
        add_quiz_button.configure(background="#1664BC",foreground="white")
        add_exam_button.configure(background="#1664BC",foreground="white")
        add_note_button.configure(background="#1664BC",foreground="white")

        frame_right_window = tk.Frame(frame_right_window_base,background="white")
        frame_right_window.pack(fill="both",expand=True)





    def add_quiz():
        clear_frame()

        def calculate_pass_quiz():
            quiz_name = (str(ent1_add_quiz.get())).lower()
            quiz_total = int(ent2_add_quiz.get())
            quiz_true = int(ent3_add_quiz.get())
            quiz_false = quiz_total-quiz_true
            quiz_totpoint = int(ent4_add_quiz.get())
            
            pointperquest = quiz_totpoint/quiz_total
            quiz_point = quiz_true*pointperquest

            # Send Quiz to database
            quiz_query = f"insert into quiz (time, student_key, lesson, total_question, answered_true, answered_false, score) values(CURRENT_TIMESTAMP, '{ogr_key}','{quiz_name}',{quiz_total},{quiz_true},{quiz_false},{quiz_point});"
            mycursor.execute(quiz_query)
            mydb.commit()

            tk.messagebox.showinfo(title=None, message=f"Sınav Kaydedildi!\nSınav notu:{quiz_point}")

        add_quiz_button.configure(background="white",foreground="#1664BC")
        see_quiz_button.configure(background="#1664BC",foreground="white")
        #summary_note_button.configure(background="#1664BC",foreground="white")
        #add_exam_button.configure(background="#1664BC",foreground="white")
        #see_exam_button.configure(background="#1664BC",foreground="white")
        #add_note_button.configure(background="#1664BC",foreground="white")
        payment_button.configure(background="#1664BC",foreground="white")


        frame_right_window = tk.Frame(frame_right_window_base,background="white")
        frame_right_window.pack(fill="both",expand=True)


        klavuz_text = "\nQuiz ekleme alanına hoşgeldiniz. \n\n"
        klavuz_text = klavuz_text + f"\nSistemimizde 'Quiz' ifadesi tek dersi kapsayan sınavlar için kullanılmaktadır. Aşağıdaki adımları uygulayarak {ogr[1]} için bir quiz ekleyin. " 
        klavuz_text = klavuz_text +"\n\t 1. Ders Seçin."
        klavuz_text = klavuz_text +"\n\t 2. Quizdeki toplam soru adedini girin."
        klavuz_text = klavuz_text +"\n\t 3. Doğru cevap sayısını girin."
        klavuz_text = klavuz_text +"\n\t 4. Tam puan değerini girin."
        klavuz_text = klavuz_text + f"\n Program sizin için {ogr[1]} adlı öğrencinin notunu hesaplayıp kaydedecektir. Tüm quizleri kayıtlar adlı bölümden gözlemleyebilirsiniz."
        
        klavuz_widget_word = tk.Text(master=frame_right_window,highlightthickness=0 ,wrap="word",highlightcolor="blue",relief="flat",font=("Time New Roman",10),height=14)
        klavuz_widget_word.insert(INSERT, klavuz_text)
        klavuz_widget_word.pack(fill="x",padx=50)
        klavuz_widget_word.config(state="disabled")


        frame_summary_add_quiz = tk.Frame(master=frame_right_window,highlightthickness=1,highlightbackground="#1664BC",background="white")
        frame_summary_add_quiz.pack()

        # Labels for adding quiz
        lbl1_add_quiz = tk.Label(master=frame_summary_add_quiz, text="DERS",background="white")
        lbl1_add_quiz.grid(row=0,column=0,sticky="we",padx=5)

        lbl2_add_quiz = tk.Label(master=frame_summary_add_quiz, text="SORU SAYISI",background="white")
        lbl2_add_quiz.grid(row=0,column=1,sticky="we",padx=5)

        lbl3_add_quiz = tk.Label(master=frame_summary_add_quiz, text="DOĞRU CEVAP",background="white")
        lbl3_add_quiz.grid(row=0,column=2,sticky="we",padx=5)

        lbl4_add_quiz = tk.Label(master=frame_summary_add_quiz, text="TAM PUAN",background="white")
        lbl4_add_quiz.grid(row=0,column=3,sticky="we",padx=5)

        
        optionmenu_variable_for_class = tk.StringVar()
        optionmenu_variable_for_class.set(classes_dersler[0]) # default value

        ent1_add_quiz = ttk.Combobox(master=frame_summary_add_quiz,state="readonly", values=classes_dersler)
        ent1_add_quiz.grid(row=1,column=0,sticky="we",pady=5,padx=5)

        ent2_add_quiz = tk.Entry(master=frame_summary_add_quiz,background="white")
        ent2_add_quiz.grid(row=1,column=1,sticky="we",pady=5,padx=5)
        
        ent3_add_quiz = tk.Entry(master=frame_summary_add_quiz,background="white")
        ent3_add_quiz.grid(row=1,column=2,sticky="we",pady=5,padx=5)

        ent4_add_quiz = tk.Entry(master=frame_summary_add_quiz,background="white")
        ent4_add_quiz.grid(row=1,column=3,sticky="we",pady=5,padx=5)

        add_quiz_commit_button = tk.Button(master=frame_summary_add_quiz, text="Sınav Ekle",font=("Calibri",12),relief="flat",border=0,width=10,foreground="white",background="#1664BC",borderwidth=0,command=calculate_pass_quiz)
        add_quiz_commit_button.grid(row=2,column=0,columnspan=4,sticky="we")


    def see_quiz_data():
        
        def clear_all():
            for item in see_quiz_tree.get_children():
                see_quiz_tree.delete(item)

        def get_quiz_data():

            clear_all()
            
            def plot():
                plt.figure(1)
                plt.title(f"{ogr_adi.lower()} - {str(comboclass.get()).lower()} başarı grafiği: ")
                plt.xlabel("Sınavlar")
                plt.ylabel("Başarı Yüzdesi")
                plt.plot(x,y)
                plt.scatter(x,y,s=100,c="red")
                plt.xticks(x)
                plt.show()

            
            
            search_source = ogr_key

            # query example : select * from quiz where student_key like 'mg12131415161' and lesson like 'türkçe'
            search_ogr_query = f"Select * from quiz where student_key like '{ogr_key}' and lesson like '{str(comboclass.get()).lower()}';"
            mycursor.execute(search_ogr_query)
            finded_ogr = mycursor.fetchall()
            idcount = 0
            tr_caunt = 0
            sucsess_percent = []
            for i in finded_ogr:
                see_quiz_tree.insert(parent='',index="end",iid=idcount,values=(i[1],i[3],i[4],i[5],i[6],i[7]))
                idcount = idcount+1
                suc = float(i[4])
                suc = 100/suc

                suc = suc*int(i[5])

                sucsess_percent.append([idcount,suc])
            


            x = []
            y = []
            for i in range(len(sucsess_percent)):
                x.append(sucsess_percent[i][0])
                y.append(sucsess_percent[i][1])
                 

            

            succes_button.configure(text=f"{str(comboclass.get())} dersi için başarı grafiği çizdir!")
            succes_button.configure(command=plot)


        clear_frame()
        
        see_quiz_button.configure(background="white",foreground="#1664BC")
        add_quiz_button.configure(background="#1664BC",foreground="white")
        #add_exam_button.configure(background="#1664BC",foreground="white")
        #see_exam_button.configure(background="#1664BC",foreground="white")
        #summary_note_button.configure(background="#1664BC",foreground="white")
        #add_note_button.configure(background="#1664BC",foreground="white")
        payment_button.configure(background="#1664BC",foreground="white")


        frame_right_window = tk.Frame(frame_right_window_base,background="white")
        frame_right_window.pack(fill="both",expand=True)

        klavuz_text = "\nBu alanda eklenen quiz verilerini gözlemleyebilirsiniz. \n\n"
        klavuz_text = klavuz_text + f"\nSistemimizde {ogr[1]} adlı öğrenci için toplanan verilerin incelenmesi adına aşağıdaki eylemleri gerçekleştirin." 
        klavuz_text = klavuz_text +"\nBir ders seçin ve sonuçları getir butonu ile listeleyin. Daha sonra isterseniz seçilen ders kapsamında elde edilen sonuçları grafik haline getirebilirsiniz."
        
        klavuz_widget_word = tk.Text(master=frame_right_window,highlightthickness=0 ,wrap="word",highlightcolor="blue",relief="flat",font=("Time New Roman",10),height=8)
        klavuz_widget_word.insert(INSERT, klavuz_text)
        klavuz_widget_word.pack(fill="x",padx=50)
        klavuz_widget_word.config(state="disabled")

        frame_right_window_class_selection = tk.Frame(master=frame_right_window,highlightthickness=1,highlightbackground="#1664BC",background="white")
        frame_right_window_class_selection.pack(fill="x",padx=50)

        combolesson = tk.Label(master=frame_right_window_class_selection,text="Ders Seçin: ",font=("Calibri",12),foreground="#1664BC",background="white")
        combolesson.pack(fill="y",side="left")

        # quiz analize section.
        comboclass = ttk.Combobox(master=frame_right_window_class_selection,state="readonly", values=classes_dersler)
        comboclass.pack(fill="both",expand=True,side="left")


        get_data_button = tk.Button(master=frame_right_window_class_selection,text="Verileri Getir",font=("Calibri",12),relief="flat",border=0,width=10,foreground="white",background="#1664BC",borderwidth=0,command=get_quiz_data)
        get_data_button.pack(fill="both",expand=True,side="left")

        # Building a tree for quiz datas.
        see_quiz_tree = ttk.Treeview(master=frame_right_window)
        see_quiz_tree['columns'] = ('date','lesson','questions','ans_true','ans_falseorempty','score')

        see_quiz_tree.column('#0',width=0,stretch=NO,anchor=CENTER)
        see_quiz_tree.column('date',minwidth=100,width=100,anchor=CENTER)
        see_quiz_tree.column('lesson',minwidth=100,width=100,anchor=CENTER)
        see_quiz_tree.column('questions',minwidth=100,width=100,anchor=CENTER)
        see_quiz_tree.column('ans_true',minwidth=100,width=100,anchor=CENTER)
        see_quiz_tree.column('ans_falseorempty',minwidth=100,width=100,anchor=CENTER)
        see_quiz_tree.column('score',minwidth=100,width=100,anchor=CENTER)


        see_quiz_tree.heading('date',text="Tarih")
        see_quiz_tree.heading('lesson',text="Ders")
        see_quiz_tree.heading('questions',text="Soru Sayısı")
        see_quiz_tree.heading('ans_true',text="Doğru")
        see_quiz_tree.heading('ans_falseorempty',text="Yanlış/Boş")
        see_quiz_tree.heading('score',text="Puan")
        
        see_quiz_tree.pack(fill="both",expand=True,padx=50,pady=5)


        succes_button = tk.Button(master=frame_right_window,text="Önce ders seçin.",font=("Calibri",12),relief="flat",border=0,width=10,foreground="white",background="#1664BC",borderwidth=0)
        succes_button.pack(fill="x",padx=50,pady=2)

        notice_button = tk.Button(master=frame_right_window,text="Bildirim Gönder",font=("Calibri",12),relief="flat",border=0,width=10,foreground="white",background="green",borderwidth=0)
        notice_button.pack(fill="x",padx=50)


    def add_exam():
        
        def save_exam_l9(class_nets,pass_data):
            score = score_ent.get()
            if ogr_class < 4 :
                # id, save_time, student_key, matematik, fen, turkce, sosyal, total_question, answered_question, answered_true, answered_false, total_net, score                q = f"insert into exam_class_two (save_time, student_key, matematik, turkce, fen, sosyal, ingilizce, region, total_question, answered_question, answered_true, answered_false, total_net, score)"  +  f" values (now(),'{ogr_key}','{class_nets[0][2]}','{class_nets[1][2]}','{class_nets[2][2]}','{class_nets[3][2]}','{class_nets[3][2]}','{class_nets[4][2]}','{pass_data[0]}','{pass_data[1]}','{pass_data[2]}','{pass_data[3]}','{pass_data[4]}',{score})"
                q = f"insert into exam_class_one (save_time, student_key, matematik, turkce, fen, sosyal, total_question, answered_question, answered_true, answered_false, total_net, score)"  +  f" values (now(),'{ogr_key}','{class_nets[0][2]}','{class_nets[1][2]}','{class_nets[2][2]}','{class_nets[3][2]}','{pass_data[0]}','{pass_data[1]}','{pass_data[2]}','{pass_data[3]}','{pass_data[4]}',{score})"
                mycursor.execute(q)
                mydb.commit() 
            elif ogr_class < 9 and ogr_class > 3:
                # database fielnames = id, save_time, student_key, matematik, fen, turkce, sosyal, total_question, answered_question, answered_true, answered_false, total_net, score
                q = f"insert into exam_class_two (save_time, student_key, matematik, turkce, fen, sosyal, ingilizce, region, total_question, answered_question, answered_true, answered_false, total_net, score)"  +  f" values (now(),'{ogr_key}','{class_nets[0][2]}','{class_nets[1][2]}','{class_nets[2][2]}','{class_nets[3][2]}','{class_nets[3][2]}','{class_nets[4][2]}','{pass_data[0]}','{pass_data[1]}','{pass_data[2]}','{pass_data[3]}','{pass_data[4]}',{score})"
                mycursor.execute(q)
                mydb.commit() 

        def calculateUNI():
            exam_type_ogr = combo_exam_type.get()
            exam_sequence_ogr = combo_sequence_type.get()
            score = score_ent.get()

            q = f"insert into exam_class_three (save_time, student_key, type, sequence, score) " + f"values (now(),'{ogr_key}','{exam_type_ogr}','{exam_sequence_ogr}', {score})"
            mycursor.execute(q)
            mydb.commit() 

        def calculate_exam():

            pass_data = []
            class_nets = []
            total_quest = 0
            total_net = 0
            total_ans_true = 0
            total_ans_false = 0

            score_pass = score_ent.get()
            for i in range(0,len(classes_exam)):
                
                true_ans = int(table_data[i][1].get())
                false_ans = int(table_data[i][2].get())
                net_quest = true_ans - (false_ans/3)
                
                class_nets.append([true_ans,false_ans,net_quest])

                total_quest = total_quest + int(table_data[i][0].get())
                total_ans_true = total_ans_true + int(table_data[i][1].get())
                total_ans_false = total_ans_false + int(table_data[i][2].get())
                total_net = total_net + net_quest



            pass_data.append(total_quest)
            pass_data.append(total_ans_true + total_ans_false)
            pass_data.append(total_ans_true)
            pass_data.append(total_ans_false)
            pass_data.append(total_net)
            pass_data.append(score_pass)

            #print(class_nets)
            save_exam_l9(class_nets,pass_data)




        clear_frame()
        
        #add_exam_button.configure(background="white",foreground="#1664BC")
        #see_exam_button.configure(background="#1664BC",foreground="white")
        add_quiz_button.configure(background="#1664BC",foreground="white")
        see_quiz_button.configure(background="#1664BC",foreground="white")
        #summary_note_button.configure(background="#1664BC",foreground="white")
        #add_note_button.configure(background="#1664BC",foreground="white")
        payment_button.configure(background="#1664BC",foreground="white")


        frame_right_window = tk.Frame(frame_right_window_base,background="white")
        frame_right_window.pack(fill="both",expand=True)


        klavuz_text = f"\nBu alanda sistemimizde {ogr[1]} adı ile kayıtlı olan öğrenci için deneme sınavı verilerini ekleyebilirsiniz.  \n\n"
        klavuz_text = klavuz_text + f"\nSistemimizde {ogr[1]} adlı öğrenci için toplanan verilerin incelenmesi adına aşağıdaki eylemleri gerçekleştirin." 
        klavuz_text = klavuz_text +"\nDersleri ve sınav sonucunda elde edilen net değerlerini kaydedin."
        
        klavuz_widget_word = tk.Text(master=frame_right_window,highlightthickness=0 ,wrap="word",highlightcolor="blue",relief="flat",font=("Time New Roman",10),height=8)
        klavuz_widget_word.insert(INSERT, klavuz_text)
        klavuz_widget_word.pack(fill="x",padx=50)
        klavuz_widget_word.config(state="disabled")


        frame_add_exam = tk.Frame(master=frame_right_window,highlightthickness=1,highlightbackground="#1664BC",background="white")
        frame_add_exam.pack()

        # Labels for adding quiz


        if ogr_class < 9:
            
            lbl1_add_quiz = tk.Label(master=frame_add_exam, text="DERS",background="white")
            lbl1_add_quiz.grid(row=0,column=0,sticky="we",padx=5)

            lbl2_add_quiz = tk.Label(master=frame_add_exam, text="SORU SAYISI",background="white")
            lbl2_add_quiz.grid(row=0,column=1,sticky="we",padx=5)

            lbl3_add_quiz = tk.Label(master=frame_add_exam, text="DOĞRU CEVAP",background="white")
            lbl3_add_quiz.grid(row=0,column=2,sticky="we",padx=5)

            lbl4_add_quiz = tk.Label(master=frame_add_exam, text="YANLIŞ",background="white")
            lbl4_add_quiz.grid(row=0,column=3,sticky="we",padx=5)

            table_data = []

            for i in range(0,len(classes_exam)):
                tk.Label(master=frame_add_exam, text=f"{classes_dersler[i]}",background="white",foreground="black",font=("Time New Roman",10)).grid(row=i+1,column=0,sticky="we",padx=5)
                row_ent = []
                row_ent.append(tk.Entry(master=frame_add_exam,background="white"))
                row_ent[0].grid(row=i+1,column=1,sticky="we",pady=5,padx=5)
            
                row_ent.append(tk.Entry(master=frame_add_exam,background="white"))
                row_ent[1].grid(row=i+1,column=2,sticky="we",pady=5,padx=5)

                row_ent.append(tk.Entry(master=frame_add_exam,background="white"))
                row_ent[2].grid(row=i+1,column=3,sticky="we",pady=5,padx=5)

                table_data.append(row_ent)
                    
        else : 
            
            sequence_types = ["TYT","Sayılsal Oturumu","Sözel Oturumu", "Eşit Ağırlık", "Yabancı Dil Oturumu"]
            
            lbl1_add_quiz = tk.Label(master=frame_add_exam,width=15, text="Sınav Tipi",background="white")
            lbl1_add_quiz.grid(row=0,column=0,sticky="we",padx=5)

            lbl2_add_quiz = tk.Label(master=frame_add_exam,width=15, text="Oturum Tipi",background="white")
            lbl2_add_quiz.grid(row=0,column=1,sticky="we",padx=5)

            lbl3_add_quiz = tk.Label(master=frame_add_exam,width=15, text="Puan",background="white")
            lbl3_add_quiz.grid(row=0,column=2,sticky="we",padx=5)
                
            combo_exam_type = ttk.Combobox(master=frame_add_exam ,state="readonly", values=["TYT","AYT"])
            combo_exam_type.grid(row=1, column=0, sticky="ew",padx=5)
        
            combo_sequence_type = ttk.Combobox(master=frame_add_exam ,state="readonly", values=sequence_types)
            combo_sequence_type.grid(row=1, column=1, sticky="ew",padx=5)

            score_ent = tk.Entry(master=frame_add_exam,background="white",font=("Time New Roman",12,"bold"),foreground="black")
            score_ent.grid(row=1,column=2,sticky="ew",pady=5,padx=5)

            add_quiz_commit_button = tk.Button(master=frame_add_exam, text="Sınav Ekle",font=("Calibri",12),relief="flat",border=0,width=10,foreground="white",background="#1664BC",borderwidth=0,command=calculateUNI)
            add_quiz_commit_button.grid(row=2,column=0,columnspan=3,sticky="we")
            


        if ogr_class < 9:
            tk.Label(master=frame_add_exam, text="PUAN",background="white",foreground="green",font=("Time New Roman",12,"bold")).grid(row=i+2,column=0,sticky="we",padx=5)
            score_ent = tk.Entry(master=frame_add_exam,background="white")
            score_ent.grid(row=i+2,column=1,columnspan=3,sticky="we",pady=5,padx=5)

            add_quiz_commit_button = tk.Button(master=frame_add_exam, text="Sınav Ekle",font=("Calibri",12),relief="flat",border=0,width=10,foreground="white",background="#1664BC",borderwidth=0,command=calculate_exam)
            add_quiz_commit_button.grid(row=i+3,column=0,columnspan=4,sticky="we")

        else :
            pass

    def see_exam():
        clear_frame()
        
        #see_exam_button.configure(background="white",foreground="#1664BC")
        #add_exam_button.configure(background="#1664BC",foreground="white")
        add_quiz_button.configure(background="#1664BC",foreground="white")
        see_quiz_button.configure(background="#1664BC",foreground="white")
        #summary_note_button.configure(background="#1664BC",foreground="white")
        #add_note_button.configure(background="#1664BC",foreground="white")
        payment_button.configure(background="#1664BC",foreground="white")


        frame_right_window = tk.Frame(frame_right_window_base,background="white")
        frame_right_window.pack(fill="both",expand=True)


    def add_note():
        clear_frame()

        #add_note_button.configure(background="white",foreground="#1664BC")
        #see_exam_button.configure(background="#1664BC",foreground="white")
        #add_exam_button.configure(background="#1664BC",foreground="white")
        add_quiz_button.configure(background="#1664BC",foreground="white")
        see_quiz_button.configure(background="#1664BC",foreground="white")
        #summary_note_button.configure(background="#1664BC",foreground="white")
        payment_button.configure(background="#1664BC",foreground="white")
        
        frame_right_window = tk.Frame(frame_right_window_base,background="white")
        frame_right_window.pack(fill="both",expand=True)    


    def payment_data_page():
        clear_frame()

        def clear_all():
            for item in see_paymets_tree.get_children():
                see_paymets_tree.delete(item)

        def update_payment():

            selected_pay = int(see_paymets_tree.focus())+1
            update_query = f"UPDATE paymet_student SET month{selected_pay} = 'ödendi' WHERE student_key = '{ogr_key}';"
            mycursor.execute(update_query)
            mydb.commit()

            clear_frame()
            payment_data_page()


            
            
        def payment_table():
            nowdate = datetime.now()
            this_month = nowdate.month
            today = nowdate.day
            idcount = 0
            aylar=["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]
            year = nowdate.year
            month_count = 0
            date1 = datetime(year,nowdate.month,today)
            for i in month_array:

                

                if month_array[month_count] < month_array[month_count-1] :
                    year = year+1

                

                date2 = datetime(year, i, ogr_pay_day)
                if  date2 > date1 :
                    see_paymets_tree.insert(parent='',index='end', iid=idcount,values=(aylar[i-1],payment_data[0][2],payment_data[0][4+idcount],f"{(date2-date1).days} Gün var"))
                else :    
                    see_paymets_tree.insert(parent='',index='end', iid=idcount,values=(aylar[i-1],payment_data[0][2],payment_data[0][4+idcount],f"{(date2-date1).days} Gün geçti"))

                idcount = idcount + 1
                pay_diff_days = 0
                month_count = month_count + 1


        # f"Select * from student where '{search_source}' IN (name, surname, personal_id, mother_name, father_name, class, school, email, adres, parent_tel, student_tel, student_key);"
        payment_search_query = f"Select * from paymet_student where '{ogr_key}' in (student_key)"
        mycursor.execute(payment_search_query)
        payment_data = mycursor.fetchall()
        rates = []
        ogr_pay_day = payment_data[0][1]
        for i in range(4,16):
            rates.append(payment_data[0][i])



        ogr_pay_month = payment_data[0][3]
        month_array = []
        for i in range(1,13):
            gonna_pay = ogr_pay_month + i
            if gonna_pay > 12:
                gonna_pay = gonna_pay % 12

            month_array.append(gonna_pay)

        
        
        payment_button.configure(background="white",foreground="#1664BC")
        #see_exam_button.configure(background="#1664BC",foreground="white")
        #add_exam_button.configure(background="#1664BC",foreground="white")
        add_quiz_button.configure(background="#1664BC",foreground="white")
        see_quiz_button.configure(background="#1664BC",foreground="white")
        #summary_note_button.configure(background="#1664BC",foreground="white")
        #add_note_button.configure(background="#1664BC",foreground="white")
        #add_note_button.configure(background="#1664BC",foreground="white")
        
        frame_right_window = tk.Frame(frame_right_window_base,background="white")
        frame_right_window.pack(fill="both",expand=True)

        klavuz_text = "Ödeme görüntüleme ekranına hoşgeldin. :\n\n"
        klavuz_text = klavuz_text + f"Bu bölümde hesap kesim tarihi {ogr_pay_day}/{ogr_pay_month} olan öğrencinin ödemeleri için kalan günleri görüntüleyebilirsiniz. " 
        klavuz_text = klavuz_text +"Toplanan ücret bilgileri sadece programın kurulu olduğu şahsi bilgisayarda depolanır. Nabla bu verileri dışarı aktarmaz."
        
        klavuz_widget_word = tk.Text(master=frame_right_window,highlightthickness=0 ,wrap="word",highlightcolor="blue",relief="flat",font=("Time New Roman",10),height=5,foreground="red")
        klavuz_widget_word.insert(INSERT, klavuz_text)
        klavuz_widget_word.pack(fill="x",padx=50, pady=10)
        klavuz_widget_word.config(state="disabled")

        scroll_tree = tk.Frame(frame_right_window,background="white")
        scroll_tree.pack(fill="both",padx=50,pady=20)

        scroll_tree_inner = tk.Frame(scroll_tree,background="white")
        scroll_tree_inner.pack(fill="both")
        
        
        see_paymets_tree = ttk.Treeview(master=scroll_tree_inner,height=13)
        tree_scrollbary = tk.Scrollbar(master=scroll_tree_inner, orient=VERTICAL, command=see_paymets_tree.yview)
        tree_scrollbarx = tk.Scrollbar(master=scroll_tree, orient=HORIZONTAL, command=see_paymets_tree.xview)
        see_paymets_tree.configure(yscrollcommand=tree_scrollbary.set)
        see_paymets_tree.configure(xscrollcommand=tree_scrollbarx.set)

        see_paymets_tree['columns'] = ('mont','coast','statu','overtime')
        see_paymets_tree.heading('mont', text='AY')
        see_paymets_tree.heading('coast', text='TUTAR')
        see_paymets_tree.heading('statu', text='DURUM')
        see_paymets_tree.heading('overtime', text='AŞIM')

        see_paymets_tree.column('#0',width=0,stretch=NO)
        see_paymets_tree.column('mont',anchor="center")
        see_paymets_tree.column('coast',anchor="center")
        see_paymets_tree.column('statu',anchor="center")
        see_paymets_tree.column('overtime',anchor="center")

        see_paymets_tree.pack(fill="both",side='left',expand=True)
        tree_scrollbary.pack(side="right",fill="y")
        tree_scrollbarx.pack(side="top",fill="x")

        # U+27F3
        payment_table()
        
        
        """
        SELECT student_key, month1 FROM paymet_student WHERE student_key = 'ey53365612351'; 
        UPDATE paymet_student SET month1 = 'ödendi' WHERE student_key = 'ey53365612351';
        
        """


        pay_ogr_button = tk.Button(frame_right_window,text="Ödendi Olarak İşaretle",border=2,font=("Calibri",12,"bold"),relief="flat",highlightthickness=10, activebackground='#1664BC',activeforeground="white",highlightcolor="blue",foreground="white",background="green",command=update_payment).pack(fill="x",side="top",padx=50,pady=5)
        refreshpay = tk.Button(frame_right_window,text="Sayfayı Yenile",border=2,font=("Calibri",12,"bold"),relief="flat",highlightthickness=10,background="#1664BC",foreground="white",highlightcolor="blue",command=save_student).pack(fill="x",side="top",padx=50,pady=5)
        
        
        
        

        

        


    righ_menu_panel = tk.Frame(master=main_window, background="white")
    righ_menu_panel.place(relx=0.1,y=0,relwidth=0.9,relheight=1.0)
    
    righ_menu_panel_titlebar = tk.Frame(master=righ_menu_panel,background="white")
    righ_menu_panel_titlebar.pack(fill="x")

    righ_menu_panel_button = tk.Button(master=righ_menu_panel_titlebar, text="\u2190",font=("Calibri",20,"bold"),border=0,relief="flat",highlightthickness=0, activebackground='white',activeforeground="orange",highlightcolor="blue",foreground="orange",background="white",command=see_student)
    righ_menu_panel_button.pack(side="left",padx=10,pady=5)

    righ_menu_panel_title = Label(master=righ_menu_panel,text="Öğrenci Profili",font=("Calibri",16,"bold"), foreground="#1664BC",background="white")
    righ_menu_panel_title.pack(fill="x")



    frame_base = tk.Frame(righ_menu_panel,background="white")
    frame_base.pack(fill="both",padx=50)


    frame_left = tk.Frame(frame_base,background="white")
    frame_left.pack(fill="both",side="left")

    tk.Frame(master=frame_base,background="#1664BC",width=1).pack(side="left",fill="y")
    
    frame_right = tk.Frame(frame_base,background="white")
    frame_right.pack(fill="both",side="left",expand=True)
    
    tk.Frame(master=frame_right,background="#1664BC").pack(fill="x")

    frame_right_topbar = tk.Frame(frame_right,background="white")
    frame_right_topbar.pack(fill="x")

    tk.Frame(master=frame_base,background="#1664BC",width=1).pack(side="left",fill="y")


    
    label = tk.Label(frame_left,image=image_for_student_profile,background="white").grid(row=0,rowspan=2,column=0,columnspan=2,sticky="ew")

    lbl_ogr_adi = Label(frame_left, text=f"Öğrenci Adı: {ogr_adi}",font=("Times New Roman",12), foreground="black",background="white").grid(row=2,column=0,sticky="w",pady=10,padx=5,columnspan=2)
    lbl_ogr_soyadi = Label(frame_left, text=f"Öğrenci Soyadı: {ogr_soyadi}",font=("Times New Roman",12), foreground="black",background="white").grid(row=3,column=0,sticky="w",pady=10,padx=5,columnspan=2)
    lbl_ogr_tc = Label(frame_left, text=f"T.C. Kimlik No: {ogr_tc}",font=("Times New Roman",12), foreground="black",background="white").grid(row=4,column=0,sticky="w",pady=10,padx=5,columnspan=2)
    lbl_ogr_anne = Label(frame_left, text=f"Anne Adı: {ogr_anne}",font=("Times New Roman",12), foreground="black",background="white").grid(row=5,column=0,sticky="w",pady=10,padx=5,columnspan=2)
    lbl_ogr_baba = Label(frame_left, text=f"Baba Adı: {ogr_baba}",font=("Times New Roman",12), foreground="black",background="white").grid(row=6,column=0,sticky="w",pady=10,padx=5,columnspan=2)
    lbl_ogr_class = Label(frame_left, text=f"Sınıf: {ogr_class}",font=("Times New Roman",12), foreground="black",background="white").grid(row=7,column=0,sticky="w",pady=10,padx=5,columnspan=2)
    lbl_ogr_School = Label(frame_left, text=f"Okulu: {ogr_school}",font=("Times New Roman",12), foreground="black",background="white").grid(row=8,column=0,sticky="w",pady=10,padx=5,columnspan=2)
    lbl_ogr_email = Label(frame_left, text=f"e-mail: {ogr_email}",font=("Times New Roman",12), foreground="black",background="white").grid(row=9,column=0,sticky="w",pady=10,padx=5,columnspan=2)
    lbl_ogr_adress = Label(frame_left, text=f"Adres: {ogr_adres}",font=("Times New Roman",12), foreground="black",background="white").grid(row=10,column=0,sticky="nw",pady=10,padx=5,columnspan=2)
    lbl_ogr_parent_tel = Label(frame_left, text=f"Veli Tel. No: {ogr_parent_tel}",font=("Times New Roman",12), foreground="black",background="white").grid(row=11,column=0,sticky="nw",pady=10,padx=5,columnspan=2)
    lbl_ogr_tel = Label(frame_left, text=f"Öğrenci Tel. No: {ogr_tel}",font=("Times New Roman",12), foreground="black",background="white").grid(row=12,column=0,sticky="nw",pady=10,padx=5,columnspan=2)
    tk.Frame(master=frame_left,background="#1664BC").grid(row=13,column=0,sticky="esw",columnspan=2)



    summary_note_button = tk.Button(master=frame_right_topbar, text="Özet",font=("Calibri",12,"bold"),relief="flat",border=0,width=10,foreground="black",background="white",borderwidth=0,command=profile_summary)
    #summary_note_button.pack(fill="x",side="left")

    add_quiz_button = tk.Button(master=frame_right_topbar, text="Quiz Ekle",font=("Calibri",12,"bold"),relief="flat",border=0,width=10,foreground="white",background="#1664BC",borderwidth=0,command=add_quiz)
    add_quiz_button.pack(fill="x",side="left")

    see_quiz_button = tk.Button(master=frame_right_topbar, text="Quiz Data",font=("Calibri",12,"bold"),relief="flat",border=0,width=10,foreground="white",background="#1664BC",borderwidth=0,command=see_quiz_data)
    see_quiz_button.pack(fill="x",side="left")


    add_exam_button = tk.Button(master=frame_right_topbar, text="Sınav Ekle",font=("Calibri",12,"bold"),relief="flat",border=0,width=10,foreground="white",background="#1664BC",borderwidth=0,command=add_exam)
    #see_exam_button = tk.Button(master=frame_right_topbar, text="Sınav Data",font=("Calibri",12,"bold"),relief="flat",border=0,width=10,foreground="white",background="#1664BC",borderwidth=0,command=see_exam)

    #if ogr_class > 3:
        #add_exam_button.pack(fill="x",side="left")
        #see_exam_button.pack(fill="x",side="left")




    add_note_button = tk.Button(master=frame_right_topbar, text="Not Ekle",font=("Calibri",12,"bold"),relief="flat",border=0,width=10,foreground="white",background="#1664BC",borderwidth=0,command=add_note)
    #add_note_button.pack(fill="x",side="left")

    payment_button = tk.Button(master=frame_right_topbar, text="Ödeme",font=("Calibri",12,"bold"),relief="flat",border=0,width=10,foreground="white",background="#1664BC",borderwidth=0,command=payment_data_page)
    payment_button.pack(fill="x",side="left")




    frame_right_window_base = tk.Frame(frame_right,background="gray")
    frame_right_window_base.pack(fill="both",expand=True)


    profile_summary()


def Panel_Changer(left_menu_panel_cp):

    if old_button.get() != left_menu_panel_cp :
        button_name = f"left_menu_panel_btn_{old_button.get()}.config(background = '#1664BC',foreground='white')"
        exec(button_name)
        if old_button.get() == 6:
            button_name = f"left_menu_panel_btn_{old_button.get()}.config(background = 'purple2',foreground='white')"
            exec(button_name)
        elif old_button.get() == 7:
            button_name = f"left_menu_panel_btn_{old_button.get()}.config(background = 'purple2',foreground='white')"
            exec(button_name)
        elif old_button.get() == 8:
            button_name = f"left_menu_panel_btn_{old_button.get()}.config(background = 'red',foreground='white')"
            exec(button_name)
        elif old_button.get() == 9:
            button_name = f"left_menu_panel_btn_{old_button.get()}.config(background = 'red',foreground='white')"
            exec(button_name)

    if left_menu_panel_cp == 8:
        button_name = f"left_menu_panel_btn_{left_menu_panel_cp}.config(background = 'white',foreground='red')"
        exec(button_name)
    elif left_menu_panel_cp == 9:
        button_name = f"left_menu_panel_btn_{left_menu_panel_cp}.config(background = 'white',foreground='red')"
        exec(button_name)
    elif left_menu_panel_cp == 7:
        button_name = f"left_menu_panel_btn_{left_menu_panel_cp}.config(background = 'white',foreground='purple2')"
        exec(button_name)
    elif left_menu_panel_cp == 6:
        button_name = f"left_menu_panel_btn_{left_menu_panel_cp}.config(background = 'white',foreground='purple2')"
        exec(button_name)
    else :
        button_name = f"left_menu_panel_btn_{left_menu_panel_cp}.config(background = 'white',foreground='#1664BC')"
        exec(button_name)


    if left_menu_panel_cp == 1:
        main_page()
    elif left_menu_panel_cp == 2:
        lesson_page()
    elif left_menu_panel_cp == 3:
        class_page()
    elif left_menu_panel_cp == 4:
        student_page()
    elif left_menu_panel_cp == 5:
        account_page()
    elif left_menu_panel_cp == 6:
        app_page()
    elif left_menu_panel_cp == 7:
        about_page()
    elif left_menu_panel_cp == 8:
        anounce_page()
    elif left_menu_panel_cp == 9:
        help_page()
    old_button.set(left_menu_panel_cp)
    
# login operator
lop = login_win()
if lop == True:
    main_window = tk.Tk()
    # images and resource
    image_for_student_profile = Image.open("images/student.png")
    image_for_student_profile = image_for_student_profile.resize((100,100))
    image_for_student_profile = ImageTk.PhotoImage(image_for_student_profile)

    image_for_special_lesson_pre = Image.open("images/special_class.png")
    #image_for_special_lesson = image_for_special_lesson.resize((100,100))
    image_for_special_lesson = ImageTk.PhotoImage(image_for_special_lesson_pre)

    tik = Image.open('images/tic.png')
    tik = ImageTk.PhotoImage(tik)

    close_btn_image = Image.open('images/close_button.png')
    close_btn_image = close_btn_image.resize((20,20))
    close_btn_image = ImageTk.PhotoImage(close_btn_image)

    teacherid_image = Image.open('images/teacherid.png')
    teacherid_image = ImageTk.PhotoImage(teacherid_image)


    icon = PhotoImage(file="images/a.png")
    main_window.iconphoto(False,icon)

    main_window.title("Student Manager - beta")

    screen_h = main_window.winfo_screenheight()
    screen_w = main_window.winfo_screenwidth()

    app_w = int(screen_w/1.25)
    app_h = int(screen_h/1.25)

    main_window.geometry(f"{app_w}x{app_h}+{int(screen_w*(0.5))-int(app_w*(0.5))}+{int(screen_h*(0.5))-int(app_h*(0.5))}")
    main_window.minsize(width=app_w, height=app_h)



    #PANELS
    old_button=IntVar()
    old_button.set(1)
    left_menu_panel = tk.Frame(master=main_window,background="white")
    left_menu_panel.place(x = 0, y =0, relwidth = 0.1, relheight = 1)

    left_menu_panel_btn_1 = tk.Button(master=left_menu_panel, text="Ana Sayfa", border=0,background="#1664BC",foreground="white", font=("Calibri",12,"bold"),activebackground="red",command= lambda: Panel_Changer(1))
    left_menu_panel_btn_2 = tk.Button(master=left_menu_panel, text="Ders\nYöneticisi", border=0,background="#1664BC",foreground="white", font=("Calibri",12,"bold"),anchor=CENTER,command= lambda: Panel_Changer(2))
    left_menu_panel_btn_3 = tk.Button(master=left_menu_panel, text="Öğretmen\nVerisi", border=0,anchor=CENTER,background="#1664BC",foreground="white", font=("Calibri",12,"bold"),command= lambda: Panel_Changer(3))
    left_menu_panel_btn_4 = tk.Button(master=left_menu_panel, text="Öğrenci\nVerisi", border=0,anchor=CENTER,background="#1664BC",foreground="white", font=("Calibri",12,"bold"),command= lambda: Panel_Changer(4))
    left_menu_panel_btn_5 = tk.Button(master=left_menu_panel, text="Hesap\nBilgisi", border=0,anchor=CENTER,background="#1664BC",foreground="white", font=("Calibri",12,"bold"),command= lambda: Panel_Changer(5))
    left_menu_panel_btn_6 = tk.Button(master=left_menu_panel, text="Uygulama\nBilgisi", border=0,anchor=CENTER,background="purple2",foreground="white", font=("Calibri",12,"bold"),command= lambda: Panel_Changer(6))
    left_menu_panel_btn_7 = tk.Button(master=left_menu_panel, text="Hakkımızda ", border=0,background="purple2",foreground="white", font=("Calibri",12,"bold"),command= lambda: Panel_Changer(7))
    left_menu_panel_btn_8 = tk.Button(master=left_menu_panel, text="Duyurular ", border=0,background="red", font=("Calibri",12,"bold"), foreground="white",command= lambda: Panel_Changer(8))
    left_menu_panel_btn_9 = tk.Button(master=left_menu_panel, text="Yardım", border=0,background="red", font=("Calibri",12,"bold"), foreground="white",command= lambda: Panel_Changer(9))

    left_menu_panel_btn_1.pack(side="top", expand=True, fill="both")
    left_menu_panel_btn_2.pack(side="top", expand=True, fill="both")
    left_menu_panel_btn_3.pack(side="top", expand=True, fill="both")
    left_menu_panel_btn_4.pack(side="top", expand=True, fill="both")
    left_menu_panel_btn_5.pack(side="top", expand=True, fill="both")
    left_menu_panel_btn_6.pack(side="top", expand=True, fill="both")
    left_menu_panel_btn_7.pack(side="top", expand=True, fill="both")
    left_menu_panel_btn_8.pack(side="top", expand=True, fill="both")
    #left_menu_panel_btn_9.pack(side="top", expand=True, fill="both")

    main_page()

    button_name = f"left_menu_panel_btn_{1}.config(foreground = '#1664BC',background='white')"
    exec(button_name)



    main_window.mainloop()
