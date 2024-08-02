import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import importlib
import helpers
import os
importlib.reload(helpers)
from helpers import check_if_folder, remove_result_tables

def import_eqe_file(path):
    df = pd.read_csv(path, header = 6, sep = '\t')