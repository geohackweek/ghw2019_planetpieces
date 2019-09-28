
'''
Tools to reclassify imagery based on reflectance values
'''

import rasterio
from rasterio.plot import show
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap

# Reflectance values (based on what a human thinks + visual tweaking)
snow_class = {'blue': (0.4,1),'green': (0.4,1),'red': (0.4,1),'nir': (0.2,0.8)}
veg_class = {'blue': (0,0.1),'green': (0,0.3),'red': (0,0.1),'nir': (0,0.3)}
rock_class = {'blue': (0,0.2),'green': (0,0.15),'red': (0,0.2),'nir': (0.1,0.6)}

def spec_class(arr, classf):
    '''function to classify an image based on a range of wavelengths in each band'''
    if len(classf)!=arr.shape[2]:
        print("!!!Not all band ranges defined")
        exit()
    for c in range(0,len(classf)):
        if c==0: ar0 = arr[:,:,c]
        ar0 = np.ma.masked_outside(ar0, classf[list(classf.keys())[c]][0],classf[list(classf.keys())[c]][1])
    return(ar0)

def create_class(snow, veg, rock, maskNaN=None):
    '''
    Combines classified reflectance images into landcover image
    snow=0
    vegetation=1
    rock/soil=2
    unclassified=3
    '''
    # fill masked values
    snowfill = np.ma.filled(snow, fill_value=3)
    vegfill = np.ma.filled(veg, fill_value=3)
    rockfill = np.ma.filled(rock, fill_value=3)

    # combine images
    # priority to 1)snow 2)rock 3)vegetation
    class_img = snowfill
    class_img = np.where(class_img<1.0, 0, class_img)
    vv = np.where(vegfill<1.0, 1, vegfill); class_img[vv==1] = vv[vv==1]
    rr = np.where(rockfill<1.0, 2, rockfill); class_img[rr==2] = rr[rr==2]
    # 
    if maskNaN is not None:
        class_img[maskNaN==-9999] = np.nan
    return(class_img)

def plot_class(img):
    '''
    quick image to plot landcover composite with pre-selected colors
    '''
    # color selection
    cols = LinearSegmentedColormap.from_list('cols',['c','g','m','k'])
    fig, ax = plt.subplots(1, figsize=(16, 12))
    pimg = ax.imshow(img, cmap=cols)
    #fig.colorbar(pimg, ax=ax)
    plt.title("Landcover classification map", fontsize=20);

    # add legend
    bar_snow = ax.bar(np.arange(0,10), np.arange(1,11), color='c')
    bar_veg = ax.bar(np.arange(0,10), np.arange(30,40), bottom=np.arange(1,11), color='g')
    bar_rock = ax.bar(np.arange(0,10), np.arange(1,11), color='m')
    bar_unclass = ax.bar(np.arange(0,10), np.arange(30,40), bottom=np.arange(1,11), color='k')
    # create blank rectangle
    extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
    ax.legend(
        handles = [extra, bar_snow, bar_veg, bar_rock, bar_unclass], 
        labels=("Class types", "Snow", "Vegetation", "Rock/soil", "Unclassified"),
        prop={'size': 15}
    )

def plot_sub(ar, arr_title='Rock reflectance threshholds',
            masks=0):
    '''plots each band masked by selected range of values for a given feature'''
    # cols 
    cmaps=['Blues',"Greens","Reds","Reds"]

    # new style method 1; unpack the axes
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15,15), sharex=True, sharey=True)
    plt.subplots_adjust(wspace=0,hspace=0)
    # masking
    ar0 = np.ma.masked_outside(ar[:,:,0], masks[list(masks.keys())[0]][0],masks[list(masks.keys())[0]][1])
    ar1 = np.ma.masked_outside(ar[:,:,1], masks[list(masks.keys())[1]][0],masks[list(masks.keys())[1]][1])
    ar2 = np.ma.masked_outside(ar[:,:,2], masks[list(masks.keys())[2]][0],masks[list(masks.keys())[2]][1])
    ar3 = np.ma.masked_outside(ar[:,:,3], masks[list(masks.keys())[3]][0],masks[list(masks.keys())[3]][1])

    #ax1.plot(ar0, cmap=cmaps[c])
    show(ar0, cmap=cmaps[0], ax=ax1); show(ar1, cmap=cmaps[1], ax=ax2)
    show(ar2, cmap=cmaps[2], ax=ax3); show(ar3, cmap=cmaps[3], ax=ax4)
    
    # titles
    ax1.set_title(list(masks.keys())[0]); ax2.set_title(list(masks.keys())[1])
    ax3.set_title(list(masks.keys())[2]); ax4.set_title(list(masks.keys())[3])
    fig.suptitle(arr_title, fontsize=16)


def reshape_vrts(img_stack):
    '''Function to reshape vrt image stack for classification'''
    for layer in range(0, img_stack.shape[0]):
        arr=img_stack[layer, :, :]
        if layer == 0:
            reshaped = arr
        else:
            reshaped = np.dstack((reshaped, arr))
    return reshaped

def plot_spec(arr, cmap='Greys_r', arr_title='Plot title',
            width=16, height=12, sv=None,
            mask_low=None, mask_high=None, vmin=None, vmax=None):
    '''
    Copied from data_tools.py - Function that quickly plots input array and masks data based on defined limits
    '''
    
    fig, ax = plt.subplots(1, figsize=(width, height))
    if mask_low is not None:
        arr = np.ma.masked_outside(arr, mask_low, mask_high)
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