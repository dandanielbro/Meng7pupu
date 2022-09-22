# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statsmodels.api as sm
import os

# Global parmeters
filename = "raw_data.csv"

# def draw_scatter(x_data, y_data):

def read_and_format_csv(filename):
    try:
        # Read csv file and ust 'tab' as delimiter
        df = pd.read_csv(filename, delimiter=',')

        # If the file is not seperated by common raise exception and use common as delimiter
        if(df.shape[1] != 4):
            raise Exception("Input file is not seperated by ','")

    except Exception:
        print("Use 'tab' as the delimiter")

        # Read csv file and ust 'tab' as delimiter
        df = pd.read_csv(filename, delimiter='\t')

    # Drop the time columns
    df.drop(df.columns[0], axis=1, inplace=True)

    return df

def drop_outlier(df):
    # Format the dataframe
    df_formatted, _ = format_and_get_unit(df)

    array_columns = df_formatted.columns

    print(df_formatted.shape)

    # Drop the data which is greater than 50 or less than 0
    df_formatted.drop(df_formatted[(df_formatted[array_columns[2]] > 200) | (df_formatted[array_columns[2]] < 0)].index, inplace=True)
    print(df_formatted.shape)

    return df_formatted

def format_and_get_unit(df):
    # take out the unit from the df
    unit = df.iloc[[0]]
    
    # Drop the unit from the df
    df.drop(index=0, axis=1, inplace=True)
    
    # Transform the type of df into float64
    df = df.astype('float64')

    return df, unit
    

def generate_OLS_model(df_x, df_y):
    model = sm.OLS(df_y, sm.add_constant(df_x))
    model_fit = model.fit()
    p = model_fit.params
    print(p)

    return p

def draw_scatter_with_OLS(df_x, df_y):
    # Format the dataframe
    df_x_formatted, unit_x = format_and_get_unit(df_x)
    df_y_formatted, unit_y = format_and_get_unit(df_y)
    
    # Generate linear coefficient of OLS
    para_for_OLS = generate_OLS_model(df_x_formatted, df_y_formatted)

    # Generate figure
    fig, ax = plt.subplots()

    # Scatter plot
    ax.scatter(df_x_formatted, df_y_formatted, s=20, c="black")

    # Draw OLS on axes
    ax.plot(df_x_formatted, (para_for_OLS[0] + para_for_OLS[1]*df_x_formatted), 'r-')
    
    ax.set_xlabel(df_x.name)
    ax.set_ylabel(df_y.name)

def draw_bubble_chart(df_x, df_y, df_z):
    # Format the dataframe
    df_x_formatted, unit_x = format_and_get_unit(df_x)
    df_y_formatted, unit_y = format_and_get_unit(df_y)
    df_z_formatted, unit_z = format_and_get_unit(df_z)

    # Normalize the df_z to [0, 1]
    diff = df_z_formatted.max() - df_z_formatted.min()
    df_z_norm = (df_z_formatted-df_z_formatted.min())/diff

    fig, ax = plt.subplots()

    ax.scatter(df_x_formatted, df_y_formatted, s=df_z_norm*100, alpha=0.5)
    ax.set_xlabel(df_x.name)
    ax.set_ylabel(df_y.name)


if __name__ == "__main__":
    # Read the csv file into a dataframe and drop the time columns
    df_raw = read_and_format_csv(filename)

    # Store the names of the columns for calling
    array_columns = df_raw.columns

    # Drawing the scatter plot and the OLS line
    draw_scatter_with_OLS(df_x=df_raw[array_columns[0]], df_y=df_raw[array_columns[1]])

    # Dropping(Hidding) the outlier data and draw the bubble chart
    df_no_outlier = drop_outlier(df_raw)
    draw_bubble_chart(df_x=df_no_outlier[array_columns[0]], df_y=df_no_outlier[array_columns[1]], df_z=df_no_outlier[array_columns[2]])

    plt.show()