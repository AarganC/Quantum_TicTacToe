import logging
from contracts import Agent, GameState
from qiskit import IBMQ
from qiskit.tools.monitor import job_monitor
from qiskit.providers.ibmq import least_busy
from qiskit.tools.visualization import plot_histogram
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class QuantumAgent(Agent,):
    def __init__(self):
        self.move = 0
        self.num_qubits = 9
        self.num_t_gates = [0] * self.num_qubits
        self.action_space_size = [None] * self.num_qubits
        self.i = 0

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
            # print(x)
            board[x] = None

        # print(board)

        num_qubits = 9

        use_ibm = False
        if self.i == 0 and use_ibm:
            IBMQ.save_account(
                'mykey',
                overwrite=True)

            IBMQ.load_account()
            # provider = IBMQ.get_provider(hub='ibm-q')

            # backend = least_busy(provider.backends(filters=lambda x:
            # x.configuration().n_qubits >= 9 and
            #     not x.configuration().simulator and
            #     x.status().operational == True))
            # print("least busy backend: ", backend)
            self.i += 1


        # reset the T gate counter
        self.num_t_gates = [0] * num_qubits
        # Reserve des adresses mémoire afin de stocker 9 qbits
        q = QuantumRegister(num_qubits)
        # Le classicalregister permet definir un registre pour stocker les résultats, dans se cas 9 qbits qui
        # correspondent à l'ensemble des cases du jeu
        c = ClassicalRegister(num_qubits)
        # Création du circuit
        qc = QuantumCircuit(q, c)

        # make the option definitely a 1 if there is a move in the space already
        for index, move in enumerate(board):

            if move:
                # delete action from possibilities
                qc.x(q[index])
            else:
                # this space is a potential move
                # so put into a superposition
                qc.h(q[index])

                t_count = 0

                # so it is the start of a row
                if index % 3 == 0:

                    # two pieces in a row - need to block/win
                    if board[index + 1] and board[index + 2] and board[index + 1] == board[index + 2]:
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    # only one of the spaces is occupied (^ is xor, but they both have to explicitly be bools)
                    elif bool(board[index + 1]) ^ bool(board[index + 2]):
                        qc.t(q[index])
                        t_count += 1

                # so it is the middle of a row
                if index % 3 == 1:

                    # two pieces in a row - need to block/win
                    if board[index + 1] and board[index - 1] and board[index + 1] == board[index - 1]:
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    elif bool(board[index + 1]) ^ bool(board[index - 1]):
                        qc.t(q[index])
                        t_count += 1

                # so it is the end of a row
                if index % 3 == 2:
                    # two pieces in a row - need to block/win
                    if board[index - 1] and board[index - 2] and board[index - 1] == board[index - 2]:
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    elif bool(board[index - 1]) ^ bool(board[index - 2]):
                        qc.t(q[index])
                        t_count += 1

                # so is the top row
                if index / 3 < 1:
                    if board[index + 3] and board[index + 6] and board[index + 3] == board[index + 6]:
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    elif bool(board[index + 3]) ^ bool(board[index + 6]):
                        qc.t(q[index])
                        t_count += 1

                # so it is the middle row
                if 2 > index / 3 >= 1:
                    if board[index - 3] and board[index + 3] and board[index - 3] == board[index + 3]:
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    elif bool(board[index - 3]) ^ bool(board[index + 3]):
                        qc.t(q[index])
                        t_count += 1

                # so it is the top row
                if index / 3 >= 2:
                    if board[index - 3] and board[index - 6] and board[index - 3] == board[index - 6]:
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    elif bool(board[index - 3]) ^ bool(board[index - 6]):
                        qc.t(q[index])
                        t_count += 1

                self.num_t_gates[index] = t_count

        # hard code in the diagonals
        if board[0] and board[0] == board[4]:
            qc.t(q[8])
            qc.t(q[8])
            qc.t(q[8])
            self.num_t_gates[8] += 3
        if board[0] and board[0] == board[8]:
            qc.t(q[4])
            qc.t(q[4])
            qc.t(q[4])
            self.num_t_gates[4] += 3
        if board[4] and board[4] == board[8]:
            qc.t(q[0])
            qc.t(q[0])
            qc.t(q[0])
            self.num_t_gates[0] += 3
        if board[2] and board[2] == board[4]:
            qc.t(q[6])
            qc.t(q[6])
            qc.t(q[6])
            self.num_t_gates[6] += 3
        if board[2] and board[2] == board[6]:
            qc.t(q[4])
            qc.t(q[4])
            qc.t(q[4])
            self.num_t_gates[4] += 3
        if board[4] and board[4] == board[6]:
            qc.t(q[2])
            qc.t(q[2])
            qc.t(q[2])
            self.num_t_gates[2] += 3

        for index, move in enumerate(board):
            if not move:
                qc.h(q[index])
            else:
                # if there is already a move there - don't show that any t gates were applied
                self.num_t_gates[index] = -1
        qc.measure(q, c)

        backend = Aer.get_backend('qasm_simulator')
        logger.info("Made the circuit, running it on the backend: {}".format(backend))
        shots = 100
        # job_sim = execute(qc, backend, shots=shots)
        job_sim = execute(qc, backend=backend, shots=shots)
        sim_result = job_sim.result().get_counts(qc)

        job_monitor(job_sim, interval=2)

        counts = [0]*num_qubits

        for key, count in sim_result.items():
            # need to iterate over the results and see when the value was chosen most

            # keys are the opposite way round to expected
            key = key[::-1]
            for index, val in enumerate(key):
                if val == '1':
                    counts[index] += count

        max_count = 0
        max_index = 0
        for index, count in enumerate(counts):
            if not board[index] and count > max_count:
                max_index = index
                max_count = count

        self.move = max_index
        results = job_sim.result()
        answer = results.get_counts(qc)

        '''
        plot_circuit = qc.draw(output="mpl")
        plot_hist = plot_histogram(answer)
        plot_circuit = qc.draw(output="mpl")
        plot_hist.show()
        plot_circuit.show()
        plot_hist.savefig('quantum_grover_agent_histogram.png')
        '''

        # logger.info("Quantum choice = {}".format(self.move))
        return self.move

    def observe(self, r: float, t: bool, player_index: int):
        pass
