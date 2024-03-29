# Blood-Donation-Automation

Inspiration of this project is from https://data.moh.gov.my/dashboard/blood-donation KKM blood donation public dashboard.

This project involving automated data pipeline where pull data from github and run through ETL where the output is data visualization.
Later, the data visualization will be send to stakeholder using telegram bot. 

For reading the data, I mainly use pandas library as it powerful enough to read most of the datatype and save as dataframe.
I also use numpy to transform my data, ie reshape data.
For data visualization, I just use matplotlib because it have all I need.
For map plotting, I use geopandas to read geoJSON file i got from https://www.igismap.com/download-malaysia-shapefile-area-map-free-country-boundary-state-polygon/
As for how I interacting with the Telegram Bot, I use API key to send message to Telegram Group.
Then I automated all those process with Windows Task Scheduler with trigger daily, every 9.00AM, with or without user logged on the computer and will wake the computer to run the task.

![image](https://github.com/AsyrafMustaffa-01/Blood-Donation-Automation/assets/155541067/805cce8a-31a3-4e41-8b9c-90fc335972e3)
![image](https://github.com/AsyrafMustaffa-01/Blood-Donation-Automation/assets/155541067/d46712c9-4401-41a1-b3ff-c5e02c1544e9)

Here is the snip of task scheduler configuration.

## Results

![image](https://github.com/AsyrafMustaffa-01/Blood-Donation-Automation/assets/155541067/dcf2c27f-2c80-4dc2-b522-62a34ebca85c)
![image](https://github.com/AsyrafMustaffa-01/Blood-Donation-Automation/assets/155541067/e642a10e-12fc-42dc-9ff9-883deda1de66)

Here is the snip of the end result, update to telegram group.
