import csv
from faker import Faker
import random

# create a Faker instance
fake = Faker()

# define the number of rows to generate
num_rows = 100

# generate fake data for the orders table
inventories = []
for i in range(1, num_rows+1):
    quantity = random.randint(1, 10)
    created_at = fake.date_this_century()
    inventories.append((i, quantity, created_at))

# write the orders data to a CSV file
with open('data/inventories.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'quantity', 'created_at'])
    writer.writerows(inventories)