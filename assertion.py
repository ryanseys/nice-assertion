from flask import Flask, render_template, request, redirect, url_for
import base64
import json

app = Flask(__name__)
# app.config['DEBUG'] = True

TITLE = "Nice assertion! ;)"
NOT_VALID_ASSERTION = "Invalid assertion! :("
VALID_ASSERTION = "Success! Valid assertion! :)"


@app.route('/')
def index():
    return render_template('index.html', title=TITLE)


@app.route('/assertion', methods=['POST', 'GET'])
def assertion():
    if request.method == 'POST':
        assertion = request.form['assertion']
        arr = assertion.split('~')
        if(len(arr) != 2):
            return NOT_VALID_ASSERTION
        first_arr = arr[0].split('.')
        second_arr = arr[1].split('.')
        if((len(first_arr) != 3) or (len(second_arr) != 3)):
            return NOT_VALID_ASSERTION

        try:
            header1 = base64.b64decode(first_arr[0])
            payload1 = base64.b64decode(first_arr[1])
            sig1 = first_arr[2]

            header2 = base64.b64decode(second_arr[0])
            payload2 = base64.b64decode(second_arr[1])
            sig2 = second_arr[2]

            kwargs = {'indent': 4, 'separators': (',', ': ')}
            h1json = json.dumps(json.loads(header1), **kwargs)
            p1json = json.dumps(json.loads(payload1), **kwargs)
            h2json = json.dumps(json.loads(header2), **kwargs)
            p2json = json.dumps(json.loads(payload2), **kwargs)

        except Exception as e:
            return NOT_VALID_ASSERTION + " Error: " + str(e)

        return render_template('assertion.html', title=TITLE, header1=h1json, payload1=p1json, header2=h2json, payload2=p2json, sig1=sig1, sig2=sig2)
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
