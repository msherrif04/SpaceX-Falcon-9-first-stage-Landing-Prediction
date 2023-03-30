import requests

# Takes the dataset and uses the launchpad column to call the API and append the data to the list

def getLaunchSite(data):
    Longitude =[]
    Latitude =[]
    LaunchSite =[] 
    for x in data['launchpad']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
            Longitude.append(response['longitude'])
            Latitude.append(response['latitude'])
            LaunchSite.append(response['name'])
    return (Longitude, Latitude, LaunchSite)