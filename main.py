import os
from time import time

from const import DL_DIR, CLEAN
from date_iterator import DateConstructor
from madis_class import Madis


def main():

    start = time()
    # set up directories
    if not os.path.exists(DL_DIR):
        print("...creating folder: {}\n".format(DL_DIR))
        os.makedirs(DL_DIR)

    if not os.path.exists(CLEAN):
        print("...creating folder: {}\n".format(CLEAN))
        os.makedirs(CLEAN)

    # instantiate iterator
    date_pack = DateConstructor(2015, (9, 9), (27, 30), 0)
    dates = iter(date_pack)

    print('begin file download for year 2015\n')
    for i in range(13):
        # start this ugly shit code and chug a beer
        Madis(long_ext=(-85.0, -80.6), lat_ext=(38.3, 42.4), start_time=start, iterator=dates).get_files()

    print('finished download in: {}'.format(time() - start))


if __name__ == '__main__':
    main()
