
def seconds_to_time(seconds: int) -> tuple:
    ''' Converts number of seconds to hours, minutes and seconds. '''
    seconds = seconds % (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return (hours, minutes, seconds)

def querystring_to_time(time: str) -> str:
    ''' Decodes query string passed as an argument to string suitable as ffmpeg argument. '''
    times = [x.rjust(2,'0') for x in time.split('_')]
    times[-1] = times[-1].rjust(3, '0')
    return f'{times[0]}:{times[1]}:{times[2]}.{times[3]}'
