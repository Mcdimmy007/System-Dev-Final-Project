def test_signup_form(client):
    # test the signup form
    response = client.get("/signup")
    assert response.status_code == 200
    assert b"Create an Account." in response.data

    response = client.post(
        "/signup",
        data={
            "name": "John Doe",
            "email": "john.doe@example.com",
            "password": "password",
            "confirm": "password",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Sign up for a user account." in response.data

    response = client.post(
        "/signup",
        data={
            "name": "",
            "email": "john.doe@example.com",
            "password": "password",
            "confirm": "password",
        },
        follow_redirects=True,
    )
    assert b"This field is required." in response.data

    response = client.post(
        "/signup",
        data={
            "name": "John Doe",
            "email": "invalid-email",
            "password": "password",
            "confirm": "password",
        },
        follow_redirects=True,
    )
    assert b"Enter a valid email." in response.data

    response = client.post(
        "/signup",
        data={
            "name": "John Doe",
            "email": "john.doe@example.com",
            "password": "weak",
            "confirm": "weak",
        },
        follow_redirects=True,
    )
    assert b"Select a stronger password." in response.data

    response = client.post(
        "/signup",
        data={
            "name": "John Doe",
            "email": "john.doe@example.com",
            "password": "password",
            "confirm": "wrong-password",
        },
        follow_redirects=True,
    )
    assert b"Passwords must match." in response.data
