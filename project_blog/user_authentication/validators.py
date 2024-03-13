from abc import ABC, abstractmethod
import re
from typing import Self

class Validator(ABC):
    def __init__(self: Self, data: str, error: object):
        self.data: str = data
        self.error: object = error

    @abstractmethod
    def validate(self: Self) -> bool:
        pass

class EmailValidator(Validator):
    """Class Used to validate email formate"""
    regex: str = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    def validate(self: Self) -> bool:
        """
        Method used to validate email address

        Raises:
            - Raises self.error: Invalid email address. if the email is not valid

        Returns:
            - True in case if email is valid\
                otherwise raises an error from self.error
        """
        email: str = self.data
        if re.fullmatch(self.regex, email):
            return True
        raise self.error("Invalid email address.")

class NameValidator(Validator):
    """Class Used to validate name format"""

    def validate(self: Self) -> bool:
        """
        Function used to validate name

        Raises:
            - Raises Response error: Name can only contain characters.

        Returns:
            - True incase the name is valid otherwise raises Error\
                through self.error object passed into the class.
        """
        # Grab the name
        name: str = self.data
        # Check if name contains only alphabets
        if not name.isalpha():
            raise self.error("Your first name can only contain characters.")
        
        return True

class PasswordValidator(Validator):
    """Class Used to validate password"""

    def length(self: Self, password: str) -> bool:
        """
        Method used to check the length of the input password.

        Args:
            - password (str): Password input to pass by the length validations.

        Raises:
            - self.error (object): In case password is shorter than 8 characters|numbers|special characters \
                or Incase password is longer than 128 characters|numbers|special characters.

        Returns:
            - True incase password is valid in terms of lengths
        """
        if len(password) < 8:
            raise self.error(
                "Password should be longer than 8 characters|numbers|special characters."
            )
        elif len(password) > 128:
            raise self.error(
                "Password should be less than 128 characters|numbers|special characters."
            )
        else:
            return True

    def character_format(self: Self, password: str):
        """
        Method used to validate password format

        Raises:
            - self.error (object): In case password does not contain at least one character A-Z a-z.\
                or Password does not contain at least one number 0-9..

        Args:
            - password (str): Password input to pass by the format validations.
        """
        # Validate password for at least containing Alphabetical characters A-Z a-z.
        if not any(char.isalpha() for char in password):
            raise self.error("Password should contain at least one character A-Z a-z.")
        # Validate password for at least containing  Numeric characters 0-9.
        if not any(number.isnumeric() for number in password):
            raise self.error("Password should contain at least one number 0-9.")
        # Return Valid Password
        return True

    def validate(self: Self) -> bool:
        """Function used to validate password"""
        # Grab the password.
        password: str = self.data
        # Validate password by format.
        format_valid: bool = self.character_format(password)
        # Validate password by length.
        length_valid: bool = self.length(password)
        # Return validation results.
        return format_valid and length_valid
