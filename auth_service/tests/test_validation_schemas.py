from src.exceptions import InvalidEschema
from src.validation_schemas import validate_user_schema
import pytest


class TestValidateUserSchema:
    '''
      Verify validation schemas 
    '''

    def test_valid_user_schema(self):
        valid_schema = {
            'name': 'Alex',  # >= 4 length
            'password': 'abdfghi8#',  # >= 8 length
            'email': 'anemail@test.com'
        }

        validate_user_schema(valid_schema)

    def test_full_invalid_user_schema(self):
        '''
            Check if passing a complete invalid user_schema
            raises an exception with the detail of all invalid fields
        '''

        full_invalid_schema = {
            'name': 'ale',  # short username
            'password': 'abdfghia',  # Not symbol and number field
            'email': 'userexamplecom'  # no valid email
        }

        with pytest.raises(InvalidEschema) as e_info:
            validate_user_schema(full_invalid_schema)

        invalid_params = e_info.value.invalid_params
        name_message = invalid_params['name']['message']
        password_message = invalid_params['password']['message']
        email_message = invalid_params['email']['message']

        assert name_message == 'The name field must have at least 4 characters'
        assert password_message == 'The password field must have at least 1 symbol or at least 1 number'
        assert email_message == 'Invalid email format'

    def test_invalid_name_raise_error(self):
        '''
            Verify if parse an schema with short nname raise
            exception and the error message is the expected
        '''
        shcema_with_invalid_name = {
            'name': 'Ale',
            'password': 'abdfghi#',  # >= 8 length
            'email': 'an_email@test.com'
        }
        with pytest.raises(InvalidEschema) as e_info:
            validate_user_schema(shcema_with_invalid_name)

        name_message = e_info.value.invalid_params['name']
        assert 'The name field must have at least 4 characters' in name_message['message']

    def test_invalids_password_raises_error(self):
        '''
            Verify if parse and schema with wrong password raise exception
            and the error message is the expected for an short name

            first parse an invalid password: 8 length with no symbol or number
            seccond parse an short password: symbol and number but length < 8
        '''
        schema_with_invalid_password = {
            'name': 'Alea',
            'password': 'abdfghia',  # missig symbol or number
            'email': 'anemail@test.com'
        }
        with pytest.raises(InvalidEschema) as e_info:
            validate_user_schema(schema_with_invalid_password)

        password_message = e_info.value.invalid_params['password']
        assert 'The password field must have at least 1 symbol or at least 1 number' in password_message[
            'message']

        # sets a password with invalid length but with symbols
        schema_with_invalid_password['password'] = 'abcdf#'
        with pytest.raises(InvalidEschema) as e_info:
            validate_user_schema(schema_with_invalid_password)

        password_message = e_info.value.invalid_params['password']
        assert 'The password field must have at least 8 characters' in password_message[
            'message']

    def test_invalid_email_raise_error(self):
        '''
            Verify if parse an schema with invalid email raise InvalidEschema
            and if the message is the expected for invalid email
        '''
        schema_with_invalid_email = {
            'name': 'Aled',  # >= 4 length
            'password': 'abdfghi8#',  # >= 8 length
            'email': 'anemail.com'
        }

        with pytest.raises(InvalidEschema) as e_info:
            validate_user_schema(schema_with_invalid_email)

        assert e_info.value.invalid_params['email']['message'] == 'Invalid email format'

    def test_missing_name_raise_error(self):
        shcema_with_invalid_name = {
            'password': 'abdfghi#',  # >= 8 length
            'email': 'an_email@test.com'
        }
        with pytest.raises(InvalidEschema) as e_info:
            validate_user_schema(shcema_with_invalid_name)

        assert 'name' in e_info.value.missing_params
