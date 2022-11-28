# draw_bubble.py

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib import cm
import pandas as pd
import numpy as np

# Global parameters
_filename = "example_data/raw_bubble.csv"
_title = "Optimum Temperature for Tea Leaf Growth"

# Configuration
plt.rcParams['font.sans-serif'] = ['Times New Roman']

upper_limit_of_normal_data = 200    # Will drop data greater than upper_limit in function-"drop_outlier"
lower_limit_of_normal_data = 0      # Will drop data less than lower_limit in function-"drop_outlier"
data_to_show = 50                   # Only annotate the data greater than or equal to "data_to_show" on bubble chart

title_x_axis = "Sonic Temperature"
title_y_axis = "Shortwave Radiation"
title_z_axis = "Carbon Dioxide Flux"

unit_x_axis = r'$^oC$'
unit_y_axis = r'$W/m^2$'
unit_z_axis = r'$\mu mol m^{-2} s^{-1}$'

def read_and_format_csv(filename):
    try:
        # Read csv file and use 'tab' as delimiter
        df = pd.read_csv(filename, delimiter=',')

        # If the file is not seperated by common raise exception and use common as delimiter
        if(df.shape[1] != 3):
            raise Exception("Input file is not seperated by ','")

    except Exception:
        print("Use 'tab' as the delimiter")

        # Read csv file and ust 'tab' as delimiter
        df = pd.read_csv(filename, delimiter='\t')

    # Drop the time columns
    # df.drop(df.columns[0], axis=1, inplace=True)

    return df

def drop_outlier(df):
    array_columns = df.columns
    amount_ori = df.shape[0]

    # Drop the data which is greater than upper_limit or less than lower_limit
    df.drop(df[(df[array_columns[2]] > upper_limit_of_normal_data) |
               (df[array_columns[2]] < lower_limit_of_normal_data)].index,
            inplace=True)
    amount_processed = df.shape[0]

    print(f"Find {amount_ori-amount_processed} outlier(s) on the raw_data.")

    return df

def format(df):
    # Transform the type of df into float64,
    df = df.astype('float64')

    return df

def draw_bubble_chart(df_x, df_y, df_z):
    # Normalize the df_z to [0, 1]
    # diff = df_z.max() - df_z.min()
    # df_z_norm = (df_z-df_z.min())/diff + 0.001

    fig, ax = plt.subplots()

    ax.scatter(df_x, df_y, s=50, c=df_z, cmap="viridis", alpha=0.8, label=f"{title_z_axis} ({unit_z_axis})")
    for i in range(0, df_x.shape[0]):
        z = df_z.iloc[i]
        if(z >= data_to_show):
            ax.annotate(str(round(z,2)), (df_x.iloc[i], df_y.iloc[i]))

    # Put the title
    ax.set_title(_title)
    
    # Put the label on each axis
    ax.set_xlabel(f"{title_x_axis} ({unit_x_axis})")
    ax.set_ylabel(f"{title_y_axis} ({unit_y_axis})")

    # Put the colorbar on the chart
    norm = Normalize(vmin=df_z.min(), vmax=df_z.max())
    fig.colorbar(cm.ScalarMappable(norm=norm, cmap="viridis"), ax=ax)

    # Put the legend on the chart
    ax.legend()

if __name__ == "__main__":
    # Read the csv file into a dataframe and drop the time columns
    df_raw = read_and_format_csv(_filename)

    # Format the df_raw & take out the units
    df_formatted = format(df_raw)

    # Store the names of the columns for calling
    array_columns = df_formatted.columns

    # Dropping(Hidding) the outlier data and draw the bubble chart
    df_no_outlier = drop_outlier(df_formatted)
    draw_bubble_chart(df_x=df_no_outlier[array_columns[0]],
                      df_y=df_no_outlier[array_columns[1]],
                      df_z=df_no_outlier[array_columns[2]])

    plt.show()