from fileinput import filename
from unicodedata import name
from urllib import response
import django
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from pdfparser.settings import BASE_DIR
from .models import profile
import PyPDF2
from email.policy import strict
from googletrans import Translator
import json
import os
import mimetypes


def solution(file_name):
    def correct_kn(s):
        s = s.replace('ತನದರ ', 'ತಂದೆ ')
        s = s.replace('ರಮಧಶ', 'ರಮೇಶ್ ಅವರದು ')
        s = s.replace('ಚಚನಬನಯ', 'ಚೌಣಾಬಾಯಿ ')
        s = s.replace('ವರರ', 'ವರ್ಷಗಳು ')
        s = s.replace('ಉದರಗನಧಗ‍', 'ಉದ್ಯೋಗ ')
        s = s.replace('ಒಕಕಲರತನ', 'ಒಕ್ಕಲುತನ ')
        s = s.replace('ಸನ', 'ನಿಧನರಾದರು ')
        s = s.replace('ಹರಗಲ', 'ಕೃಷಿ ')
        s = s.replace('ಮನರಕರಲಸ', 'ಮನೆಗೆಲಸ ')
        s = s.replace('ವಕಧಲರರ', 'ವಕೀಲ ')
        s = s.replace('ಅಪರನಧ', 'ಅಪರಾಧ ')
        s = s.replace('ದನನನಕ', 'ದಿನಾಂಕ ')
        s = s.replace('ಅಪರನಧಗಳರಭನ.ದನ.ನಿಧನರಾದರು', 'ವಿಭಾಗ ')
        s = s.replace(' ಸರಪರಪನಬರಲ', 'ಸೆಪ್ಟೆಂಬರ್ ')
        s = s.replace('ಕಲನ.', 'ವಿಭಾಗ')
        s = s.replace('ಸ.ಸ. ನನ.', 'ಸಿ . ಸಿ . ಸಂಖ್ಯೆ ')
        return s

    def correct_mr(s):
        s = s.replace('माफर ि', 'द्वारे ')
        s = s.replace(' ्फकारदीचे', 'तक्रारदार ')
        s = s.replace('िां्', 'नाव ')
        s = s.replace('धंदा', 'व्यवसाय ')
        s = s.replace('पाकर', 'पार्क ')
        s = s.replace('दाेडाईचा', 'Dondai ')
        s = s.replace('जज.', 'जिल्हा ')
        s = s.replace('र.', 'संख्या ')
        s = s.replace('नकाक्निणरक', 'निर्णय ')
        s = s.replace('नकाकालक', 'न्यायालय ')
        s = s.replace('उत्र', 'उत्तर ')
        s = s.replace('आ दे श', 'ऑर्डर करा ')
        s = s.replace('्क', 'वय ')
        s = s.replace(' ्रर', 'वर्षे ')
        return s

    def correct_ta(s):
        s = s.replace('తసడడ', 'తండ్రి ')
        s = s.replace('ససవతతరమల', 'సంవత్సరాలు ')
        s = s.replace('వవత', 'వృత్తి ')
        s = s.replace('గగమస', 'గ్రామం ')
        s = s.replace('మసడలస', 'మండలం ')
        s = s.replace('జలల', 'జిల్లా ')
        return s

    sop = ""
    # file_name = 'maharastra.pdf'

    pdfFileObj = open(file_name, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
    s = ""
    translator = Translator()
    no_of_page = pdfReader.numPages
    sop = ""
    string = ""
    for i in range(no_of_page):
        pageObj = pdfReader.getPage(i)
        s = pageObj.extractText()
        x = translator.detect(s).lang
        if(x == "kn"):
            s = correct_kn(s)
        if(x == "mr"):
            s = correct_mr(s)
        if(x == "ka"):
            s = correct_ta(s)
        # print(s)
        out = translator.translate(s)
        sop = sop+out.text
    sop = sop.lower()
    # print(sop)

    t = {
        "dist_name": "",
        "police_station": "",
        "fir_date": "",
        "fir_no": "",
        "state": "",
        "accused_name_1": "",
        "accused_name_1_org": "",
        "act": "",
        "act_org": "",
        "address_org": "",
        "age_1_org": "",
        "complaint_information_date_year_of_birth": "",
        "complaint_information_date_year_of_birth_org": "",
        "complaint_infromation_father_husband_name": "",
        "complaint_infromation_father_husband_name_org": "",
        "complaint_information_name": "",
        "complaint_information_name_org": "",
        "complaint_informan_nationality": "india ",
        "complaint_informan_nationality_org": "",
        "date": "",
        "details_address_1": "",
        "details_address_1_org": "",
        "dist_name_pdf": "",
        "dist_name_pdf_org": "",
        "fir_no_org": "",
        "occupation": "",
        "occupation_org": "",
        "occurrence_of_offence_date_from": "",
        "occurrence_of_offence_date_to": "",
        "occurrence_of_offence_time_from": "",
        "occurrence_of_offence_time_period": "",
        "occurrence_of_offence_time_to": "",
        "place_of_occurrence_district_org": "",
        "place_of_occurrence_name_of_police_station": "",
        "place_of_occurrence_name_of_police_station_org": "",
        "police_station_org": "",
        "sections": "",
        "sections_org": "",
        "year": ""
    }

    def info_fill(y):
        r1 = 0
        x = ""
        while(r1 < len(sop)):
            r1 = sop.find(y, r1)
            if(r1 != -1):
                r1 = r1+len(y)
                while(sop[r1] != '  ' and sop[r1] != "," and r1 < len(sop) and sop[r1] != "."):
                    r1 = r1+1
                    x = x+sop[r1]
                if(sop[r1] == ","):
                    x = x.replace(",", " ,")
                else:
                    x = x+" ,"
                r1 = r1 + 1
            else:
                break
        return x

    def info_fill_numdata(y):
        r1 = sop.find(y)
        if(r1 != -1):
            x = ""
            r1 = r1+len(y)
            while(sop[r1] != '  ' and r1 < len(sop) and sop[r1] != "." and sop[r1] != ","):
                r1 = r1+1
                x = x+sop[r1]
            if(sop[r1] == ","):
                x = x.replace(",", " ,")
            else:
                x = x+" ,"
            return x
        return ""

    def info_fill_sec_data(y):
        r1 = 0
        x = ""
        while(r1 < len(sop)):
            r1 = sop.find(y, r1)
            if(r1 != -1):
                r1 = r1+len(y)
                while(sop[r1] != '  ' and r1 < len(sop) and sop[r1] != "."):
                    r1 = r1+1
                    x = x+sop[r1]
                if(sop[r1] == ","):
                    x = x.replace(",", " ,")
                else:
                    x = x+" ,"
                r1 = r1 + 1
            else:
                break
        return x

    def info_fill_date(y):
        r1 = 0
        x = ""
        while(r1 < len(sop)):
            r1 = sop.find(y, r1)
            if(r1 != -1):
                r1 = r1+len(y)
                while(sop[r1] != '  ' and sop[r1] != "," and r1 < len(sop) and sop[r1] != '\n'):
                    r1 = r1+1
                    x = x+sop[r1]
                if(sop[r1] == ","):
                    x = x.replace(",", " ,")
                else:
                    x = x+" ,"
                r1 = r1 + 1
            else:
                break
        return x

    t["accused_name_1"] += info_fill("applicant's name")
    if(t["accused_name_1"] == ""):
        t["accused_name_1"] += info_fill("accused name")
        if(t["accused_name_1"] == ""):
            t["accused_name_1"] += info_fill("name")

    t["address_org"] += info_fill("contact address")
    if(t["address_org"] == ""):
        t["address_org"] += info_fill("address")

    t["police_station_org"] += info_fill("adress (local police station)")
    if(t["police_station_org"] == ""):
        t["police_station_org"] += info_fill("police station address")
        if(t["police_station_org"] == ""):
            t["police_station_org"] += info_fill("police station")

    t["occupation"] += info_fill("job")
    if(t["occupation"] == ""):
        t["occupation"] += info_fill("employment")
        if(t["occupation"] == ""):
            t["occupation"] += info_fill("occupation")

    t["sections"] += info_fill_sec_data("section")

    t["complaint_infromation_father_husband_name"] += info_fill(
        "father's name")
    if(t["complaint_infromation_father_husband_name"] == ""):
        t["complaint_infromation_father_husband_name"] += info_fill("father's")
        if(t["complaint_infromation_father_husband_name"] == ""):
            t["complaint_infromation_father_husband_name"] += info_fill(
                "father")

    t["date"] += info_fill_date("date of the crime")
    if(t["date"] == ""):
        t["date"] += info_fill_date("dated")
        if(t["date"] == ""):
            t["date"] += info_fill_date("date")

    t["age_1_org"] += info_fill_numdata("age")

    t["fir_no"] += info_fill_date("c. c. no.")
    if(t["fir_no"] == ""):
        t["fir_no"] += info_fill_date("fir no.")

    json_object = json.dumps(t, indent=4)
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)


def home(request):
    return render(request, 'home.html')


def normalupload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        url = fs.url(filename)
        new_profile = profile(
            image=url
        )
        new_profile.save()
        t = 'media/'+myfile.name
        solution(t)
        return redirect('/home/')
    else:
        return redirect('/home/')


def downloader(request):
    # print("dtrdgfd")
    # return redirect('/home/')
    filename = 'sample.json'
    #base_dir = os.path.dirname(os.path.dirname(os.path.abspath))
    filepath = os.path.join(
        'C:\\Users\\HP\\Desktop\\prs\\pdfparser\\', filename)
    #filepath = base_dir+filename
    path = open(filepath, 'rb')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
