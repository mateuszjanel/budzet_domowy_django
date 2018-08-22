from mainapp.models import Currency
from django.core.exceptions import ObjectDoesNotExist
import json
def run():
	with open('dane') as json_file:
		data = json.load(json_file)
	for p in data[0]['rates']:
		try:
			currency = Currency.objects.get(id=p['code'])
			currency.rate = p['mid']
			currency.save()
		except ObjectDoesNotExist:
			tmp = Currency(id = p['code'], rate = p['mid'])
			tmp.save()
	print('Crone did his job')
