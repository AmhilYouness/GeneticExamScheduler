import csv
import io
from StudentData import StudentData


class DataLoader:
    def __init__(self, courses_file=None, teachers_file=None, students_file=None):
        # self.courses_path = courses_path
        # self.teachers_path = teachers_path
        # self.students_path = students_path
        self.courses_file = courses_file
        self.teachers_file = teachers_file
        self.students_file = students_file
        self.courses = []
        self.teachers = []
        self.students = []
        self.load_data()


    def is_course_in_list(self, code):
        for course in self.courses:
            if code == course[0]:
                return True
        return False
    
    
    # def load_courses(self):
    #     #with open("data/temp_courses.csv") as csv_file:       # Sample Dataset 
    #     with open(self.courses_path) as csv_file:            # Provided Dataset
    #         csv_reader = csv.reader(csv_file, delimiter=',')  # Loading courses
    #         for row in csv_reader:
    #             code_title = row[0], row[1]

    #             if not self.is_course_in_list(code_title[0]):
    #                 self.courses.append(code_title)
    def load_courses(self):
        with io.TextIOWrapper(self.courses_file, encoding="utf-8") as text_file:
            csv_reader = csv.reader(text_file, delimiter=',')  # Loading courses
            for row in csv_reader:
                code_title = row[0], row[1]
                print(code_title)
                if not self.is_course_in_list(code_title[0]):
                    self.courses.append(code_title)



    def load_teachers(self):
        with io.TextIOWrapper(self.teachers_file, encoding="utf-8") as text_file:
            csv_reader = csv.reader(text_file, delimiter=',')  # Loading teachers
            for row in csv_reader:
                if len(row) > 0:
                    name = row[0]
                    self.teachers.append(name)


    def add_student(self, name, cc):                               # Add a course for a specific student in the list
        for student in self.students:
            if student.name == name:
                if cc not in student.courses:                              # To cater repeated value
                    student.add_course(cc)
                return

        new_student = StudentData(name, cc)
        self.students.append(new_student)

    
    def load_students(self):
        with io.TextIOWrapper(self.students_file, encoding="utf-8") as text_file:
            csv_reader = csv.reader(text_file, delimiter=',')  # Reading students and their courses
            line = 0
            for row in csv_reader:
                if line != 0:
                    name = row[1]
                    cc = row[2]
                    self.add_student(name, cc)
                line += 1

    def load_data(self):
        self.load_courses()
        self.load_teachers()
        self.load_students()


