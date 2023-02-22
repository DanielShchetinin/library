from visual_params import visual_space
from exceptions import *

class Address:

    
    def __init__(self, country: str, city: str, street: str, building_number: int):
        
        self._country = country
        self._city = city
        self._street = street
        self._building_number = building_number

        
    def get_city(self):
        return self._city
    
    def get_full_address(self):
        return f"\nCountry: {self._country}.\nCity: {self._city}.\nStreet: {self._street}.\
                \n\nbuilding_number: {self._building_number}.\n\n"

    @staticmethod
    def create_address_for_library():
        country = input("| Please enter a country: ")
        city = input("| Please enter a city: ")
        street = input("| Please enter a street: ")
        
        if country.isdigit() or city.isdigit() or street.isdigit():
            raise CantBeDigit()
        
        building_number = int(input("| Please enter a buliding number: "))

        if building_number < 0:
            raise NegativeNumber()
        
        else:

            address_for_use = Address(country, city, street, building_number)
            return address_for_use
    
    @staticmethod
    def create_address_for_customer():

        country = input("| Please enter a country: ")
        city = input("| Please enter a city: ")
        street = input("| Please enter a street: ")
        building_number = int(input("| Please enter a buliding number: "))

        if country.isdigit() or city.isdigit() or street.isdigit():
            raise CantBeDigit()
        
        if building_number < 0:
            raise NegativeNumber()
        
        else:

            address_for_use = Address(country, city, street, building_number)
            return address_for_use
        
    def __str__(self):
        return f"{self._country}, {self._city}, {self._street} {self._building_number}."
    
    def __repr__(self):
        return self.__str__()