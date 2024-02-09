import random

def GuessTheNumber():
    random_number = random.randint(1, 20)
    print("Hello! What is your name?")
    username = str(input())
    print("Well, " + username + ", I am thinking of a number between 1 and 20.")
    attempts = 0
    while True:
        usernum = int(input())
        attempts += 1
        if(usernum < random_number):
            print("Your guess is too low. \nTake a guess.")
        elif(usernum > random_number):
            print("Your guess is too high. \nTake a guess.")
        else:
            print(f"Good job, {username}! You guessed my number in {attempts} guesses!")
            break

GuessTheNumber()