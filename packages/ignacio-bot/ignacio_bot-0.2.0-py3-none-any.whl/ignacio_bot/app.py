from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_session import Session
from openai import OpenAI

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# OpenAI API Key
client = OpenAI()

# Define the system message
system_message = open('system_context.txt', 'r').read()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def get_data():
    if request.method == 'POST':
        if 'messages' not in session:
            session['messages'] = []
        
        data = request.get_json()
        text=data.get('data')
        user_input = text
        #user_input = request.form['message']
        session['messages'].append({"role": "user", "content": user_input})
        
        try:
            # Get the chat history
            messages = [{"role": "system", "content": system_message}] + session['messages']
            
            # Get the response from OpenAI
            response = client.chat.completions.create(
                            model="ft:gpt-3.5-turbo-1106:personal:ignacio:9hfPEnGH",
                            messages=messages,
                            temperature=1, # Do not go above 1!
                            max_tokens=1024,
                            top_p=1,
                            frequency_penalty=0,
                            presence_penalty=0
                            )
            
            assistant_response = response.choices[0].message.content
            session['messages'].append({"role": "assistant", "content": assistant_response})
            return jsonify({"response":True, "message": assistant_response})
        except Exception as e:
            print(e)
            error_message = f'Error: {str(e)}'
            return jsonify({"message":error_message,"response":False})

@app.route('/clear')
def clear():
    session.pop('messages', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)