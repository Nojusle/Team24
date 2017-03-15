'''
pip install xlrd
student number: c1668782
'''
import xlrd



# returns dictionary where row number is key of dictionary containing row elements
# row elements dictionary where column number is key and value is value
def excel_to_dict(file):
    file_dict = {}
    file = xlrd.open_workbook(file)
    xl_sheet = file.sheet_by_index(0)
    num_cols = xl_sheet.ncols   # Number of columns
    for i in range(1, xl_sheet.nrows):    # Iterate through rows
        row_dict = {}
        for col_idx in range(0, num_cols):  # Iterate through columns
            cell_obj = xl_sheet.cell(i, col_idx)  # Get cell object by row, col\
            row_dict[col_idx] = cell_obj.value
        file_dict[i] = row_dict
    return file_dict

# def csv_to_dict(file):


def assign_tutors(students_file, tutor_list):
    info = excel_to_dict(students_file)
    counter = 0
    counter2 = 0
    tutors_number = len(tutor_list)
    student_number = len(info) - 1
    students_in_group = student_number/tutors_number

    for i in info:
        if i > 0:
            counter +=1
            info[i][4] = tutor_list[counter2]
            if counter > students_in_group:
                counter = 0
                counter2 +=1
    return info
    


def print_to_console(file_name):
    tutor_list = ['tutor1', 'tutor2', 'tutor3', 'tutor4', 'tutor5', 'tutor6', 'tutor7', 'tutor8', 'tutor9', 'tutor10', 'tuto11', 'tutor12']
    instance = assign_tutors(file_name, tutor_list)
    for i in instance:
        line =  [instance[i][x] for x in instance[i]]
        print(i, "    ",line[1], line[2], line[4], line[5])
