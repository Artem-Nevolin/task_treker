from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, create_engine, insert, select,\
    desc, update
from datetime import datetime

app = Flask(__name__)

metadata = MetaData()
engine = create_engine('sqlite:///task.db', echo=True) # используем относительный путь

conn = engine.connect()
#print(engine)

# таблица регистрации
registration_user = Table('registration_user', metadata,
    Column('id', Integer(), primary_key=True),
    Column('login', String(15), nullable=False),
    Column('password', String(15), nullable=False)
)

 # таблица создания новых заданий и отслеживания статуса
task_user = Table('task_user', metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(100), nullable=False),
    Column('text', String(), nullable=False),
    Column('status', String(), nullable=True),
    Column('task_on', DateTime(), default=datetime.now),
    Column('task_work', DateTime()),
    Column('task_of', DateTime()),
    Column('task_cancell', DateTime(), default=None),
    Column('task_time_job', DateTime())
)
metadata.create_all(engine)

# создание страницы регистрации
@app.route('/', methods= ['POST', 'GET'])
def registration():
    if request.method == "POST":  # TODO
        login1 = request.form.get('login')
        password1 = request.form.get('password')
        ins = registration_user.insert()
        new_user = ins.values(login = login1, password = password1)
        conn = engine.connect()
        conn.execute(new_user)
        return redirect("/task_creat")
    else:
        return render_template("registration.html")

# coздание страницы "Создать задачу"
@app.route('/task_creat', methods= ['POST', 'GET'])
def tast_creat():
    if request.method == "POST":  # TODO
        name1 = request.form.get('name')
        text1 = request.form.get('text')
        ins = task_user.insert()
        new_user = ins.values(name=name1, text=text1, status=None)
        conn = engine.connect()
        conn.execute(new_user)
        return redirect('/task_open')
    else:
        return render_template("task_creat.html")

# coздание страницы "Открытые задачи"
@app.route('/task_open', methods= ['POST', 'GET'])
def tast_open():
    conn = engine.connect()
    sel = select([task_user]).order_by(desc(task_user.c.task_on))
    r = conn.execute(sel)
    articles = r.fetchall()
    return render_template("task_open.html", articles=articles)

# страница выполнения заданий.
@app.route('/task_work', methods= ['POST', 'GET'])
def tast_work2():

    if request.method == "POST":
        conn = engine.connect()
        stm = task_user.update().values(status=None)
        conn.execute(stm)
        return render_template("task_work.html")
    else:
        conn = engine.connect()
        sel = select([task_user]).order_by(desc(task_user.c.task_on))
        r = conn.execute(sel)
        articles = r.fetchall()
    return render_template("task_work.html", articles=articles)

# обработка нажатий на "Взять в работу"
@app.route('/task_work/<int:id>')
def adding(id):
    task_work1 = datetime.now()
    s = task_user.update().where(task_user.c.id == id).values(status='1', task_work=task_work1)
    conn = engine.connect()
    conn.execute(s)
    return redirect('/task_open')


# обработка нажатий на "Выполнено"
@app.route('/task_finish/<int:id>')
def adding_finish(id):
    task_of1 = datetime.now()
    s = task_user.update().where(task_user.c.id == id).values(status='2', task_of=task_of1)
    conn = engine.connect()
    conn.execute(s)
    return redirect('/task_open')


# обработка нажатий на кнопку "Отменить"
@app.route('/task_cancell/<int:id>')
def adding_cancell(id):
    task_cancell1 = datetime.now()
    s = task_user.update().where(task_user.c.id == id).values(status='2', task_cancell=task_cancell1)
    conn = engine.connect()
    conn.execute(s)
    return redirect('/task_open')

# страница с "Архив"
@app.route('/backup')
def backup_open():
    conn = engine.connect()
    sel = select([task_user]).order_by(desc(task_user.c.task_on))
    r = conn.execute(sel)
    articles = r.fetchall()
    return render_template("backup.html", articles=articles)


# страница "Статистика"
@app.route('/stat')
def stat():
    conn = engine.connect()
    sel = select([task_user]).order_by(desc(task_user.c.task_on))
    r = conn.execute(sel)
    articles = r.fetchall()

    # расчет количества открытых задач
    count_task_on = 0
    for i in articles:
        if not i[3] and i[4]:
            count_task_on += 1

    # расчет количества отмененных задач
    count_task_cancell = 0
    for i in articles:
        if i[7]:
            count_task_cancell += 1

    # расчет количества открытых задач
    count_task_work = 0
    for i in articles:
        if not i[6] and i[5]:
            count_task_work += 1

    # расчет среднего времени выполнения задачи
    #сount_time_job_sum = None
    for i in articles:

        if i[6]:
            print(i[6])
            task_time_job = i[6]-i[5]
            print('Привет')
            print(task_time_job)
            temp = None
            if task_time_job:
                temp = task_time_job + task_time_job
            print("temp", temp)
            print('________')
            print(task_time_job)
            #print(сount_time_job_sum)
            #s = task_user.update().values(task_time_job=task_time_job)
            #conn = engine.connect()
            #conn.execute(s)


    return render_template("stat.html", articles=articles, count_task_on=count_task_on,
                           count_task_cancell=count_task_cancell, count_task_work=count_task_work)



if __name__ == "__main__":
    app.run(debug=True)
