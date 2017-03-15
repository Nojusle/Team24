'''
pip install xlrd
student number: c1668782
'''
from tkinter import *
from uploads import *
import xlrd
from tkinter import filedialog
from tkinter import ttk
import sqlite3
 

tutor_list = ['tutor1', 'tutor2', 'tutor3', 'tutor4', 'tutor5', 'tutor6', 'tutor7', 'tutor8', 'tutor9', 'tutor10', 'tuto11', 'tutor12']


 
class Upluad_main(Frame):
    db_conn = 0
    theCursor = 0
    curr_student = 0

    def setup_db(self):
        # Open or create database
        self.db_conn = sqlite3.connect('student.db')
        # The cursor traverses the records
        self.theCursor = self.db_conn.cursor()
        # Create the table if it doesn't exist
        try:
            self.db_conn.execute("CREATE TABLE if not exists STUDENTS(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, SCode TEXT NOT NULL, Surname TEXT NOT NULL, Forename1 TEXT NOT NULL, Forename2 TEXT NOT NULL, TUTOR TEXT NOT NULL, Course TEXT NOT NULL, AYear TEXT NOT NULL, UEmail TEXT NOT NULL);")
 
            self.db_conn.commit()
 
        except sqlite3.OperationalError:
            print("ERROR : Table not created")
 

    def stud_add(self):
        self.db_conn.execute("INSERT INTO Students (SCode, Surname, Forename1, Forename2, TUTOR, Course , AYear, UEmail) " +
                                                 "VALUES ('" + self.fn_entry_value.get() + "', '" + self.ln_entry_value.get() +
                                                  "', '" + self.f1_entry_value.get() + "', '" + self.f2_entry_value.get() +
                                                   "', '" + self.tu_entry_value.get() + "', '" + self.co_entry_value.get() + 
                                                   "', '" + self.ay_entry_value.get() + "', '" + self.ue_entry_value.get() +
                                                    "')")
        # Clear the entry boxes
        self.fn_entry.delete(0, "end")
        self.ln_entry.delete(0, "end")
        self.f1_entry.delete(0, "end")
        self.f2_entry.delete(0, "end")
        self.tu_entry.delete(0, "end")
        self.co_entry.delete(0, "end")
        self.ay_entry.delete(0, "end")
        self.ue_entry.delete(0, "end")
 
        # Update list box with student list
        self.update_listbox()



    def delete_database(self):
        self.db_conn.execute("DROP TABLE Students;")
        self.update_listbox()
        self.setup_db()
 

    def stud_upload(self, tutor_list):
        student_dict = {}
        self.file_opt = options = {}
        options['defaultextension'] = '.xls'
        options['filetypes'] = [('all files', '.*'), ('csv files', '.csv'), ('excel files', '.xls')]
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = 'This is a title'

    # get filename
        filename = filedialog.askopenfilename(**self.file_opt)

        if filename:
            student_dict = assign_tutors(filename, tutor_list) 

        if student_dict:
            for i in student_dict:
                row =  [student_dict[i][x] for x in student_dict[i]]

                # Insert students in the db
                self.db_conn.execute("INSERT INTO Students (SCode, Surname, Forename1, Forename2, TUTOR, Course , AYear, UEmail) " +
                                         "VALUES ('" + row[0] + "', '" + row[1] + "', '" + row[2] + "', '" + row[3] + "', '" + row[4] +
                                          "', '" + row[5] + "', '" + row[6] + "', '" + row[7] + "')")
                self.fn_entry.delete(0, "end")
                self.ln_entry.delete(0, "end")
                self.f1_entry.delete(0, "end")
                self.f2_entry.delete(0, "end")
                self.tu_entry.delete(0, "end")
                self.co_entry.delete(0, "end")
                self.ay_entry.delete(0, "end")
                self.ue_entry.delete(0, "end")
                self.update_listbox()


    # Load listbox selected student into entries
    def load_student(self, event=None):
        # Get index selected which is the student id
        lb_widget = event.widget
        try:
            index = str(lb_widget.curselection()[0] + 1)

        except IndexError:
            index = -1
            print("You cant select that ")

        if index != -1:
        # Store the current student index
            self.curr_student = index
            # Retrieve student list from the db
            try:
                result = self.theCursor.execute("SELECT ID, SCode, Surname, Forename1, Forename2, TUTOR, Course , AYear, UEmail FROM Students WHERE ID=" + index)
                # You receive a list of lists that hold the result
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
     
            except sqlite3.OperationalError:
                print("The Table Doesn't Exist")
     
            except:
                print("2 : Couldn't Retrieve Data From Database")
 

    # Update student info
    def stud_save(self, event=None):
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
            except sqlite3.OperationalError:
                print("Database couldn't be Updated")

            # self.fn_entry.delete(0, "end")
            # self.ln_entry.delete(0, "end")
            # self.f1_entry.delete(0, "end")
            # self.f2_entry.delete(0, "end")
            # self.tu_entry.delete(0, "end")
            # self.co_entry.delete(0, "end")
            # self.ay_entry.delete(0, "end")
            # self.ue_entry.delete(0, "end")

        self.db_conn.commit()
        self.update_listbox()


    def clear_student(self, event=None):
        try:
            self.db_conn.execute("UPDATE Students SET SCode='" +
                                 "" + "', Surname='" + "" "', Forename1='" + "" +
                                 "', Forename2='" + "" + "', TUTOR='" + "" + "', Course='" +
                                  "" + "', AYear='" + "" + "', UEmail='" + "" + "' WHERE ID=" +
                                    self.curr_student)
            self.db_conn.commit()
        except sqlite3.OperationalError:
            print("Database couldn't be Updated")

        self.fn_entry.delete(0, "end")
        self.ln_entry.delete(0, "end")
        self.f1_entry.delete(0, "end")
        self.f2_entry.delete(0, "end")
        self.tu_entry.delete(0, "end")
        self.co_entry.delete(0, "end")
        self.ay_entry.delete(0, "end")
        self.ue_entry.delete(0, "end")
        self.update_listbox()


    def update_listbox(self):
        self.list_box.delete(0, END)
        try:
            result = self.theCursor.execute("SELECT ID, SCode, Surname, Forename1, Forename2, TUTOR, Course , AYear, UEmail FROM Students")
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
                self.list_box.insert(stud_id,
                                     stud_code + "        " +
                                     stud_f1 + "        " +
                                     stud_f2 + "        " +
                                     stud_tu + "        " +
                                     stud_co + "        " +
                                     stud_ay + "        "+
                                     stud_ue)
        except sqlite3.OperationalError:
            print("The Table Doesn't Exist")
        except:
            print("1: Couldn't Retrieve Data From Database")


    def display(self):
                # ----- 0 Row -----
        title = Label(root, text="Personal Tutor \n Managment System", font=('MS', 20,'bold'))
        title.grid(row=0, rowspan=2, column=4, pady=10)

        # ----- 6st Row -----
        SCode_label = Label(root, text="Student Code")
        SCode_label.grid(row=6, column=0, padx=10, pady=10, sticky=W)
        # Will hold the changing value stored first name
        self.fn_entry_value = StringVar(root, value="")
        self.fn_entry = ttk.Entry(root,
                                  textvariable=self.fn_entry_value)
        self.fn_entry.grid(row=6, column=1, columnspan=3, sticky=W+E)

        # ----- 7nd Row -----
        Surname_label = Label(root, text="Surname")
        Surname_label.grid(row=7, column=0, padx=10, pady=10, sticky=W)
        # Will hold the changing value stored last name
        self.ln_entry_value = StringVar(root, value="")
        self.ln_entry = ttk.Entry(root,
                                  textvariable=self.ln_entry_value)
        self.ln_entry.grid(row=7, column=1,columnspan=3, sticky=W+E)

        # ----- 8nd Row -----
        Forename1_label = Label(root, text="Forename1")
        Forename1_label.grid(row=8, column=0, padx=10, pady=10, sticky=W)
        # Will hold the changing value stored last name
        self.f1_entry_value = StringVar(root, value="")
        self.f1_entry = ttk.Entry(root,
                                  textvariable=self.f1_entry_value)
        self.f1_entry.grid(row=8, column=1, columnspan=3, sticky=W+E)

        # ----- 9nd Row -----
        forename2_label = Label(root, text="Forename2")
        forename2_label.grid(row=9, column=0, padx=10, pady=10, sticky=W)
        # Will hold the changing value stored last name
        self.f2_entry_value = StringVar(root, value="")
        self.f2_entry = ttk.Entry(root,
                                  textvariable=self.f2_entry_value)
        self.f2_entry.grid(row=9, column=1, columnspan=3, sticky=W+E)

        # ----- 10nd Row -----
        Tutor_label = Label(root, text="Tutor")
        Tutor_label.grid(row=10, column=0, padx=10, pady=10, sticky=W)
        # Will hold the changing value stored last name
        self.tu_entry_value = StringVar(root, value="")
        self.tu_entry = ttk.Entry(root,
                                  textvariable=self.tu_entry_value)
        self.tu_entry.grid(row=10, column=1, columnspan=3, sticky=W+E)

        # ----- 11nd Row -----
        course_label = Label(root, text="Course Code")
        course_label.grid(row=11, column=0, padx=10, pady=10, sticky=W)
        # Will hold the changing value stored last name
        self.co_entry_value = StringVar(root, value="")
        self.co_entry = ttk.Entry(root,
                                  textvariable=self.co_entry_value)
        self.co_entry.grid(row=11, column=1, columnspan=3, sticky=W+E)

        # ----- 12nd Row -----
        academic_year_label = Label(root, text="Academic year")
        academic_year_label.grid(row=12, column=0, padx=10, pady=10, sticky=W)

        # Will hold the changing value stored last name
        self.ay_entry_value = StringVar(root, value="")
        self.ay_entry = ttk.Entry(root,
                                  textvariable=self.ay_entry_value)
        self.ay_entry.grid(row=12, column=1, columnspan=3, sticky=W+E)

         # ----- 13nd Row -----
        uni_email_label = Label(root, text="University Email")
        uni_email_label.grid(row=13, column=0, padx=10, pady=10, sticky=W)
        # Will hold the changing value stored last name
        self.ue_entry_value = StringVar(root, value="")
        self.ue_entry = ttk.Entry(root,
                                  textvariable=self.ue_entry_value)
        self.ue_entry.grid(row=13, column=1, columnspan=3, sticky=W+E)

        # ----- 14rd Row -----
        self.submit_button = ttk.Button(root, text="Add", command=lambda: self.stud_add())
        self.submit_button.grid(row=14, column=0, sticky=E, pady=10,)

        self.upload_button = ttk.Button(root, text="Upload", command=lambda: self.stud_upload(tutor_list))
        self.upload_button.grid(row=14, column=1, sticky=E+W, pady=10,)

        self.update_button = ttk.Button(root, text="Save", command=lambda: self.stud_save())
        self.update_button.grid(row=14, column=2, sticky=E+W, pady=10,)

        self.clear_button = ttk.Button(root, text="Remove", command=lambda: self.clear_student())
        self.clear_button.grid(row=14, column=3, pady=10,sticky=W)

        # -----15nd-----

        self.clear_button = ttk.Button(root, text="Delete Student Database", command=lambda: self.delete_database())
        self.clear_button.grid(row=15, column=0, columnspan=4, pady=5, sticky=E)

        # ----- others ----

        scrollbar = Scrollbar(root)

    def __init__(self, master):

        self.list_box = Listbox(root)
        self.list_box.bind('<<ListboxSelect>>', self.load_student)
        self.list_box.insert(1, "Students Here")
        self.list_box.grid(row=6, rowspan=10, column=4, columnspan=8, ipadx=250, padx=50, pady=10, sticky=E+W+N+S)
 
        root.title("Uplaod students")
        root.geometry("1100x800")

        # Call for database to be created
        self.setup_db()
        Frame.__init__(self, master)
        self.display()
        self.update_listbox()
 


# Get the root window object
root = Tk()
root.title("Personal Tutor Managment System Team 24")
# Create the calculator
app = Upluad_main(root)
# Run the app until exited
root.mainloop()



