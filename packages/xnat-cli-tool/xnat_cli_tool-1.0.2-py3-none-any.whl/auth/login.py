import json 
import sys
import os 
from xnat import connect

def login(args):
    if not args.username or not args.secret:
        print("Please provide username and secret")
        sys.exit(1)
        
    username = args.username
    secret = args.secret

    config_file = os.path.expanduser('~/.config/xnat_cli/config.json')
    config_data = {'server': '10.230.12.52'}  

    os.makedirs(os.path.dirname(config_file), exist_ok=True)

    try:
        with open(config_file, 'r') as file:
            existing_data = json.load(file)
            config_data.update(existing_data)
    except FileNotFoundError:
        print("Config file not found. A new one will be created with default values.")
    except json.JSONDecodeError:
        print("Warning: Config file is corrupt. It will be overwritten.")

    server = config_data['server']

    try:
        with connect(server, username, secret) as session:
            try:
                config_data.update({'username': username, 'secret': secret, "valid": True})

                with open(config_file, 'w') as file:
                    json.dump(config_data, file, indent=4)

                print(f"Logged in successfully with username: {username}")
            except Exception as e:
                print(f"Error saving credentials to config file: {e}")
                sys.exit(1)
    except Exception as e:
        print(f"Failed to login. Please check your username or secret. Error: {e}")
        sys.exit(1)
