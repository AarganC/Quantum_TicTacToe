from agents import RandomRolloutAgent, QuantumAgent
from environments.tictactoe import TicTacToeGameState
from runners import run_to_the_end

if __name__ == "__main__":
    gs = TicTacToeGameState()
    agent0 = RandomRolloutAgent(100, False)
    agent1 = QuantumAgent()

    print(gs)
    run_to_the_end([agent0, agent1], gs)
    print(gs)
