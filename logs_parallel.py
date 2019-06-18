import sys
import os
import threading
from queue import Queue
import requests
from setup import AUTH


class DownloadThread(threading.Thread):
    def __init__(self, queue, destfolder):
        super(DownloadThread, self).__init__()
        self.queue = queue
        self.destfolder = destfolder
        self.daemon = True
        # self.file_type = file_type

    def run(self):
        while True:
            url = self.queue.get()
            try:
                self.download_url(url)
            except Exception as e:
                print("Error: {}".format(e))
            self.queue.task_done()

    def download_url(self, url):
        session_id = url.split('/')[-2]
        log_filename_dest = os.path.join(self.destfolder, session_id)

        response = requests.get(url, auth=AUTH)

        with open(log_filename_dest, 'wb') as filename:
            filename.write(response.content)


def download(urls, destfolder, numthreads=10):
    queue = Queue()
    for url in urls:
        queue.put(url)

    for i in range(numthreads):
        t = DownloadThread(queue, destfolder)
        t.start()

    queue.join()


if __name__ == "__main__":
    download(sys.argv[1:], "/Users/mukeshtiwari/Desktop/tmp")
