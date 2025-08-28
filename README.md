# Blood-Donation-Automation

## Overview

Blood-Donation-Automation is a data pipeline project inspired by the [KKM blood donation public dashboard](https://data.moh.gov.my/dashboard/blood-donation). It automates the process of fetching, transforming, visualizing, and sharing blood donation data with stakeholders via Telegram.

## Features

- **Automated Data Pipeline:** Pulls data from GitHub, processes it using ETL, and generates visualizations.
- **Data Visualization:** Uses `matplotlib` for charts and `geopandas` for map plotting.
- **Telegram Bot Integration:** Sends visualizations and updates to a Telegram group using the Telegram Bot API.
- **Scheduled Automation:** Runs daily at 9:00 AM via Windows Task Scheduler, even if the user is not logged in.

## Technologies Used

- **Python** (`pandas`, `numpy`, `matplotlib`, `geopandas`)
- **Telegram Bot API**
- **Windows Task Scheduler**

## Folder Structure

```
Automation/
    Automation.py
GeoJSON Malaysia/
    malaysia_singapore_brunei_State level 1.geojson
telegram bot/
    tele.py
    telegram_bot.ipynb
    testingPlace.ipynb
    log.txt
    output.png
Visualization/
    age_demographic_of_non_returning_donor.png
    age_demographic_of_returning_donor.png
    daily_trends_of_blood_donor_for_past_week.png
    map_donor_percentage_by_state.png
    monthly_trends_of_blood_donor_for_10_years.png
    rmap_donor_percentage_by_state.png
    weekly_trends_of_blood_donor_for_past_year.png
    yearly_trends_of_blood_donor.png
```

## How It Works

1. **Data Extraction:** Data is pulled from GitHub and loaded using `pandas`.
2. **Transformation:** Data is reshaped and cleaned with `numpy` and `pandas`.
3. **Visualization:** Charts and maps are generated using `matplotlib` and `geopandas`.
4. **Notification:** Visualizations are sent to stakeholders via Telegram using the bot in [`telegram bot/tele.py`](telegram%20bot/tele.py).
5. **Automation:** The entire process is scheduled and managed by Windows Task Scheduler.

## Visualization Samples

![Weekly Trends](https://github.com/AsyrafMustaffa-01/Blood-Donation-Automation/assets/155541067/805cce8a-31a3-4e41-8b9c-90fc335972e3)
![Monthly Trends](https://github.com/AsyrafMustaffa-01/Blood-Donation-Automation/assets/155541067/d46712c9-4401-41a1-b3ff-c5e02c1544e9)

## Results

![Telegram Update](https://github.com/AsyrafMustaffa-01/Blood-Donation-Automation/assets/155541067/dcf2c27f-2c80-4dc2-b522-62a34ebca85c)
![End Result](https://github.com/AsyrafMustaffa-01/Blood-Donation-Automation/assets/155541067/e642a10e-12fc-42dc-9ff9-883deda1de66)

## Setup & Usage

1. **Clone the repository**
2. **Install dependencies**
   ```sh
   pip install pandas numpy matplotlib geopandas python-telegram-bot
   ```
3. **Configure Telegram Bot**
   - Place your bot token in `bot token.txt`.
   - Update group/chat ID in [`telegram bot/tele.py`](telegram%20bot/tele.py).
4. **Run the automation script**
   ```sh
   python Automation/Automation.py
   ```
5. **Schedule with Windows Task Scheduler**
   - Set up a daily trigger at 9:00 AM.

## Data Sources

- Blood donation data: [KKM Dashboard](https://data.moh.gov.my/dashboard/blood-donation)
- Malaysia GeoJSON: [IGISMAP](https://www.igismap.com/download-malaysia-shapefile-area-map-free-country-boundary-state-polygon/)

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
