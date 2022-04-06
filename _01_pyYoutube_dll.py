from logging import Logger
from os import path
from json import load,\
    dump
from datetime import datetime
from yt_dlp import YoutubeDL
from time import sleep
from random import getrandbits

from _00_config import cloud_storage_root

class YTdownloader():

    ydl_opts: dict
    _log: Logger
    all_input_rows: list

    def __init__(self):
        super(YTdownloader, self).__init__()

    def load_watched_from_disc(self):

        if path.isfile(path.join(cloud_storage_root, 'watched_vids.json')):
            with open (path.join(cloud_storage_root, 'watched_vids.json'), 'r') as json_file_handle:
                self.watched_vids = load(json_file_handle)
        else:
            self.watched_vids = {}


    def analyze_input(self):

        self.load_watched_from_disc()
        self.analyzed_input = {'id_already_watched': [],
                               'id_not_watched': []}

        for row_id, raw_data in enumerate(self.all_input_rows):

            if '?v=' in raw_data:
                video_id = raw_data.split('?v=')[-1]
            else: # else used in case only IDs are provided for a quick sync-up
                video_id = raw_data

            if video_id in self.watched_vids.keys():
                self.analyzed_input['id_already_watched'].append(raw_data)
            else:
                self.analyzed_input['id_not_watched'].append(raw_data)
                self.watched_vids[video_id] = {'download_time': str(datetime.now())}

        self._log.info('Watched_vids:\n{}'.format('\n'.join(self.analyzed_input['id_already_watched'])))
        self._log.info('NOT watched_vids:\n{}'.format('\n'.join(self.analyzed_input['id_not_watched'])))


    def save_on_disk(self):
        with open(path.join(cloud_storage_root, 'watched_vids.json'), 'w') as json_file_handle:
            dump(self.watched_vids, json_file_handle, indent=2)

        self._log.info('Json saved on the disk.')

    def download_unwatched_vids(self,
                                download_path):

        for video_link in self.analyzed_input['id_not_watched']:
            self.ydl_opts['outtmpl'] = path.join(download_path, f"{getrandbits(20)}_%(title)s.%(ext)s")
            with YoutubeDL(self.ydl_opts) as ydl:
                while True:
                    try:
                        ydl.download([video_link])
                        break
                    except:
                        self._log.error('Exception found in {}. Retrying in 10 sec...'.format(video_link))
                        sleep(10)