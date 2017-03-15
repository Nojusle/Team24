from tkinter import *
from tkinter import ttk
import sqlite3
 
 
class SearchExample(Frame):
    db_conn = 0
    theCursor = 0
    curr_student = 0

    def __init__(self, master):

        self.list_box = Listbox(root)
        self.list_box.insert(1, "Students Here")
        self.list_box.grid(row=2, rowspan=5, column=0, columnspan=5, ipadx=300, padx=50, pady=10, sticky=E+W+N+S)
 
        root.title("Search students")
        root.geometry("1100x800")

        self.db_conn = sqlite3.connect('student.db')
        self.theCursor = self.db_conn.cursor()

        Frame.__init__(self, master)
        self.display()
        self.update_listbox()


    def search(self):
        search_query = self.search_entry_value.get()

        # Delete items in the list box
        self.list_box.delete(0, END)
 
        # Get students from the db
        try:
            result = self.theCursor.execute("SELECT ID, SCode, Surname, Forename1, Forename2, TUTOR, Course , AYear, UEmail FROM Students WHERE ID = "+ str(search_query) )
 
            # You receive a list of lists that hold the result
            for row in result:
 
                stud_id = row[0]
                stud_fname = row[1]
                stud_lname = row[2]
                stud_f1 = row[3]
                stud_f2 = row[4]
                stud_tu = row[5]
                stud_co = row[6]
                stud_ay = row[7]
                stud_ue = row[8]
 
                self.list_box.insert(stud_id,
                                     stud_fname + "        " +
                                     stud_lname + "        " +
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



    def update_listbox(self):
        self.list_box.delete(0, END)
        try:
            result = self.theCursor.execute("SELECT ID, SCode, Surname, Forename1, Forename2, TUTOR, Course , AYear, UEmail FROM Students")
            for row in result:
                stud_id = row[0]
                stud_fname = row[1]
                stud_lname = row[2]
                stud_f1 = row[3]
                stud_f2 = row[4]
                stud_tu = row[5]
                stud_co = row[6]
                stud_ay = row[7]
                stud_ue = row[8]
                self.list_box.insert(stud_id,
                                     stud_fname + "        " +
                                     stud_lname + "        " +
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
        title = Label(root, text="Personal Tutor Managment System", font=('MS', 20,'bold'))
        title.grid(row=0, column=2, pady=10)

        # ----- 1st Row -----

        ID_lable = Label(root, text="Enter ID:", font=('MS', 10,'bold'))
        ID_lable.grid(row=1, column=0, sticky=E)

        self.search_entry_value = StringVar(root, value="")
        self.search_entry = ttk.Entry(root, textvariable=self.search_entry_value)
        self.search_entry.grid(row=1, column=1, columnspan=2, padx=50, sticky=W+E)

        self.submit_button = ttk.Button(root, text="Search", command=lambda: self.search())
        self.submit_button.grid(row=1, column=3, sticky=W+E)

        self.submit_button = ttk.Button(root, text="See all", command=lambda: self.update_listbox())
        self.submit_button.grid(row=1, column=4, sticky=W)

        # ----- display -----

        scrollbar = Scrollbar(root)

 



root = Tk()
root.title("Personal Tutor Managment System Team 24")
app = SearchExample(root)
root.mainloop()



