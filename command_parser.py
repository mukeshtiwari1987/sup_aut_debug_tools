import csv
import os
import sys
import requests
import datetime
import logging

LOG_FILENAME = 'debug.log'
format_string = '%(levelname)s: %(asctime)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, filename=LOG_FILENAME, format=format_string)


UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
BROWSERSTACK_URL = "https://automate.browserstack.com/logs/"
AUTH = (os.environ["BROWSERSTACK_USERNAME"], os.environ["BROWSERSTACK_KEY"])


def file_to_meta_extractor(file):
    with open(UPLOAD_FOLDER + file) as csv_file:
        meta_info_list = list(csv.DictReader(csv_file, delimiter=','))

    return meta_info_list


def session_to_raw_log_downloader(session_id):
    response = requests.get(BROWSERSTACK_URL + session_id, auth=AUTH)
    raw_log_txt = DOWNLOAD_FOLDER + session_id + ".txt"
    with open(raw_log_txt, 'wb') as raw_filename:
        raw_filename.write(response.content)


def raw_log_reader(file_path):
    with open(file_path, "r") as f:
        data = f.readlines()
        data = data[1:]

    return data


def time_stamp_calculator(end_time, begin_time):
    duration = end_time - begin_time

    return duration.total_seconds()


def command_time_group_calculator(end_time, begin_time):

    temp_duration = float(time_stamp_calculator(end_time, begin_time))

    if temp_duration <= 2:
        return "zero_to_two"
    elif 2 < temp_duration <= 5:
        return "two_to_five"
    elif 5 < temp_duration <= 10:
        return "six_to_ten"
    elif 10 < temp_duration <= 15:
        return "ten_to_fifteen"
    else:
        return "more_than_fifteen"


def command_latency_calculator(session_raw_info):
    command_information_list = []
    command_description_list = []
    command_request_time_list = []
    command_response_time_list = []
    session_dict = {}

    for line in session_raw_info:
        words = line.split()
        if "START_SESSION" in words:
            session_start_time = ' '.join(words[0:2])
            start_time_obj = datetime.datetime.strptime(session_start_time, '%Y-%m-%d %H:%M:%S:%f')
            session_dict["session_start_time"] = session_start_time
        elif "STOP_SESSION" in words:
            session_end_time = ' '.join(words[0:2])
            end_time_obj = datetime.datetime.strptime(session_end_time, '%Y-%m-%d %H:%M:%S:%f')
            session_dict["session_end_time"] = session_end_time
            # session_dict["session_duration"] = time_stamp_calculator(end_time_obj, start_time_obj)
        elif "REQUEST" in words:
            request_time = ' '.join(words[0:2])
            request_time_obj = datetime.datetime.strptime(request_time, '%Y-%m-%d %H:%M:%S:%f')
            command_request_time_list.append(request_time_obj)
            command_description_list.append(" ".join(words[5:len(words)]))
        elif "DEBUG" in words:
            request_time = ' '.join(words[0:2])
            request_time_obj = datetime.datetime.strptime(request_time, '%Y-%m-%d %H:%M:%S:%f')
            command_request_time_list.append(request_time_obj)
            command_description_list.append(" ".join(words[5:len(words)]))
        elif "RESPONSE" in words:
            response_time = ' '.join(words[0:2])
            response_time_obj = datetime.datetime.strptime(response_time, '%Y-%m-%d %H:%M:%S:%f')
            command_response_time_list.append(response_time_obj)

    for i in range(len(command_request_time_list)):
        command_dict = {
            "command_description": command_description_list[i],
            "command_request_time": command_request_time_list[i].strftime('%Y-%m-%d %H:%M:%S:%f'),
            "command_response_time": command_response_time_list[i].strftime('%Y-%m-%d %H:%M:%S:%f'),
            "command_duration_seconds": time_stamp_calculator(command_response_time_list[i],
                                                              command_request_time_list[i]
                                                              ),
            "command_time_group": command_time_group_calculator(command_response_time_list[i],
                                                                command_request_time_list[i]
                                                                )
        }
        command_information_list.append(command_dict)

    session_dict["command_information"] = command_information_list

    session_dict["zero_to_two"] = 0
    session_dict["two_to_five"] = 0
    session_dict["six_to_ten"] = 0
    session_dict["ten_to_fifteen"] = 0
    session_dict["more_than_fifteen"] = 0

    for cil in command_information_list:
        for key, value in cil.items():
            if key == "command_time_group" and value == "zero_to_two":
                session_dict["zero_to_two"] += 1
            elif key == "command_time_group" and value == "two_to_five":
                session_dict["two_to_five"] += 1
            elif key == "command_time_group" and value == "six_to_ten":
                session_dict["six_to_ten"] += 1
            elif key == "command_time_group" and value == "ten_to_fifteen":
                session_dict["ten_to_fifteen"] += 1
            elif key == "command_time_group" and value == "more_than_fifteen":
                session_dict["more_than_fifteen"] += 1

    return session_dict


def information_merge(meta_info_list):
    session_info_list = []

    for meta in meta_info_list:
        raw_log_path = DOWNLOAD_FOLDER + meta['hashed_id'] + ".txt"
        session_raw_info = raw_log_reader(raw_log_path)
        session_dict = command_latency_calculator(session_raw_info)
        session_dict["created_day"] = meta['created_day']
        session_dict["user_id"] = meta['user_id']
        session_dict["build_name"] = meta['build_name']
        session_dict["build_id"] = meta['build_id']
        session_dict["session_name"] = meta['session_name']
        session_dict["session_id"] = meta['hashed_id']
        session_dict["session_duration"] = meta['duration']
        session_dict["inside_time"] = meta['inside_time']
        session_dict["outside_time"] = meta['outside_time']
        session_dict["os"] = meta['os']
        session_dict["os_version"] = meta['os_version']
        session_dict["browser"] = meta['browser']
        session_dict["browser_version"] = meta['browser_version']
        session_dict["status"] = meta['status']
        session_info_list.append(session_dict)

    return session_info_list


def command_parser_main(csv_fn):
    meta_info_list = file_to_meta_extractor(csv_fn)

    for meta in meta_info_list:
        session_to_raw_log_downloader(meta['hashed_id'])
    final_result = information_merge(meta_info_list)

    return final_result


if __name__ == '__main__':
    if len(sys.argv) == 2:
        csv_filename = sys.argv[1]
        command_parser_main(csv_filename)
    else:
        print("Usage: python3 command_parser.py filename.csv")
