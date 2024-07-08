# Quantum Computer Simulator

This is a simple project to simulate quantum behaviour on your local machine. One of the benefit of running this locally is there is essentially no limit on how many qubits can scale too, it comes down to your PC's specs and how many qubits you as a person handle.

# How to use

1. Create a simple python file, say `main.py`, with the following content.

```
import simple_qsim

# Register number of qubits you want to use.
s = [
	simple_qsim.q() for _ in  range(3)
]

# Sample Circuit
c = [
["H", s[0]],
["H", s[1]],
["H", s[2]],
["Z", s[2]],
["CZ", s[0], s[1]],
["H", s[0]],
["H", s[1]],
["H", s[2]],
]

# Run the circuit
simple_qsim.run(s, shots=10000, circuit=c)
```

2. Then run it using python
   `python3 main.py`
3. You should see something like:

```
8 Possible States


[25.85, [0, 1, 1]]
[25.07, [1, 0, 1]]
[24.77, [1, 1, 1]]
[24.31, [0, 0, 1]]
```

You can verify or use the GUI on IBM's platform here: [IBM Quantum Composer](https://quantum.ibm.com/composer/)

# Available Gates

You can learn more about quantum gates at [Wikipeida](https://en.wikipedia.org/wiki/Quantum_logic_gate)

1. Single Qubit Gates

````
	a. Hadamard Gate (H)
		Puts the qubit in super position
		Use - ```["H", q[n]]```
	b. Pauli Gates (X,Y,Z)
		Spins the qubit 90deg in that axis
		Use - ["X", q[n]]
			  ["Y", q[n]]
			  ["Z", q[n]]
````

2. Controlled Gates

```
	a. Controlled-NOT (CNOT)
		Performs a not operation on targed when the control bit is |1⟩
		Use - ["CNOT", <target>, <control>]
	b. Controlled-Z (CZ)
		Performs a Pauli Z operation on targed when the control bit is |1⟩
		Use - ["CZ", <target>, <control>]
```

# Contribution

I might or might not update this repo myself, however I am open to contribution!

# License

All the code available in this repo is under apache 2.0 license.
