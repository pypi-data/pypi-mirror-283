def premer_files_1():
    #mode='r' - читать
    #mode='w' - вписать
    #Кодировка
    # encoding='utf-8' - основная
    # encoding='cp1251' - если utf8 выдаст ошибку кодировки

    doc_list  = [] #Список куда сохраняем строки файла
    with open(r'name_file.txt или путь до него', mode='r', encoding='utf-8') as file:
        for line in file:
            doc_list.append(line) #Добавляем строки в список

    #Все после этого работаем с списко, каждый объект в списке - строка из файла


def premer_files_2():
    file = open(r'name_file.txt', mode='w', encoding='utf-8')
    pere = 'Любой объект в формате строки'
    file.write(pere) #Вписали что то в файл
    file.close()