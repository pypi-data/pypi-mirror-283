from snaptec_resolver.src.utilities.singleton import Singleton
from snaptec_resolver.constants import constants
import json

class CountryMapper(metaclass=Singleton):
    def __init__(self,) -> None:
        print("Created CountryMapper")
        CountryMapper.country_data = CountryMapper.get_all_country()

    @staticmethod
    def get_all_country():
        with open(constants.country_id_path) as json_file:
            country_data = json.load(json_file)
        return country_data

    @staticmethod
    def get_country_name_from_country_id(country_id):
        return CountryMapper.country_data.get(country_id)

    @staticmethod
    def get_country_ids_from_name(country_name):
        pass