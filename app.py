from main import create_app

blueprints = [
    "main.controller:v1",
]

app = create_app("development", blueprints)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
