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
registration_user = Table('registration', metadata,
    Column('id', Integer(), primary_key=True),
    Column('login', String(15), nullable=False),
    Column('password', String(15), nullable=False)
)

 # таблица создания новых заданий и отслеживания статуса
task_user = Table('task_creat', metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(100), nullable=False),
    Column('text', String(), nullable=False),
    Column('status', String(), nullable=True),
    Column('task_on', DateTime(), default=datetime.now),
    Column('task_work', DateTime(), default=None),
    Column('task_of', DateTime(), default=None),
    Column('task_cancell', DateTime(), default=None)
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
        return render_template("task_creat.html")

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
        #return render_template("task_open.html")
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
    #articles = conn.execute(select([task_user]).order_by(desc(task_user.c.task_on))).fetchall()
    return render_template("task_open.html", articles=articles)

# страница выполнения заданий
@app.route('/task_work', methods= ['POST', 'GET'])
def tast_work2():

    if request.method == "POST":
        print('if')
        conn = engine.connect()

        stm = task_user.update().values(status=None)
        conn.execute(stm)
        return render_template("task_work.html")
    else:
        print('else')
        conn = engine.connect()
        sel = select([task_user]).order_by(desc(task_user.c.task_on))
        r = conn.execute(sel)
        articles = r.fetchall()
    return render_template("task_work.html", articles=articles)


@app.route('/user/<string:name>/<int:id>') # отслеживание странички user
def user(name, id):
    return "User page: " + name + " - " + str(id)



if __name__ == "__main__":
    app.run(debug=True)
