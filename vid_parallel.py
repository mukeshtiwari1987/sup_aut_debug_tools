from multiprocessing import Pool
import requests


def check_url(video_url_list):

    with requests.get(video_url_list["video_url"], stream=True, timeout=5) as video_url_response_data:
            if video_url_response_data.headers['Content-Type'] == 'application/octet-stream; charset=utf-8':
                video_url_dict = {
                    "video": "Yes",
                    "hashed_id": video_url_list["hashed_id"]
                }
            else:
                video_url_dict = {
                    "video": "No",
                    "hashed_id": video_url_list["hashed_id"]
                }

    return video_url_dict


def vid_parallel_download(thread, video_url_list):
    p = Pool(processes=thread)
    result = p.map(check_url, video_url_list)

    return result
