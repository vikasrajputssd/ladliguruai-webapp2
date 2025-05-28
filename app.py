from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'ladli_ju_secret_key'

# Home Page - नाम जप
@app.route('/')
def home():
    count = session.get('jap_count', 0)
    return render_template('index.html', count=count)

@app.route('/jap', methods=['POST'])
def jap():
    count = session.get('jap_count', 0)
    count += 1
    session['jap_count'] = count
    return redirect(url_for('home'))

# दर्शन पेज
@app.route('/darshan')
def darshan():
    # आप अपनी पसंद के दर्शन फोटो यहां जोड़ सकते हैं
    photo = url_for('static', filename='images/radha_krishna.jpg')
    return render_template('darshan.html', photo=photo)

# क्विज़ पेज
quiz_questions = [
    {'q': 'श्यामा-श्याम के नाम जप से क्या लाभ होता है?', 'options': ['शांति', 'धन', 'अन्न'], 'answer': 'शांति'},
    {'q': 'राधा कृष्ण किस शहर से जुड़े हैं?', 'options': ['वृंदावन', 'अयोध्या', 'कानपुर'], 'answer': 'वृंदावन'},
]

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'score' not in session:
        session['score'] = 0
        session['q_index'] = 0

    if request.method == 'POST':
        selected = request.form.get('option')
        q_index = session['q_index']
        if selected == quiz_questions[q_index]['answer']:
            session['score'] += 1
        session['q_index'] += 1

    q_index = session['q_index']
    if q_index >= len(quiz_questions):
        score = session['score']
        session.pop('score')
        session.pop('q_index')
        return render_template('quiz.html', done=True, score=score, total=len(quiz_questions))

    question = quiz_questions[q_index]
    return render_template('quiz.html', question=question, done=False)

if __name__ == '__main__':
    app.run(debug=True)
