from flask import Flask

app: Flask = Flask(__name__)


@app.route("/")
def check() -> str:
  return "App is healthy"

if __name__ == "__main__":
  app.run(host="localhost", port=5000, debug=True)