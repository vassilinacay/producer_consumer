import threading
import time
import random

# share buffer/queue
buffer = []
BUFFER_SIZE = 6

# locks and condition to simulate the synchronization
buffer_lock = threading.Lock()
not_full = threading.Condition(buffer_lock)
not_empty = threading.Condition(buffer_lock)

# producer thread function
def restaurant():
	global buffer
	# this range produce 10 items
	for _ in range(10):
		# simulate random production time
		time.sleep(2)

		with not_full:
			while len(buffer) == BUFFER_SIZE:
				print("Serving bunch of orders. Wait for a few minutes...")
				# wait while the buffer is full
				not_full.wait()

			# List of food/products
			food_list = ["Pizza", "Burger", "Sushi", "Pasta", "Salad"]
			# Select a random item from the list
			item = random.choice(food_list)
			buffer.append(item)
			print("Order Placed:", item)
			print("Serving:", item)

			# notify the delivery_team that the buffer is not empty
			not_empty.notify()

# consumer thread function
def delivery_team():
	global buffer

	for _ in range(10):
		with not_empty:
			while len(buffer) == 0:
				print("\nWaiting for order...")
				# wait while the buffer is empty 
				not_empty.wait()

			# remove the order from the buffer and deliver it
			item = buffer.pop(0)
			print("Order delivered:", item)

			# notify the restaurant that the buffer is not empty
			not_full.notify()

# create and start the producer and consumer threads
producer_thread = threading.Thread(target=restaurant)
consumer_thread = threading.Thread(target=delivery_team)

producer_thread.start()
consumer_thread.start()

# wait for the threads to finish
producer_thread.join()
consumer_thread.join()
