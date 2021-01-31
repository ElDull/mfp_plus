import click
import os
import importlib
from getpass import getpass, getuser
passman = importlib.import_module("main")
HOME = '/home/'+getuser()
@click.command()
@click.option('-a', '--all',is_flag=True, help = "Display all services")
@click.option('-s', '--service', help = "Get credentials for service")
@click.option('-n', '--new',is_flag=True, help = "Create new service")
def main(all, service, new):
    master_password = getpass("Enter master password: ")
    key = passman.make_key(master_password)

    home_scan = [i.name for i in os.scandir(HOME) if i.is_file()]

    if ".passman_master" not in home_scan:
        passman.store_key(key)
        main()
    if ".passman" not in home_scan:
        with open(f'{HOME}/.passman', 'w') as f:
            f.write('{}')
    if passman.validate_key(key):
        if (all):
            d = passman.fetch_dict()
            for k,v in d.items():
                decrypt_creds(d,key,k)
        elif (new):
            d = passman.fetch_dict()
            service_name = input("Input service name: ")
            username = input("Input username or email: ")
            password = getpass()
            creds = (username, password)
            d.update(passman.encrypt_creds(key, creds, service_name))
            passman.update_json(d)
        elif (service != None):
            d = passman.fetch_dict()
            try:
                print(passman.decrypt_creds(d, key, service))
            except:
                raise Exception("Service doesn't exist")

def get_for_service(service_name, master_password):
    key = passman.make_key(master_password)
    if passman.validate_key(key):
        d = passman.fetch_dict()
        return passman.decrypt_creds(d,key,service_name)
    else:
        raise Exception("Wrong Password!")

if __name__ == "__main__":
    main()