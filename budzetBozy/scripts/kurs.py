import django
import json
from .models import Currency

with open('dane') as data_file:
	data_loaded = json.load(data_file)

print(data_loaded)
