from agents import CommandLineAgent, RandomAgent, RandomRolloutAgent
from environments.tictactoe import TicTacToeGameState
from runners import run_to_the_end

if __name__ == "__main__":
    gs = TicTacToeGameState()
    agent0 = CommandLineAgent()
    agent1 = RandomRolloutAgent(100, False)

    print(gs)
    run_to_the_end([agent0, agent1], gs)
    print(gs)
