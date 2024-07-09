import pstats
import cProfile
import pyximport
pyximport.install()

import approxe

# Repeat multiple times because Cython is so fast
def run(repeat=2000):
    for i in range(repeat):
        approxe.approx_e()

cProfile.runctx("run()", globals(), locals(), "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()

approxe.approx_e(display=True)

import numpy as np
import dot_cython

a = np.random.randn(100, 200).astype(np.float32)
b = np.random.randn(200, 50).astype(np.float32)
