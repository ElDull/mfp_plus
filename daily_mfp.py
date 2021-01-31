import importlib
import json
import schedule
from getpass import getuser, getpass
from datetime import date
import time
mfp = importlib.import_module('scrape_mfp')
HOME = '/home/'+getuser()
master_password = getpass()
status = mfp.login(master_password)
if status == "":
    print("login successful")
def job(t):
    today = date.today()
    d = {today.strftime("%d-%m-%Y"):mfp.get_all()}
    with open(f'{HOME}/db.json','w' ) as db:
        json.dump(d,db)
    print(t)
    return
schedule.every().day.at("21:45").do(job, "it is 01:00")

while True:
    schedule.run_pending()
    time.sleep(60)