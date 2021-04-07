from pytube import YouTube
import pprint

links = ['']
save_location = r'C:\propriu\temp\01_new_youtube videos\videos'

for link in links:

    video = YouTube(link)

    print('The link {} has the following streams:'.format(link))
    pprint.pprint(list(video.streams), indent=2)

    for itag in [22, 45]:
        print('Trying to download itag {}...'.format(itag))
        try:
            video.streams.get_by_itag(22).download(save_location)
            print('Downloaded successfully !')
            break
        except:
            print('Failed to downlaod for the current tag. Trying the next one')
