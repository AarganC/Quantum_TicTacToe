from contracts import Agent, GameState


class WebAgent(Agent):
    def __init__(self):
        self.action = -1
        self.message = "OK"

    def act(self, gs: GameState) -> int:
        print(gs)
        available_actions = gs.get_available_actions(gs.get_active_player())

        if self.action in available_actions:
            self.message = "Your turn"
            return self.action
        else:
            self.message = "Action not valid, please try again with : " + str(available_actions)
            return -1

    def observe(self, r: float, t: bool, player_index: int):
        pass
