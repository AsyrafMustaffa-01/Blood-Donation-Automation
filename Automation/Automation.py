import requests
import datetime
import pandas as pd
import plotly.express as px
from datetime import datetime
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

sendPhoto_bot_url = "https://api.telegram.org/bot6905941845:AAEE8qD7HZ0GJYO5BT6kvoATAi1jFBFGF0g/sendPhoto"
file = open(r'C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\telegram bot\\log.txt', 'a')
# Load the GeoJSON file
gdf_states = gpd.read_file("malaysia_singapore_brunei_State level 1.geojson")

try:
    daily_donation_data = pd.read_csv("https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/donations_state.csv")
    returning_donor_data = pd.read_parquet("https://dub.sh/ds-data-granular")
    malaysia_data = daily_donation_data[daily_donation_data['state']=='Malaysia']
    malaysia_states_data = daily_donation_data[daily_donation_data['state'] != 'Malaysia']
    malaysia_states_data['date'] = pd.to_datetime(malaysia_states_data['date'])

    last_30days_data_malaysia = malaysia_data.tail(30)
    plt.figure(figsize=(18, 10))
    plt.plot(last_30days_data_malaysia['date'], last_30days_data_malaysia['daily'], color='red', linestyle='-', linewidth=2)

    plt.title("Daily Trends of Blood Donor for Past Week in Malaysia")
    plt.xticks(last_30days_data_malaysia['date'], rotation = 45)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xlabel("Dates")
    plt.ylabel("Daily Donors")

    # save plot
    plt.savefig("C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\daily_trends_of_blood_donor_for_past_week.png")

    # data_m['date'] = pd.to_datetime(malaysia_data['date'])
    # data_m = malaysia_data.set_index(['date'])
    copy_malaysia_data = malaysia_data.copy()
    # Identify numeric columns excluding 'object' columns
    numeric_columns = copy_malaysia_data.select_dtypes(exclude='object').columns

    # Resample data and calculate monthly mean
    data_weekly = copy_malaysia_data[numeric_columns].resample('W').mean().reset_index()

    # Extract date and value columns
    dates = data_weekly['date'].tail(52)
    values = data_weekly['daily'].tail(52)

    # Create the plot with Matplotlib
    plt.figure(figsize=(15, 5))
    plt.plot(dates, values, linestyle='-', color='red')

    # Customize plot
    plt.title("Weekly Trends of Blood Donor for Past Year in Malaysia")
    plt.xlabel("Dates")
    plt.ylabel("Average Weekly Donors")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save plot
    plt.savefig("C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\weekly_trends_of_blood_donor_for_past_year.png")

    # Identify numeric columns excluding 'object' columns
    numeric_columns = copy_malaysia_data.select_dtypes(exclude='object').columns

    # Resample data and calculate monthly mean
    data_monthly = copy_malaysia_data[numeric_columns].resample('M').mean().reset_index()

    # Extract date and value columns
    dates = data_monthly['date'].tail(120)
    values = data_monthly['daily'].tail(120)

    # Create the plot with Matplotlib
    plt.figure(figsize=(15, 5))
    plt.plot(dates, values, linestyle='-', color='red')

    # Customize plot
    plt.title("Monthly Trends of Blood Donor for Last 10 Years in Malaysia")
    plt.xlabel("Dates")
    plt.ylabel("Average Monthly Donors")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # save plot
    plt.savefig("C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\monthly_trends_of_blood_donor_for_10_years.png")

    # Identify numeric columns excluding 'object' columns
    numeric_columns = copy_malaysia_data.select_dtypes(exclude='object').columns

    # Resample data and calculate monthly mean
    data_yearly = copy_malaysia_data[numeric_columns].resample('Y').mean().reset_index()

    # Extract date and value columns
    dates = data_yearly['date']
    values = data_yearly['daily']  # Assuming 'daily' is your value column

    # Create the plot with Matplotlib
    plt.figure(figsize=(15, 5))
    plt.plot(dates, values, linestyle='-', color='red')

    # Customize plot
    plt.title("Yearly Trends of Blood Donor in Malaysia")
    plt.xlabel("Dates")
    plt.ylabel("Average Yearly Numbers")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # save plot
    plt.savefig("C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\yearly_trends_of_blood_donor.png")

    current_year = datetime.today().year
    data_2023 = malaysia_states_data[malaysia_states_data['date'].dt.year == current_year-1]
    data_2023.head()
    annual_totals = data_2023.groupby('state')['daily'].sum()
    nation_total = data_2023['daily'].sum()
    percentage_contributions = (annual_totals / nation_total) * 100
    percentage_contributions = percentage_contributions.round(2)  # Round to 2 decimal places
    data_percentage_contribution = pd.DataFrame(percentage_contributions)
    data_percentage_contribution=data_percentage_contribution.reset_index()

    data_percentage_contribution.loc[data_percentage_contribution['state'] == 'Melaka', 'state'] = 'Malacca'
    data_percentage_contribution.loc[data_percentage_contribution['state'] == 'W.P. Kuala Lumpur', 'state'] = 'Kuala Lumpur'
    data_percentage_contribution.loc[data_percentage_contribution['state'] == 'Pulau Pinang', 'state'] = 'Penang'

    # Check if "Perlis" is in the 'state' column
    if 'Perlis' not in data_percentage_contribution['state'].values:
        # Adding a new row for Perlis
        new_row = pd.DataFrame({'state': 'Perlis', 'daily': 0.0}, index=[0])
        data_percentage_contribution = pd.concat([data_percentage_contribution, new_row], axis=0, ignore_index=True)

    # Merge the GeoPandas DataFrame with the DataFrame containing your data
    merged_data = gdf_states.merge(data_percentage_contribution, left_on='shapename', right_on='state')
    # set the range for the choropleth
    vmin, vmax = data_percentage_contribution['daily'].min(), data_percentage_contribution['daily'].max()
    # Plotting the map
    fig, ax = plt.subplots(1, 1, figsize=(15, 8))
    ax.set_title('Heatmap of Donor Percentage Contribution by State')

    # Plot the choropleth map
    merged_data.plot(column='daily', cmap='OrRd', linewidth=0.5, ax=ax, edgecolor='0.8')

    # Create colorbar as a legend
    sm = plt.cm.ScalarMappable(cmap='OrRd', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    # add the colorbar to the figure
    cbar = fig.colorbar(sm, ax=ax, location = 'bottom')
    # Display the map
    plt.show()
    #saving our map as .png file.
    fig.savefig('C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\map_donor_percentage_by_state.png')

    returning_donor = returning_donor_data.loc[returning_donor_data["donor_id"].duplicated()]

    one_time_donor = returning_donor_data[~returning_donor_data["donor_id"].isin(returning_donor["donor_id"])]

    all_donor = int(returning_donor_data['donor_id'].nunique())
    returning_donor_count = int(returning_donor['donor_id'].nunique())
    non_returning_donor_count = int(len(one_time_donor))

    percentage_return = (returning_donor_count / all_donor * 100)
    formatted_percentage_returning_donor = f"{percentage_return:.2f}"  # Format as string
    # print(formatted_percentage+"%")

    percentage_not_return = non_returning_donor_count/all_donor * 100
    formatted_percentage_non_return = f"{percentage_not_return:.2f}"
    # print(formatted_percentage_non_return+"%")

    one_time_donor['visit_date'] = pd.to_datetime(one_time_donor['visit_date'])
    one_time_donor['Age'] = one_time_donor['visit_date'].dt.year - one_time_donor['birth_date']
    distinct_donor_data = returning_donor.drop_duplicates(subset='donor_id', keep='last')
    num_people_coming_more_than_once = int(len(distinct_donor_data))
    # print("Number of people coming more than once:", num_people_coming_more_than_once)

    distinct_donor_data['visit_date'] = pd.to_datetime(distinct_donor_data['visit_date'])
    distinct_donor_data['Age'] = distinct_donor_data['visit_date'].dt.year - distinct_donor_data['birth_date']

    bin_edges = range(0, 110, 10)
    # Create the histogram
    plt.hist(one_time_donor['Age'], bins=bin_edges)  # Adjust bins as needed

    # Customize the plot
    plt.title("Demographic of Non Returning donor")
    plt.xlabel("Ages")
    plt.ylabel("Frequency")
    plt.grid(False)  # Show grid on both axes

    # Save the histogram as a PNG image
    plt.savefig("C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\age_demographic_of_non_returning_donor.png")

    # Create the histogram
    plt.hist(distinct_donor_data['Age'], bins=bin_edges)  # Adjust bins as needed

    # Customize the plot
    plt.title("Demographic of Returning donor")
    plt.xlabel("Values")
    plt.ylabel("Frequency")
    plt.grid(False)  # Show grid on both axes

    # Save the histogram as a PNG image
    plt.savefig("C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\age_demographic_of_returning_donor.png")

    # Calculate the histogram using NumPy
    counts, bins = np.histogram(distinct_donor_data['Age'], bins=bin_edges)

    # Print the bin edges and frequencies
    print("Bin Edges:", bins)
    print("Frequencies:", counts)

    # Optionally, create a DataFrame for further analysis
    histogram_data = pd.DataFrame({"bin_edges": bins[:-1], "frequency": counts})

    # Find the index of the maximum frequency
    max_frequency_index = histogram_data['frequency'].idxmax()

    # Retrieve the corresponding bin edge
    max_bin_edge = histogram_data.loc[max_frequency_index, 'bin_edges']

    photo = {"photo" : open("C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\age_demographic_of_returning_donor", 'rb')}

    parameter = {
    "chat_id" : "-4171022632",
    "caption" : f"The age demographic shows that blood donor around the age {max_bin_edge} to {max_bin_edge+10} is the most frequent returning blood donor."
    }

    resp_sendPhoto = requests.get(sendPhoto_bot_url, data=parameter, files=photo)

    file.write(f'{datetime.datetime.now()} - script successfully run \n')
except Exception:
    file.write(f'{datetime.datetime.now()} - {Exception} \n')