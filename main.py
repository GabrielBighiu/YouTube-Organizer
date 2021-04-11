from pytube import YouTube
import pprint,\
    sys, \
    os

links = ['']
save_location = r'C:\propriu\temp\01_new_youtube videos\videos'

for link in links:

    video = YouTube(link)

    print('The link {} has the following streams:'.format(link))
    pprint.pprint(list(video.streams), indent=2)

    success = False
    # video & audio
    for itag in [22, 45, 35, 44]:
        print('Trying to download itag {}...'.format(itag))
        try:
            video.streams.get_by_itag(itag).download(save_location)
            print('Downloaded successfully !')
            success = True
            break
        except:
            print('Failed to downlaod for the current tag. Trying the next one')

    if not success:
        print('Cannot download mixed audio & video. Downloading sequentially ...')
        # video only
        for itag in [136, 247, 298, 302, 334, 135, 168, 218, 244, 245, 246, 333]:
            print('Trying to download itag {}...'.format(itag))
            try:
                video.streams.get_by_itag(itag).download(os.path.join(save_location, 'video_only'))
                print('Downloaded successfully !')
                success = True
                break
            except:
                print('Failed to downlaod for the current tag. Trying the next one')

        # audio only
        for itag in [141, 140, 139, 171, 251, 250, 249]:
            print('Trying to download itag {}...'.format(itag))
            try:
                video.streams.get_by_itag(itag).download(os.path.join(save_location, 'audio_only'))
                print('Downloaded successfully !')
                success = True
                break
            except:
                print('Failed to downlaod for the current tag. Trying the next one')


    if not success:
        sys.exit('Failed to download the video !')
