import hashlib

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    hashed_password = db.Column(db.String(64), nullable=False)

    def set_password(self, password):
        salt = 'somesaltvalue'
        hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        self.hashed_password = hashed_password

    def check_password(self, password):
        salt = 'somesaltvalue'
        hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        return self.hashed_password == hashed_password
