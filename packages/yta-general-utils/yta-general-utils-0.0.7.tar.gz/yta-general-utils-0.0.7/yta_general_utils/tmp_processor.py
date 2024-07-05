from random import randint
from dotenv import load_dotenv

from datetime import datetime
import os

load_dotenv()

WIP_FOLDER = os.getenv('WIP_FOLDER')

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

def create_tmp_filename(filename):
    """
    Returns a temporary file name with 'WIP_FOLDER' prefix and a timestamp suffix.

    If you provide 'file.wav' it will return something like 
    'wip/file_202406212425.wav'.
    """
    # TODO: Rename this as it uses wip and we do not mention it
    # TODO: Issue if no extension provided
    return WIP_FOLDER + to_tmp_filename(filename)