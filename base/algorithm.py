from .models import *
def algo():
			post=Post.objects.all()
			for data in  post:
				if data.completed != True:
						factor=data.cash_received/int(data.cash_required)*100
						final = (100-data.age)*0.4+data.category*0.35*100+factor*0.25
						my_formatter="{0:.2f}"
						Final=my_formatter.format(final)
						print("Factor",factor)
						print("Final",Final)
						data.sort_factor = Final
						if data.cash_received >= int(data.cash_required):
						  data.completed = True
						data.save()
				else:
					print("Excluded",data.id)
            