def premer_erroe():
    #Ловим все ошибки
    try:
        i = 0
        print(10 / i)
        print('сделано')
    except:
        # ловим все ошибки
        print('нельзя делить на ноль!')

    # нужно указывать конкретную ошибку что бы поймать только её
    try:
        i = 0
        print(10 / i)
        print('сделано')
    except ZeroDivisionError:  # указываем имя класса
        print('нельзя делить на ноль!')


    #если хотим создать ошибку

    raise RuntimeError('Что то напиши если хочешь')


class NewError(BaseException): #СО0здали кастомную ошибку, что бы вызывать с прикольным именем
    pass