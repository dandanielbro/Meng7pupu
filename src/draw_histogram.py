# draw_histogram.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Global parameters
_filename = "example_data/gwp_histogram.csv"
_title = "Global Warming Potential contrast with CH4 and CO2"

# Configuration
plt.rcParams['font.sans-serif'] = ['Times New Roman']

def draw_histogram(df=pd.DataFrame()):
    # Generate figure
    fig, ax = plt.subplots()

    # Generate m_xticks
    step = 5
    m_xticks = df.iloc[:,0][::step]
    print(m_xticks)

    # Draw histogram
    ax.bar(x=df.iloc[:,0],
           height=df.iloc[:,1],
           label="CO2")
    ax.bar(x=df.iloc[:,0],
           height=df.iloc[:,2],
           label="CH4",)
    ax.legend()
    ax.grid(linestyle=':')
    ax.set_xticks(ticks = np.arange(0, (len(df.iloc[:,0])), step),
                  labels = m_xticks,
                  rotation = 90)
    ax.set_title(_title)

    return None

def revise_dataframe(df=pd.DataFrame()):
    # Replace NaN with 0
    df.fillna(0, inplace=True)
    
    return df

if __name__ == "__main__":
    # Read the csv file into a dataframe
    df = pd.read_csv(_filename)

    # Revise the data
    df_revised = revise_dataframe(df)
    print(df_revised)

    # Draw the histogram
    draw_histogram(df_revised)
    
    plt.tight_layout()
    plt.show()