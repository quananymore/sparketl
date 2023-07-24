import csv
from faker import Faker
import random

# create a Faker instance
fake = Faker()

# define the number of rows to generate
num_rows = 100

# generate fake data for the order_detail table
user_details = []
for i in range(1, num_rows+1):
    user_id = random.randint(1, 100)
    address = fake.address()
    city = fake.city()
    postcode = fake.postcode()
    country = fake.country()
    user_details.append((i, user_id, address, city, postcode,country))

# write the order_detail data to a CSV file
with open('data/user_details.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'user_id', 'address', 'city', 'postcode','country'])
    writer.writerows(user_details)