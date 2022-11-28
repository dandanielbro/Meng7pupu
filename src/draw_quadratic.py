# draw_quadratic.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Global parameters
_filename = "example_data/ols.csv"
_title = "Quadratic"

# Configuration
plt.rcParams['font.sans-serif'] = ['Times New Roman']

title_x_axis = "Sonic Temperature"
title_y_axis = "Shortwave Radiation"

unit_x_axis = r'$^oC$'
unit_y_axis = r'$W/m^2$'

def read_and_format_csv(filename):
    try:
        # Read csv file and use 'tab' as delimiter
        df = pd.read_csv(filename, delimiter=',')

        # If the file is not seperated by common raise exception and use common as delimiter
        if(df.shape[1] != 2):
            raise Exception("Input file is not seperated by ','")

    except Exception:
        print("Use 'tab' as the delimiter")

        # Read csv file and ust 'tab' as delimiter
        df = pd.read_csv(filename, delimiter='\t')

    # Drop the time columns
    # df.drop(df.columns[0], axis=1, inplace=True)

    return df

def format(df):
    # Transform the type of df into float64,
    df = df.astype('float64')

    return df

def log_out(filename, message):
    with open(filename, 'w') as f:
        print(message, file=f)

def draw_scatter_with_quadratic(df_x, df_y):
    # Generate coefficients of quadratic 
    coef = np.polyfit(df_x, df_y, 2)
    df_y_fit = np.polyval(coef, df_x)

    # Generate figure
    fig, ax = plt.subplots()

    # Scatter plot
    ax.scatter(df_x, df_y, s=20, c="black", label="Original Data")

    # Draw OLS on axes
    ax.plot(df_x, df_y_fit, 'r-',
            label="Quadratic curve")
    
    # Put the title
    ax.set_title(_title)

    # Put the label on each axis
    ax.set_xlabel(f"{title_x_axis} ({unit_x_axis})")
    ax.set_ylabel(f"{title_y_axis} ({unit_y_axis})")

    # Put the legend on the chart
    ax.legend()

if __name__ == "__main__":
    # Read the csv file into a dataframe and drop the time columns
    df_raw = read_and_format_csv(_filename)

    # Format the df_raw & take out the units
    df_formatted = format(df_raw)

    # Store the names of the columns for calling
    array_columns = df_formatted.columns

    # Sorting the dataframe according to the x value
    df_formatted.sort_values(by=array_columns[0], inplace=True)

    # Drawing the scatter plot and the quadratic curve
    draw_scatter_with_quadratic(df_x=df_formatted[array_columns[0]],
                                df_y=df_formatted[array_columns[1]])

    plt.show()