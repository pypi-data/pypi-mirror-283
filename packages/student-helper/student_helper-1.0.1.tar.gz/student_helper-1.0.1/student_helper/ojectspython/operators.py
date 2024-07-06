def premer_if():
    """Это пример if - блоки elif и else не являются обязателдьными"""
    x = 10

    if x < 0: #Если x < 10
        print('Меньше нуля')
        result = -1
    elif x == 0: #Если x = 0
        print('Равно нулю')
        result = 0

    else: #Иначе
        print('Больше нуля, но не равно единице')
        if x == 42:
            print('Вау!')
        result = 42
    print('дотвидания!')

    # операторы сравнения
    # >
    # <
    # >=
    # <=
    # ==
    # !=

    # группировка условий
    # or
    # and
    # not


def premer_for():
    zoo_pets = [
        'lion', 'monkey', 'skunk',
        'elephant', 'horse',
    ]
    #Пример 1
    for i in range(10):
        print('Эта фраза появаится 10 раз')


    #Пример 2
    for animal in zoo_pets:
        if animal == 'skunk':
            print('Фууу...')
            continue #Прерывает цикл но не заканчивает (опционально)
        print('Сейчас переменная animal указывает на', animal)
        if animal == 'elephant':
            print('Нашли слона! :)')
            break #Прекратить цикл досрочно (опционально)
        print('Это не слон....')
    else: #Сработает в конце цикла если не было break (опционально)
        print('Тут слона нет...')
    print('Выход из цикла')


def premer_while():
    i = 1
    while i < 10:
        i = i * 2
        print(i)

    #continue vreak и else - работают как в for


def premer_function(param='какой то параметр', param_2='Еще параметр'):
    res = param + param_2 #Эти параметры можем использовать по имени
    return 'Не забывай возвращать результат (и принимать res_2 = premer_function())'

#res_2 = premer_function()



