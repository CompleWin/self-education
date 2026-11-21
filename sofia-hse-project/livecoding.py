import random

def ask_number(text, low, high):
    while True:
        try:
            number = int(input(text))
        except:
            print("Введите целое число.")
            continue

        if low <= number <= high:
            return number
        else:
            print(f"Введите число от {low} до {high}")


def morning():
    event = random.choice(list(events))
    print(event, events[event], 'руб.')
    return events[event]


def lunch(family, day, skipped_days):
    cost = 1000 * family

    if len(skipped_days) == 3:
        print("Семья уже три дня голодает, поэтому сегодня покупаем продукты")
    else:
        print(f"Продукты стоят: {cost} руб.")
        answer = ask_number("1) Купить 2) Пропустить: ", 1, 2)
        if answer == 2:
            skipped_days.append(day)
            return 0

    skipped_days.clear()
    return cost



events = {
    "Нашли деньги в куртке.": 500,
    "Сбила машина.": 5000,
    "Заболел простудой.": -1500,
    "Нестерпимо захотелось кофе.": -300,
    "Вернули долг.": 1000
}

family = ask_number("Введите количество членов семьи: ", 3, 7)
start_budget = 10_000 * family
print(f'Количество членов семьи: {family}, бюджет семьи: {start_budget}')

budget = start_budget
days_lived = 0
skipped_days = []
print("Если в бюджете останется ноль рублей или меньше, игра закончится.")

while budget > 0:

    day = days_lived + 1
    print(f"\nДень: {day}. Бюджет: {budget} руб.")

    record = {"день": day, "получено": 0, "потрачено": 0, "биржа": 0}

    # Утро
    change = morning()
    budget += change
    if change > 0:
        record["получено"] += change
    else:
        record["потрачено"] -= change

    # Обед
    if budget > 0:
        cost = lunch(family, day, skipped_days)
        budget -= cost
        record["потрачено"] += cost

    # Вечер (биржа)
    if budget > 0:
        # Игра на бирже
        pass


    print(f"Осталось денег: {budget} руб.")

    if budget <= 0:
        reason = "Банкротство"
    else:
        days_lived += 1
        answer = ask_number("1) Следующий день 2) Закончить игру: ", 1, 2)
        if answer == 2:
            reason = "Выход игрока"
            break

print(f'\nИгра окончена. Причина: {reason}. Прожито игровых дней: {days_lived}')