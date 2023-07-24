import csv
from faker import Faker

# create a Faker instance
fake = Faker()

# define the number of rows to generate
num_rows = 100

# generate fake data for the order_detail table
users = []
for i in range(1, num_rows+1):
    username = fake.user_name()
    firstname = fake.first_name()
    lastname = fake.last_name()
    email = fake.email()
    created_at = fake.date_time_between(start_date='-1y', end_date='now')
    users.append((i, username, firstname, lastname, email,created_at))

# write the order_detail data to a CSV file
with open('data/users.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'username', 'firstname', 'lastname', 'email','created_at'])
    writer.writerows(users)