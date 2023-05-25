from flask import Flask, render_template, request
from utils import create_question_object, create_score_object, get_field

app = Flask(__name__, template_folder="templates")

emailList = []
passwordList = []
wholeCredentials = []
email = ""
password = ""
name = ""
authentic = ""


@app.route("/quiz", methods=["POST", "GET"])
def quiz():
    qno = 0
    whole_quiz = []
    questions = []
    myFile = open("questions.txt", "r")
    questions = myFile.read().splitlines()
    myFile.close()

    for element in questions:
        qno += 1
        obj = create_question_object(element, qno)
        whole_quiz.append(obj)

    qno = 0
    return render_template("quiz.html", array=whole_quiz)


@app.route("/index")
def home():

    global email
    global password

    if email == "admin@host.local" and password == "12789":
        return render_template("admin.html")
    elif verify(email, password):
        return render_template("user.html", var=authentic)
    return render_template("index.html")


@app.route("/onsignup", methods=["POST", "GET"])
def submit():

    global email
    global password
    global name

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    complete = (
        str(name)
        + ","
        + str(email)
        + ","
        + str(password)
        + ","
        + "0"
        + ","
        + "0"
        + ","
        + "0"
    )

    myFile = open("user_data.txt", "a")
    print(complete, file=myFile, sep="\n")
    myFile.close()
    return render_template("index.html")


@app.route("/onlogin", methods=["POST", "GET"])
def userVerify():

    global email
    global password
    global wholeCredentials
    global authentic
    email = request.form.get("email")
    password = str(request.form.get("password"))

    myFile = open("user_data.txt", "r")
    wholeCredentials = myFile.read().splitlines()
    myFile.close()

    if verify(email, password):
        return render_template("user.html", var=authentic)

    elif email == "admin@host.local" and password == "12789":
        return render_template("admin.html")
    return render_template("invalid.html")


def verify(email, pw):

    emailList = []
    passwordList = []
    global authentic

    wholeCredentials = []

    myFile = open("user_data.txt", "r")
    wholeCredentials = myFile.read().splitlines()
    myFile.close()

    for idx in range(0, len(wholeCredentials)):
        emailList.append(get_field(wholeCredentials[idx], 1))
        passwordList.append(get_field(wholeCredentials[idx], 2))

    print(len(wholeCredentials))
    print(len(emailList))
    print(len(passwordList))

    for idx in range(0, len(emailList)):
        if email == emailList[idx] and pw == passwordList[idx]:
            authentic = get_field(wholeCredentials[idx], 0)
            print(authentic)
            return True
    return False


@app.route("/showall", methods=["POST", "GET"])
def showll():

    objects_list = []
    whole = []

    myFile = open("user_data.txt", "r")
    whole = myFile.read().splitlines()
    myFile.close()

    for element in whole:
        obj = create_score_object(element)
        objects_list.append(obj)

    return render_template("showall.html", list=objects_list)


@app.route("/addquestion", methods=["POST", "GET"])
def add_question():
    ques = request.form.get("question")
    op1 = request.form.get("op1")
    op2 = request.form.get("op2")
    op3 = request.form.get("op3")
    op4 = request.form.get("op4")
    cor = request.form.get("corop")

    complete = ques + "," + op1 + "," + op2 + "," + op3 + "," + op4 + "," + cor
    myFile = open("questions.txt", "a")
    print(complete, file=myFile, sep="\n")
    myFile.close()
    return render_template("admin.html")


@app.route("/submit", methods=["POST", "GET"])
def submit_quiz():

    global email
    wholeCredentials = []

    attempts = []
    score = 0
    whole_quiz = []

    myFile = open("questions.txt", "r")
    questions = myFile.read().splitlines()
    myFile.close()
    number = 0
    for element in questions:
        obj = create_question_object(element, number)
        whole_quiz.append(obj)

    for idx in range(0, len(whole_quiz)):
        mcq = "mcq" + str(idx + 1)
        attempts.append(request.form.get(mcq))

    for udx in attempts:
        print(udx)

    for idx in range(0, len(whole_quiz)):
        if whole_quiz[idx].correct == attempts[idx]:
            score += 1

    myFile = open("user_data.txt", "r")
    wholeCredentials = myFile.read().splitlines()
    myFile.close()

    for idx in range(0, len(wholeCredentials)):
        if email == get_field(wholeCredentials[idx], 1):
            wholeCredentials[idx] = (
                str(get_field(wholeCredentials[idx], 0))
                + ","
                + str(get_field(wholeCredentials[idx], 1))
                + ","
                + str(get_field(wholeCredentials[idx], 2))
                + ","
                + str(score)
                + ","
                + str(len(attempts))
                + ","
                + str(len(whole_quiz))
            )

    myFile = open("user_data.txt", "w")
    for record in wholeCredentials:
        print(record, file=myFile, sep="\n")
    myFile.close()

    print("Your score is:", score)
    return render_template("user.html")


@app.route("/login", methods=["POST", "GET"])
def validation():
    return render_template("login.html")


@app.route("/show", methods=["POST", "GET"])
def results():
    global email
    wholeCredentials = []
    attempts = 0
    myFile = open("user_data.txt", "r")
    wholeCredentials = myFile.read().splitlines()
    myFile.close()

    score = 0
    print(email)
    for result in wholeCredentials:
        check = get_field(result, 1)
        if email == check:
            score = str(get_field(result, 3))
            attempts = str(get_field(result, 4))

    return render_template("result.html", var1=score, var2=attempts)


@app.route("/register", methods=["POST", "GET"])
def register():
    return render_template("register.html")


@app.route("/quizstrt", methods=["POST", "GET"])
def strt():
    return render_template("quizstrt.html")


@app.route("/contact", methods=["POST", "GET"])
def get_social():
    return render_template("contact.html")


@app.route("/add", methods=["POST", "GET"])
def add():
    return render_template("addques.html")


@app.route("/logout", methods=["POST", "GET"])
def logout():
    global email
    global password
    email = ""
    password = ""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
