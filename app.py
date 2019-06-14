from flask import Flask, render_template, request, json
app = Flask(__name__)


@app.route("/")
def main():
    keyword = request.args.get('inputKeyword')
    if keyword:
        print("query param keyword: -->", keyword)
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def signUp():
    # read the posted values from the UI
    keyword = request.form['inputKeyword']
    # _email = request.form['inputEmail']
    print("front-end keyword --->", keyword)

    return json.dumps({'data': 'you have entered ' + keyword + ' !!'})


if __name__ == "__main__":
    app.run(debug=True)
