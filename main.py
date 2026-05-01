from app import create_app

if __name__ == "__main__":
    app = create_app()
    print(app.url_map)
    print("--------REGISTERED ROUTES-----------")
    for rule in app.url_map.iter_rules():
        print(f"{rule} -> {rule.endpoint}")
    print("------------------------------------\n")

    app.run(host='0.0.0.0', port=8080, debug=True)