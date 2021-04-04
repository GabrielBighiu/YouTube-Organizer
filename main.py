from pytube import YouTube
import pprint

links = ['https://www.youtube.com/watch?v=-f9U11pbQQI']

for link in links:

    video = YouTube(link)

    print('The link {} has the following streams:'.format(link))
    pprint.pprint(list(video.streams), indent=2)

    for itag in [22, 45]:
        print('Trying to download itag {}...'.format(itag))
        try:
            video.streams.get_by_itag(22).download()
            print('Downloaded successfully !')
            break
        except:
            print('Failed to downlaod for the current tag. Trying the next one')
