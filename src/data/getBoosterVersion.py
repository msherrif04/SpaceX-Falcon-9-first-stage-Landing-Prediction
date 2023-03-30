import requests

# Takes the dataset and uses the rocket column to call the API and append the data to the list
def getBoosterVersion(data):
    BoosterVersion=[]
    for x in data['rocket']:
        if x:
            response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
            BoosterVersion.append(response['name'])
    return BoosterVersion