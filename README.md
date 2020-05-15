## Tic Tac Toe

> Special Tic Tac Toe based on quantum 

| developers | Github |
|--|--|
| Aargan COINTEPAS | [url](https://github.com/AarganC) |
| Bernard VONG | [url](https://github.com/bernardVong) |

### Done 
 - [x] add basic quantum agent
 - [x] add grover quantum agent
 - [x] add command line agent
 - [x] add web interface agent
 - [x] manage multiple agents on GUI
 - [x] connected to IBM servers
 - [x] plot circuit and qbits
 - [ ] fix plot display on GUI (related to [this issue](https://github.com/Qiskit/qiskit-terra/issues/4439))


### Requirements
Environment working on :
- Python 3.7
- Qiskit 0.19.1 
- Flask 1.1.2

> if needed, set the correct versions below install commands

    pip install qiskit
    pip install matplotlib
	pip install jupyter
	pip install ipywidgets
	pip install seaborn
	pip install pygments
	pip install flask
	    

### Quick Start
GUI :
- launch server:	`bash run.sh`
- then open games :
	- [http://localhost:5000/basic](http://localhost:5000/basic)
	- [http://localhost:5000/grover](http://localhost:5000/grover)


Command line : 
- choose one experiment on /environments/tictactoe/[EXPERIMENT].py
- and then `python [EXPERIMENT].py`


### Notes 

The main modifications for Quantum are located on `agents` folder and `environments` folder

We have commented the plot display in basic and grover agents, because of Qiskit [issue #4439](https://github.com/Qiskit/qiskit-terra/issues/4439).

This project is based on an Custom Tic Tac Toe project and on [TicTacQ](https://qiskit.org/experiments/tictacq/) project

