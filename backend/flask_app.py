from flask import Flask, render_template, request
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



app = Flask(__name__)

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
    data = DataLoader(files[0], files[1], files[2])
    population_size = random.randint(50, 200)          # number of solutions in a population
    max_generations = random.randint(100, 1000)        # how long to iterate
    crossover_probability = 1
    mutation_probability = 0.6
    res = genetic_algo(population_size, max_generations, crossover_probability, mutation_probability, data.courses, data.teachers,
                       data.students)

    # print_custom_schedule(res)
    # print_check()
    # print(res)
    return res


def process_data(csv_data):
    # Perform processing on the CSV data
    # Here, you can implement your custom logic
    # For demonstration, we'll just return the data as a string
    return str(csv_data)

if __name__ == '__main__':
    app.run(debug=True)
