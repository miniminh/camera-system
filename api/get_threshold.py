import os
import numpy as np

from age_gender import predict
from utils import distance

for root, dirs, files in os.walk('save'):
    for file1 in files:
        f1 = os.path.join(root, file1)
        temp1 = np.load(f1)
        for file2 in files:
            f2 = os.path.join(root, file2)
            temp2 = np.load(f2)
            dis = distance(temp1, temp2)
            print(file1, file2, dis)