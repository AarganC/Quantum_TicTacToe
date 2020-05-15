import logging
import random
import numpy as np
from qiskit import Aer, execute, QuantumCircuit, QuantumRegister, ClassicalRegister
from contracts import Agent, GameState

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class QuantumGroverAgent(Agent,):
    def __init__(self):
        self.move = 0
        self.vector = [0]*8
        self.counts = {}

    def act(self, gs: GameState) -> int:
        """
        Args:
            board [int] : the current state of the board
        Returns:
            int : the index of the move to be made
        """

        # TODO would it be better to only map to qubits that could be moves
        # However this would mean lots of index/physical qubit number swaps

        board = [-1] * 9
        # print(board)
        # print(gs.get_available_actions(gs.get_active_player()))
        for x in gs.get_available_actions(gs.get_active_player()):
            print(x)
            board[x] = None

        # print(board)

        # create a superpositon of potential moves
        groverCircuit, registers = self._board_to_superposition(board)

        # this means the only avaliable space is the last one
        if isinstance(groverCircuit, int):
            self.move = groverCircuit
            return

        # add the oracle
        QuantumGroverAgent._oracle(groverCircuit, registers[0])

        # add the diffusion operator
        QuantumGroverAgent._inversion_about_average(groverCircuit, registers[0], 3)

        # measure the results
        groverCircuit.measure(registers[0], registers[1])

        # run the circuit
        backend = Aer.get_backend('qasm_simulator')
        shots = 1024
        results = execute(groverCircuit, backend=backend, shots=shots).result()
        answer = results.get_counts()

        reversed_answer = {}

        # reverse all the keys
        for state, count in answer.items():
            reversed_answer[state[::-1]] = count

        print(reversed_answer)

        # get the highest move
        max_count = 0
        winning_state = ''
        for state, count in reversed_answer.items():
            if count > max_count:
                max_count = count
                winning_state = state

        print('The move is ', winning_state, ' which is the same as ', str(int(winning_state, 2)))

        self.move = int(winning_state, 2)
        self.counts = reversed_answer

        # shouldn't happen? but just in case
        if board[int(winning_state, 2)]:
            spaces = [i for i, mv in enumerate(board) if mv is None]
            self.move = random.choice(spaces)

        # logger.info("Quantum choice = {}".format(self.move))
        return self.move


    def observe(self, r: float, t: bool, player_index: int):
        pass

    def _board_to_superposition(self, board):
        # have to strip off the last thing to fit into 3 qubits
        board = board[:-1]

        spaces = [i for i, space in enumerate(board) if space is None]

        print('spaces at ', spaces)

        if len(spaces) == 0:
            # no spaces - so must have to go in the last space (8)
            return 8, None

        # all the spaces need to be equally likely
        amplitude = 1 / np.sqrt(len(spaces))
        print('amplitude : ', amplitude)

        desired_vector = [amplitude if i in spaces else 0 for i in range(len(board))]
        print('vector ', desired_vector)

        self.vector = desired_vector

        q = QuantumRegister(3)
        c = ClassicalRegister(3)
        qc = QuantumCircuit(q, c)

        qc.initialize(desired_vector, [q[0], q[1], q[2]])

        return qc, (q, c)

    @staticmethod
    def _n_controlled_Z(circuit, controls, target):
        """Implement a Z gate with multiple controls"""
        if len(controls) > 2:
            raise ValueError('The controlled Z with more than 2 controls is not implemented')
        elif len(controls) == 1:
            circuit.h(target)
            circuit.cx(controls[0], target)
            circuit.h(target)
        elif len(controls) == 2:
            circuit.h(target)
            circuit.ccx(controls[0], controls[1], target)
            circuit.h(target)

    @staticmethod
    def _inversion_about_average(circuit, register, n):
        """Apply inversion about the average step of Grover's algorithm."""
        circuit.h(register)
        circuit.x(register)
        QuantumGroverAgent._n_controlled_Z(circuit, [register[j] for j in range(n - 1)], register[n - 1])
        circuit.x(register)
        circuit.h(register)

    @staticmethod
    def _oracle(circuit, register):
        circuit.z(register[2])
