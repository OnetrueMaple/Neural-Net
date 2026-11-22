import sys
sys.path.insert(0, "../")
from builder import *

#'''
save_test = Network()
save_test.modelID = "save_test"
save_test.base_precision = -5
save_test.learning_rate  = 0.1

save_test.recalcPrecision()

buildDense(save_test, 5, 5, 2, 2)
print("save_test data:")
printrawnetwork(save_test)
save(save_test, "save-test.net", overwrite=True)

load_test = Network()
buildDense(load_test, 2, 2, 2, 2)

load("save-test.net", load_test, validate=False)
print("load_test data:")
printrawnetwork(load_test)
#'''
