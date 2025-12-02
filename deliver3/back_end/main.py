from app import create_app

app = create_app()
app.secret_key = 'super_secret_key_for_demo_purposes' # Needed for session

if __name__ == '__main__':
    app.run(debug=True, port=5000)
