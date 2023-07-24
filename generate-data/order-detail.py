import csv
from faker import Faker
import random

# create a Faker instance
fake = Faker()

# define the number of rows to generate
num_rows = 100000

# generate fake data for the order_detail table
order_detail_data = []
for i in range(1, num_rows+1):
    order_id = random.randint(1, 100)
    product_id = random.randint(1, 100)
    quantity = random.randint(1, 10)
    price = round(random.uniform(10000, 100000), 2)
    order_detail_data.append((i, order_id, product_id, quantity, price))

# write the order_detail data to a CSV file
with open('data/order_detail.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'order_id', 'product_id', 'quantity', 'price'])
    writer.writerows(order_detail_data)