import os
import threading
import time
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from extensions import db, jwt, cache, celery
from routes import auth_bp, admin_bp, staff_bp, trekker_bp
from models import User, Trek, Booking, StaffProfile
from datetime import datetime

# Helper function to initialize Celery
def init_celery(app, celery_instance):
    use_redis = app.config.get('REDIS_AVAILABLE', False)
    celery_instance.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        timezone='UTC',
        broker_connection_retry_on_startup=use_redis,
        task_always_eager=not use_redis,
        task_eager_propagates=True
    )

    if use_redis:
        # Configure celery beat schedule only when a real broker is available.
        from celery.schedules import crontab
        celery_instance.conf.beat_schedule = {
            'daily-reminder-at-18': {
                'task': 'tasks.celery_worker.daily_reminder_task',
                'schedule': crontab(hour=18, minute=0)
            },
            'monthly-report-at-1st-9am': {
                'task': 'tasks.celery_worker.monthly_report_task',
                'schedule': crontab(day_of_month=1, hour=9, minute=0)
            }
        }

    class ContextTask(celery_instance.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery_instance.Task = ContextTask

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/', template_folder='../frontend/dist')
    app.config.from_object(config_class)
    
    # Enable CORS — allow local dev + Vercel/Netlify production frontend
    allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:8080,http://127.0.0.1:8080')
    CORS(app, origins=[o.strip() for o in allowed_origins.split(',')])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    
    # Bind Celery
    init_celery(app, celery)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(trekker_bp)
    
    # Serve Frontend Single Page App (Vue CLI build)
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        import os
        from flask import send_from_directory
        if path.startswith('api/'):
            return jsonify({'error': 'Endpoint not found'}), 404
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            index_path = os.path.join(app.static_folder, 'index.html')
            if not os.path.exists(index_path):
                return jsonify({
                    'error': 'Frontend not built. Run: cd frontend && npm install && npm run build'
                }), 503
            return send_from_directory(app.static_folder, 'index.html')

    # Seed Database on start
    with app.app_context():
        db.create_all()
        from seed import seed_data
        seed_data()

    # Background scheduler using stdlib threading — no extra dependencies
    def run_daily_reminder():
        with app.app_context():
            from tasks.celery_worker import daily_reminder_task
            daily_reminder_task()

    def run_monthly_report():
        with app.app_context():
            from tasks.celery_worker import monthly_report_task
            monthly_report_task()

    def scheduler_loop():
        while True:
            now = datetime.utcnow()
            # Daily reminder at 18:00 UTC
            if now.hour == 18 and now.minute == 0:
                run_daily_reminder()
            # Monthly report on 1st of each month at 09:00 UTC
            if now.day == 1 and now.hour == 9 and now.minute == 0:
                run_monthly_report()
            # Sleep 55 seconds — checks every minute, avoids double-firing within the same minute
            time.sleep(55)

    t = threading.Thread(target=scheduler_loop, daemon=True)
    t.start()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
