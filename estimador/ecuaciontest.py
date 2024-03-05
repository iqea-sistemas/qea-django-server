import numpy as np


# x = np.array([6,15.3,19,24.9,33,40.2,75,90,105.9])
# y = np.array([1084.36,2331.91,3633.61,3477.73,3952.69,6261.74,10431.47,25520.66,18531.06])

x = np.array([10,30 ,55,90, 500])
y = np.array([19455.58,21578.87,30056.43,43082.64, 250000])



newX1 = 200
# newX2 = 100
# newX3 = 105.9
# newX4 = 115

coef = np.polyfit(x,y,2)

p1 = np.polyval(coef, newX1)
# p2 = np.polyval(coef, newX2)
# p3 = np.polyval(coef, newX3)
# p4 = np.polyval(coef, newX4)


print(f'para flujo de {newX1} el costo seria de {p1} ')
# print(f'para flujo de {newX2} el costo seria de {p2} ')
# print(f'para flujo de {newX3} el costo seria de {p3} ')
# print(f'para flujo de {newX4} el costo seria de {p4} ')
