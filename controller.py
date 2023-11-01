from flask import Flask, render_template, request
from utils import create_question_object, create_score_object, get_field

app = Flask(__name__, template_folder="templates")

ADMIN_EMAIL = "admin@host.local"
ADMIN_PASSWORD = "12789"

email_list = []
password_list = []
wholeCredentials = []
email = ""
password = ""
name = ""
authentic = ""


@app.route("/quiz", methods=["POST", "GET"])
def quiz():
    qno = 0
    quiz = []
    questions = []

    questions_file = open("questions.txt", "r")
    questions = questions_file.read().splitlines()
    questions_file.close()

    for question in questions:
        qno += 1
        question_object = create_question_object(question, qno)
        quiz.append(question_object)

    qno = 0
    return render_template("quiz.html", array=quiz)


@app.route("/index")
def home():

    global email
    global password
    global authentic

    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
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
    user = (
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

    users_data_file = open("users_data.txt", "a")
    print(user, file=users_data_file, sep="\n")
    users_data_file.close()

    return render_template("index.html")


@app.route("/onlogin", methods=["POST", "GET"])
def user_verify():

    global email
    global password
    global wholeCredentials
    global authentic
    email = request.form.get("email")
    password = str(request.form.get("password"))

    if verify(email, password):
        return render_template("user.html", var=authentic)

    elif email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        return render_template("admin.html")
    return render_template("invalid.html")


def verify(email, password):

    global authentic
    email_list = []
    password_list = []
    users = []

    users_data_file = open("users_data.txt", "r")
    users = users_data_file.read().splitlines()
    users_data_file.close()

    for idx in range(0, len(users)):
        email_list.append(get_field(users[idx], 1))
        password_list.append(get_field(users[idx], 2))


    for idx in range(0, len(email_list)):
        if email == email_list[idx] and password == password_list[idx]:
            authentic = get_field(users[idx], 0)
            return True
    return False


@app.route("/showall", methods=["POST", "GET"])
def show_all():

    scores_list = []
    users = []

    user_data_file = open("users_data.txt", "r")
    users = user_data_file.read().splitlines()
    user_data_file.close()

    for user in users:
        user_score = create_score_object(user)
        scores_list.append(user_score)

    return render_template("showall.html", list=scores_list)


@app.route("/addquestion", methods=["POST", "GET"])
def add_question():
    question_string = request.form.get("question")
    option_1 = request.form.get("op1")
    option_2 = request.form.get("op2")
    option_3 = request.form.get("op3")
    option_4 = request.form.get("op4")
    correct_option = request.form.get("corop")

    question = (
        question_string
        + ","
        + option_1
        + ","
        + option_2
        + ","
        + option_3
        + ","
        + option_4
        + ","
        + correct_option
    )
    questions_file = open("questions.txt", "a")
    print(question, file=questions_file, sep="\n")
    questions_file.close()
    return render_template("admin.html")


@app.route("/submit", methods=["POST", "GET"])
def submit_quiz():

    global email
    users = []

    attempts = []
    score = 0
    quiz = []

    questions_file = open("questions.txt", "r")
    questions = questions_file.read().splitlines()
    questions_file.close()
    number = 0

    for question in questions:
        question_object = create_question_object(question, number)
        quiz.append(question_object)

    for idx in range(0, len(quiz)):
        mcq = "mcq" + str(idx + 1)
        attempts.append(request.form.get(mcq))


    for idx in range(0, len(quiz)):
        if quiz[idx].correct == attempts[idx]:
            score += 1

    user_data_file = open("users_data.txt", "r")
    users = user_data_file.read().splitlines()
    user_data_file.close()

    for idx in range(0, len(users)):
        if email == get_field(users[idx], 1):
            users[idx] = (
                str(get_field(users[idx], 0))
                + ","
                + str(get_field(users[idx], 1))
                + ","
                + str(get_field(users[idx], 2))
                + ","
                + str(score)
                + ","
                + str(len(attempts))
                + ","
                + str(len(quiz))
            )

    user_data_file = open("users_data.txt", "w")
    for user in users:
        print(user, file=user_data_file, sep="\n")
    user_data_file.close()

    return render_template("user.html")


@app.route("/login", methods=["POST", "GET"])
def validation():
    return render_template("login.html")


@app.route("/show", methods=["POST", "GET"])
def results():
    global email
    users = []
    attempts = 0

    users_data_file = open("users_data.txt", "r")
    users = users_data_file.read().splitlines()
    users_data_file.close()

    score = 0
    for user in users:
        check = get_field(user, 1)
        if email == check:
            score = str(get_field(user, 3))
            attempts = str(get_field(user, 4))

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
