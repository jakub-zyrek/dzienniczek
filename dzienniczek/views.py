from django.shortcuts import render
import sqlite3



def login(request):
    if "id" in request.session.keys():
        return render(request, "home.html")
    else:
        return render(request, 'login.html')

def changeGrades(x):
    grades = []
    for y in x:
        print(y[0] % int(y[0]))
        if y[0] % int(y[0]) == 0:
            grades.append(int(y[0]))
        elif y[0] % int(y[0]) == 0.5:
            grades.append(str(int(y[0])) + "+")
        elif y[0] % int(y[0]) == 0.75:
            grades.append(str(int(y[0]) + 1) + "-")
        else:
            grades.append(y[0])

    return grades

def students():
    connect = sqlite3.connect("database/database.db")
    cursor = connect.cursor()

    zapytanie = "SELECT id, name, surname FROM users WHERE role = 2"

    result = [[x[0], x[1], x[2]] for x in cursor.execute(zapytanie).fetchall()]

    for i, x in enumerate(result):
        temp = "SELECT grade FROM grades WHERE student = " + str(x[0]) + ""
        grades = changeGrades(cursor.execute(temp).fetchall())
        result[i].append(grades)

    return result

def grades(stu):
    connect = sqlite3.connect("database/database.db")
    cursor = connect.cursor()

    zapytanie = "SELECT name FROM grades WHERE student = " + str(stu)

    names = [x[0] for x in cursor.execute(zapytanie).fetchall()]

    temp = "SELECT grade FROM grades WHERE student = " + str(stu)
    grades = changeGrades(cursor.execute(temp).fetchall())

    return [[names[i], grades[i]] for i in range(len(grades))]

def home(request):
    connect = sqlite3.connect("database/database.db")
    cursor = connect.cursor()

    if "grade" in request.POST.keys() and "addGradeId" in request.session.keys():
        grade = request.POST['grade']
        name = request.POST['name']
        studentId = request.session['addGradeId']
        teacherId = request.session['id']

        zapytanie = "INSERT INTO grades (grade, name, student, teacher) VALUES (" + grade + ", '" + name + "', " + studentId + ", " + str(teacherId) + ")"
        cursor.execute(zapytanie)
        connect.commit()

    if "id" in request.session.keys():
        if request.session["role"] == 1:
            return render(request, "home.html", {
                "name": request.session["name"],
                "surname": request.session["surname"],
                "role": request.session["role"],
                "students": students()
            })
        elif request.session["role"] == 2:
            return render(request, "home.html", {
                "name": request.session["name"],
                "surname": request.session["surname"],
                "role": request.session["role"],
                "grades": grades(request.session["id"])
            })
    elif "login" in request.POST.keys():
        login = request.POST["login"]
        password = request.POST["password"]

        zapytanie = "SELECT id, name, surname, role FROM users WHERE login = '" + login + "' AND password = '" + password + "'"
        data = cursor.execute(zapytanie).fetchall()

        if len(data) == 0:
            return render(request, "login.html", { "error": True })
        else:
            request.session["id"] = data[0][0]
            request.session["name"] = data[0][1]
            request.session["surname"] = data[0][2]
            request.session["role"] = data[0][3]

            if request.session["role"] == 1:
                return render(request, "home.html", {
                    "name": request.session["name"],
                    "surname": request.session["surname"],
                    "role": request.session["role"],
                    "students": students()
                })
            elif request.session["role"] == 2:
                return render(request, "home.html", {
                    "name": request.session["name"],
                    "surname": request.session["surname"],
                    "role": request.session["role"],
                    "grades": grades(request.session["id"])
                })

    return render(request, "login.html")

def logout(request):
    request.session.clear()
    return render(request, "login.html")


def addgrade(request):
    if "id" in request.GET.keys():
        request.session["addGradeId"] = request.GET["id"]
        return render(request, "addgrade.html")
    else:
        return render(request, "home.html")