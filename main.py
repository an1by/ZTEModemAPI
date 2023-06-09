import argparse
import json

import modem
import utils

def main():
    parser = argparse.ArgumentParser(description='ZTE MF79U API. (C) Aniby 2023.')
    parser.add_argument('--file', metavar='F', help='Settings file in json format with "ip" and "password" keys.')
    parser.add_argument('--ip', metavar='I', help='IP-address where hosts modem\'s GUI. By default: "192.168.0.1".')
    parser.add_argument('--password', metavar='P', help='Password for modem\'s GUI. By default: "admin"')
    parser.add_argument('--get', metavar='G', help='Data what you need from modem. Format: "attribute1 attribute2 &etc..."')
    parser.add_argument('--debug', action=argparse.BooleanOptionalAction, help='Debug feature.')
    args = parser.parse_args()

    if (not args.get) or (len(args.get.split(' ')) <= 0):
        utils.debug('Except data for get', "error", True)
        return
    dataToGet = args.get.split(' ')

    if args.debug:
        utils.debug_feature = True

    if args.file:
        with open(args.file, "r") as settings_file:
            converted = json.load(settings_file);
            if "ip" in converted:
                modem.ip = converted["ip"]
            if "password" in converted:
                modem.password = converted["password"]
    elif args.password or args.ip:
        if args.password:
            modem.password = args.password
        if args.ip:
            modem.ip = args.ip
    else:
        utils.debug('Except data for authorization', "error", True)
        return
    
    modem.auth(True)
    if "sms_list" in dataToGet:
        utils.debug(modem.getSMSList(), force=True)
        dataToGet.remove("sms_list")
    if "main_info" in dataToGet:
        utils.debug(modem.getInfo(), force=True)
        dataToGet.remove("main_info")
    utils.debug(modem.getSomething(dataToGet), force=True)

if __name__ == '__main__':
    main()