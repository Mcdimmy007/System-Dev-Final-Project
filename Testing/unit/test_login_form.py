from app.login.login_form import LoginForm

def test_login_form():
    form = LoginForm()
    assert form.email.label.text == 'Email'
    assert form.password.label.text == 'Password'
    assert form.submit.label.text == 'Log In'
    assert form.email.validators == [DataRequired(), Email(message='Enter a valid email.')]
    assert form.password.validators == [DataRequired()]
