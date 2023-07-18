import csv
from faker import Faker
import random

# create a Faker instance
fake = Faker()

# define the number of rows to generate
num_rows = 100

# generate fake data for the orders table
orders_data = []
for i in range(1, num_rows+1):
    user_id = random.randint(1, 10)
    total = round(random.uniform(100, 1000), 2)
    payment = random.choice(['credit', 'debit', 'cash'])
    created_at = fake.date_time_between(start_date='-1y', end_date='now')
    orders_data.append((i, user_id, total, payment, created_at))

# write the orders data to a CSV file
with open('data/orders.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'user_id', 'total', 'payment', 'created_at'])
    writer.writerows(orders_data)