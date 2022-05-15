from flask import Blueprint, render_template, url_for, redirect

main = Blueprint('main', __name__)

# Main Authentication
@main.route('/login')
def login():
    return render_template('login.html', logged_in=False)

@main.route('/signup')
def signup():
    return render_template('signup.html',logged_in=False)


# Base
@main.route('/')
def index():
    return render_template('index.html',logged_in=False)


@main.route('/welcome')
def welcome():
    return render_template('welcome.html',logged_in=True)

@main.route('/logout')
def sair():
    return redirect(url_for('main.index'))


#Simulations
@main.route('/simulations/criarSimulacoes', methods=['GET'])
def criarSimulacoes():
    return render_template('createSimulation.html',logged_in=True)

@main.route('/simulations/', methods=['GET'])
def verSimulacoes():
    return render_template('listSimulations.html',logged_in=True)


@main.route('/simulations/menu/<simId>')
def simulationMenu(simId):
    return render_template('simMenu.html', simId=simId,logged_in=True)
