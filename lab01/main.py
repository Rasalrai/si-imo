import os.path

from instance_reader import InstanceReader

if __name__ == '__main__':
    nodes = InstanceReader(os.path.join("data", "kroA100.tsp"), 100).get_matrix()
    # print(nodes[0, :10])
