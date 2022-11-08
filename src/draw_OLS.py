# draw_OLS.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Global parameters
_filename = "example_data/ols.csv"
_title = "OLS"

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

def format_and_get_unit(df):
    # take out the unit from the df
    units = df.iloc[[0]]
    
    # Drop the unit from the df
    df.drop(index=0, axis=1, inplace=True)
    
    # Transform the type of df into float64,
    # type of units into string
    df = df.astype('float64')
    units = units.astype('str')

    return df, units

def log_out(filename, message):
    with open(filename, 'w') as f:
        print(message, file=f)

def generate_OLS_model(df_x, df_y):
    model = sm.OLS(df_y, sm.add_constant(df_x))
    model_fit = model.fit()
    p = model_fit.params
    print(f"Equation of OSL: y = {p[1]}*x + ({p[0]})")
    log_out("Summary_of_OSL.txt", model_fit.summary())

    return p

def draw_scatter_with_OLS(df_x, df_y):
    # Generate linear coefficient of OLS
    para_for_OLS = generate_OLS_model(df_x, df_y)

    # Generate figure
    fig, ax = plt.subplots()

    # Scatter plot
    ax.scatter(df_x, df_y, s=20, c="black", label="Original Data")

    # Draw OLS on axes
    x_limit = (para_for_OLS[0]/para_for_OLS[1])*(-1)    # Get the x-value which leads to zero y-value
    df_drop_x = df_x[df_x < x_limit]   # Filter out the x-value which the corresponding y-value will < 0
    ax.plot(df_drop_x, (para_for_OLS[0] + para_for_OLS[1]*df_drop_x), 'r-',
            label="Ordinary Least Squres")
    
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
    df_formatted, units = format_and_get_unit(df_raw)

    # Store the names of the columns for calling
    array_columns = df_formatted.columns

    # Drawing the scatter plot and the OLS line
    draw_scatter_with_OLS(df_x=df_formatted[array_columns[0]],
                          df_y=df_formatted[array_columns[1]])

    plt.show()