'''
pip install xlrd
TEAM 24
'''
from tkinter import *
from uploads import *
from tkinter import messagebox as tkMessageBox
import xlrd
import smtplib 
from tkinter import filedialog
from tkinter import ttk
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3
 
 

class Upluad_main(Frame):
    db_conn = 0
    theCursor = 0
    curr_student = 0
    tutor_list = []
    last_search = False
    last_tutor = False
    tutor_selected = False
    temp_var = ""
    temp_var2 = ""
    query_list = []

    # ------------------------------------ Database ------------------------------------
#creates a databese if not created
    def setup_db(self):
        # Open or create database
        self.db_conn = sqlite3.connect('systems.db')
        # The cursor traverses the records
        self.theCursor = self.db_conn.cursor()
        # Create the table if it doesn't exist
        try:
            self.db_conn.execute("CREATE TABLE if not exists STUDENTS" +
                                    "(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"+
                                    " SCode TEXT NOT NULL, Surname TEXT NOT NULL,"+
                                    " Forename1 TEXT NOT NULL, Forename2 TEXT NOT NULL,"+
                                    " TUTOR TEXT NOT NULL, Course TEXT NOT NULL,"+
                                    " AYear TEXT NOT NULL, UEmail TEXT NOT NULL);")
 
            self.db_conn.commit()
 
        except sqlite3.OperationalError:
            print("ERROR : Table not created")


        try:
            self.db_conn.execute("CREATE TABLE if not exists TUTORS" +
                                    "(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"+
                                    " TUTOR TEXT NOT NULL);")
 
            self.db_conn.commit()
 
        except sqlite3.OperationalError:
            print("ERROR : Table not created")

#deletes students database
    def delete_database(self):
        self.db_conn.execute("DROP TABLE Students;")
        self.setup_db()
        self.update_listbox()
        self.update_tutor_listbox()

#deletes tutors database
    def delete_database_tutors(self):
        self.db_conn.execute("DROP TABLE TUTORS;")
        self.setup_db()
        self.update_listbox()
        self.update_tutor_listbox()
      
    def getemails(self, tutorname): 
        self.theCursor.execute("SELECT UEmail FROM Students WHERE TUTOR = '{}'".format(tutorname[0]))
        
        return self.theCursor.fetchall()

    def send_tutor_email(self):
        self.theCursor.execute("SELECT TUTOR FROM Students") 
        tutor_list = self.theCursor.fetchall()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        for i in tutor_list:
            
            server.login('dqscoursework@gmail.com', 'team24coursework')
            
            me = "dqscoursework@gmail.com"
            emails = self.getemails(i)

            # Create the container (outer) email message.
            msg = MIMEMultipart()
            msg = MIMEText("""Dear Student: Your tutor for the year is {}""".format(i[0]))
            msg['Subject'] = 'Testing the Email - Python'
            # me == the sender's email address
            # emails = the list of all recipients' email addresses
            msg['From'] = me
            msg['To'] = '\n'.join(''.join(elems) for elems in emails)
            msg.preamble = 'Your Tutor'

            

            server.sendmail(me, emails, msg.as_string()) 

        server.quit()  

    # ------------------------------------ Search ------------------------------------
#gets value from user and with it calls show_studets function
    def search_student(self, *args):
        search_query = self.search_entry_value.get()
        self.delete_entry_boxes()

        self.temp_var = search_query

        if self.tutor_selected:
            self.show_tutors_student(search_query, self.temp_var2)
        else:
            self.show_student(search_query)

# Go to database and fetches results who correspond with query
    def show_student(self, search_query):
        # Delete items in the list box
        try:
            result = self.theCursor.execute(
                "SELECT * FROM Students WHERE Surname LIKE '%" + search_query + 
                                            "%' OR SCode LIKE '" + search_query + 
                                            "' OR Forename1 LIKE '%" + search_query +
                                             "%' OR Forename2 LIKE '%" + search_query + 
                                            "%' OR TUTOR LIKE '" + search_query + 
                                            "' OR Course LIKE '%" + search_query + 
                                            "%' OR UEmail LIKE '%" + search_query + "%'"
                                                                        )
            self.last_search = True
            self.last_tutor = False
            self.list_box_update(result)

        except sqlite3.OperationalError:
            print("The Table Doesn't Exist")
        except:
            print("1: Couldn't Retrieve Data From Database")

#============================== Searching the personal tutor list for individual students =======================================

#goes to database and searches for particular tutors student   
    def show_tutors_student(self, search_query, temp_var2):

        try:
            result = self.theCursor.execute(
                "SELECT * FROM Students WHERE TUTOR LIKE '" + self.tutor_list[int(temp_var2)] + "' AND Surname LIKE '%" + search_query + 
                                            "%' OR TUTOR LIKE '" + self.tutor_list[int(temp_var2)] + "' AND SCode LIKE '%" + search_query + 
                                            "%' OR TUTOR LIKE '" + self.tutor_list[int(temp_var2)] + "' AND Forename1 LIKE '%" + search_query +
                                             "%' OR TUTOR LIKE '" + self.tutor_list[int(temp_var2)] + "' AND Forename2 LIKE '%" + search_query + 
                                            "%' OR TUTOR LIKE '" + self.tutor_list[int(temp_var2)] + "' AND Course LIKE '%" + search_query + 
                                            "%' OR TUTOR LIKE '" + self.tutor_list[int(temp_var2)] + "' AND UEmail LIKE '%" + search_query + "%'"
                                                                        )
                                        
            self.list_box_update(result)
            self.last_search = True # it means that to update list_box last time was used search
            self.last_tutor = False # to update list_box last time was used selection of particular tutor

        except sqlite3.OperationalError:
            print("The Table Doesn't Exist nepaejo")
        except:
            print("1: Couldn't Retrieve Data From Database")

# ==================================================================================================================================
    # ------------------------------------ Edits ------------------------------------
 
#====== Teams of five or more: Delete a student from the tutor list and re-assign a single student to an alternative tutor ==============

#adds student to database
    def stud_add(self):
        self.db_conn.execute(
            "INSERT INTO Students"+
            " (SCode, Surname, Forename1, Forename2, TUTOR, Course , AYear, UEmail) " +
             "VALUES ('" + self.fn_entry_value.get() + "', '" + self.ln_entry_value.get() +
              "', '" + self.f1_entry_value.get() + "', '" + self.f2_entry_value.get() +
               "', '" + self.tu_entry_value.get() + "', '" + self.co_entry_value.get() + 
               "', '" + self.ay_entry_value.get() + "', '" + self.ue_entry_value.get() +
             "')")

        self.delete_entry_boxes()
        self.update_listbox()
        self.update_tutor_listbox()
#==========================================================================================================================================
#                                                   Nojus Lenciauskas
# ====================== Upload an excel / csv file of new students and assign new students to personal tutees ============================

 #uploads file and adds it to database
    def stud_upload(self, tutor_list):
        student_dict = {}
        self.file_opt = options = {}
        options['defaultextension'] = '.xls'
        options['filetypes'] = [('all files', '.*'), ('excel files', '.xls')]
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = 'This is a title'

    # get filename
        filename = filedialog.askopenfilename(**self.file_opt)

        self.query_tutors_database()
        if filename:
            student_dict = excel_to_dict2(filename) 

        self.add_students_to_database(student_dict)

#assigns students to tutors
    def assign_students(self):
        self.query_tutors_database()
        student_dict = self.qurey_students_database()

        assigned_student_dict = assign_tutors2(student_dict, self.tutor_list)
        if assigned_student_dict:
            self.delete_database()
            self.add_students_to_database(assigned_student_dict)
            self.db_conn.commit()


#adds assign students to database
    def add_students_to_database(self, student_dict):
        
        if student_dict:
            for i in student_dict:
                row = [x[1] for x in i[1]]


                # Insert students in the db
                self.db_conn.execute(
                    "INSERT INTO Students "+
                    "(SCode, Surname, Forename1, Forename2, TUTOR, Course , AYear, UEmail) " +
                    "VALUES ('" +row[0] + "', '" + row[1] + "', '" +row[2] + "', '" + row[3] + 
                    "', '" + row[4] + "', '" + row[5] + "', '" +  row[6] + "', '" + row[7] + 
                     "')")
            self.delete_entry_boxes()
            self.update_listbox()
            self.update_tutor_listbox()


# ================================================================================================================================================

#uploads tutor file to database
    def tutors_upload(self):
        self.file_opt = options = {}
        options['defaultextension'] = '.xls'
        options['filetypes'] = [('all files', '.*'), ('excel files', '.xls')]
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = 'This is a title'

    # get filename
        filename = filedialog.askopenfilename(**self.file_opt)

        if filename:
            tutors_list = excel_to_list(filename) 
#tutor file is converted to simple list
        if tutors_list:
            for i in tutors_list:

                # Insert tutors in the db
                self.db_conn.execute(
                    "INSERT INTO TUTORS (TUTOR) VALUES ('" + i + "')")
            self.db_conn.commit()
            self.delete_entry_boxes()
            self.update_listbox()
            self.update_tutor_listbox()

# gets all tutors and assigns it as public variable
    def query_tutors_database(self):
        try:
            result = self.theCursor.execute("SELECT * FROM TUTORS")
            tutors_list = [i[1] for i in result]
            self.tutor_list = tutors_list
        except:
            print('Tutor list not retrieved')

# goes to database, fetches all info, converts it to combination of list ant tuples
    def qurey_students_database(self):
        converted = []
        result = self.theCursor.execute("SELECT * FROM STUDENTS")
        for number, row in enumerate(result):
            if row[1]:
                row_list = []
                for index, item in enumerate(row):
                    if index != 0:
                        row_list.append([index-1, item])
                converted.append((number+1, row_list))
        return converted

# Bad function, goes to databese, converts all info to list/tuples without empty elements, 
# daletes database, creates new database, uploads all students to database
    def refresh_stuent_list(self):
        student_dict = self.qurey_students_database()
        if student_dict:
            self.delete_database()
            self.add_students_to_database(student_dict)
            self.db_conn.commit()

# allows to update existing student information
    def stud_update(self, event=None):
        # Update student records with change made in entry
        if self.curr_student:

            try:
                self.db_conn.execute("UPDATE Students SET SCode='" + self.fn_entry_value.get() +
                                                 "', Surname='" + self.ln_entry_value.get() +
                                                  "', Forename1='" + self.f1_entry_value.get() +
                                                   "', Forename2='" + self.f2_entry_value.get() +
                                                    "', TUTOR='" + self.tu_entry_value.get() +
                                                     "', Course='" + self.co_entry_value.get() +
                                                      "', AYear='" + self.ay_entry_value.get() +
                                                       "', UEmail='" + self.ue_entry_value.get() +
                                                        "' WHERE ID=" +  self.curr_student)
                self.db_conn.commit()
                self.update_tutor_listbox()
                self.load_last_query(self.temp_var)


            except sqlite3.OperationalError:
                print("Database couldn't be Updated")


# ============================ Teams of five or more: Delete a student from the tutor list and re-assign a single student to an alternative tutor =====================

# cleans all fields for student, it is kind of student deletion, because students details are no longer shown
# in combination with //refresh_stuent_list()// function, completes job
    def clear_student(self, event=None):
        try:
            self.db_conn.execute("UPDATE Students SET SCode='" +
                                 "" + "', Surname='" + "" "', Forename1='" + "" +
                                 "', Forename2='" + "" + "', TUTOR='" + "" + "', Course='" +
                                  "" + "', AYear='" + "" + "', UEmail='" + "" + "' WHERE ID=" +
                                    self.curr_student)
        except sqlite3.OperationalError:
            print("Database couldn't be Updated")

        self.delete_entry_boxes()
        self.update_tutor_listbox()

        self.load_last_query(self.temp_var)


# ================================================================================================================================================


# ------------------------------------------------ Controls ----------------------------------------------------------

# deletes input boxes
    def delete_entry_boxes(self):
        self.search_entry.delete(0, "end")
        self.fn_entry.delete(0, "end")
        self.ln_entry.delete(0, "end")
        self.f1_entry.delete(0, "end")
        self.f2_entry.delete(0, "end")
        self.tu_entry.delete(0, "end")
        self.co_entry.delete(0, "end")
        self.ay_entry.delete(0, "end")
        self.ue_entry.delete(0, "end")

# updates list box with new info from students
    def list_box_update(self, result):
        self.list_box.delete(0, END)
        dictionary = {}
        small_d = {}
        query_list = []
        for row in result:
            stud_id = row[0]
            stud_id_copy = str(stud_id)
            stud_code = row[1]
            stud_surn = row[2]
            stud_f1 = row[3]
            stud_f2 = row[4]
            stud_tu = row[5]
            stud_co = row[6]
            stud_ay = row[7]
            stud_ue = row[8]

            self.list_box.insert(stud_id," %-3s| %-15s %-20s %-20s %-20s %-20s %-20s %-20s %-20s " % (stud_id_copy, stud_code, stud_surn, stud_f1, stud_f2, stud_tu, stud_co, stud_ay, stud_ue))
            if self.last_tutor or self.last_search:
                query_list.append(stud_id)
        self.query_list = query_list

# when student is selected, outputs it info to entry box, where user can edit it
    def entry_box_update(self, result):
        for row in result:
            stud_id = row[0]
            stud_code = row[1]
            stud_surn = row[2]
            stud_f1 = row[3]
            stud_f2 = row[4]
            stud_tu = row[5]
            stud_co = row[6]
            stud_ay = row[7]
            stud_ue = row[8]
            # Set values in the entries
            self.fn_entry_value.set(stud_code)
            self.ln_entry_value.set(stud_surn)
            self.f1_entry_value.set(stud_f1)
            self.f2_entry_value.set(stud_f2)
            self.tu_entry_value.set(stud_tu)
            self.co_entry_value.set(stud_co)
            self.ay_entry_value.set(stud_ay)
            self.ue_entry_value.set(stud_ue)


# Load listbox selected student into entries
    def load_student(self, event=None):
# Get index selected first element= 1, eight= 8
        lb_widget = event.widget
        try:
            index = str(lb_widget.curselection()[0] + 1)

        except IndexError:
            index = -1
            print("You cant select that ")

        if index != -1:
#changes index to the id of student from returned list
            if self.last_tutor or self.last_search:
                index = str(self.query_list[int(index)-1])

        # Store the current student index
            self.curr_student = index
            # Retrieve student info from the db
            try:
                result = self.theCursor.execute("SELECT * FROM Students WHERE ID=" + index)
        # load results to entry boxes to edit it
                self.entry_box_update(result)
     
            except sqlite3.OperationalError:
                print("The Table Doesn't Exist")
     
            except:
                print("2 : Couldn't Retrieve Data From Database")


# ==================Display information on the quota of tutees each staff member has been assigned per year or degree group ==================

# goes to database, counts all students assign to each tutor and outputs it to tutor list box
    def update_tutor_listbox(self):
        self.query_tutors_database() 
        self.list_box2.delete(0, END)

        # dictionaty = {}
# goes throw list of tutors and gets student number assgint to each of them, then combines it to sting and outputs to tutors list box
        for i, item in enumerate(self.tutor_list):
            try:
                result = self.theCursor.execute("SELECT count(*) FROM Students WHERE TUTOR LIKE '" + item + "';" )
                for j, row in enumerate(result):
                    quota = row[0]


                    string = (item + '   strudents quota:  ' + str(quota))
                # dictionaty[i] = [item, quota]
                self.list_box2.insert(END, string)


            except sqlite3.OperationalError:
                print("The Table Doesn't Exist")
     
            except:
                print("2 : Couldn't Retrieve Data From Database")


# =============================================================================================================================================

# =========================================== Displaying lists of tutees for a particular personal tutor =====================================

# when pressed loads pressed tutor students.
    def load_tutors_students(self, event=None):
        lb_widget = event.widget
        try:
# gets tutor chosen from the list
            index2 = str(lb_widget.curselection()[0])

        except IndexError:
            index2 = -1
            print("You cant select that ")
        if index2 != -1:
        # Store the current student index
            self.temp_var = index2
            self.temp_var2 = index2
            self.delete_entry_boxes()
            self.show_tutor_students(index2)

# goes to database and searches for all students of particular tutor
    def show_tutor_students(self, index2):

        try:
            result = self.theCursor.execute("SELECT * FROM Students WHERE TUTOR LIKE '" + self.tutor_list[int(index2)] + "';")
            # You receive a list of lists that hold the result
            self.last_search = False
            self.last_tutor = True
            self.tutor_selected = True
            self.list_box_update(result)

        except sqlite3.OperationalError:

            print("The Table Doesn't Exist")
        except:

            print("1: Couldn't Retrieve Data From Database")



# =============================================================================================================================================


# loads ALL student to list box
    def update_listbox(self):
        try:
            result = self.theCursor.execute("SELECT * FROM Students")

            self.last_search = False
            self.last_tutor = False
            self.tutor_selected = False
            self.temp_var = ""
            self.temp_var2 = ""
            self.delete_entry_boxes()
            self.list_box_update(result)

        except sqlite3.OperationalError:
            print("The Table Doesn't Exist")
        except:
            print("1: Couldn't Retrieve Data From Database")

#loads that same info to the screen as was choise before by the user
#e.g if user wants to edit particulat tutor student it keeps that tutor students on the schreen and refreses when updated
    def load_last_query(self, temp_var):
        if self.last_search:
            self.show_student(self.temp_var)
        elif self.last_tutor:
            self.show_tutor_students(self.temp_var)
        else:
            self.update_listbox()


    def display(self):

        # ----- 0 Row -----

        title = Label(root, text="Personal Tutor Management System", font=('MS', 20,'bold'))
        title.grid(row=0, rowspan=1, column=5, sticky=S)

        # ----- 3rd Row -----

        self.upload_button = ttk.Button(root, text="Upload Students", command=lambda: self.stud_upload(self.tutor_list))
        self.upload_button.grid(row=3, column=0, columnspan=2, sticky=E+W, pady=(20,0), padx=(10, 0))

        self.upload_tutors_button = ttk.Button(root, text="Upload Tutors", command=lambda: self.tutors_upload())
        self.upload_tutors_button.grid(row=3, column=2, columnspan=2, sticky=E+W, pady=(20,0), padx=(10, 0))

        self.upload_button = ttk.Button(root, text="Assign", command=lambda: self.assign_students())
        self.upload_button.grid(row=3, column=4, columnspan=1, sticky=E+W, pady=(20, 0), padx=(10, 0)) 

        self.search_entry_value = StringVar(root, value="")
        self.search_entry = ttk.Entry(root, textvariable=self.search_entry_value)
        self.search_entry.grid(row=3, column=5, columnspan=3, padx=(50, 0), pady=(20, 0), sticky=W+E)

        self.seach_button = ttk.Button(root, text="Search", command=lambda: self.search_student())
        self.seach_button.grid(row=3, column=8, pady=(20, 0), sticky=W)
        
         # ----- 6th Row ----- 

        SCode_label = Label(root, text="Student Code")
        SCode_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=W)
        # Will hold the changing value stored first name
        self.fn_entry_value = StringVar(root, value="")
        self.fn_entry = ttk.Entry(root, textvariable=self.fn_entry_value)
        self.fn_entry.grid(row=6, column=2, columnspan=3, sticky=W+E)

        # ----- 7th Row -----

        Surname_label = Label(root, text="Surname")
        Surname_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky=W)
        # Will hold the changing value stored last name
        self.ln_entry_value = StringVar(root, value="")
        self.ln_entry = ttk.Entry(root,
                                  textvariable=self.ln_entry_value)
        self.ln_entry.grid(row=7, column=2,columnspan=3, sticky=W+E)

        # ----- 8th Row -----

        Forename1_label = Label(root, text="Forename1")
        Forename1_label.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky=W)
        # Will hold the changing value stored last name
        self.f1_entry_value = StringVar(root, value="")
        self.f1_entry = ttk.Entry(root,
                                  textvariable=self.f1_entry_value)
        self.f1_entry.grid(row=8, column=2, columnspan=3, sticky=W+E)

        # ----- 9th Row -----

        forename2_label = Label(root, text="Forename2")
        forename2_label.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky=W)
        # Will hold the changing value stored last name
        self.f2_entry_value = StringVar(root, value="")
        self.f2_entry = ttk.Entry(root,
                                  textvariable=self.f2_entry_value)
        self.f2_entry.grid(row=9, column=2, columnspan=3, sticky=W+E)

        # ----- 10th Row -----

        Tutor_label = Label(root, text="Tutor")
        Tutor_label.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky=W)
        # Will hold the changing value stored last name
        self.tu_entry_value = StringVar(root, value="")
        self.tu_entry = ttk.Entry(root,
                                  textvariable=self.tu_entry_value)
        self.tu_entry.grid(row=10, column=2, columnspan=3, sticky=W+E)

        # ----- 11th Row -----

        course_label = Label(root, text="Course Code")
        course_label.grid(row=11, column=0, columnspan=2, padx=10, pady=10, sticky=W)
        # Will hold the changing value stored last name
        self.co_entry_value = StringVar(root, value="")
        self.co_entry = ttk.Entry(root,
                                  textvariable=self.co_entry_value)
        self.co_entry.grid(row=11, column=2, columnspan=3, sticky=W+E)

        # ----- 12th Row -----

        academic_year_label = Label(root, text="Academic year")
        academic_year_label.grid(row=12, column=0, columnspan=2, padx=10, pady=10, sticky=W)

        # Will hold the changing value stored last name
        self.ay_entry_value = StringVar(root, value="")
        self.ay_entry = ttk.Entry(root, textvariable=self.ay_entry_value)
        self.ay_entry.grid(row=12, column=2, columnspan=3, sticky=W+E)

         # ----- 13th Row -----

        uni_email_label = Label(root, text="University Email")
        uni_email_label.grid(row=13, column=0, columnspan=2, padx=10, pady=10, sticky=W)
        # Will hold the changing value stored last name
        self.ue_entry_value = StringVar(root, value="")
        self.ue_entry = ttk.Entry(root,
                                  textvariable=self.ue_entry_value)
        self.ue_entry.grid(row=13, column=2, columnspan=3, sticky=W+E)

        # ----- 14th Row -----

        self.submit_button = ttk.Button(root, text="Add", command=lambda: self.stud_add())
        self.submit_button.grid(row=14, column=2, sticky=E, pady=10)

        self.update_button = ttk.Button(root, text="Update", command=lambda: self.stud_update())
        self.update_button.grid(row=14, column=3, sticky=E+W, pady=10)

        self.clear_button = ttk.Button(root, text="Remove", command=lambda: self.clear_student())
        self.clear_button.grid(row=14, column=4, pady=10,sticky=W)

        #-------- 18th row -------------

        self.clear_button = ttk.Button(root, text="Notify Students", command=lambda: self.send_tutor_email()) 
        self.clear_button.grid(row=18, column=2, columnspan=2, sticky=W+E)

        #-------- 20th row -------------

        self.clear_button = ttk.Button(root, text="Delete Student Database", command=lambda: self.delete_database() if tkMessageBox.askquestion("Confirmation", "Are You Sure?", icon='warning') == "yes" else tkMessageBox.showinfo("Deleting Student Database", "Nothing was Deleted")) 
        self.clear_button.grid(row=20, column=2, columnspan=2, sticky=W+E)

        #-------- 21st row -------------

        self.clear2_button = ttk.Button(root, text="Delete Tutor Database", command=lambda: self.delete_database_tutors() if tkMessageBox.askquestion("Confirmation", "Are You Sure?", icon='warning') == "yes" else tkMessageBox.showinfo("Deleting Tutor Database", "Nothing was Deleted"))
        self.clear2_button.grid(row=21, column=2, columnspan=2, sticky=W+E)

        #-------- 22nd row -------------

        self.save_button = ttk.Button(root, text="Save", command=lambda: self.db_conn.commit())
        self.save_button.grid(row=22, column=10, sticky=W)        


    def __init__(self, master):

        self.list_box = Listbox(root)
        self.list_box.bind('<<ListboxSelect>>', self.load_student)
        self.list_box.insert(END, "Students Here")
        self.list_box.grid(row=6, rowspan=10, column=5, columnspan=8, ipadx=250, padx=50, pady=10, sticky=E+W+N+S)

        self.refresh_all = ttk.Button(root, text="Show All", command=lambda: self.update_listbox())
        self.refresh_all.grid(row=3, column=9, pady=(20, 0), sticky=E)

        self.refresh_all = ttk.Button(root, text="Refresh", command=lambda: self.refresh_stuent_list())
        self.refresh_all.grid(row=3, column=10, pady=(20, 0), sticky=W)

        

        scrollbar = Scrollbar(root)

        # bind .listbox { set item [%W get [%W nearest %y]] }
        self.list_box2 = Listbox(root)
        self.list_box2.bind('<<ListboxSelect>>', self.load_tutors_students)
        self.list_box2.insert(END)
        self.list_box2.grid(row=16, rowspan=6, column=5, columnspan=8, ipadx=250, padx=50, pady=10, sticky=E+W+N+S)


        root.title("Upload students")
        root.geometry("1120x720")

        # Call for database to be created
        self.setup_db()
        Frame.__init__(self, master)
        self.display()
        self.update_listbox()
        self.update_tutor_listbox()
 



root = Tk()
root.title("Personal Tutor Management System Team 24")
app = Upluad_main(root)
root.mainloop()