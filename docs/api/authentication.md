# Authentication

For clients to authenticate, the token key should be included in the *Authorization* HTTP header. The key should be prefixed by the string literal "Token" or "token", with whitespace separating the two strings. For exapmle:

```
Authorization: Token 3729f87c3d274c994264127967c3a0d6c34fe4da
```

User must be **active** and **verified** in order to perform actions as authenticated user, if not an HTTP `401 Unauthorized` response with appropiate error message will be returned.

If user will provide invalid data, HTTP `400 Bad request` response with appropiate error message will be returned.


## Retrieving Tokens
Token can be obtained when user sing in application with the following request:

**Request**:

`POST` `/api/user/signin/`

Parameters:

Name | Type | Description
---|---|---
email | string | The user's email addres
password | string | The user's password

**Response**:
```json
{ 
    "token" : "3729f87c3d274c994264127967c3a0d6c34fe4da" 
}
```

### Google sign in
Token can be also obtained when user was registred via google sign up.
In that case following request will return authorization token:

**Request**:

`POST` `/api/user/signin-social/google-oauth2/`

Parameters:

Name | Type | Description
---|---|---
access_token | string | Google authorization token

**Response**:
```json
{ 
    "token" : "3729f87c3d274c994264127967c3a0d6c34fe4da" 
}
```
More on google sign in funcionality:

[google oauth2](https://developers.google.com/identity/protocols/oauth2)


## Sign out
In order to sign out, user have to make following request, which will result in removing
all tokens associated with user:

**Request**:

`GET` `/api/user/signout/`

Headers:

```
Authorization: Token 3729f87c3d274c994264127967c3a0d6c34fe4da
```

**Response**:
```json
{ 
    "Success" : "User signed out." 
}
```