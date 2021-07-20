# Simple Student Information System (Version 2)
# Raihana A. Hadjisalic

from tkinter import *
import sqlite3
from tkinter import ttk
from tkinter import messagebox

top = Tk()


def SSIS(root):
    root.title("STUDENT INFORMATION SYSTEM")
    root.geometry(f'{1200}x{600}+{80}+{60}')
    root.config(bg='pink')
    root.resizable(False, False)

    conn = sqlite3.connect('StudentsData.db')
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = 1")

    c.execute("""CREATE TABLE IF NOT EXISTS studentdata(
              ID_NUMBER VARCHAR(9) NOT NULL PRIMARY KEY,
              STUD_NAME VARCHAR(100) NOT NULL,
              STUD_GENDER VARCHAR(10) NOT NULL,
              YEAR_LEVEL VARCHAR(10) NOT NULL,
              STUD_COURSE_CODE VARCHAR(20) NOT NULL,
              FOREIGN KEY (STUD_COURSE_CODE)
              REFERENCES  coursedata(COURSE_CODE)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE             
              )""")

    c.execute("""CREATE TABLE IF NOT EXISTS coursedata(
            COURSE_CODE VARCHAR(20) NOT NULL PRIMARY KEY,
            COURSE_NAME VARCHAR(100) NOT NULL
            )""")

    idnum = StringVar()
    name = StringVar()
    year = StringVar()
    gender = StringVar()
    courseid = StringVar()
    srchidnum = StringVar()
    srchcrscode = StringVar()

    sheadlabel = Label(root, text="", bg="pink", fg="black", font=("Blinker", 30, "bold"), anchor="center")
    sheadlabel.place(x=10, y=10, width=1180, height=50)
    studentroot = LabelFrame(root, bg='pink', text="    STUDENT DETAILS   ", font=("Blinker", 19, "bold"))
    courseroot = LabelFrame(root, bg='pink',  text="    COURSE DETAILS   ", font=("Blinker", 19, "bold"))
    displayroot = LabelFrame(root, bg='pink', font=("Blinker", 19, "bold"))
    displayroot.place(x=470, y=80, height=400, width=720)
    slabel = Label(displayroot, bg="black", fg="pink", font=("Blinker", 12, "bold"), anchor="w")
    slabel.place(x=10, y=15, height=30, width=90)
    esrchid = Entry(displayroot, textvariable=srchidnum, font=("Lucida Console", 11))
    esrchcode = Entry(displayroot, textvariable=srchcrscode, font=("Lucida Console", 11))

    studlist = Frame(displayroot, bg="white")
    courselist = Frame(displayroot, bg="white")

    sy = Scrollbar(studlist, orient=VERTICAL)
    sx = Scrollbar(studlist, orient=HORIZONTAL)
    cy = Scrollbar(courselist, orient=VERTICAL)
    studlisttable = ttk.Treeview(studlist, columns=("id_no", "name", "gender", "course", "year"),
                                 xscrollcommand=sx, yscrollcommand=sy)
    courselisttable = ttk.Treeview(courselist, columns=("course_code", "course_name"),
                                   yscrollcommand=cy)

    def student():
        clist = []
        c.execute("SELECT COURSE_CODE from coursedata")
        res = c.fetchall()
        for x in res:
            clist.append(x[0])

        key = StringVar()

        def addStudent():
            studid = idnum.get()
            if studid == "" or name.get() == "" or gender.get() == "" or year.get() == "" or courseid.get() == "":
                messagebox.showerror("Error", "Please fill out all fields!")
                return
            elif len(studid) != 9 or studid[4] != '-' or not studid.replace("-", "").isdigit():
                messagebox.showerror("Error", "Invalid ID Number")
                return
            else:
                if messagebox.askyesno("Add Student", "Do you wish to add the student to database?"):
                    try:
                        c.execute("INSERT INTO studentdata VALUES(?, ?, ?, ?, ?)",
                                  (studid, name.get(), gender.get(), year.get(), courseid.get()))
                        messagebox.showinfo("Success", "Student added to database!")
                        conn.commit()
                        clear()
                        searchStudent()
                    except sqlite3.IntegrityError:
                        if courseid.get() not in clist:
                            messagebox.showerror("Error", "Course ID not in database")
                        else:
                            messagebox.showerror("Error", "Student ID already in database!")

        def searchStudent():
            if srchidnum.get() == "":
                c.execute("SELECT * FROM studentdata")
            elif not srchidnum.get().replace("-", "").isdigit():
                messagebox.showerror("Error", "Search Error!")
                return
            else:
                c.execute("SELECT * FROM studentdata WHERE ID_NUMBER LIKE ?", ('%' + srchidnum.get() + '%',))
            search = c.fetchall()
            studlisttable.delete(*studlisttable.get_children())
            if not search:
                return
            else:
                for x in search:
                    studlisttable.insert('', END, values=(x[0], x[1], x[2], x[4], x[3]))

        def deleteStudent():
            sel = studlisttable.focus()
            cont = studlisttable.item(sel)
            rows = cont['values']
            if rows == "":
                messagebox.showerror("Error", "Select a student first!")
            else:
                if messagebox.askyesno("Delete Student", "Confirm deleting student?"):
                    c.execute("DELETE FROM studentdata WHERE ID_NUMBER=?", (rows[0],))
                    conn.commit()
                    messagebox.showinfo("Success", "Student deleted in database!")
                    clear()
                    searchStudent()
                else:
                    return

        def updateStudent():
            studid = idnum.get()
            if key.get() == "":
                messagebox.showerror("Error", "Select student first")
                return
            elif studid == "" or name.get() == "" or gender.get() == "" or year.get() == "" or courseid.get() == "":
                messagebox.showerror("Error", "Please fill out all fields!")
                return
            elif len(studid) != 9 or studid[4] != '-' or not studid.replace("-", "").isdigit():
                messagebox.showerror("Error", "Invalid ID Number")
                return
            else:
                if messagebox.askyesno("update Student", "Confirm updating student information?"):
                    try:
                        if key.get() != studid:
                            c.execute("UPDATE studentdata SET ID_NUMBER=?, STUD_NAME=?, STUD_GENDER=?, "
                                      "YEAR_LEVEL=?, STUD_COURSE_CODE=? WHERE ID_NUMBER=?",
                                      (studid, name.get(), gender.get(), year.get(), courseid.get(), key.get()))
                        else:
                            c.execute("UPDATE studentdata SET STUD_NAME=?, STUD_GENDER=?, "
                                      "YEAR_LEVEL=?, STUD_COURSE_CODE=? WHERE ID_NUMBER=?",
                                      (name.get(), gender.get(), year.get(), courseid.get(), studid))
                        conn.commit()
                        messagebox.showinfo("Success", "Student information updated!")
                        key.set("")
                        clear()
                        searchStudent()
                    except sqlite3.IntegrityError:
                        if courseid.get() not in clist:
                            messagebox.showerror("Error", "Course ID not in database")
                        else:
                            messagebox.showerror("Error", "Student ID already in database!")

        def clear():
            idnum.set("")
            name.set("")
            year.set("")
            gender.set("")
            courseid.set("")

        def selectStudent(ev):
            sel_row = studlisttable.focus()
            selco = studlisttable.item(sel_row)
            rows = selco['values']
            clear()
            key.set(rows[0])
            idnum.set(rows[0])
            name.set(rows[1])
            gender.set(rows[2])
            courseid.set(rows[3])
            year.set(rows[4])

        sheadlabel.config(text="STUDENT INFORMATION SYSTEM")
        displayroot.config(text="    LIST OF STUDENTS   ")
        studentroot.place(x=10, width=450, y=120, height=360)
        lid = Label(studentroot, text="  ID NUMBER", fg="pink", bg="black", font=("Pier Sans", 11, "bold"),
                    anchor="w")
        lid.place(x=10, y=20, width=135, height=35)
        eid = Entry(studentroot, textvariable=idnum, font=("Lucida Console", 12))
        eid.place(x=145, y=20, width=280, height=35)
        lname = Label(studentroot, text="  NAME", fg="pink", bg="black", font=("Pier Sans", 11, "bold"),
                      anchor="w")
        lname.place(x=10, y=60, width=135, height=35)
        ename = Entry(studentroot, textvariable=name, font=("Lucida Console", 11, "bold"))
        ename.place(x=145, y=60, width=280, height=35)
        lgender = Label(studentroot, text="  GENDER", fg="pink", bg="black", font=("Pier Sans", 11, "bold"),
                        anchor="w")
        lgender.place(x=10, y=100, width=135, height=35)
        egender = ttk.Combobox(studentroot, textvariable=gender, values=["Male", "Female"],
                               font=("Lucida Console", 12, "bold"),)
        egender.place(x=145, y=100, width=280, height=35)
        lyear = Label(studentroot, text="  YEAR LEVEL", fg="pink", bg="black", font=("Pier Sans", 11, "bold"),
                      anchor="w")
        lyear.place(x=10, y=140, width=135, height=35)
        eyear = ttk.Combobox(studentroot, textvariable=year, values=["1st Year", "2nd Year", "3rd Year",
                                                                     "4th Year", "5th Year"],
                             font=("Lucida Console", 12, "bold"))
        eyear.place(x=145, y=140, width=280, height=35)
        lcourse = Label(studentroot, text="  COURSE", fg="pink", bg="black", font=("Pier Sans", 11, "bold"),
                        anchor="w")
        lcourse.place(x=10, y=180, width=135, height=35)
        ecourse = ttk.Combobox(studentroot, textvariable=courseid, values=clist, font=("Lucida Console", 12, "bold"))
        ecourse.place(x=145, y=180, width=280, height=35)
        courseroot.place_forget()
        studbutton.place_forget()
        coursebutton.place(x=425, y=520, width=150, height=50)

        addbut = Button(studentroot, text="ADD", command=addStudent, font=("Blinker", 14, "bold"), bg="black",
                        fg="pink", activebackground="pink", activeforeground="black")
        updbut = Button(studentroot, text="UPDATE", command=updateStudent, font=("Blinker", 14, "bold"), bg="black",
                        fg="pink", activebackground="pink", activeforeground="black")
        delbut = Button(studentroot, text="DELETE", command=deleteStudent, font=("Blinker", 14, "bold"), bg="black",
                        fg="pink", activebackground="pink", activeforeground="black")
        clearbut = Button(studentroot, text="CLEAR", command=clear, font=("Blinker", 14, "bold"), bg="black",
                          fg="pink", activebackground="pink", activeforeground="black")
        addbut.place(x=25, y=270, width=90, height=35)
        updbut.place(x=125, y=270, width=90, height=35)
        delbut.place(x=225, y=270, width=90, height=35)
        clearbut.place(x=325, y=270, width=90, height=35)

        courselist.place_forget()
        studlisttable.pack_forget()
        sx.pack_forget()
        sy.pack_forget()
        studlist.place(x=0, y=65, height=300, width=715)
        slabel.config(text="  Student ID: ")
        esrchcode.place_forget()
        esrchid.place(x=100, y=15, height=30, width=200)
        searchbut = Button(displayroot, text="SEARCH", command=searchStudent, relief=FLAT,
                           font=("Blinker", 11, "bold"), bg="black", fg="pink",
                           activeforeground="black", activebackground="pink")
        searchbut.place(x=305, height=30, y=15, width=80)
        refreshbut = Button(displayroot, text="REFRESH", command=lambda: [srchidnum.set(""), searchStudent()],
                            relief=FLAT, font=("Blinker", 11, "bold"), bg="black", fg="pink",
                            activeforeground="black", activebackground="pink")
        refreshbut.place(x=390, height=30, y=15, width=80)

        sx.pack(side=BOTTOM, fill=X)
        sy.pack(side=RIGHT, fill=Y)
        sx.config(command=studlisttable.xview)
        sy.config(command=studlisttable.yview)
        studlisttable.heading("id_no", text="ID NUMBER")
        studlisttable.heading("name", text="NAME")
        studlisttable.heading("gender", text="GENDER")
        studlisttable.heading("course", text="COURSE")
        studlisttable.heading("year", text="YEAR")
        studlisttable['show'] = 'headings'
        studlisttable.column("id_no", width=100, anchor="center")
        studlisttable.column("name", width=260)
        studlisttable.column("gender", width=80, anchor="center")
        studlisttable.column("course", width=170)
        studlisttable.column("year", width=80, anchor="center")
        studlisttable.pack(fill=BOTH, expand=1)
        studlisttable.bind("<ButtonRelease-1>", selectStudent)

        srchidnum.set("")
        searchStudent()
        clear()

    def course():

        key = StringVar()

        def addCourse():
            if courseid.get() == "" or tcoursename.get(1.0, END) == "":
                messagebox.showerror("Error", "Please fill out all fields")
                return
            else:
                if messagebox.askyesno("Add Course", "Do you wish to add the course to database?"):
                    try:
                        c.execute("INSERT INTO coursedata VALUES (?, ?)",
                                  (courseid.get(), tcoursename.get(1.0, END).replace("\n", "")))
                        messagebox.showinfo("Success", "Course added to database!")
                        conn.commit()
                        clear()
                        searchCourse()
                    except sqlite3.IntegrityError:
                        messagebox.showerror("Error", "Course ID already in database!")

        def updateCourse():
            if key.get() == "":
                messagebox.showerror("Error", "Choose a course first")
                return
            elif courseid.get() == "" or tcoursename.get(1.0, END) == "":
                messagebox.showerror("Error", "Please fill out all fields")
                return
            else:
                if messagebox.askyesno("Update Course", "Update course information?"):
                    try:
                        if key.get() != courseid.get():
                            c.execute("UPDATE coursedata SET COURSE_CODE=?, COURSE_NAME=? WHERE COURSE_CODE=?",
                                      (courseid.get(), tcoursename.get(1.0, END).replace("\n", ""), key.get()))
                        else:
                            c.execute("UPDATE coursedata SET COURSE_NAME=? WHERE COURSE_CODE=?",
                                      (tcoursename.get(1.0, END).replace("\n", ""), courseid.get()))
                        conn.commit()
                        messagebox.showinfo("Success", "Course information updated!")
                        key.set("")
                        clear()
                        searchCourse()

                    except sqlite3.IntegrityError:
                        messagebox.showerror("Error", "Course ID already in database.")
                        return

        def searchCourse():
            if srchcrscode.get() == "":
                c.execute("SELECT * FROM coursedata")
            else:
                c.execute("SELECT * FROM coursedata WHERE COURSE_CODE LIKE ?", ('%' + srchcrscode.get() + '%',))
            courses = c.fetchall()
            courselisttable.delete(*courselisttable.get_children())
            if not courses:
                return
            else:
                for z in courses:
                    courselisttable.insert('', END, values=(z[0], z[1]))

        def deleteCourse():
            selco = courselisttable.focus()
            cont = courselisttable.item(selco)
            rows = cont['values']
            if rows == "":
                messagebox.showerror("Error", "Select a course first!")
                return
            else:
                if messagebox.askyesno("Delete Course", "Confirm delete course?"):
                    c.execute("DELETE FROM coursedata WHERE COURSE_CODE=?", (rows[0],))
                    conn.commit()
                    messagebox.showinfo("Success", "Course deleted in database!")
                    clear()
                    searchCourse()
                else:
                    return

        def clear():
            courseid.set("")
            tcoursename.delete(1.0, END)

        def selectCourse(ev):
            sel_row = courselisttable.focus()
            selco = courselisttable.item(sel_row)
            rows = selco['values']
            clear()
            key.set(rows[0])
            courseid.set(rows[0])
            tcoursename.insert(END, rows[1])

        sheadlabel.config(text="COURSE INFORMATION SYSTEM")
        displayroot.config(text="    LIST OF COURSES   ")
        courseroot.place(x=10, width=450, y=120, height=360)
        lcourseid = Label(courseroot, text=" COURSE ID", fg="pink", bg="black", font=("Pier Sans", 11, "bold"),
                          anchor="w")
        ecourseid = Entry(courseroot, textvariable=courseid, font=("Lucida Console", 12))
        lcoursename = Label(courseroot, text=" COURSE NAME", fg="pink", bg="black", font=("Pier Sans", 11, "bold"),
                            anchor="w")
        tcoursename = Text(courseroot, font=("Lucida Console", 11, ))
        lcourseid.place(x=10, y=20, width=150, height=35)
        ecourseid.place(x=160, y=20, width=270, height=35)
        lcoursename.place(x=10, y=60, width=150, height=35)
        tcoursename.place(x=10, y=95, width=420, height=160)
        coursebutton.place_forget()
        studentroot.place_forget()
        studbutton.place(x=425, y=520, width=150, height=50)

        addbut = Button(courseroot, text="ADD", command=addCourse, font=("Blinker", 14, "bold"), bg="black",
                        fg="pink",
                        activebackground="pink", activeforeground="black")
        updbut = Button(courseroot, text="UPDATE", command=updateCourse, font=("Blinker", 14, "bold"), bg="black",
                        fg="pink", activebackground="pink", activeforeground="black")
        delbut = Button(courseroot, text="DELETE", command=deleteCourse, font=("Blinker", 14, "bold"), bg="black",
                        fg="pink", activebackground="pink", activeforeground="black")
        clearbut = Button(courseroot, text="CLEAR", command=clear, font=("Blinker", 14, "bold"), bg="black",
                          fg="pink", activebackground="pink", activeforeground="black")
        addbut.place(x=25, y=270, width=90, height=35)
        updbut.place(x=125, y=270, width=90, height=35)
        delbut.place(x=225, y=270, width=90, height=35)
        clearbut.place(x=325, y=270, width=90, height=35)

        studlist.place_forget()
        courselisttable.pack_forget()
        cy.pack_forget()
        courselist.place(x=5, y=65, height=300, width=710)
        slabel.config(text="  Course ID: ")
        esrchid.place_forget()
        esrchcode.place(x=100, y=15, height=30, width=200)
        searchbut = Button(displayroot, text="SEARCH", command=searchCourse, relief=FLAT,
                           font=("Blinker", 11, "bold"), bg="black", fg="pink",
                           activeforeground="black", activebackground="pink")
        searchbut.place(x=305, height=30, y=15, width=80)
        refreshbut = Button(displayroot, text="REFRESH", command=lambda: [srchcrscode.set(""), searchCourse()],
                            relief=FLAT, font=("Blinker", 11, "bold"), bg="black", fg="pink",
                            activeforeground="black", activebackground="pink")
        refreshbut.place(x=390, height=30, y=15, width=80)

        cy.pack(side=RIGHT, fill=Y)
        cy.config(command=courselisttable.yview)
        courselisttable.heading("course_code", text="COURSE CODE")
        courselisttable.heading("course_name", text="COURSE NAME")
        courselisttable['show'] = 'headings'
        courselisttable.column("course_code", width=200, anchor="center")
        courselisttable.column("course_name", width=485)
        courselisttable.pack(fill=BOTH, expand=1)
        courselisttable.bind("<ButtonRelease-1>", selectCourse)

        srchcrscode.set("")
        clear()
        searchCourse()

    def toexit():
        if messagebox.askyesno("Exit", "Do you want to exit?"):
            top.destroy()
        else:
            return

    studbutton = Button(command=student, text="STUDENT", fg="pink", bg="black", font=("Blinker", 20, "bold"),
                        activebackground="pink", activeforeground="black")
    coursebutton = Button(command=course, text="COURSE", fg="pink", bg="black", font=("Blinker", 20, "bold"),
                          activebackground="pink", activeforeground="black")
    exitbutton = Button(text="EXIT", command=toexit, fg="pink", bg="black", font=("Blinker", 20, "bold"),
                        activebackground="pink", activeforeground="black")
    exitbutton.place(x=625, width=150, y=520, height=50)
    student()
    
    root.protocol("WM_DELETE_WINDOW", toexit)


ob = SSIS(top)
top.mainloop()
