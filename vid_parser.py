import csv
import sys
import logging
import json
from parallel_download import download
from setup import UPLOAD_FOLDER, DOWNLOAD_FOLDER, BROWSERSTACK_AUT_SESSION_LOG_URL
from vid_parallel import vid_parallel_download

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


def vid_status_with_session(meta_info_list):
    video_url_list = []

    for meta in meta_info_list:
        session_json = DOWNLOAD_FOLDER + meta['hashed_id'] + ".json"
        video_url = session_json_reader(session_json)
        video_url_dict = {
            "hashed_id": meta['hashed_id'],
            "video_url": video_url
        }
        video_url_list.append(video_url_dict)

    thread = 10
    video_url_dict_list = vid_parallel_download(thread, video_url_list)

    return video_url_dict_list


def information_merge(meta_info_list):
    session_info_list = []
    video_url_dict_list = vid_status_with_session(meta_info_list)

    for meta in meta_info_list:
        session_dict = dict()

        for key in meta.keys():
            session_dict[key] = meta[key]
        session_info_list.append(session_dict)

    # How to Merge Two Python Dictionaries - https://bit.ly/2MyVM48
    session_info_list = [dict(session_info_list[i], **video_url_dict_list[i]) for i in range(len(session_info_list))]

    return session_info_list


def vid_parser_main(csv_fn):
    file_type = ".json"
    meta_info_list = file_to_meta_extractor(csv_fn)
    session_urls_list = [BROWSERSTACK_AUT_SESSION_LOG_URL + meta['hashed_id'] + file_type for meta in meta_info_list]
    download(session_urls_list, DOWNLOAD_FOLDER)
    final_result = information_merge(meta_info_list)

    return final_result


if __name__ == '__main__':
    if len(sys.argv) == 2:
        csv_filename = sys.argv[1]
        vid_parser_main(csv_filename)
    else:
        print("Usage: python3 vid_parser.py filename.csv")
