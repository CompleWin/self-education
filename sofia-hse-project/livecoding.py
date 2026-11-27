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


def trade(budget, shares, price, record):
    fee = 50
    print(f"Комиссия за одну покупку или продажу: {fee} руб.")
    start_value = shares * price + budget

    for move in range(1, 11):
        print(f"Ход {move}/10. Цена: {price} руб. Деньги: {budget} руб. Акции: {shares}")
        action = ask_number("1) Купить 2) Продать 3) Ждать 4) Уйти", 1, 4)

        if action == 4:
            break

        if budget <= 0:
            break

        if action == 1:
            limit = (budget - fee) // price
            if limit >= 1:
                count = ask_number(f"Сколько купить (1-{limit})? ", 1, limit)
                cost = count * price + fee
                budget -= cost
                shares += count
                record["потрачено"] += cost
            else:
                print("На покупку с комиссией не хватает денег.")

        if action == 2:
            if shares > 0:
                count = ask_number(f"Сколько продать (1-{shares})? ", 1, shares)
                income = count * price - fee
                budget += income
                shares -= count
                record["получено"] += income
            else:
                print("У вас нет акций для продажи.")

        price = next_price(price)
        print(f"Новая цена: {price} руб.")

    end_value = shares * price + budget
    record["биржа"] = end_value - start_value
    return budget, shares, price


def next_price(price):
    if price <= 100:
        return 150
    return price + random.choice([-50, 50])


def bills(family):
    expenses = {
        "Транспорт": 150 * family,
        "Связь": 50 * family,
        "Коммунальные услуги": 300,
        "Wi-Fi": 800
    }

    details = ", ".join(f"{name}: {cost}" for name, cost in expenses.items())
    print(details, "руб.")
    return sum(expenses.values())


def save_report(history, days_lived, budget, shares, price):
    market_total = 0
    file_name = "investor_report.txt"
    with open(file_name, "w") as file:
        file.write(f"Горе-инвестор. {reason}\n")
        file.write(f"Прожито полных дней: {days_lived}\n")
        for record in history:
            market_total += record["биржа"]
            file.write(f"День {record['день']}. Получено: {record["получено"]} руб, "
                       f"потрачено: {record["потрачено"]}, результат биржи: {record['биржа']}\n")
        file.write(f"Общий результат на бирже: {market_total} руб.\n")
        file.write(f"Остаток денег: {budget} руб. Акций: {shares} по {price} руб.\n")
    print(f"Отчёт записан в {file_name}")

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
shares = 0
price = 300

history = []

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
        visit = ask_number("Вечер. 1) На биржу 2) Пропустить: ", 1, 2)
        if visit == 1:
           budget, shares, price = trade(budget, shares, price, record)

    # Обязательные траты
    if budget > 0:
        cost = bills(family)
        budget -= cost
        record["потрачено"] += cost

    history.append(record)

    print(f"Осталось денег: {budget} руб. Акций: {shares}")

    if budget <= 0:
        reason = "Банкротство"
    else:
        days_lived += 1
        answer = ask_number("1) Следующий день 2) Закончить игру: ", 1, 2)
        if answer == 2:
            reason = "Выход игрока"
            break

print(f'\nИгра окончена. Причина: {reason}. Прожито игровых дней: {days_lived}')
save_report(history, days_lived, budget, shares, price)