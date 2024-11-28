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
        if (y[0]+1) % (int(y[0])+1) == 0:
            grades.append(int(y[0]))
        elif (y[0]+1) % int(y[0]+1) == 0.5:
            grades.append(str(int(y[0])) + "+")
        elif (y[0]+1) % int(y[0]+1) == 0.75:
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

        if grade[-1] == "+":
            grade = int(grade[0]) + 0.5
        elif grade[-1] == "-":
            grade = int(grade[0]) - 0.25


        name = request.POST['name']
        studentId = request.session['addGradeId']
        teacherId = request.session['id']

        zapytanie = "INSERT INTO grades (grade, name, student, teacher) VALUES (" + str(grade) + ", '" + name + "', " + studentId + ", " + str(teacherId) + ");"
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
        elif request.session["role"] == 0:
            return adminPanel(request)
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
            elif request.session["role"] == 0:
                return adminPanel(request)

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

def adminPanel(request):
    connect = sqlite3.connect("database/database.db")
    cursor = connect.cursor()

    zapytanie = "SELECT classes.id, classes.name, users.name, users.surname, (SELECT COUNT(*) FROM students_class WHERE class_id = classes.id) FROM classes JOIN users ON classes.teacher_id = users.id"
    classes = cursor.execute(zapytanie).fetchall()

    return render(request, "adminPanel.html", {
        "name": request.session["name"],
        "surname": request.session["surname"],
        "role": request.session["role"],
        "classes": classes
    })

def addclass(request):
    connect = sqlite3.connect("database/database.db")
    cursor = connect.cursor()

    if "name" in request.POST.keys():
        name = request.POST["name"]
        teacher = request.POST["teacher"]

        zapytanie = "INSERT INTO classes (name, teacher_id) VALUES (?, ?)"
        cursor.execute(zapytanie, [name, teacher])
        connect.commit()

        return render(request, "addclass.html", {"added": True})
    else:
        zapytanie = "SELECT id, name, surname FROM users WHERE role = 1"
        teachers = cursor.execute(zapytanie).fetchall()

        return render(request, "addclass.html", {"teachers": teachers})


def editclass(request):
    if "id" in request.GET.keys():
        connect = sqlite3.connect("database/database.db")
        cursor = connect.cursor()

        if "name" in request.POST.keys():
            name = request.POST["name"]
            teacher = request.POST["teacher"]

            zapytanie = "UPDATE classes SET name = ?, teacher_id = ? WHERE id = ?"
            cursor.execute(zapytanie, [name, teacher, request.GET["id"]])
            connect.commit()

            return render(request, "editClass.html", {"id": request.GET["id"], "added": True})

        zapytanie = "SELECT id, name, surname FROM users WHERE role = 1"
        teachers = cursor.execute(zapytanie).fetchall()

        teachers

        zapytanie = "SELECT name, teacher_id FROM classes WHERE id = ?"
        result = cursor.execute(zapytanie, [request.GET["id"]]).fetchall()[0]

        return render(request, "editClass.html", {"id": request.GET["id"], "teachers": teachers, "name": result[0], "selectedTeacher": result[1]})

    return render(request, "editClass.html", {"added": True})