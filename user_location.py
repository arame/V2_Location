from helper import Helper
from geopy.geocoders import Nominatim
import re

class UserLocation:
    def __init__(self, data) -> None:
        self.data = data
        data.get_user_location_dictionary()
        self.user_locations = data.user_locations
        # initialize geolocator
        self.geolocator = Nominatim(user_agent='Tweet_locator')
        self.from_dict_cnt = 0
        self.from_geopy_cnt = 0
            
    def save_user_location(self, user_location, country_code):
        # If the user location is not already in the dictionary, 
        # then put it there in-memory and also store in the database
        row = {user_location : country_code}
        self.user_locations[user_location] = country_code
        self.data.save_user_location(user_location, country_code)
    
    def validate_user_location(self, user_location):
        if user_location == None:
            return False
        
        temp = re.sub("[^a-zA-Z]+", "", user_location)
        if len(temp) < 2:
            return False
        
        user_location_lower = user_location.lower()
        if user_location_lower == "sheher" or \
            user_location_lower == "she/her" or \
            user_location_lower == "worldwide":
            return False
        
        if "#name" in user_location_lower:
            return False
        
        if "#value" in user_location_lower:
            return False
        
        if "n/a" in user_location_lower:
            return False
        
        if " null " in user_location_lower:
            return False
        
        if " false " in user_location_lower:
            return False
        
        return True
              
    def locator(self, user_location):
        if user_location in self.user_locations:
            self.from_dict_cnt += 1
            country_code = self.user_locations[user_location]
            return country_code

        country_code = self.geo_locator(user_location)
        self.save_user_location(user_location, country_code)
        self.from_geopy_cnt += 1
        return country_code

    def geo_locator(self, user_location):
        try :
            # get location
            location = self.geolocator.geocode(user_location, language='en')
            # get coordinates
            location_exact = self.geolocator.reverse(
                        [location.latitude, location.longitude], language='en')
            # get country codes
            c_code = location_exact.raw['address']['country_code'].upper()
            country = location_exact.raw['address']['country']
            country = Helper.remove_non_ascii_characters(country)
            return c_code
        except:
            return ""
