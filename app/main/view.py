from flask import render_template, redirect, url_for, request, current_app, flash
from .forms import SearchForm, PredictForm
from . import main
from app.models import Question
from app.net.predict import predict
import config

result = None

@main.route('/', methods=['POST', 'GET'])
def index():
    form = SearchForm()
    num = 0
    if form.validate_on_submit():
        keyword = form.keyword.data
        if keyword is not None:
            quers = Question.query.filter(Question.q_text.like(
            '%' + keyword + '%'))
            for _ in quers:
                num += 1
            global result
            result = {'quers':quers,
                    'num': str(num),
                    'keyword': keyword, 
                    }
            return redirect(url_for('.list'))
    return render_template('index.html', form=form)


@main.route('/list/', methods=['POST', 'GET'])
def list():
    if request.method == 'GET':
        global result
        page = request.args.get('page', 1, type=int)
        pagination = result['quers'].paginate(page, per_page=config.PER_PAGE,
                    error_out=False)
        questions = pagination.items
        
        return render_template('list.html', questions=questions, 
                    num=result['num'], keyword=result['keyword'],
                    pagination=pagination)
    else:
        return redirect(url_for('index'))
        

@main.route('/detail/<id>', methods=['POST', 'GET'])
def detail(id):
    form = PredictForm()
    question = Question.query.filter(Question.id==int(id)).first()
    if form.validate_on_submit():
        # design a function to predict the answer
        answer = predict(question)
        flash('预测答案为:{}'.format(answer)) 
    return render_template('detail.html', form=form, question=question)