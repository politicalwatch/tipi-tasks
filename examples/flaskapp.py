from flask import Flask
app = Flask(__name__)
import tipi_alerts

@app.route("/")
def hello():
    tipi_alerts.init()
    tipi_alerts.test_task.apply_async((3, 2))
    return "Hello World!"
