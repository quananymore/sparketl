import csv
from faker import Faker
from faker_vehicle import VehicleProvider
import random

fake = Faker()
fake.add_provider(VehicleProvider)
# define the number of rows to generate
num_rows = 100

# generate fake data for the order_detail table
products = []
for i in range(1, num_rows+1):
    year = fake.random_int(min=2000, max=2023)
    make = fake.random_element(elements=('Toyota', 'Honda', 'Ford', 'Chevrolet', 'Nissan', 'BMW', 'Mercedes-Benz'))
    model = fake.vehicle_make_model()
    category = fake.random_element(elements=('Sedan', 'SUV', 'Hatchback', 'Sports Car', 'Luxury Car'))
    price = fake.pydecimal(left_digits=6, right_digits=2, positive=True)
    description = fake.text()
    created_at = fake.date_this_century()
    inventory_id = random.randint(1, 100)
    products.append((i,year,make, model, category, price, description, created_at,inventory_id))

# write the order_detail data to a CSV file
with open('../mnt/airflow/dags/files/data/products.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'Year', 'Make', 'Model', 'Category', 'price', 'description','created_at',"inventory_id"])
    writer.writerows(products)