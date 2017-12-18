from datetime import datetime
import urllib

import pandas as pd


FAMILY_URL = "http://hamilton.dm.unipi.it/~astdys2/propsynth/all_tro.members"
FAMILY_SOURCE = "source/all_tro.members"
ELEMENT_URL = "http://hamilton.dm.unipi.it/~astdys2/propsynth/all.syn"
ELEMENT_SOURCE = "source/all.syn"
DATA_SOURCE = "source/data.csv"


def load_save():

    starttime = datetime.now()
    urllib.request.urlretrieve(FAMILY_URL, FAMILY_SOURCE)
    print('Family members database downloaded. Total time passed: ', (datetime.now() - starttime).total_seconds())

    starttime = datetime.now()
    urllib.request.urlretrieve(ELEMENT_URL, ELEMENT_SOURCE)
    print('Proper synthetic elements database downloaded. Total time passed: ', (datetime.now() - starttime).total_seconds())


def check_source():

    try:
        f = open(FAMILY_SOURCE,'r')
        f.close()
        f = open(ELEMENT_SOURCE,'r')
    except OSError:
        yes = 'y' in input('Some source data have not been found. Try to download?(yes/no)').lower()
        if yes:
            load_save()
        else:
            print('No available source data provided. Terminating the program.')
            raise SystemExit


def data_create():

    df1 = pd.read_csv(FAMILY_SOURCE, delim_whitespace = True, skiprows = [0], header = None, index_col = 0, usecols = [0, 2, 3], names = ['id', 'status', 'family'])
    df2 = pd.read_csv(ELEMENT_SOURCE, delim_whitespace = True, skiprows = [0, 1], header = None, index_col = 0, usecols = [0, 2, 3, 4, 5], names = ['id', 'a', 'e', 'sinI', 'n'])

    result = pd.concat([df2, df1], axis=1, join_axes = [df2.index]).select(lambda x: str(x).isdigit())
    result[['status', 'family']] = result[['status', 'family']].fillna(0).astype(int)
    result.to_csv(DATA_SOURCE, float_format = '%.7f')

