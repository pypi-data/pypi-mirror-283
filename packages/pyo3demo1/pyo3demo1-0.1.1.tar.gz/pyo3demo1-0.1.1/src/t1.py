import time

import pyo3demo1

s = time.time()
print(pyo3demo1.sum_as_string(2,3))
print("Elapsed: {} s".format(time.time() - s))