from flask import Flask, render_template, request, redirect, url_for
import base64
import json
import binascii

app = Flask(__name__)
app.config['DEBUG'] = True

TITLE = "Nice Ass-ertion!"
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

            h1json = json.dumps(json.loads(header1), indent=4, separators=(',', ': '))
            p1json = json.dumps(json.loads(payload1), indent=4, separators=(',', ': '))
            h2json = json.dumps(json.loads(header2), indent=4, separators=(',', ': '))
            p2json = json.dumps(json.loads(payload2), indent=4, separators=(',', ': '))

        except Exception as e:
            return str(e)

            #result += "SIGNATURE 1: " + base64.b64decode(signature1) + "\n"
            #result += "SIGNATURE 2: " + base64.b64decode(signature2) + "\n"

        return render_template('assertion.html', title=TITLE, header1=h1json, payload1=p1json, header2=h2json, payload2=p2json, sig1=sig1, sig2=sig2)
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
