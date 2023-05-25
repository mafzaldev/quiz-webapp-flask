class Question:
    question = ""
    option1 = ""
    option2 = ""
    option3 = ""
    option4 = ""
    correct = ""
    qnum = ""


class Score:
    name = ""
    email = ""
    score = ""


def get_field(line, field):
    extractedField = ""
    character = ""
    idx = 0
    commaFound = 0
    while commaFound < field + 1 and idx < len(line):
        character = line[idx]
        if character == ",":
            commaFound += 1
        elif commaFound == field:
            extractedField = extractedField + character
        idx += 1
    return extractedField


def create_question_object(listElement, number):
    questionObject = Question()
    questionObject.question = get_field(listElement, 0)
    questionObject.option1 = get_field(listElement, 1)
    questionObject.option2 = get_field(listElement, 2)
    questionObject.option3 = get_field(listElement, 3)
    questionObject.option4 = get_field(listElement, 4)
    questionObject.correct = get_field(listElement, 5)
    questionObject.qnum = number
    return questionObject


def create_score_object(listElement):
    scoreObject = Score()
    scoreObject.name = get_field(listElement, 0)
    scoreObject.email = get_field(listElement, 1)
    scoreObject.score = get_field(listElement, 3)
    return scoreObject
