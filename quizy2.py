import requests
import html

#Przechowuje pytanie 
class Question:
    def __init__(self, category, questionStr, correctAnswerFlag):
        self.category = category
        self.questionStr = questionStr
        self.correctAnswerFlag = correctAnswerFlag


class Quiz:
    def __init__(self, numQuestions):
        self.apiUrl = "https://opentdb.com/api.php?amount=10&difficulty=easy&type=boolean"
        self.numQuestions = numQuestions 
        self.questionsList = []
        self.loadQuestions(numQuestions)
        # Wysyła zapytanie do strony jesli ok to Odbiera dane JSON 
    def loadQuestions(self, numQuestions):
        response = requests.get(f"{self.apiUrl}&amount={numQuestions}")
        if response.ok:
            data = response.json()
            results = data["results"] 

            for q in results:
                if q["type"] != "boolean":
                    continue  # pomijamy pytania typu 'multiple'
                category = q["category"]
                questionStr = html.unescape(q["question"])    #usuwa znaczki takie jak np &quot
                correctAnswerFlag = q["correct_answer"].lower() in ['true', '1', 'yes']  #wybiera co jest poprawna odpowedzią 
                qObj = Question(category, questionStr, correctAnswerFlag)
                self.questionsList.append(qObj)

    def startQuiz(self):
        print("\nWelcome to the Quiz!")
        numCorrectUserAnswers = 0
        numQuestions = len(self.questionsList)

        for n, q in enumerate(self.questionsList, start=1):
            print(f"\nQuestion number {n}: {q.questionStr}")
            
            answer = input("Give correct answer as y/n: ").lower().strip()
            while answer not in ['y', 'n']:
                answer = input("Please enter only 'y' or 'n': ").lower().strip()

            answerBool = answer == 'y' #Zamienia y/n na True/False

            if answerBool == q.correctAnswerFlag:
                print("Correct!")
                numCorrectUserAnswers += 1
            else:
                print("Not correct!")

        print("\nQuiz finished!")
        print(f"Number of correct answers: {numCorrectUserAnswers} out of {numQuestions}")


# Uruchomienie quizu od razu z 10 pytań
quiz = Quiz(10)
quiz.startQuiz()
