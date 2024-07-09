from snaptec_resolver.src.utilities.singleton import Singleton
import re

class PhoneNumberVerifier(metaclass=Singleton):
    def __init__(self) -> None:
        print("Created PhoneNumberVerifier")
        PhoneNumberVerifier.phone_number_regex_pattern = r'\+\d{11}|(?!)+\d{10,11}'

    @staticmethod
    def is_valid_phone_number(phone_number):
        phone_number_str = str(phone_number)
        match = re.search(PhoneNumberVerifier.phone_number_regex_pattern, phone_number_str)
        return match is not None