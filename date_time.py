import datetime

data_obj = datetime.datetime.now()

data_str = data_obj.strftime('%d-%m-%Y %H:%M:%S')

print(data_str)
