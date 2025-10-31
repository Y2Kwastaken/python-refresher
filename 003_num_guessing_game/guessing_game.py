import random

def game_loop(expected: int, guesses: int) -> None:
    while True:
        if guesses == 0:
            print("You lose the number was {}".format(expected))
            break
        usr_in: str = input("Enter a guess between (or exit): ")
        if usr_in == "exit":
            exit()
        elif usr_in.isdigit():
            guess: int = int(usr_in)
            guesses -= 1
            if guess < expected:
                print("higher")
            elif guess > expected:
                print("lower")
            else:
                print("You Win!")
                break
        

if __name__ == '__main__':
    while (True):
        print("Num Guessing Game")
        min_str: str = input("minimum number (or exit): ")
        if min_str == "exit":
            exit()
        max_str: str = input("maximum number (or exit): ")
        if max_str == "exit":
            exit()

        if not min_str.isdigit() or not max_str.isdigit():
            print("Invalid Number Input got {}, {}".format(min_str, max_str))
            exit()
        
        min: int = int(min_str)
        max: int = int(max_str)
        temp: int = 0
        
        if max < min:
            temp = max
            max = min
            min = temp
        if max == min:
            max += 1
            
        expected: int = random.randrange(min, max)
        game_loop(expected, 10)