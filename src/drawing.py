# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import os

# Global parmeters
filename = "raw_data.csv"

# def draw_scatter(x_data, y_data):

def read_and_format_csv(filename):
    # Read csv file and ust 'tab' as delimiter
    df = pd.read_csv(filename, delimiter='\t')

    # Drop the time columns
    df.drop(df.columns[0], axis=1, inplace=True)

    return df

def generate_OLS_model(df_x, df_y):
    model = sm.OLS(df_y, sm.add_constant(df_x))
    model_fit = model.fit()
    p = model_fit.params
    print(p)

    return p

def draw_scatter_with_OLS(df_x, df_y, df_z):
    # Generate linear coefficient of OLS
    para_for_OLS = generate_OLS_model(df_x, df_z)

    # Generate figure
    fig, ax = plt.subplots()

    # Scatter plot
    ax.scatter(df_x, df_y, s=20, c="black")

    # Draw OLS on axes
    ax.plot(df_x, (para_for_OLS[0] + para_for_OLS[1]*df_x), 'r-')
    
    ax.set_xlabel(df_x.name)
    ax.set_ylabel(df_y.name)

def draw_bubble_chart(df_x, df_y, df_z):
    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(df_z.min(), df_z.max())

    fig, ax = plt.subplots()

    mappable = ax.scatter(df_x, df_y, c=df_z, cmap="bwr", norm=norm, alpha=0.5)
    ax.set_xlabel(df_x.name)
    ax.set_ylabel(df_y.name)
    fig.colorbar(mappable, ax=ax)


if __name__ == "__main__":
    df_raw = read_and_format_csv(filename)
    array_columns = df_raw.columns
    print(array_columns)
    draw_scatter_with_OLS(df_x=df_raw[array_columns[0]], df_y=df_raw[array_columns[1]], df_z=df_raw[array_columns[2]])
    draw_bubble_chart(df_x=df_raw[array_columns[0]], df_y=df_raw[array_columns[1]], df_z=df_raw[array_columns[2]])

    plt.show()