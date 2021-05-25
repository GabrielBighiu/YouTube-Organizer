import youtube_dl,\
    time

download_list = ['']

ydl_opts = {'outtmpl': r'C:\propriu\temp\01_new_youtube videos\%(title)s.%(ext)s',
            'format': '[height <=? 720]'}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    for video_link in download_list:
        while True:
            try:
                ydl.download([video_link])
                break
            except:
                print('Exception found in {}. Retrying in 10 sec...'.format(video_link))
                time.sleep(10)