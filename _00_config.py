# the videos will be downloaded based on the formats priority
# if a format fails then the next attempt will be made with the next fromat descriptor
# a descriptor can be a single format (usually containing audio+video) OR
# a list of lists of formats containing both video and audio options
download_formats_prio = [
    22, # mp4 720p video+audio
    45, # webm 720p video+audio
    35, # flv 480p video+audio
    44, # webm 480p video+audio
    18, # mp4 360p video+audio
    34, # flv 360p video+audio
    43, # webm 360p video+audio
    [[136], [139, 249, 250, 140, 251]], # mp4 720p video only + any audio
    [[247], [139, 249, 250, 140, 251]], # webm 720p video only + any audio
    [[135], [139, 249, 250, 140, 251]], # mp4 480p video only + any audio
    [[168,218,244,245,246], [139, 249, 250, 140, 251]], # webm 480p video only + any audio
]

# the folder where the downloads catalog will be saved
cloud_storage_root = r'C:\Users\g4m3rx\OneDrive\backup_auto'

# the paths to be shown in the GUI as selectable paths
possible_out_paths = [
                        r'C:\propriu\temp\01_new_youtube videos',
                        r'C:\propriu\temp\01_new_youtube music'
                    ]