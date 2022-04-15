from os import listdir, remove
from os.path import isfile, join
from datetime import date, timedelta

limit_date = date.today() - timedelta(days = 7)
path = "../saves/"
files = [f for f in listdir(path) if isfile(join(path, f))]

for file in files:
    splited_name = file.split(' ')[0]

    y, m, d = splited_name.split('-')
    file_date = date(int(y), int(m), int(d))

    if(file_date < limit_date):
        remove(f'{path}{file}')
