class StudentData:
    def __init__(self, name, courses):
        self.name = name
        self.courses = []
        self.courses.append(courses)

    def add_course(self, course):
        self.courses.append(course)

    def __repr__(self):                                               
        output = "Name: " + self.name + "\t" + "Courses: " + str(self.courses) + "\n"
        return output