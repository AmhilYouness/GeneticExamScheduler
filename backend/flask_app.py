from flask import Flask, render_template, request, jsonify  
import csv
import collections
import csv
import random
from copy import deepcopy

from colorama import Fore, Back
from numpy import random
from numpy.random import randint

from GA.ga_temp import genetic_algo, print_custom_schedule, print_check
from DataLoader.dataLoader import DataLoader





app = Flask(__name__, static_folder='static')

global classroom, mydata
classroom = collections.namedtuple('classrooms', 'room_name morning invig_morning noon invig_noon')
mydata = {}
# mydata = {'2023-09-18': [classrooms(room_name='C305', morning='AI2011', invig_morning='Arshad Islam', noon='SS118', invig_noon='Aqeel Shahzad'),
#     classrooms(room_name='C308', morning='SS113', invig_morning='Sehrish Hassan', noon='EE229', invig_noon='Muhammad bin Qasim'),
#     classrooms(room_name='C302', morning='MT224', invig_morning='Hamda Khan', noon='MG223', invig_noon='Javaria Imtiaz'),
#     classrooms(room_name='C309', morning='CS218', invig_morning='Kifayat Ullah', noon='SS118', invig_noon='Noor ul Ain')],
#     '2023-09-19': [classrooms(room_name='C307', morning='MT205', invig_morning='Gul e Aisha', noon='CS219', invig_noon='Hassan Mustafa'),
#     classrooms(room_name='C309', morning='DS3011', invig_morning='Noor ul Ain', noon='CS217', invig_noon='Sidra Khalid'),
#     classrooms(room_name='C301', morning='MT205', invig_morning='Shahzad Mehmood', noon='SS118', invig_noon='Zohaib Iqbal'),
#     classrooms(room_name='C303', morning='MT205', invig_morning='Kashif Munir', noon='SS113', invig_noon='Farah Naz'),
#     classrooms(room_name='C305', morning='CS220', invig_morning='Sumera Abbas', noon='CS217', invig_noon='Mehreen Alam'),
#     classrooms(room_name='C302', morning='CS219', invig_morning='Rohail Gulbaz', noon='SS152', invig_noon='Tayyab Nadeem'),
#     classrooms(room_name='C304', morning='SE110', invig_morning='Usman Rashid', noon='CS302', invig_noon='Amna Irum'),
#     classrooms(room_name='C308', morning='CS302', invig_morning='Adnan Tariq', noon='EE229', invig_noon='Noreen Jamil'),
#     classrooms(room_name='C306', morning='CS220', invig_morning='Mehboobullah', noon='SS111', invig_noon='Maimoona Rassol')],
#     '2023-09-20': [classrooms(room_name='C301', morning='CS218', invig_morning='Javaria Imtiaz', noon='EE227', invig_noon='Noor ul Ain'),
#     classrooms(room_name='C305', morning='CY2012', invig_morning='Ameen Chilwan', noon='SE110', invig_noon='Gul e Aisha'),
#     classrooms(room_name='C302', morning='MT205', invig_morning='Shams Farooq', noon='CS211', invig_noon='Ejaz Ahmed'),
#     classrooms(room_name='C306', morning='MG220', invig_morning='Usman Ashraf', noon='CS328', invig_noon='Sidra Khalid'),
#     classrooms(room_name='C307', morning='CS219', invig_morning='Mehreen Alam', noon='CS328', invig_noon='Hammad Majeed'),
#     classrooms(room_name='C309', morning='SS111', invig_morning='Hassan Mustafa', noon='SE110', invig_noon='Arshad Islam'),
#     classrooms(room_name='C304', morning='CS217', invig_morning='Farah Jabeen Awan', noon='CS118', invig_noon='Farwa Batool'),
#     classrooms(room_name='C310', morning='EE227', invig_morning='Zeeshan Qaiser', noon='CS211', invig_noon='Maheen Arshad')],
#     '2023-09-21': [],
#     '2023-09-22': [],
#     '2023-09-25': [classrooms(room_name='C306', morning='MG223', invig_morning='Arshad Islam', noon='DS3011', invig_noon='Farah Naz')],
#     '2023-09-26': [classrooms(room_name='C304', morning='CS328', invig_morning='Irum Inayat', noon='CS307', invig_noon='Muhammad Usman'),
#     classrooms(room_name='C309', morning='CS118', invig_morning='Ejaz Ahmed', noon='AI2011', invig_noon='Zeeshan Qaiser')],
#     '2023-09-27': [],
#     '2023-09-28': [],
#     '2023-09-29': [classrooms(room_name='C309', morning='EE227', invig_morning='Asma Nisa', noon='MT224', invig_noon='Noreen Jamil'),
#     classrooms(room_name='C310', morning='MG220', invig_morning='Umair Arshad', noon='CS307', invig_noon='Farwa Batool'),
#     classrooms(room_name='C302', morning='SS118', invig_morning='Behjat Zuhaira', noon='EE227', invig_noon='Maimoona Rassol'),
#     classrooms(room_name='C304', morning='CS328', invig_morning='Hassan Mustafa', noon='CY2012', invig_noon='Usman Ashraf'),
#     classrooms(room_name='C308', morning='AI2011', invig_morning='Rohail Gulbaz', noon='CY2012', invig_noon='Asif Naeem')],
#     '2023-09-30': []}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Initialize an empty list to store the data from the CSV files
        csv_data = []
        file1 = request.files.get('file1')
        file2 = request.files.get('file2')
        file3 = request.files.get('file3')
        # Process the data as needed
        output = process_csv([file1, file2, file3])
        return render_template('index.html', output=output)

    return render_template('index.html', output=None)


def process_csv(files):
    global mydata
    data = DataLoader(files[0], files[1], files[2])
    population_size = random.randint(50, 200)          # number of solutions in a population
    max_generations = random.randint(100, 1000)        # how long to iterate
    crossover_probability = 1
    mutation_probability = 0.6
    res = genetic_algo(population_size, max_generations, crossover_probability, mutation_probability, data.courses, data.teachers,
                       data.students)
    mydata = res.days
    return []






@app.route('/get_calendar_data')
def get_calendar_data():
    events = []
    for date, classrooms in mydata.items():
        print(date)
        for classroomst in classrooms:
            # Customize this as per your data structure
            event = {
                'title': f'{classroomst.room_name} - Morning: {classroomst.morning}, Noon: {classroomst.noon}',
                'start': date,
                'invig_morning': classroomst.invig_morning,
                'invig_noon': classroomst.invig_noon,
            }
            events.append(event)
    return jsonify(events)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/get_events')
def get_events():
    events = [
        {
            'title': 'Event 1',
            'start': '2023-09-25T10:00:00',
            'end': '2023-09-25T12:00:00',
        },
        {
            'title': 'Event 2',
            'start': '2023-09-27T14:00:00',
            'end': '2023-09-27T16:00:00',
        },
    ]
    return jsonify(events)


if __name__ == '__main__':
    app.run(debug=True)
