import csv
import sys
import datetime
import logging
import json
import requests
from parallel_download import download
from setup import UPLOAD_FOLDER, DOWNLOAD_FOLDER, BROWSERSTACK_AUT_SESSION_LOG_URL

LOG_FILENAME = 'debug.log'
format_string = '%(levelname)s: %(asctime)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, filename=LOG_FILENAME, format=format_string)


def file_to_meta_extractor(file):
    with open(UPLOAD_FOLDER + file) as csv_file:
        meta_info_list = list(csv.DictReader(csv_file, delimiter=','))

    return meta_info_list


def session_json_reader(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
        data = data['automation_session']['video_url']

    return data


def vid_status_fetcher(video_url):
    session_dict = dict()

    with requests.get(video_url, stream=True, timeout=5) as video_url_response_data:
        if video_url_response_data.headers['Content-Type'] == 'application/octet-stream; charset=utf-8':
            session_dict['video'] = "Yes"
        else:
            session_dict['video'] = "No"

    return session_dict


def information_merge(meta_info_list):
    session_info_list = []

    for meta in meta_info_list:
        session_json = DOWNLOAD_FOLDER + meta['hashed_id'] + ".json"
        vid_url = session_json_reader(session_json)
        session_dict = vid_status_fetcher(vid_url)

        for key in meta.keys():
            session_dict[key] = meta[key]
        session_info_list.append(session_dict)

    return session_info_list


def vid_parser_main(csv_fn):
    file_type = ".json"
    meta_info_list = file_to_meta_extractor(csv_fn)
    raw_log_urls_list = [BROWSERSTACK_AUT_SESSION_LOG_URL + meta['hashed_id'] + file_type for meta in meta_info_list]
    download(raw_log_urls_list, DOWNLOAD_FOLDER)
    final_result = information_merge(meta_info_list)

    return final_result


if __name__ == '__main__':
    if len(sys.argv) == 2:
        csv_filename = sys.argv[1]
        vid_parser_main(csv_filename)
    else:
        print("Usage: python3 vid_parser.py filename.csv")
