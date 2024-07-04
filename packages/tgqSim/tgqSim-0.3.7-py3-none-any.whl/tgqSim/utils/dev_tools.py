from subprocess import Popen, PIPE
import numpy as np
import os
import ctypes


def get_cuda_version():
    try:
        # Run nvcc command to get CUDA version
        p = Popen(["nvcc", "--version"], stdout=PIPE)
        stdout, _ = p.communicate()
        # Extract CUDA version from the output
        output = stdout.decode('utf-8')
        output_lines = output.split("\n")
        for line in output_lines:
            if line.strip().startswith("Cuda compilation tools"):
                cuda_version = line.split()[4].rstrip(",")
                return cuda_version
        return None
    except Exception as e:
        print("Error:", e)
        return None


def get_normalization(frequency: dict)->dict:
    sum_freq = sum(frequency.values())
    for key in frequency.keys():
        frequency[key] = frequency[key] / sum_freq
    return frequency


def free_state(state):
    lib = get_cuda_lib()
    lib.freeAllMem.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.complex128)
    ]
    lib.freeAllMem.restype = None
    lib.freeAllMem(state)


def get_cuda_lib():
    cuda_version = get_cuda_version().replace(".", "-")
    lib_name = f"cuda_{cuda_version}_tgq_simulator.so"
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    dll_path = os.path.abspath(current_directory + '/lib/' + lib_name)
    lib = ctypes.CDLL(dll_path)
    return lib
