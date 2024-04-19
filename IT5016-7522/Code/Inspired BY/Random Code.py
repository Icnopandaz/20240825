# Source: https://thecleverprogrammer.com/2022/06/29/number-guessing-game-using-python/ 

import random # Import Random Number Generator
n = random.randrange(1,100) # Random Range between 1 and 100
guess = int(input("Enter any number: ")) # User inputs a number
while n!= guess: # In a new line show the guessed number
    if guess < n: # If guess is lower than the number then
        print("Too low") # Print "too low"
        guess = int(input("Enter number again: ")) # Asks for another guess
    elif guess > n: # Else, if number is higher than the number then
        print("Too high!") # Print too high
        guess = int(input("Enter number again: ")) # Asks for another guess
    else: # Otherwise, you got it right, break the code/close the app.
      break
print("you guessed it right!!")  # Print "You guessed it right", however due to how the code is written it will close the window before you see this.