import multiprocessing
import time
count=0

def task_function():
	global count
	for i in range(int(1e7)):
		count+=1
	print("Done")

first = multiprocessing.Process(target=task_function, args=())
second = multiprocessing.Process(target=task_function, args=())

first.start()
second.start()

first.join()
second.join()

time.sleep(5)
print(count)
