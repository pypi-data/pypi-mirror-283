"""
@Author: Xin Cao, Xiangning Chu, University of Colorado Boulder
This version: this function is designed to read EICS or SECS data, and return it as a pandas dataframe.
"""
import os
from .load import load
import numpy as np
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import time_double
import pandas as pd
import time
import zipfile
import pyspedas
import logging
import shutil
import gzip
import pickle
import os


def data(trange=['2012-11-05/00:00:00', '2012-11-06/00:00:00'], resolution=10, dtype=None, no_download = False, downloadonly = False, out_type = 'np', save_pickle = False):
    """
    This function loads SECS/EICS data

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: If not provided, current date or code will prompt for time range

        resolution : str
            Default: 10

        dtype: str
            Data type; Valid options:
                'EICS', 'SECA'
            Default: ['eics', 'seca']

        suffix: str
            The tplot variable names will be given this suffix.
            Default: no suffix is added.

        prefix: str
            The tplot variable names will be given this prefix.
            Default: no prefix is added.

        get_stations: bool
            Set this flag to return a list of SECS station names
            Default:  False

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables
            Default: False

        no_update: bool
            If set, only load data from your local cache
            Default: False

        no_download: bool
            If set, only load data from your local cache
            Default: False

    Returns
    ----------
        List of tplot variables created.

    Example
    ----------
        import pyspedas
        from pytplot import tplot
        secs_vars = pyspedas.secs(dtype='eics', trange=['2018-02-01', '2018-02-02'])
        tplot(['secs_eics_latlong', 'secs_eics_jxy'])

    """
    return load(trange = trange, resolution=resolution, dtype = dtype, no_download = no_download, downloadonly = downloadonly, out_type = out_type, save_pickle = save_pickle)


def read_data_files(out_files = None, dtype = None, out_type = 'np', save_pickle = False):
    """
    Read data on a daily basis with a 10-secs or other resolution
    :param out_files: the string list of the downloaded data files' path.
    :param out_type: the return type: 'np': numpy array; 'df': pandas dataframe; 'dc': dictionary
    :param dtype: the data which will be read ('EICS' or 'SECS')
    :return: a numpy nd-array acrossing one or multiple days.
    """
    file_names_arr_Dir = out_files
    start_time = time.time()
    # Reading the data at each time stamp (per resolution secs) on one specific date.

    # input the data into one pd data frame. (four columns)
    if out_type == 'df':
        if dtype == 'EICS':
            colnames = ['latitude', 'longitude', 'Jx', 'Jy']
        if dtype == 'SECS':
            colnames = ['latitude', 'longitude', 'J']
        data_all = []
        for idx, file in enumerate(file_names_arr_Dir):
            df = pd.read_csv(file, header=None, sep=r'\s+', skiprows=0, names=colnames)
            df['datetime'] = file[-19:-4]
            data_all.append(df)
        output = pd.concat(data_all, axis=0, ignore_index=True)

    elif out_type == 'np':
        latitude = []
        longitude = []
        date_time = []
        if dtype == 'EICS':
            Jx = []
            Jy = []
            for file in file_names_arr_Dir:
                di = np.loadtxt(file)
                num_row = np.shape(di)[0]
                latitude.extend(di[:, 0])
                longitude.extend(di[:, 1])
                Jx.extend(di[:, 2])
                Jy.extend(di[:, 3])
                date_time.extend(np.full(num_row, file[-19:-4]))
            num_row2 = len(latitude)
            data_all = np.array([latitude, longitude, Jx, Jy, date_time])
            data_all = data_all.reshape([5, num_row2])
            data_all = np.transpose(data_all)

        if dtype == 'SECS':
            J = []
            for file in file_names_arr_Dir:
                di = np.loadtxt(file)
                num_row = np.shape(di)[0]
                latitude.extend(di[:, 0])
                longitude.extend(di[:, 1])
                J.extend(di[:, 2])
                date_time.extend(np.full(num_row, file[-19:-4]))
            num_row2 = len(latitude)
            data_all = np.array([latitude, longitude, J, date_time])
            data_all = data_all.reshape([4, num_row2])
            data_all = np.transpose(data_all)

        output = data_all

    elif out_type == 'dc':
        data_dict = {}
        Jx = []
        Jy = []
        J = []

        date_time = []
        flag = 0
        filename_day1 = file_names_arr_Dir[0]


        for idx, file in enumerate(file_names_arr_Dir): # per dat file with 1 min resolution.
            if not os.path.isfile(file):
                continue # jump ouf of the current iteration, into the next iteration of the same loop.
            if os.stat(file).st_size == 0: # check if the file is empty.
                continue

            di = np.loadtxt(file)
            if np.shape(di)[0] > 0 and flag == 0:
                num_row = np.shape(di)[0] # np array
                latitude = di[:, 0] # np array
                longitude = di[:, 1] # np array
                flag = 1

            if dtype == 'EICS':
                Jx.append(di[:, 2]) # list [np.arrays]
                Jy.append(di[:, 3]) # list [np.arrays]
            if dtype == 'SECS':
                J.append(di[:, 2])  # list [np.arrays]
            date_time.append(file[-19:-4]) # list of str

        date_time = np.array(date_time) # np array of str
        date_time = time_double(date_time) # np array of float
        if dtype == 'EICS':
            Jx = np.vstack(Jx) # np array
            Jy = np.vstack(Jy) # np array
            data_dict = {'time': date_time, 'latitude': latitude, 'longitude': longitude, 'Jx': Jx, 'Jy': Jy}
        if dtype == 'SECS':
            J = np.vstack(J)  # np array
            data_dict = {'time': date_time, 'latitude': latitude, 'longitude': longitude, 'J': J}
        output = data_dict


    else:
        raise TypeError("%r are invalid keyword arguments" % out_type)

    if save_pickle == True:
        if out_type == 'dc':  # too large, not useful.
            with open('data_dc.pkl', 'wb') as f:
                pickle.dump(output, f)

        # f.close()
    logging.info('running time of output ' + out_type + ": --- %s seconds ---" % (time.time() - start_time))

    return output


def data_selecttime(data = None, dtime = None):
    Data_Days = data
    tp = dtime
    datetime_tp = tp[0:4] + tp[5:7] + tp[8:10] + '_' + tp[11:13] + tp[14:16] + tp[17:19]
    Data_Days_time = Data_Days.loc[Data_Days['datetime'] == datetime_tp]
    return Data_Days_time



