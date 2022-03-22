#!/usr/bin/env python3

#importing packages to be used
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np
import sys
import matplotlib
import seaborn as sns
import random
import matplotlib.patches as mpatches

taxa_color_scheme = {'C0006A1':'#eb4034','C0059E1':'#8a130b','C0112A1':'#ba7d79','C0124A1':'#e8d2d1','C0020A1':'#805553','C0022A1':'#a85e8b','C0175A1':'#ff99d7','C0028A1':'#b5006e'}

#defining fuction to pick random color and add to dictionary which it does not already exist
def get_color(taxa):

    chars = '0123456789ABCDEF'

    if taxa in taxa_color_scheme:
        
        taxa_color = taxa_color_scheme[taxa]

    else:
        taxa_color_scheme[taxa] = '#'+''.join(random.sample(chars,6))
        taxa_color = taxa_color_scheme[taxa]

    return taxa_color

#setting font and axes globally
matplotlib.rc('font', serif='Helvetica Neue')
matplotlib.rc('axes',linewidth=2)

VCHIP_data = pd.read_csv(sys.argv[1],sep=",")

Consortia = sys.argv[2]

stacked_fig, stacked_axs = plt.subplots(1,1, figsize=(6,8), facecolor='w', edgecolor='k')
stacked_fig.subplots_adjust(left=0.30,right=0.925,bottom=0.1,top=0.9, wspace=0.1,hspace=0.1)

bar_width = 0.75

legend_entries = {}

VCHIP_data['bottom_count'] = pd.Series([0.0 for x in range(len(VCHIP_data.index))], index=VCHIP_data.index)

for strain in range(1,len(VCHIP_data.columns)-1):

    VCHIP_taxa = VCHIP_data.columns[strain]

    VCHIP_taxa_color = get_color(VCHIP_taxa)

    if VCHIP_taxa not in legend_entries:

            legend_entries[VCHIP_taxa] = taxa_color_scheme[VCHIP_taxa]

    stacked_axs.bar(VCHIP_data['Timepoint'],VCHIP_data[VCHIP_taxa],width=bar_width,bottom=VCHIP_data['bottom_count'],color=VCHIP_taxa_color,clip_on=False)

    VCHIP_data['bottom_count'] = VCHIP_data['bottom_count'] + VCHIP_data[VCHIP_taxa]

stacked_axs.set_ylim([-0.02,1.0])
stacked_axs.set_xlim([-.5,5])

stacked_axs.tick_params(width=2)
stacked_axs.set_yticks([0.0,0.2,0.4,0.6,0.8,1.0], minor=False)
stacked_axs.set_xticks([0,1.5,2.5,3.5,4.5], minor=False)
stacked_axs.set_xticklabels(['Inoculum','1','2','3','4'])
stacked_axs.set_xlabel('Replicate',fontsize=14)
stacked_axs.xaxis.set_label_coords(0.64,-0.05)
stacked_axs.set_ylabel('Relative abundance',fontsize=14)
stacked_axs.set_title('%s' %(Consortia),fontsize=16)
stacked_axs.yaxis.grid(color='gray')
stacked_axs.set_axisbelow(True)


#create a list to store patchesin
#make legend of taxa used in this plot
patch_list = []
for taxa in legend_entries:
    data_key = mpatches.Patch(color=legend_entries[taxa],label=taxa)
    patch_list.append(data_key)
#plot taxa legend
stacked_fig.legend(handles=patch_list,loc=2,fontsize='small',title='Strain')

#saving the figure
stacked_fig.savefig('%s_plot.pdf' %(Consortia))
