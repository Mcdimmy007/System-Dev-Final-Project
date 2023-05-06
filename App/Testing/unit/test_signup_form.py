import pytest
from app.signup.signup_form import SignupForm

def test_signup_form():
    # Test empty form data
    form = SignupForm(data={})
    assert form.validate() is False
    assert 'Name' in form.name.errors
    assert 'Email' in form.email.errors
    assert 'Password' in form.password.errors
    assert 'Confirm Your Password' in form.confirm.errors

    # Test invalid email
    form = SignupForm(data={
        'name': 'Test User',
        'email': 'invalid-email',
        'password': 'password',
        'confirm': 'password'
    })
    assert form.validate() is False
    assert 'Enter a valid email.' in form.email.errors

    # Test short password
    form = SignupForm(data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'short',
        'confirm': 'short'
    })
    assert form.validate() is False
    assert 'Select a stronger password.' in form.password.errors

    # Test password mismatch
    form = SignupForm(data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password1',
        'confirm': 'password2'
    })
    assert form.validate() is False
    assert 'Passwords must match.' in form.confirm.errors

    # Test valid form data
    form = SignupForm(data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password',
        'confirm': 'password'
    })
    assert form.validate() is True
