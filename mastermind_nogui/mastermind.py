import random

colors = ['R', 'G', 'B', 'Y', 'W', 'P']
rounds = 10
range_code = 4

def code_generator():
    code = []

    for i in range(range_code):
        color = random.choice(colors)
        code.append(color)

    return code


def guess_code():
    while True:
        guess = input('Guess: ').upper().split(" ")
        
        if len(guess) != range_code:
            print(f'You must guess {range_code} colors.')
            continue

        for color in guess:
            if color not in colors:
                print(f'Invalid color: {color}. Try again.')
        else:
            break
    return guess

def check_code(guess, real_code):
    color_counts = {}
    correct_pos = 0
    incorrect_pos = 0

    for color in real_code:
        if color not in color_counts:
            color_counts[color] = 0
        color_counts[color] += 1
    
    for guess_color, real_color in zip(guess, real_code):
        if guess_color == real_color:
            correct_pos += 1
            color_counts[guess_color] -= 1
    
    for guess_color, real_color in zip(guess, real_code):
        if guess_color in color_counts and color_counts[guess_color] > 0:
            incorrect_pos += 1
            color_counts[guess_color] -= 1
    
    return correct_pos, incorrect_pos

def game():
    print(f'Welcome to mastermind, you have {rounds} tries to guess the code!')
    print(f'The valid colors are: {colors}')


    code = code_generator()
    for r in range(1, rounds + 1):
        guess = guess_code()
        correct_pos, incorrect_pos = check_code(guess, code)
        if correct_pos == range_code:
            print(f'You guess code in {r} tries!')
            break

        print(f"Correct possitions: {correct_pos} \nIncorrect possitions: {incorrect_pos}")

    else:
        print(f'You ran out of tries, the code was: {code}')

game()

