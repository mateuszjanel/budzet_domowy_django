from mainapp.models import *
from django.core.exceptions import ObjectDoesNotExist
import datetime
def run():
	standingOrders = StandingOrder.objects.all()
	for order in standingOrders:
		if order.next_date == datetime.date.today():
			trans = Transaction(user = order.user,account = order.account, title = order.title, amount = order.amount, date = datetime.date.today(), currency = order.currency, categories = order.categories)
			trans.save()
			order.next_date = order.next_date + datetime.timedelta(days = order.frequency)
			order.save()
