from flask import Flask,render_template,request,session, redirect, url_for,send_from_directory
from models import db,User,Experiment,Node,Scenario,Result
from forms import SignupForm, LoginForm,ExperimentForm,NodesForm,NodeForm
from flask_bootstrap import Bootstrap
from flask_login import  LoginManager, UserMixin,login_user, login_required, logout_user, current_user
import os
import socket
import pickle
import time

controller_address = ('127.0.0.1',9999)


app = Flask(__name__)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.debug = True
POSTGRES = {
    'user': 'berrybed',
    'pw': '1234',
    'db': 'berrybed',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'development-key'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Function to get the existing Nodes
def network_info():
    s = socket.socket()
    s.connect((controller_address))
    s.send("status/number".encode())
    msg = str(s.recv(1024),'utf-8')
    #msg = pickle.loads(msg)
    print(msg)
    counter = int(msg)
    forms = []
    nodes = []
    for i in range(counter):
        number = "status/id/" + str(i)
        print(number)
        s.send(number.encode())
        msg = s.recv(1024)
        msg = pickle.loads(msg)
        nodes.append(msg)
    print(nodes)
    s.send('close'.encode())
    s.close()
    return nodes


@app.route('/')
def index():
	return render_template("index.html")

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/signup',methods=['GET','POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('home'))
    form  = SignupForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html',form=form)
        else:
            newuser = User(form.username.data,form.password.data,form.email.data)
            db.session.add(newuser)
            db.session.commit()
            return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                session['username'] = user.username
                return redirect(url_for('home'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)         


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route('/home')
@login_required
def home():
    return render_template("home.html")

@app.route('/experiment',methods=["GET","POST"])
@login_required
def experiment():
    form = ExperimentForm()
    if request.method == "POST":
        if form.validate() == False:
            return render_template("experiment.html",form=form)
        else:
            title = form.title.data
            description = form.description.data
            etype = form.etype.data
            protocol = form.protocol.data
            duration = form.duration.data
            username = session['username']
            user = User.query.filter_by(username=username).first()
            exp = Experiment(uid=user.id,title=title,duration=duration,protocol=protocol,description=description)
            db.session.add(exp)
            db.session.flush()
            session['current_experiment'] = exp.eid
            db.session.commit()
            print(exp.eid)
            return redirect(url_for('node'))
    elif request.method == "GET":
        return render_template("experiment.html",form=form)

@app.route("/exp_history")
@login_required
def exp_history():
    username = session['username']
    user = User.query.filter_by(username=username).first()
    exps = Experiment.query.filter_by(uid=user.id)
    return render_template("exp_history.html",exps=exps)

@app.route('/node',methods=["GET","POST"])
def node():
    nodes = network_info()
    form = NodeForm()
    if request.method == "POST":
        if form.validate() == False:
            return render_template("node.html",form=form,nodes=nodes)
        else:
            name = form.name.data
            humdity = form.humdity.data
            temperature = form.temperature.data
            mode = form.mode.data
            if mode:
                protocol = "cord"
            else:
                protocol = "rott"
            eid = session['current_experiment']

            print( "name: " + str(name) + " humdity: " + str(humdity) + " temperature: " + str(temperature) + " mode:" + str(mode))
            node = Node(eid=eid,name=name,humdity=humdity,temperature=temperature,protocol=protocol)
            db.session.add(node)
            db.session.commit()
            return redirect(url_for("node"))
    elif request.method == "GET":            
        return render_template("node.html",form=form,nodes=nodes)


@app.route('/scenario',methods=["GET","POST"])
def scenario():
    eid = session['current_experiment']
    nodes = Node.query.filter_by(eid=eid)
    #scenario = ScenarioForm()
    if request.method == "POST":
            en1 = request.form.get('en1',None)
            en2 = request.form.get('en2',None)
            scenario = Scenario(eid=eid,en1=en1,en2=en2)
            db.session.add(scenario)
            db.session.commit()
            return redirect(url_for("scenario"))
    elif request.method == "GET":
        return render_template("scenario.html",nodes=nodes)

@app.route('/checknodes')
def checknodes():
    eid = session['current_experiment']
    nodes = Node.query.filter_by(eid=eid)
    return render_template("checkNodes.html",nodes=nodes)


@app.route("/sendid")
def sendid():
    eid = session['current_experiment']
    s = socket.socket()
    s.connect((controller_address))
    msg = "add/" + str(eid)
    print(msg)
    s.send(msg.encode())
    time.sleep(1)
    s.send('close'.encode())
    s.close()
    return "Experiment Added to Queue"

@app.route("/result/<eid>")
@login_required
def result(eid):
    result = Result.query.filter_by(eid=eid)
    return render_template("result.html",result=result)

@app.route("/res/<path:path>")
def send_csv(path):
    path = path.split("/")
    print(path)
    return send_from_directory(path[0], path[1])

if __name__ == '__main__':
    db.init_app(app)

    app.run()
