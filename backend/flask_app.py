from flask import Flask, render_template, request, jsonify, redirect, url_for, session, make_response
from flask_bcrypt import Bcrypt
import collections
import random
from copy import deepcopy
from colorama import Fore, Back
from numpy import random
from numpy.random import randint
from GA.ga_temp import genetic_algo, print_custom_schedule, print_check
from DataLoader.dataLoader import DataLoader
import pdfkit



app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'  
bcrypt = Bcrypt(app)


# Replace these with your actual usernames and passwords
user_database = {
    'zineb@gmail.com': bcrypt.generate_password_hash('zineb').decode('utf-8'),
    'test@gmail.com': bcrypt.generate_password_hash('test').decode('utf-8')
}

global classroom, mydata
classroom = collections.namedtuple('classrooms', 'room_name morning invig_morning noon invig_noon')


mydata = {

        "Lundi-0": [
            classroom(
                room_name="C305",
                morning="ELC2021",
                invig_morning="Mme. Intissar EL IDRISSI",
                noon="INF3071",
                invig_noon="Mme. Amal ",
            ),
            classroom(
                room_name="C308",
                morning="IND4051",
                invig_morning="Dr. Altaf EL BLIDI",
                noon="PHS1021",
                invig_noon="Mme Zineb LMAADAM",
            ),
            classroom(
                room_name="C304",
                morning="INF4071",
                invig_morning="Mme. Zineb CHAAIBI",
                noon="ELC4071",
                invig_noon="M. Abdelaziz EL AISSAOUI",
            ),
        ],
        "Lundi-1": [
            classroom(
                room_name="C301",
                morning="ELC4061",
                invig_morning="Dr. Mohamed MAINE",
                noon="MEC2012",
                invig_noon="M. Jihad EL HADI",
            ),
            classroom(
                room_name="C309",
                morning="SSH1022",
                invig_morning="Dr. Safae",
                noon="IND4051",
                invig_noon="Mme Zineb LMAADAM",
            ),
            classroom(
                room_name="C310",
                morning="MEC2012",
                invig_morning="M. Abdelaziz EL AISSAOUI",
                noon="ELC3051",
                invig_noon="Dr. Oussama SMIMITE",
            ),
            classroom(
                room_name="C304",
                morning="IND4041",
                invig_morning="M. El Mehdi GUENDOULI",
                noon="ELC2021",
                invig_noon="M. Khalid EL FAYQ",
            ),
        ],
        "Mardi-0": [
            classroom(
                room_name="C305",
                morning="CHM1011",
                invig_morning="Dr. Boujemaa NACIRI",
                noon="INF4081",
                invig_noon="M. Yassine TALIZZA",
            ),
            classroom(
                room_name="C307",
                morning="INF4101",
                invig_morning="M. Mustapha El MINOR",
                noon="ELC3061",
                invig_noon="Dr. Mohamed MAINE",
            ),
            classroom(
                room_name="C303",
                morning="ELC3071",
                invig_morning="Dr. Brahim BOUKANJIME",
                noon="ELC4051",
                invig_noon="Dr. Btissame ES SETTE",
            ),
        ],
        "Mardi-1": [],
        "Mercredi-0": [
            classroom(
                room_name="C301",
                morning="INF4091",
                invig_morning="Mme Aoulaya KERMAOUI",
                noon="INF4061",
                invig_noon="M. El Mehdi GUENDOULI",
            ),
            classroom(
                room_name="C310",
                morning="IND4051",
                invig_morning="M. Mohamed ACHTCHY",
                noon="ELC3071",
                invig_noon="M. Khalid EL FAYQ",
            ),
        ],
        "Mercredi-1": [
            classroom(
                room_name="C306",
                morning="INF4081",
                invig_morning="M. Youssef EL MINOR",
                noon="ELC2021",
                invig_noon="M. Amine AZNAG",
            ),
            classroom(
                room_name="C307",
                morning="ELC3051",
                invig_morning="Mme. Intissar EL IDRISSI",
                noon="MAT1011",
                invig_noon="M.Amir BAINHAIDA",
            ),
        ],
        "Jeudi-0": [
            classroom(
                room_name="C307",
                morning="SSH3021",
                invig_morning="M. Abdelaziz EL AISSAOUI",
                noon="INF1021",
                invig_noon="M. Zaid EL FID",
            ),
            classroom(
                room_name="C306",
                morning="SSH4031",
                invig_morning="M. Mohamed AASLI",
                noon="SSH3031",
                invig_noon="M. Amine BENDERMA",
            ),
            classroom(
                room_name="C305",
                morning="ELC1021",
                invig_morning="M. Mustapha El MINOR",
                noon="INF2031",
                invig_noon="Dr. Btissame ES SETTE",
            ),
        ],
        "Jeudi-1": [
            classroom(
                room_name="C308",
                morning="MEC2011",
                invig_morning="M. Lahcen LEILI",
                noon="MAT3031",
                invig_noon="M. Ahmed EL IDRISSI",
            ),
            classroom(
                room_name="C303",
                morning="ELC1021",
                invig_morning="Dr. Oussama SMIMITE",
                noon="MAT1021",
                invig_noon="Dr. Altaf EL BLIDI",
            ),
            classroom(
                room_name="C301",
                morning="ELC3061",
                invig_morning="Mme. Zahra EL AIDDOUD",
                noon="MAT2021",
                invig_noon="Mme Zineb LMAADAM",
            ),
            classroom(
                room_name="C306",
                morning="ELC4071",
                invig_morning="M. Mustapha El MINOR",
                noon="ELC3041",
                invig_noon="Dr. Lamiae OULANTI",
            ),
        ],
        "Vendredi-0": [
            classroom(
                room_name="C302",
                morning="MAT2022",
                invig_morning="M. Mustapha El MINOR",
                noon="PHS1021",
                invig_noon="M. Zaid EL FID",
            )
        ],
        "Vendredi-1": [
            classroom(
                room_name="C308",
                morning="SSH1021",
                invig_morning="M. Yassine DAHANE",
                noon="INF3081",
                invig_noon="M. Mustapha El MINOR",
            ),
            classroom(
                room_name="C301",
                morning="INF3061",
                invig_morning="Mme. Zahra EL AIDDOUD",
                noon="INF3061",
                invig_noon="Mme Zineb LMAADAM",
            ),
        ],
        "Samedi-0": [
            classroom(
                room_name="C306",
                morning="INF1021",
                invig_morning="Mme. Zineb CHAAIBI",
                noon="ELC3071",
                invig_noon="Mme Aoulaya KERMAOUI",
            ),
            classroom(
                room_name="C305",
                morning="ELC4071",
                invig_morning="M. Jihad EL HADI",
                noon="SSH4032",
                invig_noon="Dr. Oussama SMIMITE",
            ),
            classroom(
                room_name="C308",
                morning="PHS2021",
                invig_morning="M. Yassine DAHANE",
                noon="INF2031",
                invig_noon="M. Khalid EL FAYQ",
            ),
        ],
}



@app.route('/')
def index():
    # Check if the user is authenticated, if not, redirect to the login page
    if not user_authenticated():
        return redirect(url_for('login'))
    return render_template('index.html', output=None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('password')

        if username in user_database and bcrypt.check_password_hash(user_database[username], password):
            # User is authenticated, redirect to a protected route or perform other actions
            session["username"] = username
            return redirect(url_for('index'))
        else:
            # Authentication failed, show an error message
            error_message = 'Invalid username or password'
            print("error_message")
            return render_template('login.html', error_message=error_message)
    return render_template('login.html', error_message=None)


def user_authenticated():
    username = session.get('username')
    return username is not None and username in user_database


def start_algo(files, pop, gen, croi, mut):
    global mydata
    data = DataLoader(files[0], files[1], files[2])
    population_size = pop#random.randint(50, 200)          # number of solutions in a population
    max_generations = gen#random.randint(100, 1000)        # how long to iterate
    crossover_probability = croi#1
    mutation_probability = mut#0.6
    res = genetic_algo(population_size, max_generations, crossover_probability, mutation_probability, data.courses, data.teachers,
                       data.students)
    mydata = res.days


@app.route("/cal")
def calendar_temp():
    global mydata
    result = {}
    for date, classrooms in mydata.items():
        result[date] = {}
        for classroom in classrooms:
            result[date][classroom.room_name] = {"morning" : classroom.morning, "invig_morning": classroom.invig_morning, "noon": classroom.noon, "invig_noon": classroom.invig_noon}
    return render_template("new_cal.html", data=result)

@app.route("/calendar_full")
def calendar_full():
    global mydata
    result = {}
    for date, classrooms in mydata.items():
        result[date] = {}
        for classroom in classrooms:
            result[date][classroom.room_name] = {"morning" : classroom.morning, "invig_morning": classroom.invig_morning, "noon": classroom.noon, "invig_noon": classroom.invig_noon}
    return render_template("cal.html", data=result)


def calendar():
    global mydata
    result = {}
    for date, classrooms in mydata.items():
        result[date] = {}
        for classroom in classrooms:
            result[date][classroom.room_name] = {"morning" : classroom.morning, "invig_morning": classroom.invig_morning, "noon": classroom.noon, "invig_noon": classroom.invig_noon}
    return result# return render_template("cal.html", data=result)


@app.route('/download_pdf')
def download_pdf():
    config =   pdfkit.configuration(wkhtmltopdf='C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe')
    options = {
        'page-size': 'A4',
        'orientation': 'Landscape',
    }
    try:
        # Generate PDF from the HTML content
        pdfkit.from_url('http://127.0.0.1:5000/calendar_full', 'webpage.pdf', configuration=config, options=options)

        # Create a response with the PDF file
        response = make_response(open('webpage.pdf', 'rb').read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=webpage.pdf'

        return response
    except Exception as e:
        print("Error:", str(e))



@app.route('/dashboard')
def dashboard():
    return render_template("dash.html")

@app.route('/settings')
def settings():
    return render_template("settings.html")


@app.route('/planning', methods=['GET', 'POST'])
def planning():
    # Check if the user is authenticated, if not, redirect to the login page
    if not user_authenticated():
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Initialize an empty list to store the data from the CSV files
        csv_data = []
        file1 = request.files.get('file1')
        file2 = request.files.get('file2')
        file3 = request.files.get('file3')
        pop = int(request.form.get('population'))
        gen = int(request.form.get('generation'))
        croi = float(request.form.get("croisement"))
        mut = float(request.form.get("mutation"))

        start_algo([file1, file2, file3], pop, gen, croi, mut)
        result = calendar()
        return render_template("new_cal.html", data=result)

        # return render_template('index.html', output=output)
    return render_template('planning.html', output=None)








if __name__ == '__main__':
    app.run(debug=True)
