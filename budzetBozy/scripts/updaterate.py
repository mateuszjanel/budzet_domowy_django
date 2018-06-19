from mainapp.models import Currency

def run():
	currency = Currency.objects.all()
	with open('dane') as json_file:
	data = json.load(json_file)
	for p in data['rates']:
		print('Rates: ' + p['code'])
