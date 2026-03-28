from flask import Flask
from models import db
from routes.auth import auth
from routes.banking import bank

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret123'

db.init_app(app)
app.register_blueprint(auth)
app.register_blueprint(bank)

@app.route('/')
def home():
    return "Banking App Running! Go to /register"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)