__author__ = 'Darron'

import csv
import sys
import logging
import argparse
import numpy as np

# configure logging
logger = logging.getLogger("MaxRadars")

handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s %(name)s: %(message)s'))

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)




if __name__ == "__main__":
    # set up logger
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=argparse.FileType('r'),
                        help=("path to an input file, this will "
                              "typically be train_2013.csv or "
                              "test_2014.csv"))
    parser.add_argument('--output', type=argparse.FileType('w'),
                        default=sys.stdout,
                        help=("path to an output file, "
                              "defaults to stdout"))
    # parse the arguments and run the handler associated with each task
    args = parser.parse_args()

    reader = csv.reader(args.input, delimiter=',')
    # read in the header
    header = reader.next()
    tte_idx = header.index('TimeToEnd')
    id_idx = header.index('Id')
    radar_count_arr = np.array([0,0,0,0,0,0,0,0])


    max_radar_count = 0
    total_radar_count = 0
    row_count = 0.

    # iterate over each row and estimate a rainfall probability distribution
    for i, row in enumerate(reader):
        # Each row in the file represents a single hour's observations at some
        # location and consists of a set of comma delimited fields.  Often
        # there is more than one radar observation per hour, so some fields
        # have multiple values per row, each corresponding of a single radar
        # volume scan.  For example, if five scans were completed within a
        # single hour the reflectivity field may look something like:
        #
        #     "17.5 30.5 42.0 38.5 37".
        #
        # Similarly, in this next line, we find the rainfall rate field ('RR1')
        # and then convert it from a space delimited string to a float array.
        tte = np.array(row[tte_idx].split(' '), dtype='float')

        radar_count = 0.
        last_t = 0
        row_count = row_count + 1

       # print("******* " + str(row[id_idx]) + " *******")
        for t in tte:
            if t > last_t:
                radar_count = radar_count + 1
                total_radar_count = total_radar_count + 1

            last_t = t

       #     print(str(t) + " : " + str(last_t) + " : " + str(radar_count))

        if radar_count > max_radar_count:
            max_radar_count = radar_count
            max_row_id = row[id_idx]

        radar_count_arr[radar_count-1] = radar_count_arr[radar_count-1] + 1

        # Every 1000 rows send an update to the user for progress tracking.
        if i % 1000 == 0:
            logger.info("Completed row %d : Max %d" % (i,max_radar_count))

    print("Row " +  str(max_row_id) + " has " + str(max_radar_count) + " radars.")
    print("Rowcount: %d" % row_count)
    print("Total Radar Count: %d" % total_radar_count)
    print("Average number of Radars per instance: %f" % (total_radar_count/row_count))
    print(radar_count_arr)