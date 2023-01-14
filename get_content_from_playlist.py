import json, sys

from bs4 import BeautifulSoup

user_response = input("Would you like to get links via LINK or LOCAL html? [LINK/LOCAL]: ")

link = ''

if user_response.strip().lower() == "link":
    import urllib3
    http = urllib3.PoolManager()
    r = http.request('GET', link, preload_content=False).data.decode('utf-8')

    base = "https://www.youtube.com/watch?v="

    js_variable = "var ytInitialData"

    soup = BeautifulSoup(r, features="html.parser")
    js_vars = soup.find_all('script')

    js_var = [js_var for js_var in js_vars if js_variable in js_var.text][0]

    javascript_as_dict = json.loads(js_var.text.replace(f"{js_variable} = ", "")[:-1])

    playlist_links = []

    common_part = javascript_as_dict['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer'] \
        ['content']['sectionListRenderer']['contents'][0]["itemSectionRenderer"]['contents'][0][
        "playlistVideoListRenderer"]

    playlist_id = common_part['playlistId']

    x = common_part['contents']

    for playlist_info in x:
        try:
            video_id = playlist_info['playlistVideoRenderer']['videoId']
            video_index = playlist_info['playlistVideoRenderer']['index']['simpleText']
            playlist_links.append(f"{base}{video_id}&list={playlist_id}&index={video_index}")
        except KeyError:
            pass

    print(playlist_links)

elif user_response.strip().lower() == "local":
    # if YouTube playlist has more than 100 clips, they won't be loaded, use local version
    import os
    html_file = os.path.join("input_html_playlist",
                             [file for file in os.listdir("input_html_playlist") if file.endswith(".html")][0])

    with open(html_file, "rb") as reader:
        r = reader.read().decode('utf-8')

    for line in r.split("\n"):
        split_me = "<a id=\"video-title\" class=\"yt-simple-endpoint style-scope ytd-playlist-video-renderer\" href=\""
        if split_me in line:
            print(line.split(split_me)[1].split("\" title")[0])

else:
    print("Abort")
    sys.exit(0)
