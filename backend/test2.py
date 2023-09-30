import collections
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, make_response, Response
from flask_bcrypt import Bcrypt
import pdfkit


classroom = collections.namedtuple(
    "classrooms", "room_name morning invig_morning noon invig_noon"
)

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


result = {}
for date, classrooms in mydata.items():
    result[date] = {}
    for classroom in classrooms:
        result[date][classroom.room_name] = {"morning" : classroom.morning, "invig_morning": classroom.invig_morning, "noon": classroom.noon, "invig_noon": classroom.invig_noon}

app = Flask(__name__, static_folder="static")


@app.route("/cal")
def calendar():
    return render_template("cal.html", data=result)


import pdfkit



@app.route('/download_pdf')
def download_pdf():
    config =   pdfkit.configuration(wkhtmltopdf='C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe')
    options = {
        'page-size': 'A4',
        'orientation': 'portrait',
    }
    try:
        # Generate PDF from the HTML content
        pdfkit.from_url('http://127.0.0.1:5000/cal', 'webpage.pdf', configuration=config, options=options)

        # Create a response with the PDF file
        response = make_response(open('webpage.pdf', 'rb').read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=webpage.pdf'

        return response
    except Exception as e:
        print("Error:", str(e))
        return "PDF generation failed."

if __name__ == "__main__":
    app.run(debug=True)
