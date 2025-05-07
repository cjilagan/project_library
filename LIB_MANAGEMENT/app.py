from website import create_app

app = create_app()

with app.app_context():
    for rule in app.url_map.iter_rules():
        print(rule)

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5000, debug=True)
