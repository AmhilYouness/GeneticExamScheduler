from DataLoader import DataLoader


classes_path = "C:/Users/Youness/Desktop/projiyat free/zineb pyexams/backend/data/courses.csv"
teachers_path = "C:/Users/Youness/Desktop/projiyat free/zineb pyexams/backend/data/teachers.csv"
students_path = "C:/Users/Youness/Desktop/projiyat free/zineb pyexams/backend/data/studentCourse.csv"
data = DataLoader(classes_path, teachers_path, students_path)
data.load_courses
print(data.courses)