from flask import Flask, render_template, request
import datefinder
from pytz import timezone
from datetime import datetime, timedelta
import spacy
import ast

# Configure application
app = Flask(__name__)
nlp = spacy.load("en_core_web_trf")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

str1 = 'International Admission will host a session on Sunday, June 26 at 8 a.m. Pacific Time'


def convert_datetime_timezone(dt, tz1, tz2):
    tz2 = timezone(tz2)
    tz1 = timezone(tz1)

    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime("%Y/%m/%d %I:%M:%S")

    return dt


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("search.html")
    else:
        if request.form.get('action1') == 'VALUE1':
            usertext = request.form.get("usertext").lower().strip()
            doc = nlp(usertext)
            output = datefinder.find_dates(usertext)
            output = list(output)
            for i in output:
                print(i.strftime("%Y/%m/%d %I:%M:%S"))

            if output:
                print("works")
                fromtime = output[0]
                totime = fromtime + timedelta(hours=1, minutes=0)
            else:
                fromtime = datetime.now()
                totime = datetime.now() + timedelta(hours=1, minutes=0)
                print("not yet")
            if len(output) == 2:
                totime = output[1]

            totime = totime.strftime("%Y-%m-%dT%H:%M")
            fromtime = fromtime.strftime("%Y-%m-%dT%H:%M")

            list1 = [[], []]

            for token in doc:
                list1[0].append((token.text, token.pos_))

            ents = []
            allday = ''
            address = ''
            for ent in doc.ents:
                ents.append((ent, ent.label_))
                if ent.label_ == "TIME" or ent.label_ == "DATE":
                    list1[1].append(ent.text)
                if ent.label_ == "EVENT":
                    print("checked")
                    allday = "checked"
                if ent.label_ == "LOC" or ent.label_ == "FAC" or ent.label_ == "GPE":
                    address += ent.text + " "

            for ii in range(len(list1[1])):
                for j in list1[1][ii].split():
                    list1[1].append(j)

            useful = []

            for i in list1[0]:
                if (i[1] == "NOUN" or i[1] == "VERB") and i[0] not in list1[1]:
                    useful.append(i[0])

            eventname = ''
            for i in useful:
                eventname += i + " "
            if "birthday" in usertext or "anniversary" in usertext:
                allday = "checked"
                print("checked")
            return render_template("main.html", eventname=eventname, totime=fromtime, fromtime=totime, address=address,
                                   description=usertext, allday=allday)
        elif request.form.get('action2') == 'VALUE2':
            eventname = request.form.get("eventname").strip().replace("%20", " ")
            fromtime = datetime.strptime(request.form.get("fromdaytime"), "%Y-%m-%dT%H:%M")
            totime = datetime.strptime(request.form.get("todaytime"), "%Y-%m-%dT%H:%M")
            address = request.form.get("inputaddress").strip().replace("%20", " ")
            description = request.form.get("inputdescription").strip().replace("%20", " ")

            g_cal = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={eventname}&dates={fromtime.strftime('%Y%m%dT%H%M')}/{totime.strftime('%Y%m%dT%H%M')}&details={description}&location={address}"
            yahoo = f"https://calendar.yahoo.com/?v=60&TITLE={eventname}&ST={fromtime.strftime('%Y%m%dT%H%M')}&ET={totime.strftime('%Y%m%dT%H%M')}&DESC={description}&in_loc={address}"
            o360 = f"https://outlook.office.com/calendar/0/deeplink/compose?path=/calendar/action/compose&rru=addevent&startdt={fromtime.strftime('%Y-%m-%dT%H:%M:%S')}&enddt={totime.strftime('%Y-%m-%dT%H:%M:%S')}&subject={eventname}&body={description}&location={address}"
            outlook = f"https://outlook.live.com/calendar/0/deeplink/compose?path=/calendar/action/compose&rru=addevent&startdt={fromtime.strftime('%Y-%m-%dT%H:%M:%S')}&enddt={totime.strftime('%Y-%m-%dT%H:%M:%S')}&subject={eventname}&body={description}&location={address}"

            list1 = [eventname, fromtime.strftime("%Y-%m-%dT%H:%M"), totime.strftime("%Y-%m-%dT%H:%M"), address, description]
            print(list1)
            with open("myevent.ics", 'w') as ics:
                ics.write(f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
DTSTAMP:{fromtime.strftime('%Y%m%dT%H%M%SZ')}
DTSTART:{fromtime.strftime('%Y%m%dT%H%M%SZ')}
DTEND:{totime.strftime('%Y%m%dT%H%M%SZ')}
SUMMARY:{eventname}
DESCRIPTION:{description}
LOCATION:{address}
END:VEVENT
END:VCALENDAR""")
                ics.close()
            return render_template("final.html", g=g_cal, y=yahoo, ol=outlook, o360=o360, list1=list1)
        elif request.form.get('action3')[0:6] == 'VALUE3':
            list1 = ast.literal_eval(request.form.get('action3')[6:])
            print(list1)
            return render_template("main.html", eventname=list1[0], totime=list1[1], fromtime=list1[2], address=list1[3], description=list1[4])
        else:
            return render_template("search.html")

