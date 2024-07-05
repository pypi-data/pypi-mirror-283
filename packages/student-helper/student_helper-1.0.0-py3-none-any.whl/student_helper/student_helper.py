def operators():
    #Списки - объекты для хранения
    new_list = [1, 2, 3, 4, 5, 6, 7]
    new_list_2 = list(10)
    print(new_list[0:3], new_list_2[0])
    #list.append(x)	Добавляет элемент в конец списка
    # list.extend(L)	Расширяет список list, добавляя в конец все элементы списка L
    # list.insert(i, x)	Вставляет на i-ый элемент значение x
    # list.remove(x)	Удаляет первый элемент в списке, имеющий значение x. ValueError, если такого элемента не существует
    # list.pop([i])	Удаляет i-ый элемент и возвращает его. Если индекс не указан, удаляется последний элемент
    # list.index(x, [start [, end]])	Возвращает положение первого элемента со значением x (при этом поиск ведется от start до end)
    # list.count(x)	Возвращает количество элементов со значением x
    # list.sort([key=функция])	Сортирует список на основе функции
    # list.reverse()	Разворачивает список
    # list.copy()	Поверхностная копия списка
    # list.clear()	Очищает список

def python_function():
    # --- Приведение
    # типов - --


    int()
    float()
    bool()
    str()
    list()
    tuple()
    dict()
    set()

    int('123')
    int(123.45)
    float('123')
    float('123.45')
    float(123)

    bool(123)
    bool(0)
    bool(123.45)
    bool(0.0)
    bool('123')
    bool('0')
    bool('')
    bool(None)

    str(123)
    str(123.45)
    str(True)

    my_tuple = (1, 2, 3, 3, 2, 1)
    list(my_tuple)
    set(my_tuple)

    dict([('a', 2), ('b', 3), ])

    # --- Числа ---

    # abs() - абсолютное значение числа
    abs(1)
    abs(-1)

    # round() - округление до нужного знака
    round(3.1425926, 2)
    round(3.1425926, 3)
    round(3.1425926, 0)

    # --- Cписки ---

    profit = [100, 20, 5, 1200, 42, ]

    # len() - размер списка
    len(profit)

    # max() - максимальный элемент
    max(profit)

    # min() - минимальный элемент
    min(profit)

    # sorted() - отсортированный список
    sorted(profit)

    # sum() - сумма элементов списка
    sum(profit)

    # zip() - попарная компоновка элементов двух списков
    profit = [100, 20, 5, 1200, 42, ]
    days = ['пн', 'вт', 'ср', 'чт', 'пт', ]
    res = zip(profit, days, )
    print(list(res))

    # --- Логические ---

    # all() - True если ВСЕ элементы списка/множества True
    all([True, True, True, True, ])
    all([1, 0, 1, ])
    all([1, '0', 1, ])

    # any() - True если ХОТЯ БЫ ОДИН элемент списка True
    any([True, False, True, True, ])
    any([1, 0, None, ])

    # --- Интроспекция ---

    # dir() - список всех аттрибутов обьекта
    dir(profit)
    dir([])

    # help() - встроенная помощь по функции/обьекту
    help(profit)
    help(print)

    # id() - внутренний идентификатор обьекта
    a = [1, 2, 3]
    print(id(a))
    b = a
    print(id(b))
    c = [1, 2, 3]
    print(id(c))
    print(a == b, a is b, id(a) == id(b))
    print(a == c, a is c, id(a) == id(c))
    print(id(None))
    print(id(False))
    print(id(True))

    # --- Общего назначения ---

    # hash() - значение хэша для обьекта. Что такое хэш-функции см https://goo.gl/gZLM4o
    hash('Кржижановский')
    hash(profit)

    # isinstance() - является ли обьект обьектом данного класса
    isinstance(profit, list)

    # type() - тип(КЛАСС) обьекта
    type(profit)