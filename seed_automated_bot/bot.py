import json
import string
import random

import requests
from faker import Faker

with open("config.json") as config_file:
    config = json.load(config_file)

NUMBER_OF_USERS = config['number_of_users']
MAX_POSTS_PER_USER = config['max_posts_per_user']
MAX_LIKES_PER_USER = config['max_likes_per_user']

fake_user = Faker(['en_CA'])

BASE_URL = 'http://127.0.0.1:8000'
CREATE_POST_URL = '/api/post/create'
REGISTER_URL = "/auth/register"
LOGIN_URL = '/auth/jwt/login'
GET_ALL_POSTS_URL = "/api/post/all"


def generate_password(length=12):
    """
    The generate_password function generates a random password of length 12.
        If the user wants to specify a different length, they can pass in an integer as an argument.
        The function returns the generated password.

    :param length: Set the length of the password
    :return: A string of random characters
    """
    password_characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(password_characters) for _ in range(length))
    return password


def registation_user(json_data):
    """
    The registation_user function takes in a json_data object and sends it to the server.
    The function returns the response from the server.

    :param json_data: Pass the json data to the api
    :return: A response object
    """
    url = BASE_URL + REGISTER_URL
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=json_data)
    return response


def login_and_get_token(form_data):
    """
    The login_and_get_token function takes a dictionary of form data as an argument.
    It then makes a POST request to the login endpoint, passing in the form data.
    If the response status code is 200, it returns the access token from that response's JSON payload.

    :param form_data: Pass in the username and password to the login_and_get_token function
    :return: A JWT token
    """
    url = BASE_URL + LOGIN_URL
    response = requests.post(url, data=form_data)
    if response.status_code == 200:
        token = response.json().get('access_token')
        return token
    else:
        print("Authentication error::", response.status_code)
        return None


def create_posts_with_token(token, num_of_posts=MAX_POSTS_PER_USER):
    """
    The create_posts_with_token function creates a number of posts for the user with the given JWT token.
    The function takes in two arguments:
        - token: The JWT access_token of the user who will be creating posts.
        - num_of_posts (optional): The number of posts to create for this user, defaults to MAX_POSTS_PER_USER.

    :param token: Authenticate the user
    :param num_of_posts: Specify how many posts to create
    :return: Nothing
    """
    url = BASE_URL + CREATE_POST_URL
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    for _ in range(num_of_posts):
        post_data = {
            'text': fake_user.sentence(nb_words=10)
        }
        requests.post(url, headers=headers, data=post_data)


def add_likes_to_posts(token, num_of_likes=MAX_LIKES_PER_USER, username="None"):
    """
    The add_likes_to_posts function takes in a JWT token and the number of likes to add.
    It then makes a GET request to get all posts, and gets the total number of posts.
    Then it loops through that many times, generating random post ids between 1 and the total number of posts.
    If that post id has not been liked yet by this user (to avoid duplicate likes), it will make a POST request to like that post.

    :param token: Authenticate the user
    :param num_of_likes: Determine how many likes the user will give to posts
    :param username: Print the name of the user who liked a post
    :return: Nothing
    """
    headers = {
                'Authorization': f'Bearer {token}',
                'accept': 'application/json'
            }
    liked_post_ids = []
    total_posts = requests.get(BASE_URL + GET_ALL_POSTS_URL)
    total_posts = len(total_posts.json())
    print(f"Total posts now = {total_posts}")
    for _ in range(num_of_likes):
        post_id = random.randint(1, total_posts)
        if post_id not in liked_post_ids:
            url = BASE_URL + f"/api/post/{post_id}/like"
            requests.post(url, headers=headers)
            liked_post_ids.append(post_id)
            print(f"{username.capitalize()} liked Post № {post_id}")


# !  __________________________________
# !  _____________MAIN LOOP____________
# !  __________________________________

for user in range(NUMBER_OF_USERS + 1):
    # !  ________Creating fake user________
    fake_user_name = fake_user.user_name()
    fake_email = fake_user.ascii_email()
    fake_password = generate_password(8)
    print(f"Working with {fake_user_name}...")

    # !  ________REGISTRATION________

    registration_data = {
        "email": fake_email,
        "password": fake_password,
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": fake_user_name
    }
    registation_user(registration_data)

    # !  ________Login and get JWT________
    login_data = {
        'username': fake_email,
        'password': fake_password
    }
    jwt_token = login_and_get_token(login_data)

    # !  ________Creating new posts________
    create_posts_with_token(jwt_token)

    # !  ________User add likes for posts________
    add_likes_to_posts(jwt_token, username=fake_user_name)

    user += 1
