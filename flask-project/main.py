from flask import Flask,request
import functions

app = Flask(__name__)
@app.route('/',methods=["GET"])
def main_function():
    return '''
    <form action='/results' method = 'POST'>
        <label for='company'>Comapny name:</label>
        <input type='text' id='company' name='company'>
        <button>Submit</button>
    </form>
    '''
@app.route('/results',methods=['POST'])
def post():
    info = request.form['company']
    return functions.analyzation(info)

app.run(debug=True, port=5001)