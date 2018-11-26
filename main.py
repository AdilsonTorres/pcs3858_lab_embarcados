import sys
from time import sleep

import json
import os

import argparse
import datetime
# from subprocess import Popen, PIPE
import subprocess

ACCEPTABLE_ERROR = 2


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
    file_path = os.path.abspath(os.path.dirname(sys.argv[0])) + '/../'
    return file_path + file_name


def get_detection_score():
    try:
        file_name = get_file_name('detection')
        with open(file_name, 'r') as f:
            score = int(f.readline())
        return score
    except ValueError:
        return 0
    except FileNotFoundError:
        return 0


def get_wifi_score():
    wifi_score_command = []
    # score_process = Popen(wifi_score_command, stdout=PIPE)
    score_process = subprocess.Popen(wifi_score_command)
    stdout = score_process.communicate()
    score = json.loads(stdout[0].decode('utf-8'))['client_length']

    file_name = get_file_name('wifi')

    with open(file_name, 'w') as f:
        f.truncate(0)
        f.write('{}'.format(score))

    return score


def main(args):
    detection_commands = ['python3', 'detectionExample/movidius/YoloV2NCS/Main.py']
    wifi_commands = ['sudo', '/usr/bin/ndsctl', 'json']

    if args.display:
        detection_commands.append('--display')

    # detection_process = Popen(detection_commands)
    # wifi_process = Popen(wifi_commands)
    detection_process = subprocess.Popen(detection_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        while True:
            detector_score = get_detection_score()
            # wifi_score = get_wifi_score()
            msg = '[{}]: '.format(datetime.datetime.now().strftime('%H:%M:%S'))

            color = Colors.GREEN

            # if detector_score == wifi_score:
            #     msg += 'SUCCESS - {} people counted.'.format(detector_score)
            #     color = Colors.GREEN
            #
            # elif detector_score - wifi_score > ACCEPTABLE_ERROR:
            #     msg += 'WARNING - Detector = {} | Wifi = {}.'.format(detector_score, wifi_score)
            #     color = Colors.WARNING
            # else:
            #     msg += 'ERROR - Detector = {} | Wifi = {}.'.format(detector_score, wifi_score)
            #     color = Colors.FAIL

            colorful_print(msg, color)
            sleep(args.refresh_rate)

    except KeyboardInterrupt:
        detection_process.kill()
        # wifi_process.kill()


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
