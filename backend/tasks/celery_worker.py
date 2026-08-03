from datetime import datetime, timedelta, timezone
import os
import csv
from extensions import celery, db
from models.user import User
from models.trek import Trek
from models.booking import Booking
from models.notification import Notification
from tasks.mailer import send_email


@celery.task
def daily_reminder_task():
    today = datetime.now(timezone.utc).replace(tzinfo=None)
    three_days_from_now = today + timedelta(days=3)

    treks = Trek.query.filter(
        Trek.start_date >= today,
        Trek.start_date <= three_days_from_now
    ).all()

    sent = 0
    for trek in treks:
        bookings = Booking.query.filter_by(trek_id=trek.id, booking_status='Booked').all()
        for b in bookings:
            user = b.user
            if not user:
                continue

            html = f"""
            <html><body>
            <h2>Upcoming Trek Reminder</h2>
            <p>Hello <strong>{user.name}</strong>,</p>
            <p>Your trek is starting soon!</p>
            <table border="1" cellpadding="8" style="border-collapse:collapse;">
              <tr><td><strong>Trek</strong></td><td>{trek.trek_name}</td></tr>
              <tr><td><strong>Location</strong></td><td>{trek.location}</td></tr>
              <tr><td><strong>Start Date</strong></td><td>{trek.start_date.strftime('%Y-%m-%d')}</td></tr>
              <tr><td><strong>End Date</strong></td><td>{trek.end_date.strftime('%Y-%m-%d')}</td></tr>
              <tr><td><strong>Details</strong></td><td>{trek.description or 'N/A'}</td></tr>
            </table>
            <p>Please be prepared and arrive on time. Enjoy your trek!</p>
            <p>— TrekHub Team</p>
            </body></html>
            """
            send_email(user.email, f"Reminder: Your trek '{trek.trek_name}' starts on {trek.start_date.strftime('%Y-%m-%d')}", html)
            sent += 1

    print(f"[DAILY REMINDER] Processed {sent} reminders.")
    return f"Daily reminders sent: {sent}"


@celery.task
def monthly_report_task():
    from models.user import User

    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role='TREKKER').count()
    total_bookings = Booking.query.count()

    total_slots = db.session.query(db.func.sum(Trek.total_slots)).scalar() or 0
    booked_slots = Booking.query.filter(
        Booking.booking_status.in_(['Booked', 'Completed'])
    ).count()
    participation_rate = (booked_slots / total_slots * 100) if total_slots > 0 else 0

    popular_treks = db.session.query(
        Trek.trek_name,
        Trek.location,
        db.func.count(Booking.id).label('booking_count')
    ).join(Booking).group_by(Trek.id).order_by(db.desc('booking_count')).limit(5).all()

    popular_rows = ''.join(
        f"<tr><td>{t.trek_name}</td><td>{t.location}</td><td>{t.booking_count}</td></tr>"
        for t in popular_treks
    ) or '<tr><td colspan="3">No data</td></tr>'

    month_label = datetime.now(timezone.utc).strftime('%B %Y')

    report_html = f"""
    <html>
    <head><style>
      body {{ font-family: Arial, sans-serif; color: #333; }}
      h2 {{ color: #2e7d32; }}
      table {{ border-collapse: collapse; width: 100%; margin-top: 12px; }}
      th, td {{ border: 1px solid #ccc; padding: 8px 12px; text-align: left; }}
      th {{ background: #e8f5e9; }}
    </style></head>
    <body>
      <h2>TrekHub – Monthly Activity Report</h2>
      <p><strong>Period:</strong> {month_label}</p>
      <h3>Summary</h3>
      <table>
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Total Treks Available</td><td>{total_treks}</td></tr>
        <tr><td>Registered Trekkers</td><td>{total_users}</td></tr>
        <tr><td>Total Bookings</td><td>{total_bookings}</td></tr>
        <tr><td>Participation Rate</td><td>{participation_rate:.2f}%</td></tr>
      </table>
      <h3>Top 5 Popular Treks</h3>
      <table>
        <tr><th>Trek Name</th><th>Location</th><th>Bookings</th></tr>
        {popular_rows}
      </table>
      <br><p>— TrekHub Auto-generated Report</p>
    </body>
    </html>
    """

    # Save HTML report locally
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    reports_dir = os.path.join(base_dir, 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    report_path = os.path.join(reports_dir, f"monthly_report_{datetime.now(timezone.utc).strftime('%Y_%m')}.html")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_html)
    print(f"[MONTHLY REPORT] Saved to {report_path}")

    # Email to all admins
    admins = User.query.filter_by(role='ADMIN').all()
    for admin in admins:
        send_email(admin.email, f"TrekHub Monthly Report – {month_label}", report_html)

    return "Monthly report completed"


@celery.task
def export_user_csv_task(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return "User not found"

    bookings = Booking.query.filter_by(user_id=user_id).all()

    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    exports_dir = os.path.join(base_dir, '..', 'frontend', 'public', 'exports')
    os.makedirs(exports_dir, exist_ok=True)

    filename = f"trek_history_{user_id}.csv"
    filepath = os.path.join(exports_dir, filename)

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['User ID', 'Trek Name', 'Location', 'Booking Status', 'Booking Date', 'Start Date', 'End Date'])
        for b in bookings:
            if not b.trek:
                continue
            writer.writerow([
                user_id,
                b.trek.trek_name,
                b.trek.location,
                b.booking_status,
                b.booking_date.strftime('%Y-%m-%d %H:%M'),
                b.trek.start_date.strftime('%Y-%m-%d'),
                b.trek.end_date.strftime('%Y-%m-%d')
            ])

    # Notify user in-app
    notification = Notification(
        user_id=user_id,
        message=f"Your trek history export is ready. Download it [here](/exports/{filename} ").",
    
        type="Export",
        is_read=False
    )
    db.session.add(notification)
    db.session.commit()

    # Also send email notification
    html = f"""
    <html><body>
    <h2>Your Trek History Export is Ready</h2>
    <p>Hello <strong>{user.name}</strong>,</p>
    <p>Your trekking history CSV export has been generated successfully.</p>
    <p>You can download it from your dashboard under Notifications.</p>
    <p>— TrekHub Team</p>
    </body></html>
    """
    send_email(user.email, "TrekHub – Your Export is Ready", html)

    print(f"[EXPORT] CSV ready for user {user_id}: {filepath}")
    return f"/exports/{filename}"
