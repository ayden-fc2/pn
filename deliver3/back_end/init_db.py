from app import create_app, db

def init_database():
    app = create_app()
    with app.app_context():
        db.init_db()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()
