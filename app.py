from flask import Flask, render_template, jsonify, request
from runners import run_step
from agents import CommandLineAgent, QuantumAgent, WebAgent, QuantumGroverAgent
from environments.tictactoe import TicTacToeGameState
from runners import run_to_the_end

app = Flask(
    __name__,
    template_folder='static'
)

player_agent = WebAgent()
basic_agent = QuantumAgent()
grover_agent = QuantumGroverAgent()

basic_gs = TicTacToeGameState()
grover_gs = TicTacToeGameState()



# OLD SYNCHRONOUS CODE
# run_to_the_end([player_agent, basic_agent], basic_gs)
# run_to_the_end([player_agent, grover_agent], grover_gs)



######## FAST WEB ROOTING ##########
@app.route('/basic')
def basic_index():
    data = {
        "title": "Basic Agent",
        "game": "basic"
    }
    return render_template('html/index.html', data=data)

@app.route('/grover')
def grover_index():
    data = {
        "title": "Grover Agent",
        "game": "grover"
    }
    return render_template('html/index.html', data=data)



######## FAST API ROOTING ##########
@app.route('/api/<game_type>/status')
def api_basic_agent_status(game_type):

    gs = get_gs(game_type)

    data = {
        "board": gs.board.tolist(),
        "message": "Game finished." if gs.game_over else "Your turn!"
    }
    return jsonify(data)


@app.route('/api/<game_type>/play')
def api_basic_agent_play(game_type):

    gs = get_gs(game_type)
    agent = get_agent(game_type)

    position = request.args.get("position")
    player_agent.action = int(position)

    run_step([player_agent, agent], gs)
    run_step([player_agent, agent], gs)

    data = {
        "status": 200,
        "message": player_agent.message,
        "game": "basic",
        "position_played": position
    }
    return jsonify(data)


@app.route('/api/<game_type>/restart')
def api_basic_agent_reset(game_type):

    global basic_gs
    basic_gs = TicTacToeGameState()

    data = {
        "status": 200,
        "message": "Game State reseted",
        "game": "basic"
    }
    return jsonify(data)


def get_gs(game_type):
    if game_type == 'grover':
        return grover_gs

    return basic_gs


def get_agent(game_type):
    if game_type == 'grover':
        return grover_agent

    return basic_agent
