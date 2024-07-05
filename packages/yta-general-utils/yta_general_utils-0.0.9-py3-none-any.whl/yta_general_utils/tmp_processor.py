from random import randint

from datetime import datetime

def to_tmp_filename(filename):
    """
    Receives a 'filename' and turns it into a temporary filename that is
    returned.

    This method uses the current datetime and a random integer number to
    be unique.

    If you provide 'file.wav' it will return something like 
    'file_202406212425.wav'.
    """
    delta = (datetime.now() - datetime(1970, 1, 1))
    aux = filename.split('.')

    return aux[0] + '_' + str(int(delta.total_seconds())) + str(randint(0, 10000)) + '.' + aux[1]