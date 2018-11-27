import sys
from time import sleep

import json
import os

import argparse
import datetime
from subprocess import Popen, PIPE, DEVNULL


ACCEPTABLE_ERROR = 2
MACS_CONNECTED = set()

def colorful_print(msg, color):
    print(color + msg + Colors.END)


def arg_parse():
    parser = argparse.ArgumentParser(description='Server')
    parser.add_argument('-rr', '--refresh_rate', help='Refresh rate in seconds to check modules score', type=int, default=30)
    parser.add_argument('-d', '--display', help='Display video', action='store_true')

    return parser.parse_args()


def get_file_name(origin):
    options = ['detection', 'wifi']
    if origin not in options:
        raise ValueError('Invalid origin value.')
    file_name = datetime.datetime.now().strftime('%d-%m-%Y') + '_' + origin + '.txt'
    file_path = os.path.abspath(os.path.dirname(sys.argv[0])) + '/'
    if origin == 'detection':
        file_name = 'movidius/YoloV2NCS/' + file_name
    return file_path + file_name


def get_detection_score():
    try:
        file_name = get_file_name('detection')
        with open(file_name, 'r') as f:
            score = int(f.readline())
        return score
    except ValueError:
        return -1
    except FileNotFoundError:
        return -2


def get_wifi_score():
    global MACS_CONNECTED
    wifi_score_command = ['sudo', '/usr/bin/ndsctl', 'json']
    score_process = Popen(wifi_score_command, stdout=PIPE)
    stdout = score_process.communicate(timeout=30)
    response = json.loads(stdout[0].decode('utf-8'))
    score_connected = response['client_length']

    if score_connected > 0:
        score = 0
        for client in response['clients']:
            if response['clients'][client]['state'] == 'Authenticated':
                score += 1
                MACS_CONNECTED.add(client)

    file_name = get_file_name('wifi')
    read_macs = set()
    try:
        with open(file_name, 'r') as f:
            score_read = -1
            index = 0
            for line in f.readlines():
                if index == 0:
                    score_read = int(line)
                else:
                    read_macs.add(line.strip())
                index += 1
    except FileNotFoundError:
        pass

    mac_totals = MACS_CONNECTED.union(read_macs)
    score_connected = len(mac_totals)
    with open(file_name, 'w') as f:
        content = '{}'.format(score_connected)
        for mac in mac_totals:
            content += '\n{}'.format(mac)
        f.write(content)

    return score_connected


def main(args):
    detection_commands = ['python3', 'movidius/YoloV2NCS/detectionExample/Main.py', '--graph', 'movidius/YoloV2NCS/graph']
    wifi_commands = ['sudo', '/usr/bin/ndsctl', 'json']

    if args.display:
        detection_commands.append('--display')

    detection_process = Popen(detection_commands, stdout=DEVNULL)

    try:
        while True:
            detector_score = get_detection_score()
            # wifi_score = get_wifi_score()
            msg = '[{}]: '.format(datetime.datetime.now().strftime('%H:%M:%S'))

            difference = detector_score - wifi_score

            if difference == 0:
                msg += 'SUCCESS - {} people counted.'.format(detector_score)
                color = Colors.GREEN

            elif difference > 0 and difference < ACCEPTABLE_ERROR:
                msg += 'WARNING - Detector = {} | Wifi = {}.'.format(detector_score, wifi_score)
                color = Colors.WARNING
            else:
                msg += 'ERROR - Detector = {} | Wifi = {}.'.format(detector_score, wifi_score)
                color = Colors.FAIL

            colorful_print(msg, color)
            sleep(args.refresh_rate)

    except KeyboardInterrupt:
        detection_process.kill()


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if __name__ == '__main__':
    arguments = arg_parse()
    main(arguments)
