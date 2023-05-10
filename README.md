Sure, here's the updated documentation:

## Introduction

This is a documentation of a Django REST API for a social media platform made for AccuKnox Assessment. This API allows users to create an account, log-in, send, accept and reject friend requests, view their friends and pending friend requests.

## Setup without using docker

1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install the dependencies listed in `requirements.txt`.
4. Run migrations using `python manage.py migrate`.
5. Start the server using `python manage.py runserver`.

## Setup using docker

1. Clone the repository.
2. Go to the project root
3. `docker-compose up --build -d` we add -d for detached mode.


## Endpoints

### Authentication

#### Register

- URL: `/api/v1/signup/`
- Method: `POST`
- Description: Creates a new user account.
- Request body:
  ```
  {
      "email": "example@example.com",
      "first_name": "example",
      "last_name": "last name"
      "password": "examplepassword"
  }
  ```
- Response:
  ```
  {
      "email": "example@example.com",
      "first_name": "example",
      "last_name": "last name",
  }
  ```

#### Login

- URL: `/api/v1/login/`
- Method: `POST`
- Description: Authenticates a user and creates a session.
- Request body:
  ```
  {
      "email": "example@example.com",
      "password": "examplepassword"
  }
  ```
- Response:
  ```
  Sucessfully logged in.
  ```

### Friend Request

#### Send friend request

- URL: `/api/v1/send-friend-request/`
- Method: `POST`
- Description: Sends a friend request to a user.
- Request headers:
  ```
  Authorization: Session <session_id>
  ```
- Request body:
  ```
  {
      "user_id": 2
  }
  ```
- Response:
  ```
  {
      "success": "Friend request sent."
  }
  ```

#### Accept friend request

- URL: `/api/v1/accept-friend-request/`
- Method: `POST`
- Description: Accepts a friend request.
- Request headers:
  ```
  Authorization: Session <session_id>
  ```
- Request body:
  ```
  {
      "friend_request_id": 5
  }
  ```
- Response:
  ```
  {
      "success": "Friend request accepted."
  }
  ```

#### Reject friend request

- URL: `/api/reject-friend-request/`
- Method: `POST`
- Description: Rejects a friend request.
- Request headers:
  ```
  Authorization: Session <session_id>
  ```
- Request body:
  ```
  {
      "friend_request_id": 5
  }
  ```
- Response:
  ```
  {
      "success": "Friend request rejected."
  }
  ```

#### Pending friend requests

- URL: `/api/pending-friend-requests/`
- Method: `GET`
- Description: Lists all pending friend requests.
- Request headers:
  ```
  Authorization: Session <session_id>
  ```
- Response:
  ```
  [
      {
          "id": 1,
          "from_user": {
              "id": 2,
              "username": "user2"
          },
          "to_user": {
              "id": 1,
              "username": "user1"
          }
      }
  ]
  ```

#### List friends

- URL: `/api/friends/`
- Method: `GET`
- Description: Lists all friends.
- Request headers:
  ```
  Authorization: Session <session_id>
  ```
- Response:
  ```
  [
      {
          "id": 2,
          "username": "user2"
      }
  ]
  ```

## Conclusion

In this project, we built a Django web application that provides user authentication, friend requests, and friendships functionality. We used Django's built-in authentication system and the Django REST framework to build APIs. The application can be used as a starting point for building more complex social networking applications.
