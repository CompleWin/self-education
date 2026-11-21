from random import *  # по условию разрешена только библиотека random

# Цены завтрака за одного человека: номер варианта -> цена
breakfast_prices = {'1': 200, '2': 500, '3': 1000}

# Случайные утренние события: текст события -> изменение бюджета
rand_ivents = {
    'Вы нашли в зимней куртке забытые деньги!': 1000,
    'Ваш сын занял первое место на олимпиаде по экономике!': 3000,
    'Бабушка прислала перевод на день рождения!': 2000,
    'Вам нестерпимо захотелось кофе...': -1200,
    'Сломался чайник, пришлось купить новый.': -1500,
    'Вас поймали, когда вы перебегали дорогу на красный свет, и выписали штраф!': -2500,
}

# Обязательные траты в день, которые умножаются на количество человек в семье
per_person_bills = {'Транспорт': 150, 'Мобильная связь и интернет': 50}
# Обязательные траты в день, которые не зависят от количества человек
fixed_bills = {'Wi-Fi': 30, 'Коммунальные услуги': 300}

food_price = 1000   # продукты на день за одного человека
max_skips = 3       # сколько дней подряд можно не покупать продукты
max_moves = 10      # максимум ходов на бирже за вечер
commission = 50     # комиссия биржи за каждую сделку


# ---------- Загрузка игроков из файла ----------

users = dict()  # имя: (кол-во людей в семье, бюджет, сколько дней уже прожито)
try:
    with open('stock_market_trading.txt', 'r', encoding='utf-8') as file:
        for user in file:
            user = user.strip().split(', ')  # убираем '\n' в конце и делим строку по ', '
            if len(user) == 3:  # строка в старом формате, где ещё не было дней
                user.append('0')
            # пропускаем пустые и испорченные строки
            if len(user) == 4 and user[1].isdigit() and user[2].isdigit() and user[3].isdigit():
                users[user[0]] = int(user[1]), int(user[2]), int(user[3])
except FileNotFoundError:
    pass  # файла ещё нет - значит, игроков пока нет. Он создастся в конце игры


# ---------- Функции ----------

def input_number(text, low, high):
    # Спрашивает число, пока пользователь не введёт целое число от low до high
    while True:
        try:
            number = int(input(text))
            if low <= number <= high:
                return number
            else:
                print('Ошибка!', f'Введите число от {low} до {high}.')
        except ValueError:
            print('Ошибка!', 'Необходимо ввести число.')


def registration():
    while True:
        name = input("Приветствую пользователя на нашей бирже! Пожалуйста, представьтесь: ").strip()
        # запятая сломает формат файла "имя, люди, бюджет", поэтому её запрещаем
        if name == '' or ',' in name:
            print('Ошибка!', 'Имя не может быть пустым или содержать запятую.')
        else:
            break
    if name in users:
        print('Рады видеть Вас снова в нашей игре <3', '', sep='\n')
        print(f'Прожито дней: {users[name][2]}. Ваш бюджет: {users[name][1]}р.', '', sep='\n')
        return name, users[name][0], users[name][1], users[name][2]
    else:
        n = input_number("Сколько человек в вашей семье? (от 3 до 7): ", 3, 7)
        print(f'Ваш стартовый капитал: {10000 * n}р.', '', sep='\n')
        return name, n, 10000 * n, 0  # 0 - новый игрок ещё не прожил ни одного дня


def add_money(day_stats, money):
    # Записывает изменение бюджета в статистику дня: плюс - в "Получено", минус - в "Потрачено"
    if money > 0:
        day_stats['Получено'] += money
    else:
        day_stats['Потрачено'] += -money


def morning(n):
    print('--- УТРО ---')
    # с шансом 75% обычное утро, с шансом 25% случайное событие
    morning_type = choices(['завтрак', 'событие'], weights=[75, 25])[0]
    if morning_type == 'завтрак':
        print('Обычное утро! Выберите тип завтрака:', '1)Эконом 200р/ч (Овсянка)',
              '2)Стандарт 500р/ч (Скрембл)', '3)Премиум 1000р/ч (Бенедикт)', sep='\n')
        answer_choice = input_number('Ваш выбор: ', 1, 3)
        price = breakfast_prices[str(answer_choice)] * n  # цена за человека * кол-во людей
        print(f'За утро вы потратили: {price}р.')
        return -price  # трата, поэтому со знаком минус
    else:
        ivent = choice(list(rand_ivents.keys()))  # случайный текст события
        money = rand_ivents[ivent]                 # сколько денег оно даёт/забирает
        if money > 0:
            print('Случайное событие!', f'- {ivent} +{money}р.', sep='\n')
        else:
            print('Случайное событие!', f'- {ivent} {money}р.', sep='\n')
        return money


def lunch(n, food_history):
    print('--- ОБЕД ---')
    cost = food_price * n
    # food_history[-3:] - это последние 3 дня. Если все 3 раза "Сэкономить", экономить больше нельзя
    if food_history[-max_skips:].count('Сэкономить') == max_skips:
        print(f'Семья голодает уже {max_skips} дня подряд! Сегодня придётся закупить продукты.')
        answer = 1
    else:
        print(f'1)Закупить продукты (-{cost}р.)', '2)Сэкономить (семья голодает)', sep='\n')
        answer = input_number('Ваш выбор: ', 1, 2)

    if answer == 1:
        food_history.append('Закупить')
        print(f'Вы закупили продукты на {cost}р.')
        return -cost
    else:
        food_history.append('Сэкономить')
        print('Сегодня семья осталась без продуктов...')
        return 0


def change_price(price):
    # Выбираем, что сегодня происходит на рынке. У каждого варианта свой шанс (в процентах)
    market = choices(['спокойно', 'рост', 'падение', 'обвал', 'взлёт'],
                     weights=[40, 29, 29, 1, 1])[0]
    if market == 'спокойно':
        percent = randint(-5, 5)    # цена почти не меняется
    elif market == 'рост':
        percent = randint(5, 15)    # цена растёт на 5-15%
    elif market == 'падение':
        percent = randint(-15, -5)  # цена падает на 5-15%
    elif market == 'обвал':
        percent = -50
        print('СРОЧНЫЕ НОВОСТИ! Директора компании арестовали за мошенничество. Акции рухнули на 50%!')
    else:
        percent = 50
        print('СРОЧНЫЕ НОВОСТИ! Компания выиграла госконтракт на 10 лет. Акции взлетели на 50%!')

    new_price = price + price * percent // 100
    if new_price < 100:  # чтобы акция не подешевела почти до нуля
        new_price = 100
    return new_price


def stock_market(budget, shares, price):
    print('--- ВЕЧЕР: БИРЖА ---')
    result = 0  # сколько денег пришло (+) или ушло (-) на бирже за этот вечер
    for move in range(1, max_moves + 1):
        print('', f'Ход {move} из {max_moves}',
              f'Цена акции: {price}р. | Ваши акции: {shares} шт. | Бюджет: {budget}р.',
              '1)Купить  2)Продать  3)Ждать  4)Уйти с биржи', sep='\n')
        action = input_number('Ваш выбор: ', 1, 4)

        if action == 1:
            # сколько акций можно купить, чтобы после покупки и комиссии бюджет остался больше 0
            # (поэтому обанкротиться прямо на бирже нельзя)
            max_buy = (budget - commission - 1) // price
            if max_buy <= 0:
                print('Не хватает денег даже на одну акцию!')
            else:
                count = input_number(f'Сколько акций купить? (0-{max_buy}): ', 0, max_buy)
                if count > 0:
                    budget -= count * price + commission
                    result -= count * price + commission
                    shares += count
                    print(f'Куплено {count} шт. за {count * price}р. (комиссия {commission}р.)')
        elif action == 2:
            if shares == 0:
                print('У вас нет акций для продажи!')
            else:
                count = input_number(f'Сколько акций продать? (0-{shares}): ', 0, shares)
                if count > 0:
                    budget += count * price - commission
                    result += count * price - commission
                    shares -= count
                    print(f'Продано {count} шт. за {count * price}р. (комиссия {commission}р.)')
        elif action == 4:
            print('Вы ушли с биржи.')
            break

        old_price = price
        price = change_price(price)  # после каждого хода цена меняется
        print(f'Цена акции изменилась: {old_price}р. -> {price}р.')
        if move == max_moves:
            print('Ходы на сегодня закончились!')

    print(f'Итог биржи за вечер: {result}р.')
    return budget, shares, price, result


def sell_all(shares, price):
    # Продаёт все акции по текущей цене, возвращает полученные деньги
    money = shares * price - commission
    print(f'Все акции ({shares} шт.) проданы по {price}р. Получено: {money}р. (с учётом комиссии)')
    return money


def pay_bills(n):
    print('--- КОНЕЦ ДНЯ: обязательные траты ---')
    total = 0
    for name, price in per_person_bills.items():
        print(f'{name}: {price}р. * {n} = {price * n}р.')
        total += price * n
    for name, price in fixed_bills.items():
        print(f'{name}: {price}р.')
        total += price
    print(f'Итого обязательных трат: {total}р.')
    return -total


def save_statistics(name, all_stats, reason, budget, day):
    total_received = 0
    total_spent = 0
    total_stock = 0
    with open('statistics.txt', 'a', encoding='utf-8') as file:  # 'a' - дописываем в конец файла
        file.write(f'Игрок: {name}\n')
        file.write(f'Причина окончания игры: {reason}\n')
        file.write(f'Прожито дней за эту игру: {len(all_stats)}, всего: {day}\n')
        for day_stats in all_stats:
            file.write(f"День {day_stats['День']}: получено {day_stats['Получено']}р., "
                       f"потрачено {day_stats['Потрачено']}р., биржа {day_stats['Биржа']}р.\n")
            total_received += day_stats['Получено']
            total_spent += day_stats['Потрачено']
            total_stock += day_stats['Биржа']
        file.write(f'Всего получено: {total_received}р., всего потрачено: {total_spent}р.\n')
        file.write(f'Итог на бирже (выигрыш/проигрыш): {total_stock}р.\n')
        file.write(f'Итоговый бюджет: {budget}р.\n')
        file.write('-' * 40 + '\n')
    print('', f'Прожито дней за эту игру: {len(all_stats)}, всего: {day}', f'Итог на бирже: {total_stock}р.',
          f'Итоговый бюджет: {budget}р.', 'Статистика записана в файл statistics.txt', sep='\n')


def save_users(name, n, budget, day):
    if budget > 0:
        users[name] = (n, budget, day)  # сохраняем бюджет и дни, чтобы продолжить в следующий раз
    else:
        users.pop(name, None)  # банкрот - удаляем игрока, в следующий раз он начнёт заново
    with open('stock_market_trading.txt', 'w', encoding='utf-8') as file:
        for user in users:
            file.write(f'{user}, {users[user][0]}, {users[user][1]}, {users[user][2]}\n')


def main():
    name, n, budget, days_lived = registration()
    shares = 0          # сколько акций у игрока
    price = 300        # стартовая цена акции
    food_history = []   # что выбирали на обед каждый день: 'Закупить' или 'Сэкономить'
    all_stats = []      # список словарей со статистикой каждого дня
    day = days_lived + 1  # продолжаем счёт дней с того места, где остановились
    while True:
        print('', f'========== ДЕНЬ {day} ==========', f'Ваш бюджет: {budget}р.', sep='\n')
        day_stats = {'День': day, 'Получено': 0, 'Потрачено': 0, 'Биржа': 0}  # новый словарь на каждый день

        money = morning(n)
        budget += money
        add_money(day_stats, money)
        print(f'Ваш бюджет: {budget}р.', '', sep='\n')

        money = lunch(n, food_history)
        budget += money
        add_money(day_stats, money)
        print(f'Ваш бюджет: {budget}р.', '', sep='\n')

        if budget > 0:
            print('--- ВЕЧЕР ---', 'Вам приходит предложение: "Сыграть на бирже?"', '1)Да', '2)Нет', sep='\n')
            if input_number('Ваш выбор: ', 1, 2) == 1:
                budget, shares, price, result = stock_market(budget, shares, price)
                day_stats['Биржа'] += result
        else:
            print('Денег нет - на биржу сегодня не пускают.')

        money = pay_bills(n)
        budget += money
        add_money(day_stats, money)

        # если денег не осталось, но есть акции - банк продаёт их, чтобы спасти семью
        if budget <= 0 and shares > 0:
            print('Деньги закончились! Банк принудительно продаёт ваши акции.')
            money = sell_all(shares, price)
            budget += money
            day_stats['Биржа'] += money
            shares = 0

        if budget <= 0:
            print('', f'Ваш бюджет: {budget}р.', 'Вы полный банкрот! Игра окончена :(', sep='\n')
            reason = 'Банкротство'
        else:
            print(f'Ваш бюджет на конец дня: {budget}р.', '', '1)Начать новый день', '2)Выйти из игры', sep='\n')
            if input_number('Ваш выбор: ', 1, 2) == 2:
                reason = 'Игрок вышел из игры'
                if shares > 0:  # перед выходом продаём оставшиеся акции
                    money = sell_all(shares, price)
                    budget += money
                    day_stats['Биржа'] += money
                    shares = 0
            else:
                reason = ''  # пустая строка - игра продолжается

        all_stats.append(day_stats)
        if reason != '':
            break

        day += 1
        price = change_price(price)  # за ночь цена акции тоже меняется

    save_statistics(name, all_stats, reason, budget, day)
    save_users(name, n, budget, day)


main()