import numpy as np
import matplotlib.pyplot as plt

counts = 0
numbers = []
number = eval(input("input number\n> "))

while True:
	counts += 1

	if number%2 == 0:
		number = int(number/2)
	else:
		number *= 3
		number += 1

	numbers.append(number)
	print(f"=> {number}")

	if number <= 1:
		break

print(f"total steps taken: {counts}")

ymarks = np.array(numbers)

plt.plot(ymarks)
plt.show()
