def LatLonByCEP(CEP):

    """
    Converts a zipcode into a latitude and longitude
    Returns a tuple (latitude, longitude)
    """
    from geopy.geocoders import Nominatim
    import brazilcep

    locator = Nominatim(user_agent="myGeocoder")
    cep = CEP

    address_dict = brazilcep.get_address_from_cep(cep)
    city = address_dict["city"]
    district = address_dict["district"]
    street = address_dict["street"]

    completeAddress = (f"{street}, {district}-{city}")

    location = locator.geocode(completeAddress)

    lat = location.latitude
    lon = location.longitude

    return (lat, lon)