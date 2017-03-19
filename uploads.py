'''
pip install xlrd
student number: c1668782
'''
import xlrd



def excel_to_list(file):
    tutors_list = []
    file = xlrd.open_workbook(file)
    xl_sheet = file.sheet_by_index(0)
    num_cols = xl_sheet.ncols
    for i in range(0, xl_sheet.nrows):
        for col_idx in range(0, num_cols):
            cell_obj = xl_sheet.cell(i, col_idx)
            tutors_list.append(cell_obj.value)
    return tutors_list


def excel_to_dict2(file):
    converted = []
    file = xlrd.open_workbook(file)
    xl_sheet = file.sheet_by_index(0)
    num_cols = xl_sheet.ncols   # Number of columns
    for i in range(1, xl_sheet.nrows):    # Iterate through rows
        row_list = []
        for col_idx in range(0, num_cols):  # Iterate through columns
            cell_obj = xl_sheet.cell(i, col_idx)  # Get cell object by row, col\
            row_list.append([col_idx, cell_obj.value]) 
        if row_list[0] and row_list[1] and row_list[2] and row_list[5]:
            converted.append((i-1, row_list))
    return sorted(converted, key=lambda o: o[1][5][1])


def assign_tutors2(info, tutor_list):
    counter = 0
    counter2 = 0
    tutors_number = len(tutor_list)
    students_number = len(info)
    if tutors_number:
        min_student_group = students_number // tutors_number
        left_students = students_number % tutors_number

        next_group = min_student_group
        for j, i in enumerate(info):
            counter += 1
            info[j][1][4][1] = tutor_list[counter2]
            if counter2 < tutors_number-1:
                if next_group < counter+1:
                    counter = 0
                    counter2 +=1
                    if (students_number - (j+1+(tutors_number-counter2)*min_student_group) > 0):
                        next_group = min_student_group + 1
                    else:
                        next_group = min_student_group
    return info



