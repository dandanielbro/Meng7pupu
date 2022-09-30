import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

# Global parmeters
filename = "raw_data.csv"
upper_limit_of_normal_data = 200    # Will drop data greater than upper_limit in function-"drop_outlier"
lower_limit_of_normal_data = 0      # Will drop data less than lower_limit in function-"drop_outlier"
data_to_show = 50                   # Only annotate the data greater than or equal to "data_to_show" on bubble chart

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
    array_columns = df.columns
    amount_ori = df.shape[0]

    # Drop the data which is greater than upper_limit or less than lower_limit
    df.drop(df[(df[array_columns[2]] > upper_limit_of_normal_data) |
               (df[array_columns[2]] < lower_limit_of_normal_data)].index,
            inplace=True)
    amount_processed = df.shape[0]

    print(f"Find {amount_ori-amount_processed} outlier(s) on the raw_data.")

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
    

def generate_OLS_model(df_x, df_y):
    model = sm.OLS(df_y, sm.add_constant(df_x))
    model_fit = model.fit()
    p = model_fit.params
    print(f"Equation of OSL: y = {p[1]}*x + ({p[0]})")

    return p

def draw_scatter_with_OLS(df_x, df_y, unit_x=None, unit_y=None):
    # Generate linear coefficient of OLS
    para_for_OLS = generate_OLS_model(df_x, df_y)

    # Generate figure
    fig, ax = plt.subplots()

    # Scatter plot
    ax.scatter(df_x, df_y, s=20, c="black", label="Original Data")

    # Draw OLS on axes
    x_limit = (para_for_OLS[0]/para_for_OLS[1])*(-1)    # Get the x-value which leads to zero y-value
    df_drop_x = df_x[df_x >= x_limit]
    ax.plot(df_drop_x, (para_for_OLS[0] + para_for_OLS[1]*df_drop_x), 'r-',
            label=f"y = {format(para_for_OLS[1], '.3f')}*x + ({format(para_for_OLS[0], '.3f')})")
    
    # Put the label on each axis
    if unit_x is not None:
        ax.set_xlabel(df_x.name + f"  ({unit_x.item()})")
    else:
        ax.set_xlabel(df_x)

    if unit_y is not None:
        ax.set_ylabel(df_y.name + f"  ({unit_y.item()})")
    else:
        ax.set_ylabel(df_y)

    # Put the legend on the chart
    ax.legend()

def draw_bubble_chart(df_x, df_y, df_z, unit_x=None, unit_y=None, unit_z=None):
    # Normalize the df_z to [0, 1]
    diff = df_z.max() - df_z.min()
    df_z_norm = (df_z-df_z.min())/diff + 0.001

    fig, ax = plt.subplots()

    ax.scatter(df_x, df_y, s=df_z_norm*1000, alpha=0.5, label=f"{df_z.name}  ({unit_z.item()})")
    for i in range(0, df_x.shape[0]):
        z = df_z.iloc[i]
        if(z >= data_to_show):
            ax.annotate(str(round(z,2)), (df_x.iloc[i], df_y.iloc[i]))

    # Put the label on each axis
    if unit_x is not None:
        ax.set_xlabel(df_x.name + f"  ({unit_x.item()})")
    else:
        ax.set_xlabel(df_x)

    if unit_y is not None:
        ax.set_ylabel(df_y.name + f"  ({unit_y.item()})")
    else:
        ax.set_ylabel(df_y)

    # Put the legend on the chart
    ax.legend()

if __name__ == "__main__":
    # Read the csv file into a dataframe and drop the time columns
    df_raw = read_and_format_csv(filename)

    # Format the df_raw & take out the units
    df_formatted, units = format_and_get_unit(df_raw)

    # Store the names of the columns for calling
    array_columns = df_formatted.columns

    # Drawing the scatter plot and the OLS line
    draw_scatter_with_OLS(df_x=df_formatted[array_columns[0]], unit_x=units[array_columns[0]],
                          df_y=df_formatted[array_columns[1]], unit_y=units[array_columns[1]])

    # Dropping(Hidding) the outlier data and draw the bubble chart
    df_no_outlier = drop_outlier(df_formatted)
    draw_bubble_chart(df_x=df_no_outlier[array_columns[0]], unit_x=units[array_columns[0]],
                      df_y=df_no_outlier[array_columns[1]], unit_y=units[array_columns[1]],
                      df_z=df_no_outlier[array_columns[2]], unit_z=units[array_columns[2]])

    plt.show()