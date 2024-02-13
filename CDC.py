import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pytz

def plot_radon_comparison(Radon Comparison Graphs\CCF_radon_2022-08-31__2023-02-24_Wind_Plot_Ready.csv):
    # Load data
    data = pd.read_csv(filename)

    # Create timezone objects
    utc_tz = pytz.timezone('UTC')
    mt_tz = pytz.timezone('US/Mountain')

    # Convert time column from UTC to Mountain Standard Time
    data['time'] = pd.to_datetime(data['time']).dt.tz_localize(utc_tz).dt.tz_convert(mt_tz)

    # Extract the hour of day
    hour = data['time'].dt.hour

    # Compute the mean values for each hour
    quartiles = data.groupby(hour)['radon_B'].quantile([0.25, 0.5, 0.75]).unstack()

    # Compute the outliers for each hour
    outliers = pd.DataFrame(columns=['hour', 'radon_B'])
    for h in range(24):
        q1, q3 = quartiles.loc[h, 0.25], quartiles.loc[h, 0.75]
        iqr = q3 - q1
        upper = q3 + 1.5 * iqr
        lower = q1 - 1.5 * iqr
        out = data.loc[(hour == h) & ((data['radon_B'] > upper) | (data['radon_B'] < lower)), ['time', 'radon_B']]
        out['hour'] = h
        outliers = outliers.append(out, ignore_index=True)

    # Set plot parameters
    plt.rcParams["figure.figsize"] = (14, 9)
    sns.set(style='darkgrid', font_scale=2.2)

    # Plot the results
    fig, ax = plt.subplots()
    colors = plt.cm.Set2(np.linspace(0, 1, 24))
    for h in range(24):
        ax.boxplot(data.loc[hour == h, 'radon_B'], positions=[h], widths=0.6, showmeans=True, showfliers=True, boxprops=dict(color=colors[h], linewidth=2.5), meanprops={"marker": "o", "markerfacecolor": "white", "markeredgecolor": "black", "markersize": "10"}, whis=[5, 95])
    ax.scatter(outliers['hour'], outliers['radon_B'], marker='o', facecolor='none', s=100, label='Outliers')
    ax.set_xlabel('Hour (MST)')
    ax.set_ylabel('Gas Phase Radiation (Bq/$\mathrm{m}^3$)')
    ax.set_title('Gas Phase Radiation at CCF, Dec 26, 2022, to Feb 23, 2023')
    plt.show()
    
    return fig
