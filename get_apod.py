import requests
import random
from datetime import datetime, timedelta

import nasaapi



def get_apod_image(date):
    #create the API URL with the specified date
    API_URL_DATE = f"{nasaapi.API_URL}&date={date}"

    # Make a request to the NASA API for the specified date
    response = requests.get(API_URL_DATE)

    # Check if the request was successful
    if response.status_code != 200:
        print("Error fetching data from NASA API.")
        return None, None, None
        
    data = response.json()

    #Make sure it's an image, not a video
    if data['media_type'] != 'image':
        print(f"The APOD for {date} is not an image.")
        return None, None, None
        
    #use hdurl if available, otherwise use url
    # This is the high-definition version of the image, if available
    image_url = data['hdurl'] if 'hdurl' in data else data['url']

    # This will download the image data and convert it to binary
    image_data = requests.get(image_url).content

    title = data['title']
    caption = data['explanation']
    
    return image_data, title, caption



def get_daily_image(mode="current"):
    if mode == "random":
        # Pick a random date between June 16, 1995 and today
        start_date = datetime(1995, 6, 16)
        end_date = datetime.today()
        print (f"daily image current date = {end_date}")
        random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        date_str = random_date.strftime('%Y-%m-%d')
        print (f"daily image random date = {date_str}")
        return date_str
    else:
        # Use today's date
        return datetime.today().strftime('%Y-%m-%d')
