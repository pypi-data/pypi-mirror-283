"""
-*- coding: utf-8 -*-
@Author : Cui Jinghao
@Time : 2024/6/28 15:49
@Function: common_gates
@Contact: cuijinghao@tgqs.net
"""
from typing import Union

# global parameters
BASE_SINGLE_GATE = ['h', 'x', 'y', 'z', 'rx', 'ry', 'rz', 'u3', 's', 'sdg', 't', 'tdg', "damp_I", "pd", "ad"]
BASE_DOUBLE_GATE = ['cx', 'swap', 'iswap', 'cz', 'cp', 'rxx', 'ryy', 'rzz', 'syc']
BASE_TRIPLE_GATE = ['ccx', 'cswap']


# todo: implemented these examples below only, will implement other gates classes later
class _Pauli:
    def __init__(self):
        pass

    def __call__(self):
        return

    def gate(self):
        pass


class _X(_Pauli):
    def __init__(self, qbit=0, name='x', theta=None):
        self._qbit = qbit
        self._name = name
        self._theta = theta

    def __call__(self, qbit):
        return self.gate(qbit)

    def gate(self, qbit):
        return {'qbit': qbit, 'name': self._name, 'theta': self._theta}

x = _X()


class _Y(_Pauli):
    def __init__(self, qbit=0, name='y', theta=None):
        self._qbit = qbit
        self._name = name
        self._theta = theta

    def __call__(self, qbit):
        return self.gate(qbit)

    def gate(self, qbit):
        return {'qbit': qbit, 'name': self._name, 'theta': self._theta}

class _H:
    def __init__(self, qbit=0, name='h', theta=None):
        self._qbit = qbit
        self._name = name
        self._theta = theta

    def __call__(self, qbit):
        return self.gate(qbit)

    def gate(self, qbit):
        return {'qbit': qbit, 'name': self._name, 'theta': self._theta}


h = _H()



class _RX:
    def __init__(self, qbit=0, name='rx', theta=0):
        self._qbit = qbit
        self._name = name
        self._theta = theta

    def __call__(self, qbit, theta):
        return self.gate(qbit, theta)

    def gate(self, qbit, theta):
        return {'qbit': qbit, 'name': self._name, 'theta': theta}


rx = _RX()


class _RXX:
    def __init__(self, qbit0=0, qbit1=1, name='rxx', theta=0):
        self._qbit0 = qbit0
        self._qbit1 = qbit1
        self._name = name
        self._theta = theta

    def __call__(self, qbit0, qbit1, theta):
        return self.gate(qbit0, qbit1, theta)

    def gate(self, qbit0, qbit1, theta):
        return {'qbit': [qbit0, qbit1], 'name': self._name, 'theta': theta}


rxx = _RXX()


class _CCX:
    def __init__(self, control_qbit=[0, 1], target_qbit=2, name='ccx', theta=None):
        self._control_qbit = control_qbit
        self._target_qbit = [target_qbit]
        self._name = name
        self._theta = theta

    def __call__(self, control_qbit, target_qbit):
        return self.gate(control_qbit, target_qbit)

    def gate(self, control_qbit, target_qbit):
        return {'qbit': control_qbit + [target_qbit], 'name': self._name, 'theta': self._theta}


ccx = _CCX()



