import requests
import pandas as pd
from datetime import datetime
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import numpy as np
import traceback

# sendPhoto_bot_url = "https://api.telegram.org/bot6905941845:AAEE8qD7HZ0GJYO5BT6kvoATAi1jFBFGF0g/sendPhoto"
file = open(r'C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\telegram bot\\log.txt', 'a')
bot_token = "6905941845:AAEE8qD7HZ0GJYO5BT6kvoATAi1jFBFGF0g"
chat_id = "-4171022632"
def send_photo(bot_token, chat_id, photo_path, caption):
    send_photo_bot_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    photo = {"photo": open(photo_path, 'rb')}
    parameters = {
        "chat_id": chat_id,
        "caption": caption
    }
    response = requests.post(send_photo_bot_url, data=parameters, files=photo)
    return response.json()
try:
    # Load the GeoJSON file
    gdf_states = gpd.read_file("C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\GeoJSON Malaysia\\malaysia_singapore_brunei_State level 1.geojson")
    daily_donation_data = pd.read_csv("https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/donations_state.csv")
    returning_donor_data = pd.read_parquet("https://dub.sh/ds-data-granular")
    malaysia_data = daily_donation_data[daily_donation_data['state']=='Malaysia']
    malaysia_states_data = daily_donation_data[daily_donation_data['state'] != 'Malaysia']
    malaysia_states_data['date'] = pd.to_datetime(malaysia_states_data['date'])

    returning_donor = returning_donor_data.loc[returning_donor_data["donor_id"].duplicated()]
    all_donor = int(returning_donor_data['donor_id'].nunique())
    returning_donor_count = int(returning_donor['donor_id'].nunique())
    distinct_donor_data = returning_donor.drop_duplicates(subset='donor_id', keep='last')
    num_people_coming_more_than_once = int(len(distinct_donor_data))

    distinct_donor_data['visit_date'] = pd.to_datetime(distinct_donor_data['visit_date'])
    distinct_donor_data['Age'] = distinct_donor_data['visit_date'].dt.year - distinct_donor_data['birth_date']

    bin_edges = range(0, 110, 10)
    # Create the histogram
    plt.hist(distinct_donor_data['Age'], bins=bin_edges)

    # Customize the plot
    plt.title("Demographic of Returning donor")
    plt.xlabel("Age")
    plt.ylabel("Frequency")

    # Save the histogram as a PNG image
    plt.savefig("C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\age_demographic_of_returning_donor.png")

    percentage_return = returning_donor_count / all_donor * 100
    percentage_return = round(percentage_return, 2)


    # Calculate the histogram using NumPy
    counts, bins = np.histogram(distinct_donor_data['Age'], bins=bin_edges)

    # Optionally, create a DataFrame for further analysis
    histogram_data = pd.DataFrame({"bin_edges": bins[:-1], "frequency": counts})

    # Find the index of the maximum frequency
    max_frequency_index = histogram_data['frequency'].idxmax()

    # Retrieve the corresponding bin edge
    max_bin_edge = histogram_data.loc[max_frequency_index, 'bin_edges']

    # Frequency max bin
    highest_frequency= histogram_data['frequency'].max()

    last_30days_data_malaysia = malaysia_data.tail(30)

    # Change 'date' datatype to datetime
    last_30days_data_malaysia['date'] = pd.to_datetime(last_30days_data_malaysia['date'])

    # Extract the day of the week
    last_30days_data_malaysia['day_of_week'] = last_30days_data_malaysia['date'].dt.day_name()

    # Group by day of the week and calculate the mean value for each day
    daily_summary = last_30days_data_malaysia.groupby('day_of_week')['daily'].mean()

    # Create a DataFrame from the daily summary
    daily_summary_df = pd.DataFrame({
        'Day of the Week': daily_summary.index,
        'Mean Daily Value': daily_summary.values
    })
    day_highest_value = daily_summary.idxmax()
    highest_value_daily = daily_summary.max()
    day_lowest_value = daily_summary.idxmin()
    lowest_value_daily = daily_summary.min()

    plt.figure(figsize=(18, 10))
    plt.plot(last_30days_data_malaysia['date'], last_30days_data_malaysia['daily'], color='red', linestyle='-', linewidth=2)
    plt.fill_between(last_30days_data_malaysia['date'], last_30days_data_malaysia['daily'], color = 'lightcoral')
    plt.title("Daily Trends of Blood Donor for Past Month in Malaysia")
    plt.xticks(last_30days_data_malaysia['date'], rotation = 45)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xlabel("Dates")
    plt.ylabel("Daily Donors")

    # save plot
    pic_daily_trend = plt.savefig("C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\daily_trends_of_blood_donor_for_past_week.png")

    copy_malaysia_data = malaysia_data.copy()
    # Change 'date' datatype to datetime
    copy_malaysia_data['date'] = pd.to_datetime(copy_malaysia_data['date'])
    copy_malaysia_data = copy_malaysia_data.set_index(['date'])
    # Identify numeric columns excluding 'object' columns
    numeric_columns = copy_malaysia_data.select_dtypes(exclude='object').columns
    # Resample data and calculate monthly mean
    data_weekly = copy_malaysia_data[numeric_columns].resample('W').mean().reset_index()
    
    # subset for 1 year data 
    data_weekly_subset = data_weekly.tail(52)

    # Calculate highest, lowest value for weekly
    highest_donor_weekly_index = data_weekly_subset['date'].idxmax()
    highest_donor_weekly_value =  round(data_weekly_subset['daily'].max(), 2)
    date_highest_donor_weekly = data_weekly.loc[highest_donor_weekly_index, 'date'].week
    lowest_donor_weekly_index = data_weekly_subset['date'].idxmin()
    lowest_donor_weekly_value =  round(data_weekly_subset['daily'].min(), 2)
    date_lowest_donor_weekly = data_weekly_subset.loc[lowest_donor_weekly_index, 'date'].week

    # Extract date and value columns
    dates_w = data_weekly_subset['date']
    values_w = data_weekly_subset['daily']

    # Seperate data to train simple linear regression model
    X = np.arange(len(dates_w)).reshape(-1, 1)
    y = values_w.values.reshape(-1, 1)

    # Fit linear regression model
    model_w = LinearRegression()
    model_w.fit(X, y)

    # Get the trend line
    trend_line_w = model_w.predict(X)
    trend_slope_w = model_w.coef_[0][0]
    # Interpretation based on trend slope
    if trend_slope_w > 0:
        trend_interpretation_w = "Based on the Trend Line, there are increasing trend of blood donation by weekly for the past year in Malaysia."
    elif trend_slope_w < 0:
        trend_interpretation_w = "Based on the Trend Line, there are decreasing trend of blood donation by weekly for the past year in Malaysia."
    else:
        trend_interpretation_w = "No significant trend observed of blood donation by weekly for the past year in Malaysia."

    # Create the plot with Matplotlib
    plt.figure(figsize=(15, 5))
    plt.plot(dates_w, values_w, linestyle='-', color='red', label='Blood Donor Weekly Mean')
    plt.plot(dates_w, trend_line_w, linestyle='--', color='blue', label='Trend Line')
    plt.fill_between(dates_w, values_w, color = 'lightcoral')
    # Customize plot
    plt.title("Weekly Trends of Blood Donor for Past Year in Malaysia")
    plt.xlabel("Dates")
    plt.ylabel("Average Weekly Donors")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save plot
    pic_weekly_trend = plt.savefig("C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\weekly_trends_of_blood_donor_for_past_year.png")

    # Identify numeric columns excluding 'object' columns
    numeric_columns = copy_malaysia_data.select_dtypes(exclude='object').columns

    # Resample data and calculate monthly sum
    data_monthly = copy_malaysia_data[numeric_columns].resample('M').sum().reset_index()
    data_monthly_subset = data_monthly.tail(120)
    # Change datatype to datetime
    data_monthly_subset['date'] = pd.to_datetime(data_monthly_subset['date'])

    # Extract the month name
    data_monthly_subset['Month'] = data_monthly_subset['date'].dt.month_name()

    # Group by day of the week and calculate the mean value for each month
    monthly_summary = data_monthly_subset.groupby('Month')['daily'].mean()
    # Calculate monthly highest, lowest donor value
    monthly_highest_value_index = monthly_summary.idxmax()
    highest_value_monthly = round(monthly_summary.max(),2)
    monthly_lowest_value_index = monthly_summary.idxmin()
    lowest_value_monthly = round(monthly_summary.min(), 2)
    # Extract date and value columns
    dates_m = data_monthly_subset['date']
    values_m = data_monthly_subset['daily']

    X = np.arange(len(dates_m)).reshape(-1, 1)
    y = values_m.values.reshape(-1, 1)

    # Fit linear regression model
    model_m = LinearRegression()
    model_m.fit(X, y)

    # Get the trend line
    trend_line_m = model_m.predict(X)
    trend_slope_m = model_m.coef_[0][0]

    # Interpretation based on trend slope
    if trend_slope_m > 0:
        trend_interpretation_m = "Based on the Trend Line, there are increasing trend of blood donation by Monthly for the past 10 years in Malaysia."
    elif trend_slope_m < 0:
        trend_interpretation_m = "Based on the Trend Line, there are decreasing trend of blood donation by Monthly for the past 10 years in Malaysia."
    else:
        trend_interpretation_m = "No significant trend found throughout monthly donor as it remain same. KKM need to step up blood donation campaign."

    # Create the plot with Matplotlib
    plt.figure(figsize=(15, 5))
    plt.plot(dates_m, values_m, linestyle='-', color='red', label='Blood Donor Monthly Mean')
    plt.plot(dates_m, trend_line_m, linestyle='--', color='blue', label='Trend Line')
    plt.fill_between(dates_m, values_m, color = 'lightcoral')
    # Customize plot
    plt.title("Monthly Trends of Blood Donor for Last 10 Years in Malaysia")
    plt.xlabel("Dates")
    plt.ylabel("Average Monthly Donors")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # save plot
    pic_montly_trend = plt.savefig("C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\monthly_trends_of_blood_donor_for_10_years.png")

    # Identify numeric columns excluding 'object' columns
    numeric_columns = copy_malaysia_data.select_dtypes(exclude='object').columns

    # Resample data and calculate monthly mean
    data_yearly = copy_malaysia_data[numeric_columns].resample('Y').sum().reset_index()

    # Extract date and value columns
    dates = data_yearly['date']
    values = data_yearly['daily']  # Assuming 'daily' is your value column

    X = np.arange(len(dates)).reshape(-1, 1)
    y = values.values.reshape(-1, 1)

    # Fit linear regression model
    model_y = LinearRegression()
    model_y.fit(X, y)

    # Get the trend line
    trend_line_y = model_y.predict(X)
    trend_slope_y = model_y.coef_[0][0]
    # Interpretation based on trend slope
    if trend_slope_y > 0:
        trend_interpretation_y = "Based on the Trend Line, there are increasing trend of blood donation for the past years in Malaysia. This is a promising sign for healthcare and blood donation awareness programs."
    elif trend_slope_y < 0:
        trend_interpretation_y = "Based on the Trend Line, there are decreasing trend of blood donation for the past years in Malaysia. The KKM need to find out what went wrong with their campaign to promote blood donations."
    else:
        trend_interpretation_y = "No significant trend recorded, the trend remain constant throughout the year."

    # Create the plot with Matplotlib
    plt.figure(figsize=(15, 5))
    plt.plot(dates, values, linestyle='-', color='red', label='Blood Donor Yearly Mean')
    plt.plot(dates, trend_line_y, linestyle='--', color='blue', label='Trend Line')
    plt.fill_between(dates, values, color = 'lightcoral')

    # Customize plot
    plt.title("Yearly Trends of Blood Donor in Malaysia")
    plt.xlabel("Dates")
    plt.ylabel("Sum Yearly Donor")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # save plot
    pic_yearly_trend = plt.savefig("C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\yearly_trends_of_blood_donor.png")

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
    ax.set_title('Heatmap of Donor Percentage by States for Year 2023')

    # Plot the choropleth map
    merged_data.plot(column='daily', cmap='OrRd', linewidth=0.5, ax=ax, edgecolor='0.8')

    # Add labels for states
    for x, y, label in zip(merged_data.geometry.centroid.x, merged_data.geometry.centroid.y, merged_data['shapename']):
        ax.text(x, y, label, fontsize=8, ha='center', va='center')

    # Create colorbar as a legend
    sm = plt.cm.ScalarMappable(cmap='OrRd', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    # add the colorbar to the figure
    cbar = fig.colorbar(sm, ax=ax, location = 'bottom')
    # find out highest value and state
    highestState_index = data_percentage_contribution['daily'].idxmax()
    highest_percentage = data_percentage_contribution['daily'].max()
    state_name_highest = data_percentage_contribution.loc[highestState_index, 'state']
    #saving our map as .png file.
    pic_map_donor = fig.savefig('C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\map_donor_percentage_by_state.png')

    photo_paths = [
        "C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\daily_trends_of_blood_donor_for_past_week.png",
        "C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\weekly_trends_of_blood_donor_for_past_year.png",
        "C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\monthly_trends_of_blood_donor_for_10_years.png",
        "C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\yearly_trends_of_blood_donor.png",
        "C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\map_donor_percentage_by_state.png",
        "C:\\Users\\PC\\OneDrive - Universiti Malaya\\Documents\\Github Project\\Blood-Donation-Automation\\Visualization\\age_demographic_of_returning_donor.png"
    ]

    captions = [
        f"The line area chart shows that there are trend of which days is the favourite blood donate day. which is {day_highest_value} with an average of {highest_value_daily}. Meanwhile {day_lowest_value} is the least likely people will donate their blood with an average of {lowest_value_daily}.",
        f"{trend_interpretation_w} We can also see that there are outlier where on week {date_highest_donor_weekly} with {highest_donor_weekly_value} meanwhile on week {date_lowest_donor_weekly} is the lowest donor donation recorded with {lowest_donor_weekly_value}. This might be because there are seasonality such as public holiday in Malaysia. Further investigation needed.",
        f"{trend_interpretation_m} We can also observed that there are month where on average, donors mostly donate blood on the month {monthly_highest_value_index} with {highest_value_monthly}. Meanwhile on month {monthly_lowest_value_index} with {lowest_value_monthly}.",
        f"{trend_interpretation_y}",
        f"Based on the map plot, we can see that {state_name_highest} have the highest percentage of donor for the year {current_year-1} contribute a total of {highest_percentage}%. Based on https://data.moh.gov.my/dashboard/blood-donation, the W.P Kuala Lumpur may be higher than the true donor rate (and Selangor lower) due to data from the National Blood Center's mobile campaigns around Selangor and W.P Putrajaya being recorded as data from W.P Kuala Lumpur.",
        f"The age demographic shows that blood donor around the age {max_bin_edge} to {max_bin_edge+10} is the most frequent returning blood donor with {highest_frequency}. Percentage of people will donate their blood again is {percentage_return}% with out of {all_donor} donors, {returning_donor_count} donors coming back to repeat blood donation.",
    ]

    for photo_path, caption in zip(photo_paths, captions):
        send_photo(bot_token, chat_id, photo_path, caption)
    file.write(f'{datetime.now()} - script successfully run \n')
    file.close()
except Exception as e:
    traceback.print_exc(file=file)
    file.write(f'{datetime.now()} - {e}\n')
    file.close()