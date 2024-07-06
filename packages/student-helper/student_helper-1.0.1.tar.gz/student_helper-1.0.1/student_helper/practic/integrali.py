# пример нахождения область между кривой и осью

# import matplotlib.pyplot as plt
# import numpy as np
# import sympy as sy  # библиотека для вычисления интегралов
#
#
# def f(x):
# 	return x**2
#
# x = sy.Symbol("x")
# print(sy.integrate(f(x), (x, 0, 2)))

# пример 2 с графиком
# import matplotlib.pyplot as plt
# import numpy as np
#
#
# def f(x):
# 	return x**2
#
# x = np.linspace(0, 2, 1000)
# plt.plot(x, f(x))
# plt.axhline(color="black")
# plt.fill_between(x, f(x), where=[(x > 0) and (x < 2) for x in x])
# plt.show()

# пример из лабы

# import matplotlib.pyplot as plt
# import numpy as np
# import math
#
# x = np.linspace(1, 3, 100)
# y = np.log(x + 3) / x
#
#
# plt.plot(x, y)
# plt.xlabel('x')
# plt.ylabel('f(x)')
# plt.title('График подынтегральной функции')
# plt.grid()
# plt.show()
#
#
# def f(x):
#     return math.log(x + 3) / x
#
# def rectangle_rule(a, b, n):
#     h = (b - a) / n
#     integral = 0
#     for i in range(n):
#         x = a + i*h
#         integral += f(x)
#     return integral * h
#
# def trapezoidal_rule(a, b, n):
#     h = (b - a) / n
#     integral = 0
#     for i in range(1, n):
#         x = a + i*h
#         integral += f(x)
#     return h * ((f(a) + f(b))/2 + integral)
#
# integral_rectangle = rectangle_rule(1, 3, 10000)
# integral_trapezoidal = trapezoidal_rule(1, 3, 10000)
#
# print(f"Значение определенного интеграла (метод прямоугольников): {integral_rectangle}")
# print(f"Значение определенного интеграла (метод трапеций): {integral_trapezoidal}")