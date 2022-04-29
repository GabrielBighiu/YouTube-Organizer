# the videos will be downloaded based on the formats priority
# if a format fails then the next attempt will be made with the next fromat descriptor
# a descriptor can be a single format (usually containing audio+video) OR
# a list of lists of formats containing both video and audio options
download_formats_prio = [
    22, #720p video+audio
    [[247, 136], [139, 249, 250, 140, 251]]
]

# the folder where the downloads catalog will be saved
cloud_storage_root = r'C:\Users\g4m3rx\OneDrive\backup_auto'

# the paths to be shown in the GUI as selectable paths
possible_out_paths = [
                        r'C:\propriu\temp\01_new_youtube videos',
                        r'C:\propriu\temp\01_new_youtube music'
                    ]