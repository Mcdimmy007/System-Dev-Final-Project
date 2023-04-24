from flask import render_template, redirect, url_for, request, session
from App import app, db
from App.models import User, Message
from App.utils import encrypt, decrypt

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = encrypt(request.form['password'])
            user = User.query.filter_by(username=username, password=password).first()
            if user:
                session['user_id'] = user.id
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid username or password'
                return render_template('login.html', error=error)
        except Exception as e:
            error = 'An error occurred while processing your request. Please try again later.'
            app.logger.error(str(e))
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = encrypt(request.form['password'])
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            error = 'An error occurred while processing your request. Please try again later.'
            app.logger.error(str(e))
            return render_template('register.html', error=error)
    else:
        return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        try:
            user_id = session['user_id']
            user = User.query.filter_by(id=user_id).first()
            messages = Message.query.filter_by(recipient_id=user_id).all()
            return render_template('dashboard.html', user=user, messages=messages)
        except Exception as e:
            error = 'An error occurred while processing your request. Please try again later.'
            app.logger.error(str(e))
            return render_template('dashboard.html', error=error)
    else:
        return redirect(url_for('login'))

# Setting the session key to a secure random value
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Use HTTPS
if __name__ == '__main__':
    app.run(ssl_context='adhoc')


