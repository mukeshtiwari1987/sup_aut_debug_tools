import sys
import os
import threading
from queue import Queue
import requests
from setup import AUTH


class DownloadThread(threading.Thread):
    def __init__(self, queue):
        super(DownloadThread, self).__init__()
        self.queue = queue
        self.daemon = True

    def run(self):
        while True:
            url = self.queue.get()
            try:
                self.vid_status_fetcher(url)
            except Exception as e:
                print("Error: {}".format(e))
            self.queue.task_done()

    def vid_status_fetcher(self, url):
        # change it to a different way if you require
        vid_status_list = []

        with requests.get(url, stream=True, timeout=5) as video_url_response_data:
            if video_url_response_data.headers['Content-Type'] == 'application/octet-stream; charset=utf-8':
                vid_status_list.append("Yes")
            else:
                vid_status_list.append("No")
        print(vid_status_list)

        return vid_status_list


def vid_status_thread(urls, numthreads=10):
    queue = Queue()
    for url in urls:
        queue.put(url)

    for i in range(numthreads):
        t = DownloadThread(queue)
        t.start()

    queue.join()


if __name__ == "__main__":
    vid_status_thread(sys.argv[1:], "/Users/mukeshtiwari/Desktop/tmp")
