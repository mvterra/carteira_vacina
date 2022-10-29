import configparser
import json

config_parser = configparser.ConfigParser()
config_path = "configuration"
interface_path = "interface"
config_file_path = f"{config_path}/gui.ini"
config_parser.read(config_file_path)

login_form_path = f"{interface_path}/login_form.ui"
register_form_path = f"{interface_path}/register_form.ui"

user = config_parser["remember_user"]["user"]
remember = config_parser['remember_user']['remember']
