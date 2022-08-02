import test
from dataprep.eda import plot
from dataprep.datasets import load_dataset
import numpy as np
df = load_dataset('adult')
plot(df)

