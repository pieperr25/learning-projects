from flask import Flask,request
import functions
import markdown

app = Flask(__name__)
@app.route('/',methods=["GET"])
def main_function():
    return '''
    <style>
        div {{
            text-align:center
            margin:10
        }}
    </style>
    <div>
        <form action='/results' method = 'POST'>
            <label for='company'>Comapny name:</label>
            <input type='text' id='company' name='company'>
            <button>Submit</button>
        </form>
    </div>
    '''
@app.route('/results',methods=['POST'])
def post():
    info = request.form['company']

    return f'''
    <style>
        body {{
            background-color:lightblue
            font-family:sans-serif
            margin:2
            padding:2
        }}

        h1 {{
            text-align:center
        }}
        p {{
            text-align:center
        }}



    </style>
    {markdown.markdown(functions.analyzation(info))}
    '''

app.run(debug=True, port=5001)