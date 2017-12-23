from flask import Flask, send_file, make_response, request
from webscrape import present_prices
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.data
        present_prices(keyword)
        return send_file("static/js/amazon-output.json")

    return send_file("templates/index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
