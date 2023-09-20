import collections
import csv
import random
from copy import deepcopy

from colorama import Fore, Back
from numpy import random
from numpy.random import randint

from GA.ga_temp import genetic_algo, print_custom_schedule, print_check
from DataLoader.dataLoader import DataLoader

################################################### GLOBALS #########################################################

# Hard Const 7 : Total of 10 rooms

room_names = ['C301', 'C302', 'C303', 'C304', 'C305', 'C306', 'C307', 'C308', 'C309', 'C310']

# Hard Const 3 : No exams on weekends

total_days = ['Week 1 : Mon', 'Week 1 : Tue', 'Week 1 : Wed', 'Week 1 : Thu', 'Week 1 : Fri', 'Week 2 : Mon',
              'Week 2 : Tue', 'Week 2 : Wed', 'Week 2 : Thu', 'Week 2 : Fri']#, 'Week 3 : Mon', 'Week 3 : Tue',
              #'Week 3 : Wed']

# Hard Const 5 : Each exam must have an invigilator.

classrooms = collections.namedtuple('classroom', 'room_name morning invig_morning noon invig_noon')



def main():
    classes_path = "C:/Users/Youness/Desktop/projiyat free/zineb pyexams/backend/data/courses.csv"
    teachers_path = "C:/Users/Youness/Desktop/projiyat free/zineb pyexams/backend/data/teachers.csv"
    students_path = "C:/Users/Youness/Desktop/projiyat free/zineb pyexams/backend/data/studentCourse.csv"
    data = DataLoader(classes_path, teachers_path, students_path)
    # courses, teachers, course_allocation = data.courses, data.

    population_size = random.randint(50, 200)          # number of solutions in a population
    max_generations = random.randint(100, 1000)        # how long to iterate

    crossover_probability = 1
    mutation_probability = 0.6

    print('\n\n--- Generated Parameters -----')
    print('Population size......: {}'.format(population_size))
    print('Number of generations: {}'.format(max_generations))
    print('Crossover probability: {}'.format(crossover_probability))
    print('Mutation probability: {}'.format(mutation_probability))

    res = genetic_algo(population_size, max_generations, crossover_probability, mutation_probability, data.courses, data.teachers,
                       data.students)

    # print_custom_schedule(res)
    # print_check()
    print(res)
    # print(res)


# Tell python to run main method
if __name__ == "__main__":
    main()


