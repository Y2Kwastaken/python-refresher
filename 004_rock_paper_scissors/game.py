import random

OPTIONS = {
    "rock": 0,
    "paper": 1,
    "scissors": 2
}
REVERSED = {
    0: "rock",
    1: "paper",
    2: "scissors"
}

def game_loop():
    cpu_choice: int = random.choice(list(OPTIONS.values())) # pyright: ignore[reportUnknownArgumentType, reportUnknownVariableType, reportArgumentType]
    opt_choice: int | None = None
    while opt_choice == None:
        inp: str = input("rock paper, or scissors (exit): ")
        if inp == "exit":
            exit()
        opt_choice: int | None = OPTIONS[inp]
    human_choice: int = opt_choice
    
    if human_choice == cpu_choice:
        print("Tie!")
    elif (cpu_choice - human_choice) % 3 == 1:
        print("cpu wins, cpu chose {}".format(REVERSED[cpu_choice]))
    else:
        print("player wins, cpu chose {}".format(REVERSED[cpu_choice]))

    
    

if __name__ == '__main__':
    print("Rock Paper Scissors")
    while True:
        game_loop()
    