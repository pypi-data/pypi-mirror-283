class PremerClassa():

    def __init__(self): #Срабатывает когда создается объект (obj_class = PremerClassa())
        self.color = "Бордовый металлик"
        self.price = "1 000 000 руб"
        self.max_velocity = "200 км/ч"
        self.current_velocity = "0 км/ч"
        self.engine_rpm = 0

    def start(self): #Наш метод - наджо вызывать
        self.engine_rpm = 5000

    def go(self):#Наш метод - наджо вызывать
        self.current_velocity = "20 км/ч"


# my_car = Toyota()
#
# # Объекты имеют свойства, к которым можно доступиться с помощью точки
# print(my_car.color)
# "Бордовый металлик"
# print(my_car.price)
# "1 000 000 руб"
# print(my_car.max_velocity)
# "200 км/ч"
# print(my_car.engine_rpm)
# 0
# print(my_car.current_velocity)
# "0 км/ч"