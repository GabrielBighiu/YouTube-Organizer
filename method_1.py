import youtube_dl,\
    time,\
    json,\
    os,\
    datetime

ydl_opts = {'outtmpl': r'C:\propriu\temp\01_new_youtube videos\%(title)s.%(ext)s',
            'format': '[height <=? 720]'}

cloud_storage_root = r'C:\Users\g4m3rx\OneDrive\backups_laptop'

class YTdownloader():

    def __init__(self):
        if os.path.isfile(os.path.join(cloud_storage_root, 'watched_vids.json')):
            with open (os.path.join(cloud_storage_root, 'watched_vids.json'), 'r') as json_file_handle:
                self.watched_vids = json.load(json_file_handle)
        else:
            self.watched_vids = {}

        self.links_to_dwnld = []

    def analyze_input_list(self):
        with open('input_list.txt', 'r') as input_list_handle:
            self.all_input_rows = [row.strip() for row in input_list_handle.readlines()]

        for row_id, row_data in enumerate(self.all_input_rows):

            if '?v=' in row_data:
                video_id = row_data.split('?v=')[-1]
            else: # else used in case only IDs are provided for a quick sync-up
                video_id = row_data

            if video_id in self.watched_vids.keys():
                print('ID {} already watched !'.format(video_id))
            else:
                print('{} added to watched IDs'.format(video_id))
                self.watched_vids[video_id] = {'download_time': str(datetime.datetime.now())}
                self.links_to_dwnld.append(row_data)

    def save_on_disk(self):
        with open(os.path.join(cloud_storage_root, 'watched_vids.json'), 'w') as json_file_handle:
            json.dump(self.watched_vids, json_file_handle, indent=2)

        print('Json saved on the disk.')

    def download_unwatched_vids(self):

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            for video_link in self.links_to_dwnld:
                while True:
                    try:
                        ydl.download([video_link])
                        break
                    except:
                        print('Exception found in {}. Retrying in 10 sec...'.format(video_link))
                        time.sleep(10)

worker = YTdownloader()
worker.analyze_input_list()
worker.download_unwatched_vids()
worker.save_on_disk()