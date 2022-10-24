import handover
from handover.run import Simulator

test_csv_path = "./testingProcess/processed_test4.txt"
sim = Simulator(test_csv_path)
sim.run()
