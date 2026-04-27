from app import create_app

if __name__ == "__main__":
    app = create_app()
    print(app.url_map)

    app.run(host='0.0.0.0', port=8080, debug=True)