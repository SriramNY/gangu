import random

print("🏏 Welcome to Python Cricket Game!")
print("You will play 5 overs (30 balls). Score as much as you can!")
print("Type a number between 1 and 6 on each ball. If computer chooses the same number, you're OUT!")

balls = 30
score = 0
ball_num = 1

while ball_num <= balls:
    try:
        player = int(input(f"Ball {ball_num} - Your shot (1 to 6): "))
        if player < 1 or player > 6:
            print("❗ Only numbers between 1 and 6 are allowed!")
            continue
    except ValueError:
        print("❗ Please enter a number.")
        continue

    computer = random.randint(1, 6)
    print(f"Computer bowled: {computer}")

    if player == computer:
        print("💥 Oh no! You're OUT!")
        break
    else:
        score += player
        print(f"🏃 You scored {player} runs. Total: {score}")
        ball_num += 1

print(f"\n🎉 Your final score: {score} runs in {ball_num - 1 if player == computer else balls} balls.")
print("🏆 Thanks for playing! See you next time!")