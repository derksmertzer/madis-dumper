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
    date_gen = DateConstructor()
    hour_range = date_gen.hour_range()
    month_range = date_gen.hour_range()
    dates = iter(date_gen)

    print('begin file download for year 2015\n')
    for i in range(date_gen.month_range()):
        # start this ugly shit code and chug a beer
        Madis(start_time=start, iterator=dates, hours=hour_range).get_files()

    print('finished download in: {}'.format(time() - start))


if __name__ == '__main__':
    main()
