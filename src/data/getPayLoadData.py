import requests

# Takes the dataset and uses the payloads column to call the API and append the data to the lists
def getPayLoadData(data):
    Orbit = []
    PayloadMass=[]
    for load in data['payloads']:
        if load:
            response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
            PayloadMass.append(response['mass_kg'])
            Orbit.append(response['orbit'])
    return (Orbit, PayloadMass)