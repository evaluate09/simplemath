import os, time, random 
os.system("") #Allows ANSI escape codes to work
"""~Variables - Box~"""
arrayrows = [] #Array that will contain the white space in the box
boxcolumns = 117 #Box length
boxrows = 26 #Box width

for i in range(boxcolumns): #Creates the white space in the box 
    arrayrows.append(" ")
arrayrows = "".join(arrayrows)
boxlinerows = arrayrows.replace(" ", "━") #The white space is replaced with "-" to form the bottom and top of the box

"""~Function - Cursor Positioning~"""
def cursorPosition(row=1,column=1): #Allows for cursor manipulation, the default cursor position is top left corner of the terminal x=1, y=1
    return(f"\x1B[{row};{column}H") 

def typeWriter(phrase, delay=0): #Creates a typing effect for the text being displayed
    for char in phrase:
        print(f"{char}", end="", flush=True) 
        time.sleep(delay)

"""~Function - Box~"""
def boxMaker(row): #Controls the box display
    if row == "printbox": #Prints the box
        print(f"{cursorPosition()}┏{boxlinerows}┓")
        for i in range(boxrows):
            print(f"┃{arrayrows}┃")
        print(f"┗{boxlinerows}┛{cursorPosition()}")
    elif row == "lineclear": #Clears the line that the cursor is on 
            print(f"\r\x1B[2K┃{arrayrows}┃{cursorPosition()}") 
    elif row =="boxclear": #Clears the display and reprints the box
        print(f"{cursorPosition()}\x1B[J")   
        boxMaker("printbox")

"""Function - Code Convenience"""
def validCheck(introMsg, passConditions, errorMsg): #Prints a prompt question (e.g. Which difficulty would you like to select?), checks if the user's input fulfills the pass conditions and prints an error message if the user's input is incorrect 
    while True:
        typeWriter(introMsg, 0.001) 
        placeholderInput = input(f"{cursorPosition(15,45)}Type here: ") 
        placeholderInput = placeholderInput.lower() 
        placeholderInput = placeholderInput.replace(" ", "")
        for i in range(len(passConditions)):
            if placeholderInput == passConditions[i]:
                boxMaker("boxclear")
                return placeholderInput 
        boxMaker("boxclear")
        print(errorMsg)


"""~Functions - Math Questions"""
def numGenerator(difficulty1, difficulty2, mindifficulty = 0): #Generates tworandom numbers, n1 and n2 (n1 is greater than n2) between a specified range
    while True:
        n1, n2 = (random.randint(mindifficulty, difficulty1), random.randint(mindifficulty, difficulty2))
        if n2 > n1: 
            continue
        else:
            return n1, n2   

def questionGenerator(mode, difficulty): #Takes in the user's choice for mode and difficulty, asks a subsequent maths question based on this and finally returns the actual answer to the question and the user's answer
    if isinstance(mode, str): 
        modeConvert = ["addition", "subtraction", "multiplication", "division"] #Converts the chosen mode to the numbers 0, 1, 2 or 3, if the parameter is a string
        mode = modeConvert.index(mode)
    difficultyConvert = {"easy" : 10, "medium" : 100, "hard" : 1000} 
    difficulty,secondDifficulty = difficultyConvert.get(difficulty),10 #Converts the chosen difficulty to a suitable number for the number generator range

    numstore = numGenerator(difficulty, difficulty)
    if mode == 0: #addition
        total = str(numstore[0] + numstore[1])
        typeWriter(f"{cursorPosition(13,49)}What is {numstore[0]} + {numstore[1]}?", 0.02)
        answer = input(f"{cursorPosition(15,50)}Type here: ")
        answer = answer.replace(" ", "")
        cursorPosition(15)
        boxMaker("lineclear")
    elif mode == 1: #subtraction
        total = str(numstore[0] - numstore[1])
        typeWriter(f"{cursorPosition(13,49)}What is {numstore[0]} - {numstore[1]}?", 0.02)
        answer = input(f"{cursorPosition(15,50)}Type here: ")
        answer = answer.replace(" ", "")
        cursorPosition(15)
        boxMaker("lineclear")
    elif mode == 2: #multiplication
        if difficulty == 100 or difficulty == 1000: #If the difficulty is medium or hard
            difficulty = 10
        numstore = numGenerator(difficulty, difficulty)
        total = str(numstore[0] * numstore[1])
        typeWriter(f"{cursorPosition(13,49)}What is {numstore[0]} x {numstore[1]}?", 0.02)
        answer = input(f"{cursorPosition(15,50)}Type here: ")
        answer = answer.replace(" ", "")
        cursorPosition(15)
        boxMaker("lineclear")
    elif mode == 3: #division
        if difficulty == 1000: #If the division difficulty is hard 
            difficulty = 100
        if difficulty == 100: #If the division difficulty is medium
            secondDifficulty = 10  #Set the cap of the second number to be 10
        numstore = numGenerator(difficulty, secondDifficulty, 1) 
        while numstore[0] % numstore[1] != 0: #Ensures the division question being asked results in a whole number
            numstore = numGenerator(difficulty, secondDifficulty, 1)
        total = str(int(numstore[0] / numstore[1]))
        typeWriter(f"{cursorPosition(13,49)}What is {numstore[0]} ÷ {numstore[1]}?", 0.02) 
        answer = input(f"{cursorPosition(15,50)}Type here: ")
        answer = answer.replace(" ", "")
        cursorPosition(15)
        boxMaker("lineclear")
    return total, answer

def typeGenerator(typeQ, difficulty, mode = 0): #Takes in the user's choice of question type (practice/infinite), difficulty and mode (applicable for practice mode only)
    global score,strike #The user's score, the strikes is the count for how many questions the user got wrong
    if typeQ == "practice":
        for i in range(10): #Generates 10 questions
            storeReturn = questionGenerator(mode, difficulty)
            if str(storeReturn[0]) == str(storeReturn[1]): #If the user's answer is correct
                boxMaker("boxclear")
                score += 1
                print(f"{cursorPosition(17,41)}Correct! Your score is {score}.", end = "")
            else: #If the user's answer is incorrect
                boxMaker("boxclear")
                print(f"{cursorPosition(17,40)}Incorrect! Your score is {score}.", end = "")
    elif typeQ == "infinite":
        while strike != 3:
            randMode = random.randint(0, 3) #Randomly generates either 0, 1, 2 or 3 which corresponds with the mode 
            storeReturn = questionGenerator(randMode, difficulty)
            if str(storeReturn[0]) == str(storeReturn[1]):
                boxMaker("boxclear")
                score += 1
                print(f"{cursorPosition(17,41)}Correct! Your score is {score}.", end = "")
            else:
                boxMaker("boxclear")
                strike += 1
                print(f"{cursorPosition(17,40)}Incorrect! Your score is {score}.", end = "")

"""~Sequence - Opening Animation~"""
boxMaker("printbox") #Creates the box
typeWriter(f"{cursorPosition(13,52)}Welcome to...", 0.1)
time.sleep(1)
boxMaker("lineclear")
#This print sequence creates an animation for the text "MATH.PY" 
print(f"{cursorPosition(10,27)}███╗   ███╗ █████╗ ████████╗██╗  ██╗       ██████╗ ██╗   ██╗ ██╗")
time.sleep(0.05)
print(f"{cursorPosition(11,27)}████╗ ████║██╔══██╗╚══██╔══╝██║  ██║       ██╔══██╗╚██╗ ██╔╝ ██║")
time.sleep(0.05)
print(f"{cursorPosition(12,27)}██╔████╔██║███████║   ██║   ███████║       ██████╔╝ ╚████╔╝  ██║")
time.sleep(0.05)
print(f"{cursorPosition(13,27)}██║╚██╔╝██║██╔══██║   ██║   ██╔══██║       ██╔═══╝   ╚██╔╝   ╚═╝ ")
time.sleep(0.05)
print(f"{cursorPosition(14,27)}██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║  ██╗  ██║        ██║    ██╗")
time.sleep(0.05)
print(f"{cursorPosition(15,27)}╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝  ╚═╝  ╚═╝        ╚═╝    ╚═╝") 
time.sleep(1) 
boxMaker("boxclear")
time.sleep(0.5)

"""~Input - Ask User Name~"""
while True: #Asks the user for their name, providing error messages in the case of an invalid input and only breaking out of the while loop when a valid userName is given,
    typeWriter(f"{cursorPosition(13,36)}To start, what is your name? (8 characters max)", 0.02)
    userName = input(f"{cursorPosition(15,45)}Type here: ") 
    if len(userName) > 8: #User has entered a name over 8 characters
        boxMaker("boxclear") #In case the user has overwritten the entire box with a lot of characters
        print(f"{cursorPosition(17,36)}Please enter a name that only has 8 characters.") 
        continue
    elif len(userName) == 0: #User has not entered a name
        boxMaker("boxclear") #Not necessary but keeps it consistent with len(userName) > 8
        print(f"{cursorPosition(17,36)}Please enter a name with at least 1 character.") 
        continue
    else:
        boxMaker("boxclear")
        break

"""Sequence - Welcome Animation"""
typeWriter(f"{cursorPosition(14,50)}Welcome {userName}!", 0.04) 
time.sleep(0.7)
boxMaker("lineclear")
time.sleep(0.3)

"""Input / Gameplay - User Choice Selection / Question Generator & Game End""" #Note: Simplify this code if time permits
def userChoices(): #The main gameplay function, in which the user selects their desired question type (practice/infinite), mode (addition/subtraction/multiplication/division)
    global score,strike 
    while True:
        #userType is the user's choice for infinite/practice mode
        userType = validCheck(f"{cursorPosition(13,30)}Which mode would you like to select? (Practice / Infinite)", ["practice", "infinite"], f"{cursorPosition(17, 34)}Please choose either 'practice' or 'infinite' mode.")
        time.sleep(0.3)
        if userType == "practice":
            #userQuestion is the user's choice for mode (addition/subtraction/multiplication/division)
            userQuestion = validCheck(f"{cursorPosition(13,10)}What type of questions would you like to do? (Addition / Subtraction / Multiplication / Division)", ["addition", "subtraction", "multiplication", "division"], f"{cursorPosition(17,20)}Please choose either 'addition', 'subtraction', 'multiplication, or 'division'.")
        time.sleep(0.3)
        if userType == "infinite" or userQuestion == "addition" or userQuestion == "subtraction": #userchosenQuestion == "addition" or "subtraction" <- NO doesnt raise errors what a
            #Infinite, addition and subtraction mode have the difficulties easy/medium/hard
            userDifficulty = validCheck(f"{cursorPosition(13,27)}What difficulty would you like to choose? (Easy / Medium / Hard)", ["easy", "medium", "hard"], f"{cursorPosition(17,36)}Please choose either 'easy', 'medium, or 'hard'.")
        elif  userQuestion == "division":
            #Division only has the difficulties easy/medium
            userDifficulty = validCheck(f"{cursorPosition(13,31)}What difficulty would you like to choose? (Easy / Medium)", ["easy", "medium"], f"{cursorPosition(17,39)}Please choose either 'easy' or 'medium'.")
        elif userQuestion == "multiplication":
            #Multiplcation can only be on easy difficulty
            userDifficulty = "easy"
        time.sleep(0.3)
        if userType == "practice":
            #userConfirm displays the user's choices and checks if the user is sure of them  
            userConfirm = validCheck(f"{cursorPosition(13,16)}You chose {userType} mode for {userQuestion} on {userDifficulty} difficulty. Is this correct? (Yes / No)", ["yes", "no", "y", "n"], f"{cursorPosition(17,40)}Please answer with either 'yes' or 'no'.")
            if userConfirm == "no" or userConfirm == "n": #If the user is not sure of their choices
                #userRedo asks if they would like to redo their entire choice selection 
                userRedo = validCheck(f"{cursorPosition(13,28)}Would you like to redo your entire choice selection? (Yes / No)", ["yes", "no", "y", "n"], f"{cursorPosition(17,40)}Please answer with either 'yes' or 'no'.")
                if userRedo == "yes" or userRedo == "y": #If user does want to reselect their choices 
                    continue #Then go back to the first question in this while loop
            if userConfirm == "yes" or userConfirm == "y" or userRedo == "no" or userRedo == "n": 
                #If user did not want to redo their choices, or if they were sure of their choices
                score = 0 #Resets the score
                typeGenerator(userType, userDifficulty, userQuestion) #Starts generating the practice questions
                #Practice session end
                boxMaker("boxclear")
                typeWriter(f"{cursorPosition(11,35)}Congratulations {userName}! Your final score was {score}!")  
                score = 0 #Resets the score again (perhaps not necessary, it is more just to 100% make sure the score is reset as i am using global variables for the score)
                break
        elif userType == "infinite": #see above explanations for userConfirm, userRedo and score/strike resetting
            userConfirm = validCheck(f"{cursorPosition(13,26)}You chose {userType} mode on {userDifficulty} difficulty. Is this correct? (Yes / No)", ["yes", "no", "y", "n"], f"{cursorPosition(17,40)}Please answer with either 'yes' or 'no'.")
            if userConfirm == "no" or userConfirm == "n":
                userRedo = validCheck(f"{cursorPosition(13,28)}Would you like to redo your entire choice selection? (Yes / No)", ["yes", "no", "y", "n"], f"{cursorPosition(17,40)}Please answer with either 'yes' or 'no'.")
                if userRedo == "yes" or userRedo == "y":
                    continue
            if userConfirm == "yes" or userConfirm == "y" or userRedo == "no" or userRedo == "n":
                score,strike = 0,0 
                typeGenerator(userType, userDifficulty)
                #Infinite session end
                boxMaker("boxclear")
                typeWriter(f"{cursorPosition(11,8)}Your infinite session has ended as you got 3 question wrong. Your final score was {score}. Nice job, {userName}!")
                score,strike = 0,0
                break
userChoices()
while True: #If the user wishes to play again
    goAgain = validCheck(f"{cursorPosition(13,40)}Would you like to go again (Yes / No)?", ["yes", "no", "y", "n"], f"{cursorPosition(17,40)}Please answer with either 'yes' or 'no'.")
    if goAgain == "yes" or goAgain == "y": 
        boxMaker("boxclear")
        userChoices() #Calls the above function again, going back to asking the user questions etc.
        continue
    else: 
        boxMaker("boxclear")
        typeWriter(f"{cursorPosition(13,34)}Thank you for using MATH.PY! See you next time! <3", 0.04)
        time.sleep(1)
        exit() #Exit the program