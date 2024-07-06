# #работа в экселе
# import pandas as pd
# import matplotlib.pyplot as plt
#
# df = pd.read_excel('Книга1.xlsx')
# df['Плошадь участка'] = df['Ширина Участка'] * df['Длина участка']
# df['Стоимость'] = df['Плошадь участка']*10
# print(df)
# plt.plot(df['№ участка'], df['Стоимость'], marker = 'o')
# plt.xlabel('Участки в патрушево')
# plt.ylabel('Показатель')
# plt.title('График недвижимости')
# plt.bar(df['№ участка'], df['Плошадь участка'], color = 'red', alpha = 0.5)
# plt.show()