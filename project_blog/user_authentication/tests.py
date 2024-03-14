"""
File contains Test Classess:-
    - RegisterTests (APITestCase): Class to test RegisterView.
    - LoginTests (APITestCase): Class to test LoginView.
    - LogoutTests (APITestCase): Class to test LogoutView.
    - RefreshTokenTests (APITestCase): Class to test refresh_token_view.
"""
from rest_framework.test import APITestCase
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.http import HttpResponse
from django.urls import reverse
from .models import User
from typing import Self
import json

# Create your tests here.
class RegisterTests(APITestCase):
    """Test Class for Register API"""
    # String that represents name of API for reverse
    API: str = "register-view"
    # data
    data: dict[str, str] = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': '1234!Example.',
        "first_name": "Joe",
        'last_name': "Doe",
    }
    def test_create_account(self: Self) -> None:
        """
        Test Case for creating an account successfully
        """
        # Get the link.
        url: str = reverse(self.API)
        # data
        data: dict[str, str] = self.data.copy()
        # Grab the response through post request.
        response: HttpResponse = self.client.post(url, data)

        # API Tests
        # Assert that the status code is request was successful (status code 201)
        self.assertEqual(response.status_code, 201)
        # Assert The success message return from response.
        self.assertEqual(
            'User account was successfully created.!',
            json.loads(response.content)
        )

        # User Model Tests
        # Confirm from the user model that a user with the details is created
        user: User = User.objects.get(email=data['email'])
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
    
    def test_create_account_fail(self: Self) -> None:
        """
        Test Case for creating account failure.
        """
        # Define the URL and Data to be used in this test case.
        url: str = reverse(self.API)
        # Copy data
        data: dict[str, str] = self.data.copy()
        # Remove required fields one by one and try to create the account.
        req_fields: list[str] = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
        ]
        for field in req_fields:
            copy_data: dict[str, str] =  data.copy()
            del copy_data[field]
            # Send Request & Get Response
            response: HttpResponse = self.client.post(url, copy_data)
            # Assert  Status Code of the response should be 403 Forbidden.
            self.assertEqual(response.status_code, 403)
            # Check Error Message Field Should Be Presented
            self.assertIn(field,json.loads(response.content).keys())
    
    # Need to create more tests for input validators...
            # invalid email address
            # invalid password
            # invalid first_name
            # invalid last_name
            # invalid username

# Create your tests here.
class LoginTests(APITestCase):
    """Test Class for user login API"""
    # String that represents name of API for reverse
    API: str = "login-reset-view"
    data: dict[str, str] = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': '1234!Example.',
        "first_name": "Joe",
        'last_name': "Doe",
    }
    @classmethod
    def setUpClass(cls: "LoginTests") -> None:
        """
        Set Up for Class Tests
        """
        super().setUpClass()
        # Create User with valid data
        cls.user: User = User.objects.create_user(**cls.data)
    
    def test_valid_credentials(self: Self) -> None:
        """
        Test Login Success with Valid credentials.
        """
        # Get the URL for login
        url: str = reverse(self.API)
        # Execute a post request and grab the response.
        response: HttpResponse = self.client.post(url, self.data)
        response_data: dict = json.loads(response.content)
        expected_keys: list[str] = list(self.data.keys()) + ["token"]
        # Pop password
        expected_keys.pop(2)

        # Assert Login code 201 created
        self.assertEqual(response.status_code, 201)

        # Assert Response data keys
        self.assertTrue(isinstance(response_data, dict))
        self.assertTrue(
            [key in response_data for key in expected_keys]
        )
        self.assertTrue('access' in response_data['token'])
        self.assertTrue('refresh' in response_data['token'])

        # Assert Response data values
        # Loop over response_data where we used json.loads on response.content
        for key, value in response_data.items():
            # avoid "token" key for now
            if "token" != key:
                self.assertTrue(value == self.data[key])

    def test_invalid_email(self: Self) -> None:
        """
        Test Login Failure when email address is invalid
        In case if a user email does not exists it will not indicate it and respond in 401
        """
        # Get URL
        url: str = reverse(self.API)
        #  Modify email to be invalid
        data: dict[str, str] = {
            'email':'notanemail',
            'password': '1234!Example.',
        }
        # Make Request
        response: HttpResponse = self.client.post(url, data)
        # Check Status Code
        self.assertEqual(response.status_code, 401)
        # Load JSON Data from Response Content
        response_data: dict = json.loads(response.content)
        # Check that the error message matches what we expect
        self.assertIn("Authentication credentials were not provided.", response_data["detail"])
    
    def test_wrong_password(self: Self) -> None:
        """
        Test for wrong password
        """
        # Get URL
        url: str = reverse(self.API)
        #  Modify email to be invalid
        data: dict[str, str] = {
            'email':'test@example.com',
            'password': '12312412',
        }
        # Make Request
        response: HttpResponse = self.client.post(url, data)
        # Check Status Code
        self.assertEqual(response.status_code, 404)
        # Load JSON Data from Response Content
        response_data: dict = json.loads(response.content)
        # Check that the error message matches what we expect
        self.assertIn(
            "User 'email' or 'password' is incorrect.",
            response_data['non_field_errors']
        )

# Create your tests here.
class LogoutTests(APITestCase):
    """Test Class for user logout API"""
    # String that represents name of API for reverse
    API: str = "logout-view"
    data: dict[str, str] = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': '1234!Example.',
        "first_name": "Joe",
        'last_name': "Doe",
    }
    @classmethod
    def setUpClass(cls: "LoginTests") -> None:
        """
        Set Up for Class Tests
        """
        super().setUpClass()
        # Create User with valid data
        cls.user: User = User.objects.create_user(**cls.data)
    
    def login(self: Self) -> dict[str, str]:
        """
        Method used to login user and get tokens 'access' & 'refresh'

        Returns:
            - Dictionary that contains 'access' & 'refresh' tokens
        """
        # send a request to login API  with correct credentials
        login: HttpResponse = self.client.post(
            reverse('login-reset-view'), # Login API URL
            { # Data
                'email': 'test@example.com', # Email address for login
                'password': '1234!Example.', # Password for Login
            }
        )
        # Json.loads content and get tokens
        token: str = json.loads(login.content)['token']
        # return tokens
        return token

    def test_logout(self) -> None:
        """Test for logout successfully"""
        # Grab url for logout
        url: str = reverse(self.API)
        # Generate tokens
        token: dict[str, str] = self.login()
        # Add Authorization Header to Request
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        # Send GET Request to URL
        response: HttpResponse = self.client.post(
            url,
            {"refresh_token": token['refresh']}
        )
        # Assert Status code 200
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # Assert Message
        self.assertEqual(
            'User has been logged out.',
            json.loads(response.content)
        )
    
    def test_token_blacklisted(self: Self) -> None:
        """Test Case to validate that the token has been black listed"""
        # Grab url for logout
        url: str = reverse(self.API)
        # login
        token: dict[str, str] = self.login()
        # Add Authorization Header to Request
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
        # Send GET Request to URL
        response: HttpResponse = self.client.post(
            url,
            {"refresh_token": token['refresh']}
        )

        # Assert Token is blacklisted
        # Attempt to refresh the blacklisted token
        with self.assertRaises(TokenError) as context:
            refresh_token = RefreshToken(token['refresh'])

        # Check if the expected error message is raised
        self.assertEqual(str(context.exception), "Token is blacklisted")

        # call api again and see response
        second_response: HttpResponse = self.client.post(
            url,
            {"refresh_token": token['refresh']}
        )
        # Assert Status Code 400 Bad Request
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assert Error Message to be token is blacklisted.
        self.assertEqual(
            json.loads(second_response.content)['refresh_token'][0],
            'Token is blacklisted'
        )
        

# Create your tests here.
class RefreshTokenTests(APITestCase):
    """Test Class for Refresh Token API"""
    # String that represents name of API for reverse
    API: str = "refresh-token-view"
    data: dict[str, str] = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': '1234!Example.',
        "first_name": "Joe",
        'last_name': "Doe",
    }
    @classmethod
    def setUpClass(cls: "LoginTests") -> None:
        """
        Set Up for Class Tests
        """
        super().setUpClass()
        # Create User with valid data
        cls.user: User = User.objects.create_user(**cls.data)
    
    def login(self: Self) -> dict[str, str]:
        """
        Method used to login user and get tokens 'access' & 'refresh'

        Returns:
            - Dictionary that contains 'access' & 'refresh' tokens
        """
        # send a request to login API  with correct credentials
        login: HttpResponse = self.client.post(
            reverse('login-reset-view'), # Login API URL
            { # Data
                'email': 'test@example.com', # Email address for login
                'password': '1234!Example.', # Password for Login
            }
        )
        # Json.loads content and get tokens
        token: str = json.loads(login.content)['token']
        # return tokens
        return token
    
    def test_new_tokens(self: Self) -> None:
        """
        Test case for retrieving new refresh tokens successfully
        """
        # Refresh token url
        url: str = reverse(self.API)
        # Login
        tokens: dict[str, str] = self.login()
        # Grab response
        response: HttpResponse = self.client.post(
            url,
            {"refresh_token": tokens['refresh']}
        )
        # get new_tokens
        new_tokens: dict[str, str] = json.loads(response.content)

        # Assert Status code Accepted
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        # Test Tokens
        self.assertTrue(isinstance(new_tokens, dict))
        self.assertIn("access", new_tokens)
        self.assertIn("refresh", new_tokens)
        self.assertFalse(new_tokens["access"] == tokens["access"])
        self.assertFalse(new_tokens["refresh"] == tokens["refresh"])
    
    def test_new_token_fail(self: Self) -> None:
        """
        Failed to create new tokens.
        """
        # Refresh token url
        url: str = reverse(self.API)
        # Login
        tokens: dict[str, str] = self.login()
        # Use logout API
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        # Send GET Request to URL
        logout_response: HttpResponse = self.client.post(
            reverse("logout-view"),
            {"refresh_token": tokens['refresh']}
        )

        # Grab response
        response: HttpResponse = self.client.post(
            url,
            {"refresh_token": tokens['refresh']}
        )

        # Assert  Status Code Unauthorized
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        
    

