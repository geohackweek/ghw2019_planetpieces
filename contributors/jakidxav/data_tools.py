'''
Helper functions to interact with data and files
'''

import numpy as np
import matplotlib.pyplot as plt
import rasterio

import glob


def fn_list(thisDir, fn_pattern):
    '''
    Function that returns a sorted list of filenames based on a regex pattern in specified directory
    '''
    
    fns=[]
    for f in glob.glob(thisDir + "/" + fn_pattern):
        print(f)
        fns.append(f)
    fns.sort()
    
    return fns

def read_raster(filename, band=1):
    '''
    Function that reads in raster file and returns a numpy array, along with corresponding no data value
    '''
    
    with rasterio.open(filename) as f:
        arr = f.read(band)
        no_data_value = f.nodata
    return arr, no_data_value

def plot_me(arr, cmap='Greys_r', arr_title='Plot title',
            width=16, height=12, sv=None,
            mask_value=None, vmin=None, vmax=None):
    '''
    Function that quickly plots input array and linearly maps data values to specified limits
    '''
    
    fig, ax = plt.subplots(1, figsize=(width, height))
    if mask_value is not None:
        arr = np.ma.masked_equal(arr, mask_value)
    if vmin is not None:
        vmin=vmin
        vmax=vmax
        thisPlot = ax.imshow(arr, cmap=cmap, vmin=vmin, vmax=vmax)
    else:
        thisPlot = ax.imshow(arr, cmap=cmap)
    fig.colorbar(thisPlot, ax=ax)
    plt.title(arr_title);
    if sv is not None:
        figName='plot_' + sv + '.png'
        print(figName)
        plt.savefig(figName)

def histo_me(arr, title='Title', mask_value=None,
             xaxis=None, bins=100, alpha=1,
             color='dodgerblue', edgecolor='black',
             histtype='bar', linewidth=0.5,
             sv=None,
             zero_line=None,
             range_val=None):
    '''Function to create formatted histogram of input array'''
    fig = plt.figure(figsize=(8,6))
    if mask_value is not None:
        arr[arr==mask_value]=np.nan
    plt.hist(np.ravel(arr), bins=bins, color=color, edgecolor=edgecolor,
             alpha=alpha, histtype=histtype, linewidth=linewidth, range=range_val);
    plt.title(title);
    plt.xlabel(xaxis);
    if zero_line is not None:
        if abs(np.nanmedian(arr))>1:
            plt.axvline(x=np.nanmedian(arr), linewidth=2.5, color='k', linestyle='-.');
        else:
            plt.axvline(linewidth=2.5, color='k', linestyle='-.');
    if sv is not None:
        figName='histo_' + sv + '.png'
        print(figName)
        plt.savefig(figName)

# Basic stats function
def tell_me_more(arr, name_of_someData=None, mask_no_data=None, meta=None):
    '''
    Function that prints basic statistics, type and shape of input array
    '''
    
    if name_of_someData is not None:
        pass
        # print("\nHere's what I found for:", name_of_someData)
    if mask_no_data is not None:
        arr = np.ma.masked_equal(arr, mask_no_data)
    if meta is not None:
        print("Type is", type(arr))
        print("Shape is", arr.shape)
    basic_stats = [np.nanpercentile(arr, 0.1), np.nanpercentile(arr, 1), np.nanmedian(arr), np.nanpercentile(arr, 90), np.nanpercentile(arr, 99), np.nanpercentile(arr, 99.9), np.nanstd(arr)]

#     basic_stats = [np.nanmin(arr), np.nanmedian(arr), np.nanmean(arr), np.nanpercentile(arr, 90), np.nanmax(arr), np.nanstd(arr)]
    # print("Min value is", "{0:.2f}".format(np.nanmin(arr)))
    # print("Median value is", "{0:.2f}".format(np.nanmedian(arr)))
    # print("Mean value is", "{0:.2f}".format(np.nanmean(arr)))
    # print("90th percentile value is", "{0:.2f}".format(np.nanpercentile(arr, 90)))
    # print("Max value is", "{0:.2f}".format(np.nanmax(arr)))
    # print("Std dev is", "{0:.2f}".format(np.nanstd(arr)))
    return(basic_stats)

def root_sum_squares(arr1, arr2):
    '''
    Function to calculate magnitude of two arrays of vectors.
    '''
    rss_arr=np.sqrt(arr1**2+arr2**2)
    v_line=np.median(rss_arr)
    return rss_arr, v_line
