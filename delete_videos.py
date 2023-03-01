import os
import time
import config
    
def delete_older_videos():
    ''' Removes videos older than stated in the config file from the output folder. '''
    dir_path = config.OUTPUT_PATH
    now = time.time()
    count = 0
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        file_lifespan = now - os.stat(file_path).st_mtime
    
        if file_lifespan > config.FILE_DELETE_TIME:
            if os.path.isfile(file_path):
                os.remove(file_path)
            count += 1
    return count
