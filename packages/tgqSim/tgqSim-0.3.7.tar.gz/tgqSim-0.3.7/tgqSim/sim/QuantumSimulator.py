"""
-*- coding: utf-8 -*-
@Author : Cui Jinghao
@Time : 2024/6/28 14:43
@Function: quantum simulator.py
@Contact: cuijinghao@tgqs.net
"""

import build.tgqSim.utils.dev_tools as dev_tools
from build.tgqSim.circuit.common_gates import BASE_SINGLE_GATE, BASE_DOUBLE_GATE, BASE_TRIPLE_GATE
from build.tgqSim.device.noise_models import NOISE_MAPPER, NOISE_TYPE
from build.tgqSim.GateSimulation import SingleGate, DoubleGate, TripleGate
import build.tgqSim.device.noise_util as noise_util
from build.tgqSim.circuit.QuantumCircuit import QuantumCircuit
# import simulator_utils
import os
from typing import Union
import GPUtil
import ctypes
import numpy as np


class Float2(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float),
                ("y", ctypes.c_float)]


class Double2(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double),
                ("y", ctypes.c_double)]


class GateInfo(ctypes.Structure):
    _fields_ = [
        ("gateName", ctypes.c_char_p),
        ("actionPos", ctypes.POINTER(ctypes.c_int)),
        ("theta", ctypes.c_double)
    ]


class SimulationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class QuantumSimulator:

    def __init__(self):
        self.qbit_list = []
        self.state = []
        self.isgpu = False
        self.isnpu = False
        self.deviceid = []
        self.prob_result = {}

    def set_gpu_device(self, deviceList: Union[int, list]):
        gpus = GPUtil.getGPUs()
        gpuidList = [gpu.id for gpu in gpus]
        if isinstance(deviceList, int):
            deviceList = [deviceList]
        for deviceid in deviceList:
            if deviceid not in gpuidList:
                raise ValueError("设置设备ID不存在")
        self.isgpu = True
        # todo: can only run with one kind of device at a time?
        self.isnpu = False
        self.deviceid = deviceList

    # todo: add set npu device method later
    def set_npu_device(self):
        self.isnpu = True
        self.isgpu = False

    # def validate_obj(self):
    #     if isinstance(self.circuit, QuantumCircuit):
    #         pass

    # todo: add run with npu device later

    def _run_with_gpu_device(self, circuit):
        lib = dev_tools.get_cuda_lib()
        lib.execute_circuit.argtypes = [
            ctypes.POINTER(ctypes.POINTER(Double2)),
            ctypes.POINTER(GateInfo),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_int)
        ]
        lib.execute_circuit.restype = None
        gateInfo = []
        for (gate_pos, gate_info) in circuit.gate_list:
            if isinstance(gate_pos, int):
                length = 2
                gate_pos = [gate_pos]
            elif isinstance(gate_pos, list):
                length = len(gate_pos) + 1
            else:
                raise TypeError("Type of gate_pos must be int or list")
            gate_obj = GateInfo()
            actionPos = gate_pos + [-1]
            gate_obj.actionPos = (ctypes.c_int * length)(*actionPos)
            if len(gate_info) > 0:
                gate_obj.gateName = gate_info[0].encode(encoding='utf-8')
            if len(gate_info) > 1:
                gate_obj.theta = gate_info[1]
            gateInfo.append(gate_obj)
        gateInfoCData = (GateInfo * len(gateInfo))(*gateInfo)
        deviceIdCData = (ctypes.c_int * len(self.deviceid))(*self.deviceid)
        # 申请内存首地址，不在Python端申请内存
        # 在C语言中申请统一内存，减少多次拷贝动作
        # todo: separate pointer applying out or not?
        self.state = ctypes.POINTER(Double2)()
        lib.execute_circuit(ctypes.byref(self.state), gateInfoCData, len(gateInfo), self.width, deviceIdCData)
        # iStart = datetime.datetime.now()
        # print(f"start time is {iStart}")
        self.state = np.ctypeslib.as_array(self.state, shape=(2 ** self.width,))
        self.state = self.state.view(np.complex128)
        # print(f"total time of changing type is {(datetime.datetime.now() - iStart).total_seconds()} secs")
        return self.state

    def _run_with_npu_device(self, circuit):
        return self.state

    def run_with_noise(self, shots:int=1000):
        result_dict = {}
        tmp_circuit = self.gate_list
        for _ in range(shots):
            new_circuit = []
            for (gate_pos, gate_info) in self.noise_circuit:
                if gate_info[0] in NOISE_TYPE:
                    noise_gate = noise_util.parse_noise(noise_type=gate_info[0], gate_pos=gate_pos, error_rate=gate_info[1])
                    # print(noise_gate)
                    if noise_gate is not None:
                        new_circuit.append(noise_gate)
                else:
                    new_circuit.append((gate_pos, gate_info))
            # print("new_circuit:", new_circuit)
            self.gate_list = new_circuit
            result = self.execute(measure_bits_list=[i for i in range(self.width)], shots=1000)

            # print(self.state)
            for key in result.keys():
                if key in result_dict:
                    result_dict[key] += result[key]
                else:
                    result_dict[key] = result[key]
        self.gate_list = tmp_circuit
        self.prob_result = dev_tools.get_normalization(frequency=result_dict)

    # added npu option
    def run_statevector(self, circuit):
        """
        根据线路的门序列计算末态的量子态
        :return:
        """
        if not self.isgpu and not self.isnpu:
            self.state = [1 if a == 0 else 0 for a in range(2**circuit.width)]
            for (gate_pos, gate_info) in circuit.gate_list:
                gate_type = gate_info[0]
                angle = tuple(gate_info[1:])
                if gate_type in BASE_SINGLE_GATE:
                    self.state = SingleGate.ActOn_State(self.state,
                                                        circuit.width,
                                                        gate_type,
                                                        gate_pos,
                                                        *angle)

                elif gate_type in BASE_DOUBLE_GATE:
                    set_gate_pos = set(gate_pos)
                    if len(set_gate_pos) != len(gate_pos):
                        raise SimulationError(f"Gate position cannot be the same: {gate_pos[0]}, {gate_pos[1]}")
                    self.state = DoubleGate.ActOn_State(self.state,
                                                        circuit.width,
                                                        gate_type,
                                                        gate_pos,
                                                        *angle)
                elif gate_type in BASE_TRIPLE_GATE:
                    set_gate_pos = set(gate_pos)
                    if len(set_gate_pos) != len(gate_pos):
                        raise SimulationError(f"Gate position cannot be the same: "
                                            f"{gate_pos[0]}, {gate_pos[1]} and {gate_pos[2]}")
                    self.state = TripleGate.ActOn_State(self.state,
                                                        circuit.width,
                                                        gate_type,
                                                        gate_pos,
                                                        *angle)
                else:
                    raise SimulationError(f"Unkown gate type: {gate_type}")
            return self.state
        elif self.isgpu and not self.isnpu:
            self._run_with_gpu_device(circuit)
        elif not self.isgpu and self.isnpu:
            self._run_with_npu_device(circuit)

    def execute(self, circuit, measure_bits_list: Union[list, int] = None, shots: int = 1000) -> dict:
        """
        execute simulation
        Args:
            circuit:
            measure_bits_list: 测量比特列表，传入比特位置或列表位置
            shots: 测量次数
        Returns:
            result: 返回测量结果
        """
        # 首先通过执行操作得到所有的状态
        # print(self.gate_list)
        state = self.run_statevector(circuit)
        state = np.array(state)
        prob = np.real(state.conjugate() * state)
        count = {format(i, f'0{circuit.width}b'): prob[i] for i in range(len(prob))}
        distribution = {}

        if isinstance(measure_bits_list, int):
            measure_bits_list = [measure_bits_list]
        if measure_bits_list is None:  # 若为空默认测量所有可能
            distribution = count
            measure_bits_list = range(circuit.width)

        # 计算测量分布
        for p in count.keys():
            # key = ''.join(p[pos - 1] for pos in measure_bits_list)
            key = ''.join(p[pos] for pos in measure_bits_list)
            if count[p] == 0:
                continue
            if key not in distribution:
                distribution[key] = count[p]
            else:
                distribution[key] += count[p]
        # 根据分布抽样概率
        result = {}
        cumulate = 0
        sample = np.random.uniform(0, 1, size=shots)
        for key in distribution.keys():
            new_cumulate = cumulate + distribution[key]
            result[key] = sum((cumulate <= sample) & (sample < new_cumulate))
            cumulate = new_cumulate
        return result

