from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO, emit
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Service, Incident
import eventlet
import redis

eventlet.monkey_patch()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
socketio = SocketIO(app, message_queue='redis://localhost:6379')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('User registered successfully!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    services = Service.query.all()
    return render_template('index.html', services=services)

@app.route('/public')
def public():
    services = Service.query.all()
    return render_template('public.html', services=services)

@app.route('/add', methods=['POST'])
@login_required
def add_service():
    name = request.form.get('name')
    status = request.form.get('status')
    new_service = Service(name=name, status=status)
    db.session.add(new_service)
    db.session.commit()
    socketio.emit('status_update', {'name': name, 'status': status, 'id': new_service.id}, namespace='/')
    return redirect(url_for('index'))

@app.route('/update/<int:service_id>', methods=['POST'])
@login_required
def update_service(service_id):
    service = Service.query.get(service_id)
    service.status = request.form.get('status')
    db.session.commit()
    socketio.emit('status_update', {'name': service.name, 'status': service.status, 'id': service.id}, namespace='/')
    return redirect(url_for('index'))

@app.route('/log_incident/<int:service_id>', methods=['POST'])
@login_required
def log_incident(service_id):
    description = request.form.get('description')
    status = request.form.get('status')
    new_incident = Incident(description=description, status=status, service_id=service_id)
    db.session.add(new_incident)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/api/status', methods=['GET'])
def api_status():
    services = Service.query.all()
    status_list = [
        {
            'id': service.id,
            'name': service.name,
            'status': service.status
        }
        for service in services
    ]
    return jsonify(status_list)

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    socketio.run(app, debug=True)
