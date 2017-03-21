from tkinter import *
from tkinter.ttk import *


class App(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.CreateUI()
        self.LoadTable()
        self.grid(sticky = (N,S,W,E))
        parent.grid_rowconfigure(0, weight = 1)
        parent.grid_columnconfigure(0, weight = 1)

    def CreateUI(self):
        tv = Treeview(self)
        tv['columns'] = ('Student Code', 'Surname', 'Forename1', 'Forname2', 'Tutor', 'Course', 'Year', 'Email')
        tv.heading("#0", text='No.', anchor='w')
        tv.column("#0", anchor="w", width=30)
        for x in tv['columns']:
            tv.heading(x, text=x)
            tv.column(x, anchor='center', width=100)
        tv.grid(sticky = (N,S,W,E))
        self.treeview = tv
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

    def LoadTable(self):
        self.treeview.insert('', 'end', text="1", values=('1626361',
                             'Smith', 'John', 'Max', 'Kirill', 'COMSCI', '19/20', '12312@cardiff.ac.uk'))
        self.treeview.insert('', 'end', text="1", values=('1626361',
                             'Smith', 'John', 'Max', 'Kirill', 'COMSCI', '19/20', '12312@cardiff.ac.uk'))
        self.treeview.insert('', 'end', text="1", values=('1626361',
                             'Smith', 'John', 'Max', 'Kirill', 'COMSCI', '19/20', '12312@cardiff.ac.uk'))
        self.treeview.insert('', 'end', text="1", values=('1626361',
                             'Smith', 'John', 'Max', 'Kirill', 'COMSCI', '19/20', '12312@cardiff.ac.uk'))
        self.treeview.insert('', 'end', text="1", values=('1626361',
                             'Smith', 'John', 'Max', 'Kirill', 'COMSCI', '19/20', '12312@cardiff.ac.uk'))

def main():
    root = Tk()
    App(root)
    root.mainloop()

if __name__ == '__main__':
    main()