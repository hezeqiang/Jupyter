#coding:u8
from pylab import plt, mpl, np
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
# from pprint import pprint
from collections import OrderedDict as O
import pandas as pd


#for saving fig as tif file
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
from io import BytesIO


# plot style
#produce a one-demesion array between （0，5） containing 4 element
#a = np.random.randint(0, 5, (4,))
#plt.style.available print all available style in plt
style = np.random.choice(plt.style.available);print(style);
#use specific style named ggplot
plt.style.use( 'classic')
#frequently used style
#['bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale']

# plot setting
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
mpl.rcParams['legend.fontsize'] = 12.5
# mpl.rcParams['legend.family'] = 'Times New Roman'
mpl.rcParams['font.family'] = ['Times New Roman']
mpl.rcParams['font.size'] = 14.0
# mpl.style.use('classic')

font = {'family' : 'Times New Roman', #'serif',
        'color' : 'black',
        'weight' : 'normal',
        'size' : 14,}
font_title = {'family' : 'Times New Roman', #'serif',
        'color' : 'black',
        'weight' : 'normal',
        'size' : 18,}

textfont = {'family' : 'Times New Roman', #'serif',
            'color' : 'black',
            'weight' : 'normal',
            'size' : 11.5,}

#   https://blog.csdn.net/mmc2015/article/details/72829107
# color reference

#print(matplotlib.rc_params())
#print default setting
#mpl.rcdefaults()
#use the default setting
######################
# Plotting
# get_axis is used to create axes and figure for every plotting
#refer to https://blog.csdn.net/qq_31347869/article/details/104794515
def get_axis():
    fig, axes = plt.subplots(ncols=1, nrows=1, sharex=True, figsize=(7, 4.7), dpi=80, facecolor='w', edgecolor='k') # 1 inch = 2.5cm
    fig.subplots_adjust(right=0.90, bottom=0.15, top=0.85, hspace=0.2, wspace=0.1)

    # gcf() means get the current fig, so  plt.gcf().axes() means create axes in current fig
    # grid on
    # plt.grid(color='r', linestyle='--', linewidth=1,alpha=0.3)
    plt.grid(color='lightgray', linestyle='-',linewidth=0.5,alpha=0.3)

    #figure ax size setting

    return  axes

def plot_key(ax, key, df):
    # plot the curve with time as x and values as y
    ax.plot(time, df[key].values, 'k-', lw=1)
    #set y label name
    ax.set_ylabel(key, fontdict=font)

def plot_it(ax, ylabel, d, time=None):
    count = 0
    for k, v in d.items():
        if count == 0:
            count += 1
            # ax.plot(time, v, '--', lw=2, label=k)
            ax.plot(time, v, 'k-', lw=1)
        else:
            # ax.plot(time, v, '-', lw=2, label=k)
            ax.plot(time, v, 'k-', lw=1)
    # a.plot(x1, y1, 'g^', x2, y2, 'g-')
    # ax.legend(loc='lower right', shadow=True)
    # ax.legend(bbox_to_anchor=(1.08,0.5), borderaxespad=0., loc='center', shadow=True)

    ax.set_ylabel(ylabel,fontdict=font)
    ax.set_xlabel('Time /(second)',fontdict=font)
    ax.set_title(title_fig[ID_x],fontdict=font_title ,loc='center' )

    # plt.text(0.5 * (a+b), 1, r"$\int_a^b f(x)\mathrm{d}x$")
    # LaTex insert
    # r""for LaTex, $$ for equation
    # plt.savefig('python_C_model_with_radial_control_fail/'+ylabel + '.png')

    # ax.set_xlim(0,35) # shared x
    # ax.set_ylim(0.85,1.45)

if __name__ == '__main__':

    df_info = pd.read_csv(r"./info.dat", na_values = ['1.#QNAN', '-1#INF00', '-1#IND00'])
    # if reading string is '1.#QNAN', '-1#INF00', '-1#IND00, then set the string as NaN
    data_file_name = df_info['DATA_FILE_NAME'].values[0].strip()
    # the first row is defaulted name for every column. strip() means element is a string
    #   df_info['DATA_FILE_NAME'].values[0].strip() represent the first element in colunm ['DATA_FILE_NAME']
    print(data_file_name)
    df_profiles = pd.read_csv(data_file_name, na_values = ['1.#QNAN', '-1#INF00', '-1#IND00'])
    #   read the data file containing the simulation results.

    df_title = pd.read_csv('title.txt', na_values=['1.#QNAN', '-1#INF00', '-1#IND00'])
    title_fig=list()
    for key in df_title.keys():
        title_fig.append(key)
        print(key)

    no_samples = df_profiles.shape[0]
    # get number of rows
    no_traces = df_profiles.shape[1]
    # get number of column, namely number of keys
    print(df_info, 'Simulated time: %f s.'%(no_samples * df_info['WRITE_PER_TIME'].values[0]), 'Key list:', sep='\n')

    for key in df_profiles.keys():
        print('\t', key)
    #   print all key of the data ,which is the first row string in data file
    #   the value of key is corresponding list
    time = np.arange(1, no_samples+1) * df_info['WRITE_PER_TIME'].values[0]

    ax_list = []
#    for i in range(0, no_traces, 2):    #   for i in range(1, 101，1) print from 1 to 101
#        ax_list += list(get_axis((1,2)))    #   add axis list to ax_list
    for i in range(0, no_traces):    #   for i in range(1, 101，1) print from 1 to 101
        ax_list.append(get_axis())
        #ax_list.append(get_axis(1,1))    #   add axis list to ax_list


    for ID_x, key in enumerate(df_profiles.keys()):     #   enumerate() is utilized to give num for every key
        plot_it(ax_list[ID_x], key, O([
                                        (str(ID_x), df_profiles[key]),
                                        # (str(idx), df_profiles[key]),
                                        ]), time)
        # input("Wait for key")
        # time.sleep(0.05) # wait for 0.05 second



    #   fig.savefig('figure_name.png')  must be placed before   plt.show
    #fig.savefig('%s.tif',ylabel)
    #   the final direction in the script to creat the defined figure
    plt.show()

    quit()
