import collections
import random
from copy import deepcopy

from colorama import Fore, Back
from numpy import random
from numpy.random import randint

from Schedule.schedule import Schedule

class GA:
    def __init__():
        pass

    def hconstraint_all_courses(self, schedule, courses):         # Hard Const 1 = Exam scheduled for every course
        bool_check = False

        exam_list = []
        total_exams = 0

        for day in schedule.days:                           # Getting list of all exams in the schedule week
            class_list = schedule.days[day]

            for _class in class_list:                       # Examining every classroom assigned
                m_exam = _class.morning
                n_exam = _class.noon
                total_exams += 2

                if m_exam not in exam_list:
                    exam_list.append(m_exam)

                if n_exam not in exam_list:
                    exam_list.append(n_exam)

        exam_codes = []                                     # List of all exams

        for course in courses:
            code = course[0]
            exam_codes.append(code)                         # Gets list of all exam codes of all courses

        missing = 0
        for code in exam_codes:
            if code not in exam_list:                       # Comparing the two lists
                missing += 1                                # Number of courses not listed

        if missing == 0:                                    # If the constraint is satisfied completely
            bool_check = True

        num = (1 / (1 + missing))

        return num, bool_check
    

    def hconstraint_clashing_exams(self, schedule, course_allocation):  # Hard Const 2.1 : Student has 1 exam at a time
        exam_list = []

        for day in schedule.days:                                 # Getting list of all exams in this schedule
            classes_list = schedule.days[day]

            for _class in classes_list:                           # Storing all exams for that day
                exam_list.append(_class.morning)
                exam_list.append(_class.noon)

        exam_counts = dict(collections.Counter(exam_list))

        clashes = 0
        student_names_clashes = []
        bool_check = False

        for day in schedule.days:                                 # Getting list of classrooms for every day
            classes_list = schedule.days[day]

            morning_list = []
            noon_list = []

            for _class in classes_list:                           # Getting lists of all exams on morning and noon
                morning_list.append(_class.morning)
                noon_list.append(_class.noon)

            for student in course_allocation:                     # Examining all students and their allocated courses
                course_list = student.courses
                name = student.name

                clash_flag = False                                # Checking if record clashes for a student

                count = 0
                for course in morning_list:
                    if course in course_list:
                        if course in exam_counts.keys():
                            if exam_counts[course] == 1:          # Exam only at this specific time
                                count += 1                        # Counting clashes in morning for a student

                if name not in student_names_clashes:
                    if count > 1:
                        clash_flag = True
                        clashes += 1
                        student_names_clashes.append(name)

                count = 0
                for course in noon_list:
                    if course in course_list:
                        if course in exam_counts.keys():
                            if exam_counts[course] == 1:
                                count += 1

                if name not in student_names_clashes:
                    if count > 1 and not clash_flag:
                        clashes += 1                              # Counting clashes in evening for a student
                        student_names_clashes.append(name)

        if clashes == 0:                                          # If the constraint is satisfied completely
            bool_check = True

        num = (1 / (1 + clashes))

        return num, bool_check
    

    def hconstraint_teachers_sametime(self, schedule):                  # Hard Const 5.1 : No teacher clashes at the same time
        clashes = 0
        bool_check = False

        for day in schedule.days:
            classes_list = schedule.days[day]
            morning_list = []
            noon_list = []

            for _class in classes_list:                           # Getting lists of all teachers on morning and noon
                morning_list.append(_class.invig_morning)
                noon_list.append(_class.invig_noon)

            dup_count_morning = dict(collections.Counter(morning_list))  # Getting the number of duplicate entries
            dup_count_noon = dict(collections.Counter(noon_list))

            for value in dup_count_morning.values():
                if value > 1:
                    clashes += 1                                         # Calculating the number of clashes

            for value in dup_count_noon.values():
                if value > 1:
                    clashes += 1

        if clashes == 0:                                                 # If the constraint is satisfied completely
            bool_check = True

        num = (1 / (1 + clashes))

        return num, bool_check
    
    def hconstraint_teacher_samerow(self, schedule):                           # Hard Const 6 : No teacher has duties in a row
        consecutive = 0
        bool_check = False
        for day in schedule.days:
            classes_list = schedule.days[day]
            morning_list = []
            noon_list = []

            for _class in classes_list:                                  # Getting lists of all teachers on morning and noon
                morning_list.append(_class.invig_morning)
                noon_list.append(_class.invig_noon)

            for teacher in morning_list:
                if teacher in noon_list:
                    consecutive += 1                                     # Calculating the number of consecutive duties

        if consecutive == 0:                                             # If the contraint is satisfied completely
            bool_check = True

        num = (1 / (1 + consecutive))

        return num, bool_check
    

    def sconstraint_less_days(self, schedule):                                 # Soft Const 3: Schedule in less days
        no_days = 0

        for day in schedule.days:
            classes_list = schedule.days[day]                            # Getting schedule for each day

            if not classes_list:                                         # Checks if nothing is scheduled
                no_days += 1

        n = len(total_days) - no_days
        num = (1 / (1 + n))

        return num, no_days   


    def sconstraint_mg_before(self, schedule, course_allocation):              # Soft Const 4: MG courses scheduled before CS courses
        student_list = []
        bool_check = False

        for student in course_allocation:                                # For every student
            mg_flag = False
            cs_flag = False

            for course in student.courses:                               # Checks if a student opts both CS and MG courses
                if 'MG' in course:
                    mg_flag = True
                if 'CS' in course:
                    cs_flag = True

            if mg_flag and cs_flag:
                student_list.append(student)                             # List of students meeting the condition

        student_names = []
        wrong_order = 0

        for i in range(0, len(student_list) - 1):                        # For every student
            student = student_list[i]
            cs_flag = False

            for day in schedule.days:                                    # Checks schedule of all 5 days for each student
                classes_list = schedule.days[day]
                exam_list = []

                for _class in classes_list:                              # Storing all exams for that day
                    exam_list.append(_class.morning)
                    exam_list.append(_class.noon)

                for course in student.courses:
                    if 'CS' in course:
                        if course in exam_list:
                            cs_flag = True                               # Checks if CS couse of student comes before MG

                    elif 'MG' in course:
                        if course in exam_list:
                            if cs_flag:                                  # If MG comes after CS
                                if student.name not in student_names:
                                    student_names.append(student.name)
                                    wrong_order += 1
                                i += 1

        if wrong_order == 0:                                             # If the constraint is satisfied completely
            bool_check = True

        num = (1 / (1 + wrong_order))

        return num, bool_check 


        
    def calculate_fitness(self, population, courses, course_allocation):
        for schedule in population:                                  # For each schedule in a population
            hc1, hb1 = self.hconstraint_all_courses(schedule, courses)
            hc2, hb2 = self.hconstraint_clashing_exams(schedule, course_allocation)
            hc3, hb3 = self.hconstraint_teachers_sametime(schedule)
            hc4, hb4 = self.hconstraint_teacher_samerow(schedule)
            # hc5, hb5 = hconstraint_course_scheduled_once(schedule, courses)
            sc2, empty_days = self.sconstraint_less_days(schedule)
            sc3, sb3 = self.sconstraint_mg_before(schedule, course_allocation)

            fitness = hc1 + hc2 + hc3 + hc4 + sc2 + sc3              # Calculating the fitness of the schedule
            schedule.fitness = fitness                               # Adding the fitness to the class

            if empty_days > 7:                                       # No schedule with too many empty days added
                schedule.fitness -= 2

        return population
    
    
    def get_fitness(self,schedule):                                       # Returning fitness
        return schedule.fitness
    

    def two_fittest_schedules(self, population):                           # Selecting two fittest solutions (schedules)
        pop = deepcopy(population)
        pop.sort(key=self.get_fitness, reverse=True)                      # Sorts in descending order
        return pop[0], pop[1]
    

    def parent_selection(self, population):                                # Roulette Wheel Selection

        parents = []
        total_fitness = 0

        for schedule in population:
            total_fitness += schedule.fitness

        highest, second_highest = self.two_fittest_schedules(population)  # Getting two fittest solutions
        parents.append(highest)
        parents.append(second_highest)
        fitness_sum = 0

        while len(parents) < len(population):

            individual = random.randint(0, len(population))          # Getting a random index
            fitness_sum += population[individual].fitness
            if fitness_sum >= total_fitness:                         # Individual chosen based on its probability
                if population[individual] not in parents:
                    parents.append(deepcopy(population[individual]))

        return parents
    

    def mix_days(self, parent_a, parent_b):                                # Generating new schedule
        no_days_to_mix = randint(1, len(total_days))                 # Random crossover point
        child1 = Schedule()
        child2 = deepcopy(child1)

        i = 0
        for day in total_days:

            if i < no_days_to_mix:                                  # Taking that # of days from first parent
                classes_list_a = parent_a.days[day]
                classes_list_b = parent_b.days[day]

                child1.days[day] = deepcopy(classes_list_a)
                child2.days[day] = deepcopy(classes_list_b)

            else:                                                   # Taking rest of days from second parent
                classes_list_a = parent_a.days[day]
                classes_list_b = parent_b.days[day]

                child1.days[day] = deepcopy(classes_list_b)
                child2.days[day] = deepcopy(classes_list_a)

            i += 1

        return child1, child2
    

        
    def mutate_schedule(self, schedule, mutation_probability, courses, teachers):  # Applying mutation on chromosomes

        if randint(0, 100) <= mutation_probability * 100:                    # Checking prob for mutation
            random_days = randint(0, len(total_days))                        # Selecting random no of days to change

            for i in range(0, random_days):
                                                                            # Choosing a random day
                idx = randint(0, len(total_days))
                day = total_days[idx]

                classes_list = schedule.days[day]

                                                                            # If it had assigned classes/exams
                if len(classes_list) > 0:
                    if randint(0, 2) == 1:
                        for j in range(0, len(classes_list)):                # Will change one class at a time

                            if randint(0, 2) == 1:                           # 50% probabilty for mutation
                                index = random.randint(0, len(courses))      # Randomly replacing course
                                morning = courses[index][0]

                                index = random.randint(0, len(teachers))     # Randomly replacing invigilator
                                invig_morning = teachers[index]

                                index = random.randint(0, len(courses))      # Randomly replacing course
                                noon = courses[index][0]

                                index = random.randint(0, len(teachers))     # Randomly replacing invigilator
                                invig_noon = teachers[index]

                                                                            # Updating the values
                                classes_list[j] = classes_list[j]._replace(morning=morning, invig_morning=invig_morning)
                                classes_list[j] = classes_list[j]._replace(noon=noon, invig_noon=invig_noon)
                    else:
                        classes_list.clear()

                                                        # If that day was empty, then assign it some classes/exams
                else:
                    visited_indexes = []
                    total_classrooms = random.randint(0,
                                                    5)   # Classrooms = room_name, morning, invig_morning, noon, invig_noon

                    for j in range(total_classrooms):

                        index = random.randint(0, 9)       # Generating that number of classrooms

                        while index in visited_indexes:
                            index = random.randint(0, 9)

                        room = room_names[index]
                        visited_indexes.append(index)

                        index = random.randint(0, len(courses))   # Randomly picking morning course
                        m_course = courses[index][0]

                        index = random.randint(0, len(teachers))  # Randomly picking invigilator for morning
                        m_invig = teachers[index]

                        index = random.randint(0, len(courses))   # Randomly picking noon course
                        n_course = courses[index][0]

                        index = random.randint(0, len(teachers))  # Randomly picking invigilator for noon
                        n_invig = teachers[index]

                        classes_list.append(
                            classrooms(
                                room_name=room,
                                morning=m_course,
                                invig_morning=m_invig,
                                noon=n_course,
                                invig_noon=n_invig
                            )
                        )

        return schedule  
    

    def apply_crossover(self, population, crossover_probability):       # Applying crossover

        crossovered_population = []

                                                                # Equal length crossover
        while len(crossovered_population) < len(population):
            if randint(0, 100) <= crossover_probability * 100:
                parent_a, _ = self.two_fittest_schedules(population)   # Selecting fittest parent

                                                                # Selecting a random parent
                index_b = randint(0, len(population))
                parent_b = population[index_b]

                child1, child2 = mix_days(parent_a, parent_b)

                crossovered_population.append(deepcopy(child1))
                crossovered_population.append(deepcopy(child2))

        return crossovered_population
        

    def apply_mutation(self, population, mutation_probability, courses, teachers):
        mutated_population = []

        for schedule in population:
            s = mutate_schedule(schedule, mutation_probability, courses, teachers)
            mutated_population.append(deepcopy(s))

        return mutated_population
    


    def genetic_algo(self, population_size, max_generations, crossover_probability, mutation_probability, courses, teachers,
                    course_allocation):
        if not hconstraint_three_courses(course_allocation):
            print("Data is flawed. Every student must have at least 3 courses allocated. Terminating program :(")
            return None

        best_solution = None

                                                # Generating a list of schedules
        population = [generate_population(population_size, courses, teachers)]

                                                # For seeing if algorithm is unable to optimise further
        stagnant = 0
        reset_count = 0
        solutions_list = []
        prev_best = None

        for i in range(max_generations):

                                                # Evaluating fitness
            pop = self.calculate_fitness(population[0], courses, course_allocation)

                                                # Selecting parents through roulette wheel selection
            parents = self.parent_selection(deepcopy(pop))

                                                # Applying crossover
            crossover_population = self.apply_crossover(parents, crossover_probability)
            self.calculate_fitness(crossover_population, courses, course_allocation)

                                                # Applying mutation
            mutated_population = apply_mutation(crossover_population, mutation_probability, courses, teachers)
            self.calculate_fitness(mutated_population, courses, course_allocation)

                                                # Finding fittest candidate
            schedule1, _ = self.two_fittest_schedules(mutated_population)

            if best_solution is None:
                stagnant = 0
                best_solution = deepcopy(schedule1)

            elif schedule1.fitness > best_solution.fitness:
                stagnant = 0
                best_solution = deepcopy(schedule1)

            if best_solution.fitness == prev_best:
                stagnant += 1

            prev_best = deepcopy(best_solution.fitness)

            if self.constraints_satisfied_check(best_solution, courses, course_allocation):
                constraints_satisfied_print(best_solution, courses, course_allocation)
                print()
                print(Back.BLACK + "                                                                         " + Back.RESET)
                print(
                    Back.BLACK + Fore.WHITE + "                             SOLUTION FOUND!!!!                          " + Fore.RESET + Back.RESET)
                print(Back.BLACK + "                                                                         " + Back.RESET)
                print()
                return best_solution

                                                # No further optimisation for this # of generations
            if stagnant == 50:
                if reset_count < 3:
                    print(
                        "\n-------------------\nAlgorithm is unable to optimise further. Starting over with a new random population.\n-------------------\n")
                    solutions_list.append(deepcopy(best_solution))

                    i = 0
                    stagnant = 0
                    reset_count += 1

                    pop = generate_population(population_size, courses, teachers)
                    best_solution = None
                    population.clear()
                    population.append(pop)
                    continue

                else:
                    print(
                        "\nAlgorithm unable to optimise further. Terminating program and returning best solution upto now.\n")
                    best, _ = self.two_fittest_schedules(solutions_list)
                    return best

            else:
                                                # Generating new population
                population.clear()
                population.append(mutated_population)

            if i % 25 == 0:
                print("Current generation so far: ", i)
                print("Best solution so far: \nFitness: ", best_solution.fitness)
                print_schedule(best_solution)
                constraints_satisfied_print(best_solution, courses, course_allocation)

            print(i, "- Fitness of best solution: ", best_solution.fitness, "\t( Fitness of local best solution: ",
                schedule1.fitness, ")", "\t( Stagnation: ", stagnant, ")")

        return best_solution

        


