from ast import Bytes
import random
from .vis_bloch import plot_bloch_circles


class qbit:
    """
    qbit class
    """

    def __init__(self):
        self.q = [0, 0, 1]

    def rotY90(self):
        x, y, z = self.q
        # 90 deg rot on y axis
        if z == 1 and x == 0:
            self.q[0] += 1
            self.q[2] -= 1
        elif z == 0 and x == 1:
            self.q[0] -= 1
            self.q[2] -= 1
        elif z == -1 and x == 0:
            self.q[0] -= 1
            self.q[2] += 1
        elif z == 0 and x == -1:
            self.q[0] += 1
            self.q[2] += 1

    def rotX90(self):
        x, y, z = self.q
        # 90 deg rot on y axis
        if z == 1 and y == 0:
            self.q[1] += 1
            self.q[2] -= 1
        elif z == 0 and y == 1:
            self.q[1] -= 1
            self.q[2] -= 1
        elif z == -1 and y == 0:
            self.q[1] -= 1
            self.q[2] += 1
        elif z == 0 and y == -1:
            self.q[1] += 1
            self.q[2] += 1

    def rotZ90(self):
        x, y, z = self.q
        # 90 deg rot on y axis
        if x == 1 and y == 0:
            self.q[0] -= 1
            self.q[1] -= 1
        elif x == 0 and y == -1:
            self.q[0] -= 1
            self.q[1] += 1
        elif x == -1 and y == 0:
            self.q[0] += 1
            self.q[1] += 1
        elif x == 0 and y == 1:
            self.q[0] += 1
            self.q[1] -= 1

    def X(self):
        self.rotX90()
        self.rotX90()
        return self.q

    def Y(self):
        self.rotY90()
        self.rotY90()
        return self.q

    def Z(self):
        self.rotZ90()
        self.rotZ90()
        return self.q

    def getState(self):
        return self.q

    def H(self):
        self.rotY90()
        self.rotX90()
        self.rotX90()
        return self.q

    def CNOT(self, z):
        if z == 0:
            if random.randint(0, 1) == 1:
                self.X()
        elif z == -1:
            self.X()
        return

    def Measure(self):
        if self.q[-1] == 0:
            if random.randint(0, 1) == 0:
                self.q[-1] = 1
            else:
                self.q[-1] = -1
            self.q[0] = 0
        return self.q

    def reset(self):
        self.q = [0, 0, 1]

    def visualize(self):
        plot_bloch_circles(self.q)


def run(s, circuit, shots):
    """
    Run the circuit

    Args:
        s (list): List of qbit objects
        shots (int): Number of shots to run the circuit
        circuit (list): List of gates and qbit objects

    Returns:
        None

    Example:
        >>> import simple_qsim
        >>> q = [simple_qsim.qbit()]
        >>> circuit = [
        ...     ["H", q],
        ...     ["X", q],
        ...     ["Y", q],
        ...     ["Z", q],
        ...     ["CNOT", q, q],
        ...     ["CZ", q, q],
        ... ]
        >>> simple_qsim.run(q, circuit, 10)
        [0.0, [0, 0, 1]]
        [0.0, [0, 0, 1]]
        ...
        [100.0, [1, 0, 0]]
        [100.0, [1, 0, 0]]


    """
    possibleStates = 2 ** len(s)
    print(f"{possibleStates} Possible States\n\n")
    statesFound = []
    states = []
    MeasurementHistory = []
    for _ in range(shots):
        StateChangeHistory = []
        for l, i in enumerate(circuit):
            if i[0] == "H":
                i[1].H()
            if i[0] == "X":
                i[1].X()
            if i[0] == "Y":
                i[1].Y()
            if i[0] == "Z":
                i[1].Z()
            if i[0] == "CNOT":
                i[1].CNOT(i[2].q[2])
            if i[0] == "CZ":
                i[1].H()
                i[1].CNOT(i[2].Measure()[2])
                i[1].H()
        qbitStates = []
        for i in s:
            m = i.Measure()[2]
            if m == 1:
                qbitStates.append(0)
            elif m == -1:
                qbitStates.append(1)
            elif m == 0:
                qbitStates.append(random.randint(0, 1))
            i.reset()
        MeasurementHistory.append(qbitStates)
    for i, z in enumerate(MeasurementHistory):
        if z not in states:
            statesFound.append(
                [round((MeasurementHistory.count(z) / shots) * 100, 2), z]
            )
            states.append(z)
    statesFound.sort(key=lambda x: x[0], reverse=True)
    num = int("".join(str(e) for e in statesFound[0][1]), 2)
    for i in statesFound:
        if i[0] != 0:
            print(i)
