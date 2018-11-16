from flask import Flask, render_template, request, redirect, url_for, flash, session
import config
import json
from tqdm import tqdm
from exts import db
from models import Question, User
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.methods == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username=username,
                                User.password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            flash('账号或密码错误！')
            return redirect(url_for('login'))



# JSON_PATH = './notebooks/ai_challenger_oqmrc_trainingset.json'
# insert pre-data to the database from training and valid json file

# @app.route('/insert_data')
# def insert_data():
#     with open(JSON_PATH, 'r', encoding='utf-8') as f:
#         for line in tqdm(f.readlines()):
#             dic = json.loads(line, encoding='utf-8')
#             q_text = dic['query']
#             p_text = dic['passage']
#             alternatives = dic['alternatives']
#             dataset = 'train'
#             question = Question(q_text=q_text, p_text=p_text, 
#                 alternatives=alternatives, dataset=dataset)
#             db.session.add(question)
#     db.session.commit()
#     return 'Done'
