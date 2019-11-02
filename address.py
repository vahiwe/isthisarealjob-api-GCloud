import googlemaps

gmaps = googlemaps.Client(key='AIzaSyAlvT9QoXecXq_WFfd4_slajtCnMJBXB6Y')


def verify_address(address):    
    geocode_result = gmaps.geocode(address)
    # if geocode_result != '[]':
    #     return "Address verified"
    # else:
    #     return "Couldn't verify address"
    if geocode_result == []:
        return "This address is invalid"
    else:
        geocode_result= geocode_result[0]
        if 'plus_code' in geocode_result:
            return "The Company address is valid"
        else:
            return "This address is vague, This job invite is likely a scam"
