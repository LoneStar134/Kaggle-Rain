__author__ = 'Darron'
"""
Data munging to create dataset for preliminary analysis
"""
import csv
import sys
import logging
import argparse
import numpy as np

# configure logging
logger = logging.getLogger("LoneStar_DataMunge")

handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s %(name)s: %(message)s'))

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def radar_count(row,idx) :
    tte = np.array(row[idx].split(' '), dtype='float')

    radar_count = 0
    last_t = 0
    idx_begin = 0
    idx_end = 0
    idx_pos = 0
    radar_arr = []

    for t in tte:
        if t > last_t:
            radar_count = radar_count + 1
            if idx_pos != 0 :
                idx_end = idx_pos - 1
                # print("%d : %d : %d" % (radar_count-1,idx_begin,idx_end))
                radar_arr.extend([[idx_begin,idx_end]])
                idx_begin = idx_pos

        idx_pos = idx_pos + 1

        last_t = t

        # print(str(t) + " : " + str(last_t) + " : " + str(radar_count))
    idx_end = idx_pos - 1
    # print("%d : %d : %d" % (radar_count,idx_begin,idx_end))
    radar_arr.extend([[idx_begin,idx_end]])

    return radar_arr


def calc_stats(rowid, row, idx, radar_arr,header_row,output_row) :
    radar_count = 0
    data = np.array(row[idx].split(' '), dtype='float')

    # print radar_arr
    for rad in radar_arr :
        radar_count = radar_count + 1
        radar_hdr = 'Radar%d_%s' % (radar_count,header_row[idx])
        val_arr = np.array(row[idx].split(' '), dtype='float')[rad[0]:rad[1]+1]
        # val_arr = [i for i in val_arr1 if i not in ['nan',-99000.0,-99901.0,-99903.0,999.0]]

        # print val_arr


        # str_arr = np.array(row[idx].split(' '), dtype='string')[rad[0]:rad[1]+1]
        str_arr = row[idx].split(' ')[rad[0]:rad[1]+1]

        mean = np.mean(val_arr)
        median = np.median(val_arr)
        min = np.min(val_arr)
        max = np.max(val_arr)
        std = np.std(val_arr)

        count_nan =  str_arr.count('nan')
        count_000 =  str_arr.count('-99000.0')
        count_901 =  str_arr.count('-99901.0')
        count_903 =  str_arr.count('-99903.0')
        count_999 =  str_arr.count('999.0')

        # print str_arr

        # print str_arr.count('nan')

        print("%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d" % (rowid,radar_count, mean,median,min,max,std,count_000,count_901,count_903,count_999,count_nan))


        # print rad
        # val_arr[rad[0]:rad[1]+1]
        # print radar_hdr




def produce_prep_datafile(args):
    # wrap the inputs and outputs in csv interpreters
    writer = csv.writer(args.output, delimiter=',')
    reader = csv.reader(args.input, delimiter=',')
    # read in the header
    header = reader.next()
    # the solution header is an Id, then 70 discrete cumulative probabilities
    output_header = ['Id','Radar_Count']

    for r in xrange(1,9) :
    
        radar_hdr = 'Radar%d' % r
    
        output_header.extend(['%s_Dist_Mean' % radar_hdr])
        output_header.extend(['%s_Dist_Med' % radar_hdr])
        output_header.extend(['%s_Dist_Low' % radar_hdr])
        output_header.extend(['%s_Dist_High' % radar_hdr])
        output_header.extend(['%s_Dist_StdDev' % radar_hdr])
        output_header.extend(['%s_Dist_Bad000_Count' % radar_hdr])
        output_header.extend(['%s_Dist_Bad901_Count' % radar_hdr])
        output_header.extend(['%s_Dist_Bad903_Count' % radar_hdr])
        output_header.extend(['%s_Dist_Bad999_Count' % radar_hdr])
        output_header.extend(['%s_Dist_Badnan_Count' % radar_hdr])

        output_header.extend(['%s_Composite_Mean' % radar_hdr])
        output_header.extend(['%s_Composite_Med' % radar_hdr])
        output_header.extend(['%s_Composite_Low' % radar_hdr])
        output_header.extend(['%s_Composite_High' % radar_hdr])
        output_header.extend(['%s_Composite_StdDev' % radar_hdr])
        output_header.extend(['%s_Composite_Bad900_Count' % radar_hdr])
        output_header.extend(['%s_Composite_Bad901_Count' % radar_hdr])
        output_header.extend(['%s_Composite_Bad903_Count' % radar_hdr])
        output_header.extend(['%s_Composite_Bad999_Count' % radar_hdr])
        output_header.extend(['%s_Composite_Badnan_Count' % radar_hdr])
    
        output_header.extend(['%s_Hybrid_Mean' % radar_hdr])
        output_header.extend(['%s_Hybrid_Med' % radar_hdr])
        output_header.extend(['%s_Hybrid_Low' % radar_hdr])
        output_header.extend(['%s_Hybrid_High' % radar_hdr])
        output_header.extend(['%s_Hybrid_StdDev' % radar_hdr])
        output_header.extend(['%s_Hybrid_Bad900_Count' % radar_hdr])
        output_header.extend(['%s_Hybrid_Bad901_Count' % radar_hdr])
        output_header.extend(['%s_Hybrid_Bad903_Count' % radar_hdr])
        output_header.extend(['%s_Hybrid_Bad999_Count' % radar_hdr])
        output_header.extend(['%s_Hybrid_Badnan_Count' % radar_hdr])
    
        output_header.extend(['%s_HydrType_01_Count' % radar_hdr])
        output_header.extend(['%s_HydrType_02_Count' % radar_hdr])
        output_header.extend(['%s_HydrType_03_Count' % radar_hdr])
        output_header.extend(['%s_HydrType_04_Count' % radar_hdr])
        output_header.extend(['%s_HydrType_05_Count' % radar_hdr])
        output_header.extend(['%s_HydrType_06_Count' % radar_hdr])
        output_header.extend(['%s_HydrType_07_Count' % radar_hdr])
        output_header.extend(['%s_HydrType_08_Count' % radar_hdr])
        output_header.extend(['%s_HydrType_09_Count' % radar_hdr])
        output_header.extend(['%s_HydrType_10_Count' % radar_hdr])
        output_header.extend(['%s_HydrType_11_Count' % radar_hdr])
        output_header.extend(['%s_HydrType_12_Count' % radar_hdr])
        output_header.extend(['%s_HydrType_13_Count' % radar_hdr])
        output_header.extend(['%s_HydrType_14_Count' % radar_hdr])
    
        output_header.extend(['%s_Kdp_Mean' % radar_hdr])
        output_header.extend(['%s_Kdp_Med' % radar_hdr])
        output_header.extend(['%s_Kdp_Low' % radar_hdr])
        output_header.extend(['%s_Kdp_High' % radar_hdr])
        output_header.extend(['%s_Kdp_Bad900_Count' % radar_hdr])
        output_header.extend(['%s_Kdp_Bad901_Count' % radar_hdr])
        output_header.extend(['%s_Kdp_Bad903_Count' % radar_hdr])
        output_header.extend(['%s_Kdp_Bad999_Count' % radar_hdr])
        output_header.extend(['%s_Kdp_Badnan_Count' % radar_hdr])
    
        output_header.extend(['%s_RR1_Mean' % radar_hdr])
        output_header.extend(['%s_RR1_Med' % radar_hdr])
        output_header.extend(['%s_RR1_Low' % radar_hdr])
        output_header.extend(['%s_RR1_High' % radar_hdr])
        output_header.extend(['%s_RR1_Bad900_Count' % radar_hdr])
        output_header.extend(['%s_RR1_Bad901_Count' % radar_hdr])
        output_header.extend(['%s_RR1_Bad903_Count' % radar_hdr])
        output_header.extend(['%s_RR1_Bad999_Count' % radar_hdr])
        output_header.extend(['%s_RR1_Badnan_Count' % radar_hdr])
    
        output_header.extend(['%s_RR2_Mean' % radar_hdr])
        output_header.extend(['%s_RR2_Med' % radar_hdr])
        output_header.extend(['%s_RR2_Low' % radar_hdr])
        output_header.extend(['%s_RR2_High' % radar_hdr])
        output_header.extend(['%s_RR2_Bad900_Count' % radar_hdr])
        output_header.extend(['%s_RR2_Bad901_Count' % radar_hdr])
        output_header.extend(['%s_RR2_Bad903_Count' % radar_hdr])
        output_header.extend(['%s_RR2_Bad999_Count' % radar_hdr])
        output_header.extend(['%s_RR2_Badnan_Count' % radar_hdr])
    
        output_header.extend(['%s_RR3_Mean' % radar_hdr])
        output_header.extend(['%s_RR3_Med' % radar_hdr])
        output_header.extend(['%s_RR3_Low' % radar_hdr])
        output_header.extend(['%s_RR3_High' % radar_hdr])
        output_header.extend(['%s_RR3_Bad900_Count' % radar_hdr])
        output_header.extend(['%s_RR3_Bad901_Count' % radar_hdr])
        output_header.extend(['%s_RR3_Bad903_Count' % radar_hdr])
        output_header.extend(['%s_RR3_Bad999_Count' % radar_hdr])
        output_header.extend(['%s_RR3_Badnan_Count' % radar_hdr])
    
        output_header.extend(['%s_RadQualIndex_Mean' % radar_hdr])
        output_header.extend(['%s_RadQualIndex_Med' % radar_hdr])
        output_header.extend(['%s_RadQualIndex_Low' % radar_hdr])
        output_header.extend(['%s_RadQualIndex_High' % radar_hdr])
        output_header.extend(['%s_RadQualIndex_Bad900_Count' % radar_hdr])
        output_header.extend(['%s_RadQualIndex_Bad901_Count' % radar_hdr])
        output_header.extend(['%s_RadQualIndex_Bad903_Count' % radar_hdr])
        output_header.extend(['%s_RadQualIndex_Bad999_Count' % radar_hdr])
        output_header.extend(['%s_RadQualIndex_Badnan_Count' % radar_hdr])
    
        output_header.extend(['%s_Reflectivity_Mean' % radar_hdr])
        output_header.extend(['%s_Reflectivity_Med' % radar_hdr])
        output_header.extend(['%s_Reflectivity_Low' % radar_hdr])
        output_header.extend(['%s_Reflectivity_High' % radar_hdr])
        output_header.extend(['%s_Reflectivity_Bad900_Count' % radar_hdr])
        output_header.extend(['%s_Reflectivity_Bad901_Count' % radar_hdr])
        output_header.extend(['%s_Reflectivity_Bad903_Count' % radar_hdr])
        output_header.extend(['%s_Reflectivity_Bad999_Count' % radar_hdr])
        output_header.extend(['%s_Reflectivity_Badnan_Count' % radar_hdr])
    
        output_header.extend(['%s_ReflectivityQC_Mean' % radar_hdr])
        output_header.extend(['%s_ReflectivityQC_Med' % radar_hdr])
        output_header.extend(['%s_ReflectivityQC_Low' % radar_hdr])
        output_header.extend(['%s_ReflectivityQC_High' % radar_hdr])
        output_header.extend(['%s_ReflectivityQC_Bad900_Count' % radar_hdr])
        output_header.extend(['%s_ReflectivityQC_Bad901_Count' % radar_hdr])
        output_header.extend(['%s_ReflectivityQC_Bad903_Count' % radar_hdr])
        output_header.extend(['%s_ReflectivityQC_Bad999_Count' % radar_hdr])
        output_header.extend(['%s_ReflectivityQC_Badnan_Count' % radar_hdr])
    
        output_header.extend(['%s_Velocity_Mean' % radar_hdr])
        output_header.extend(['%s_Velocity_Med' % radar_hdr])
        output_header.extend(['%s_Velocity_Low' % radar_hdr])
        output_header.extend(['%s_Velocity_High' % radar_hdr])
        output_header.extend(['%s_Velocity_Bad900_Count' % radar_hdr])
        output_header.extend(['%s_Velocity_Bad901_Count' % radar_hdr])
        output_header.extend(['%s_Velocity_Bad903_Count' % radar_hdr])
        output_header.extend(['%s_Velocity_Bad999_Count' % radar_hdr])
        output_header.extend(['%s_Velocity_Badnan_Count' % radar_hdr])
    
        output_header.extend(['%s_Zdr_Mean' % radar_hdr])
        output_header.extend(['%s_Zdr_Med' % radar_hdr])
        output_header.extend(['%s_Zdr_Low' % radar_hdr])
        output_header.extend(['%s_Zdr_High' % radar_hdr])
        output_header.extend(['%s_Zdr_Bad900_Count' % radar_hdr])
        output_header.extend(['%s_Zdr_Bad901_Count' % radar_hdr])
        output_header.extend(['%s_Zdr_Bad903_Count' % radar_hdr])
        output_header.extend(['%s_Zdr_Bad999_Count' % radar_hdr])
        output_header.extend(['%s_Zdr_Badnan_Count' % radar_hdr])
    
        output_header.extend(['%s_LogWaterVolume_Mean' % radar_hdr])
        output_header.extend(['%s_LogWaterVolume_Med' % radar_hdr])
        output_header.extend(['%s_LogWaterVolume_Low' % radar_hdr])
        output_header.extend(['%s_LogWaterVolume_High' % radar_hdr])
        output_header.extend(['%s_LogWaterVolume_Bad900_Count' % radar_hdr])
        output_header.extend(['%s_LogWaterVolume_Bad901_Count' % radar_hdr])
        output_header.extend(['%s_LogWaterVolume_Bad903_Count' % radar_hdr])
        output_header.extend(['%s_LogWaterVolume_Bad999_Count' % radar_hdr])
        output_header.extend(['%s_LogWaterVolume_Badnan_Count' % radar_hdr])
    
        output_header.extend(['%s_MassWeightedMean_Mean' % radar_hdr])
        output_header.extend(['%s_MassWeightedMean_Med' % radar_hdr])
        output_header.extend(['%s_MassWeightedMean_Low' % radar_hdr])
        output_header.extend(['%s_MassWeightedMean_High' % radar_hdr])
        output_header.extend(['%s_MassWeightedMean_Bad900_Count' % radar_hdr])
        output_header.extend(['%s_MassWeightedMean_Bad901_Count' % radar_hdr])
        output_header.extend(['%s_MassWeightedMean_Bad903_Count' % radar_hdr])
        output_header.extend(['%s_MassWeightedMean_Bad999_Count' % radar_hdr])
        output_header.extend(['%s_MassWeightedMean_Badnan_Count' % radar_hdr])
    
        output_header.extend(['%s_MassWeightedSD_Mean' % radar_hdr])
        output_header.extend(['%s_MassWeightedSD_Med' % radar_hdr])
        output_header.extend(['%s_MassWeightedSD_Low' % radar_hdr])
        output_header.extend(['%s_MassWeightedSD_High' % radar_hdr])
        output_header.extend(['%s_MassWeightedSD_Bad900_Count' % radar_hdr])
        output_header.extend(['%s_MassWeightedSD_Bad901_Count' % radar_hdr])
        output_header.extend(['%s_MassWeightedSD_Bad903_Count' % radar_hdr])
        output_header.extend(['%s_MassWeightedSD_Bad999_Count' % radar_hdr])
        output_header.extend(['%s_MassWeightedSD_Badnan_Count' % radar_hdr])

    output_header.extend(['Expected'])

    # write the header to file
    writer.writerow(output_header)

    for i, row in enumerate(reader):
        # print("******* " + str(row[header.index('Id')]) + " *******")
        radar_array = radar_count(row,header.index('TimeToEnd'))

        # print(radar_array)

        output_row = [row[header.index('Id')]]
        output_row.extend([radar_array.__len__()])

        # calc_stats(row,header.index('DistanceToRadar'),radar_array,header,output_row)
        # calc_stats(row,header.index('RadarQualityIndex'),radar_array,header,output_row)
        calc_stats(row[header.index('Id')],row,header.index('Zdr'),radar_array,header,output_row)

        writer.writerow(output_row)

        # write the solution row
        # solution_row = [id_num]
        # solution_row.extend(approx_rr1)
        # writer.writerow(solution_row)
        # Every 1000 rows send an update to the user for progress tracking.
        if i % 1000 == 0:
            logger.info("Completed row %d" % i)

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
    produce_prep_datafile(args)
