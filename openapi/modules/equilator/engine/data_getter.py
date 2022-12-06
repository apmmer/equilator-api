import os
import pickle
from time import time
from loguru import logger
from numpy import ndarray


class DataGetter:
    """
    Contains methods for returning constants
    (unpacked or stored in mem).
    """

    @staticmethod
    def load_preflop_matrix() -> ndarray:
        """
        Unpickles and returns preflop_matrix (still encrypted)
        """

        start = time()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path+'/bin/enc_preflop_matrix.pkl', 'rb') as f:
            preflop_full_matrix = pickle.load(f)
        end = time()
        logger.info(f'time of pickle loading= {end - start}')
        return preflop_full_matrix
