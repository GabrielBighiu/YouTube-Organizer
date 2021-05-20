from pytube import YouTube
import pprint,\
    sys, \
    os,\
    subprocess,\
    shutil,\
    time,\
    multiprocessing,\
    traceback

links = ['']
save_location = r'C:\propriu\temp\01_new_youtube videos'

def parse_url(link):

    video = YouTube(link)

    print('The link {} has the following streams:'.format(link))
    pprint.pprint(list(video.streams), indent=2)

    combined_success = False
    separate_success_video = False
    separate_success_audio = False
    # video & audio
    for itag in [22, 45, 35, 44]:
        print('Trying to download itag {}...'.format(itag))
        try:
            video.streams.get_by_itag(itag).download(save_location)
            print('Downloaded successfully !')
            combined_success = True
            break
        except:
            print('Failed to download for the current tag. Trying the next one')

    if not combined_success:
        print('Cannot download mixed audio & video. Downloading sequentially ...')
        # video only
        for itag in [136, 247, 298, 302, 334, 135, 168, 218, 244, 245, 246, 333, 134, 133, 242]:
            print('Trying to download itag {}...'.format(itag))
            try:
                video.streams.get_by_itag(itag).download(os.path.join(save_location, 'video_only'))
                print('Downloaded successfully !')
                separate_success_video = True
                break
            except:
                print('Failed to download for the current tag. Trying the next one')

        # audio only
        for itag in [141, 140, 139, 171, 251, 250, 249]:
            print('Trying to download itag {}...'.format(itag))
            try:
                video.streams.get_by_itag(itag).download(os.path.join(save_location, 'audio_only'))
                print('Downloaded successfully !')
                separate_success_audio = True
                break
            except:
                print('Failed to download for the current tag. Trying the next one')

    if not combined_success and (not separate_success_video or not separate_success_audio):
        sys.exit('Failed to download the video !')

    if separate_success_video and separate_success_audio:
        video_file = os.path.join(save_location, 'video_only', os.listdir(os.path.join(save_location, 'video_only'))[0])
        audio_file = os.path.join(save_location, 'audio_only', os.listdir(os.path.join(save_location, 'audio_only'))[0])
        subprocess.call('ffmpeg.exe -i "{}" -i "{}" -c:v copy -c:a aac "{}"'.format(video_file,
                                                                                  audio_file,
                                                                                  os.path.join(save_location, os.path.basename(video_file))))
        shutil.rmtree(os.path.join(save_location, 'video_only'))
        shutil.rmtree(os.path.join(save_location, 'audio_only'))

def slave_thread(link):

    while True:
        try:
            parse_url(link)
            break
        except:
            print('Exception found. Retrying ...')
            traceback.print_exc()
            time.sleep(5)

if __name__ == '__main__':
    for link in links:
        while True:
            process = multiprocessing.Process(target=slave_thread, args=(link,))
            process.start()
            process.join(timeout=60)
            if process.is_alive():
                process.terminate()
                print('Process force terminated.')
            else:
                print('Process finished by itself.')
                break
