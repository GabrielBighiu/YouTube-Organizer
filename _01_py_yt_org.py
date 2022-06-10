from logging import Logger
from os import path
from json import load, \
    dump
from datetime import datetime
from yt_dlp import YoutubeDL
from logging import getLogger
from random import getrandbits
from _00_config import cloud_storage_root, \
    download_formats_prio
from traceback import format_exc


class YTdownloader():
    _log: Logger
    all_input_rows: list

    def __init__(self):
        super(YTdownloader, self).__init__()

    def load_watched_from_disc(self):

        if path.isfile(path.join(cloud_storage_root, 'watched_vids.json')):
            with open(path.join(cloud_storage_root, 'watched_vids.json'), 'r') as json_file_handle:
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
            else:  # else used in case only IDs are provided for a quick sync-up
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

    def download_format(self,
                        video_link,
                        format,
                        download_path,
                        rand_bites):
        try:
            with YoutubeDL({'outtmpl': path.join(download_path, f"{rand_bites}_%(title)s.%(ext)s"),
                            'format': str(format),
                            'logger': getLogger()}) as ydl:
                ydl.download([video_link])
                return True
        except:
            self._log.error(
                f"Found exception while downloading {video_link}, format {format}\n{format_exc(chain=False)}")
            return False

    def download_unwatched_vids(self,
                                download_path):

        download_success = []
        for video_link in self.analyzed_input['id_not_watched']:
            rand_bites = getrandbits(20)
            downloaded = False
            for format_descriptor in download_formats_prio:
                if isinstance(format_descriptor, int):
                    self._log.info(f"Downloading {video_link} with format {format_descriptor}")
                    if self.download_format(video_link=video_link,
                                            format=format_descriptor,
                                            download_path=download_path,
                                            rand_bites=rand_bites):
                        downloaded = True
                        download_success.append(video_link)
                        break
                else:
                    success = 0
                    video_part_processed = False
                    for format_group in format_descriptor:

                        """
                        if the video part has been processed but could not be downloaded,
                        do not attempt to download the video part
                        """

                        if video_part_processed and success == 0:
                            break

                        for group_option in format_group:
                            self._log.info(f"Downloading {video_link} with format {group_option}")
                            if self.download_format(video_link=video_link,
                                                    format=group_option,
                                                    download_path=download_path,
                                                    rand_bites=rand_bites):
                                success += 1
                                download_success.append(video_link)
                                break
                        video_part_processed = True
                    if success == 2:
                        downloaded = True
                        break
            if not downloaded:
                self._log.error(f"Failed to download {video_link}")
                return download_success

        return 'success'
