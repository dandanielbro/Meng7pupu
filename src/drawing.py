# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import cm
# from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
# import numpy as np
import pandas as pd
# import statsmodels.api as sm

# Global paarmeters
filename = "raw_data.csv"

# def draw_scatter(x_data, y_data):

def read_and_format_csv(filename):
    # Read csv file and ust 'tab' as delimiter
    df = pd.read_csv(filename, delimiter='\t')

    # Drop the time columns
    df.drop(df.columns[0], axis=1, inplace=True)

    return df

def draw_scatter_with_OSL(df_x, df_y):
    plt.scatter(df_x, df_y, s=30)
    plt.xlabel(df_x.name)
    plt.ylabel(df_y.name)
    plt.show()

def draw_bubble_chart(df_x, df_y, df_z):
    # Normalize the data to range [0,1]
    # print(df_z.max())
    # print(df_z.min())
    # range_diff = df_z.max() - df_z.min()
    # min = df_z.min()
    # df_z = (df_z-min)/range_diff
    # print(df_z*100)
    # print(df_z.max())
    # print(df_z.min())

    plt.scatter(df_x, df_y, s=(df_z+200), alpha=0.6)
    plt.xlabel(df_x.name)
    plt.ylabel(df_y.name)
    plt.show()

def draw_surface_plot(df_x, df_y, df_z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.bar(df_x, df_y, df_z, zdir='y')

    plt.xlabel(df_x.name)
    plt.ylabel(df_y.name)

    plt.show()

if __name__ == "__main__":
    df_raw = read_and_format_csv(filename)
    array_columns = df_raw.columns
    # draw_scatter_with_OSL(df_x=df_raw[array_columns[1]], df_y=df_raw[array_columns[0]])
    draw_bubble_chart(df_x=df_raw[array_columns[0]], df_y=df_raw[array_columns[1]], df_z=df_raw[array_columns[2]])
    # draw_surface_plot(df_x=df_raw[array_columns[0]], df_y=df_raw[array_columns[1]], df_z=df_raw[array_columns[2]])
    # print(df_raw)
