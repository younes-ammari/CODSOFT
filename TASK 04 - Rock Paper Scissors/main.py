import random


def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'scissors' and computer_choice == 'paper') or \
         (user_choice == 'paper' and computer_choice == 'rock'):
        return "You win!"
    else:
        return "Computer wins!"


def rock_paper_scissors():
    choices = ['rock', 'paper', 'scissors']
    while True:
        print("\nWelcome to Rock-Paper-Scissors!")
        print("Choose your move: rock, paper, or scissors (or type 'quit' to exit)")

        user_choice = input("Your choice: ").lower()
        if user_choice == 'quit':
            print("Thanks for playing!")
            break
        elif user_choice not in choices:
            print("Invalid choice! Please choose rock, paper, or scissors.")
            continue

        computer_choice = random.choice(choices)
        print("Computer's choice:", computer_choice)

        result = determine_winner(user_choice, computer_choice)
        print(result)


if __name__ == "__main__":
    rock_paper_scissors()
