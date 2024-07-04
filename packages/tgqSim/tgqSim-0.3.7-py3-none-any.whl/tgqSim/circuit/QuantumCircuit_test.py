"""
-*- coding: utf-8 -*-
@Author : Cui Jinghao
@Time : 2024/7/2 14:37
@Function: test
@Contact: cuijinghao@tgqs.net
"""

from build.tgqSim.circuit.QuantumCircuit import QuantumCircuit
import build.tgqSim as tgqs
import numpy as np
from build.tgqSim.sim.QuantumSimulator import QuantumSimulator


if __name__ == '__main__':
    # use case as below
    nQubits = 3
    qc = QuantumCircuit(0)
    qc.add_qubits(nQubits, name='qft')
    # hgatetest = tgqs.h(1)
    # hgate = tgqs.h(1)
    # # print(hgate)
    # qc.append(hgate)
    # print(qc.gate_list)

    xgate = tgqs.x(1)
    qc.append(xgate)
    print(qc.gate_list)
    # rxgate = tgqs.rx(qbit=1, theta=0.707)
    # # print(rxgate)
    # qc.append(rxgate)
    # print(qc.gate_list)
    # rxxgate = tgqs.rxx(0,1,0.707)
    # qc.append(rxxgate)
    # print(qc.gate_list)
    # ccxgate = tgqs.ccx([0,2],1)
    # qc.append(ccxgate)
    # print(qc.gate_list)
    # simulator = QuantumSimulator()
    # # get state vector
    # simulated_state = simulator.run_statevector(qc)
    # print(simulated_state)
    #
    # # get probability vector
    # result = simulator.execute(qc)
    # print(result)
    # qc.add_single_gate(hgatetest)
    # qc.append()
    # for i in range(nQubits):
    #     if nQubits - 2 == i:
    #         qc.x(i)
    #     else:
    #         qc.h(i)
    # for i in range(nQubits - 1, -1, -1):
    #     for j in range(i, -1, -1):
    #         if j == i:
    #             qc.h(j)
    #         else:
    #             qc.cp(control_qubit=j, target_qubit=i, theta=np.pi / (2 ** (i - j)))
    # qc.x(0)
    # for i in range(0, nQubits // 2):
    #     qc.swap(qubit_1=i, qubit_2=nQubits - 1 - i)
    #
    # simulator = QuantumSimulator()
    # simulator.
    # qc.run_statevector()
    # print(qc.state)
    # print(len(qc.state))
    # measure_pos = sorted([1, 0], reverse=True)
    # print(qc.execute(measure_bits_list=measure_pos))
    # qc.show_quantum_circuit()
