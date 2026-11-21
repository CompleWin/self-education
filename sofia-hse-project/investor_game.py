import random


def ask_number(prompt, low, high):
    while True:
        try:
            number = int(input(prompt))
        except ValueError:
            print("Введите целое число.")
            continue
        if low <= number <= high:
            return number
        print(f"Введите число от {low} до {high}.")


def morning():
    event = random.choice(list(events))
    print(event, events[event], "руб.")
    return events[event]


def lunch(family, day, skipped_days):
    cost = 500 * family
    if len(skipped_days) == 3:
        print("Семья три дня без продуктов. Сегодня покупаем еду.")
    else:
        print(f"Продукты стоят {cost} руб.")
        answer = ask_number("1) Купить  2) Пропустить: ", 1, 2)
        if answer == 2:
            skipped_days.append(day)
            return 0
    skipped_days.clear()
    return cost


def bills(family):
    expenses = {
        "Транспорт": 150 * family,
        "связь": 50 * family,
        "коммунальные услуги": 300,
    }
    details = ", ".join(f"{name}: {cost}" for name, cost in expenses.items())
    print(f"{details} руб.")
    return sum(expenses.values())


def next_price(price):
    if price == 100:
        return 150
    return price + random.choice([-50, 50])


def trade(budget, shares, price, record):
    fee = 50
    print(f"Комиссия за одну покупку или продажу: {fee} руб.")
    start_value = budget + shares * price
    for move in range(1, 11):
        print(f"Ход {move}/10. Цена: {price} руб. Деньги: {budget} руб. Акций: {shares}.")
        action = ask_number("1) Купить  2) Продать  3) Ждать  4) Уйти: ", 1, 4)
        if action == 4:
            break
        if action == 1:
            limit = (budget - fee) // price
            if limit >= 1:
                count = ask_number(f"Сколько купить (1–{limit})? ", 1, limit)
                cost = count * price + fee
                budget -= cost
                shares += count
                record["потрачено"] += cost
            else:
                print("На покупку с комиссией не хватает денег.")
        elif action == 2:
            if shares > 0:
                count = ask_number(f"Сколько продать (1–{shares})? ", 1, shares)
                income = count * price - fee
                budget += income
                shares -= count
                record["получено"] += income
            else:
                print("У семьи нет акций для продажи.")

        if budget <= 0:
            break
        price = next_price(price)
        print(f"Новая цена: {price} руб.")

    end_value = budget + shares * price
    record["биржа"] = end_value - start_value
    return budget, shares, price


def save_report(history, days_lived, reason, budget, shares, price):
    market_total = 0
    with open("investor_report.txt", "w", encoding="utf-8") as file:
        file.write(f"Горе-инвестор. {reason}\n")
        file.write(f"Прожито полных дней: {days_lived}\n")
        for record in history:
            market_total += record["биржа"]
            file.write(f"День {record['день']}. Получено: {record['получено']} руб., "
                       f"потрачено: {record['потрачено']} руб., "
                       f"результат биржи: {record['биржа']} руб.\n")
        file.write(f"Общий результат на бирже: {market_total} руб.\n")
        file.write(f"Остаток денег: {budget} руб. Акций: {shares} по {price} руб.\n")
    print("Отчёт записан в investor_report.txt.")


events = {
    "Нашли деньги в кармане пальто.": 500,
    "Получили оплату за подработку.": 1800,
    "Пришлось заменить чайник.": -900,
    "Купили лекарства.": -400,
}

family = ask_number("Сколько человек в семье (3–7)? ", 3, 7)
start_budget = 10000 * family
print(f"Бюджет семьи: {start_budget} руб.")

budget = start_budget
shares = 0
price = 500
skipped_days = []
history = []
days_lived = 0
print("Если в бюджете останется ноль рублей или меньше, игра закончится.")

while budget > 0:
    day = days_lived + 1
    print(f"\nДень {day}. Бюджет: {budget} руб.")
    record = {"день": day, "получено": 0, "потрачено": 0, "биржа": 0}

    change = morning()
    budget += change
    if change > 0:
        record["получено"] += change
    else:
        record["потрачено"] += -change

    if budget > 0:
        cost = lunch(family, day, skipped_days)
        budget -= cost
        record["потрачено"] += cost

    if budget > 0:
        visit = ask_number("Вечер. 1) На биржу  2) Пропустить: ", 1, 2)
        if visit == 1:
            budget, shares, price = trade(budget, shares, price, record)

    if budget > 0:
        cost = bills(family)
        budget -= cost
        record["потрачено"] += cost

    history.append(record)

    print(f"\nОсталось денег: {budget} руб. Акций: {shares}.")

    print("=" * 50)

    if budget <= 0:
        reason = "Банкротство"
    else:
        days_lived += 1
        if ask_number("1) Следующий день  2) Закончить игру: ", 1, 2) == 2:
            reason = "Выход игрока"
            break

print(f"Игра окончена. {reason}. Прожито полных дней: {days_lived}.")
save_report(history, days_lived, reason, budget, shares, price)
