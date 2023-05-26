class Question:
    question = ""
    option1 = ""
    option2 = ""
    option3 = ""
    option4 = ""
    correct = ""
    qnum = ""

    # create a constructor
    def __init__(self, question, option1, option2, option3, option4, correct, qnum):
        self.question = question
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        self.option4 = option4
        self.correct = correct
        self.qnum = qnum


class Score:
    name = ""
    email = ""
    score = ""

    # create a constructor
    def __init__(self, name, email, score):
        self.name = name
        self.email = email
        self.score = score


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
    return Question(
        get_field(listElement, 0),
        get_field(listElement, 1),
        get_field(listElement, 2),
        get_field(listElement, 3),
        get_field(listElement, 4),
        get_field(listElement, 5),
        number,
    )


def create_score_object(listElement):
    return Score(
        get_field(listElement, 0), get_field(listElement, 1), get_field(listElement, 3)
    )
