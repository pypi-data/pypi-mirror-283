import numpy as np


class ArrayInitialization:
    """
    This class is for initializing arrays, contains functions for
    checking array type and generating empty arrays.
    """

    def array_check(self, arr):
        """
        If the input argument is a list, it is converted to an ndarray.
        If the input argument is already an ndarray, it is reshaped to (n, )
        and its data type is converted to float.

        Args:
            arr (any): _description_

        Returns:
            ndarray: shape (n, )
        """
        if type(arr) == list:
            self.new_arr = np.array(arr, dtype=float)
        elif type(arr) == np.ndarray:
            if len(arr.shape) == 1:
                self.new_arr = np.array(arr, dtype=float)
            else:
                if arr.shape[0] < arr.shape[1]:
                    self.new_arr = np.squeeze(arr, axis=0)
                else:
                    self.new_arr = np.squeeze(arr, axis=1)
                self.new_arr = np.array(self.new_arr, dtype=float)

        return self.new_arr

    def gen_init_arrays(self, t0, y0):
        """
        Function to generate a list of empty arrays for the containers
        of time, y, and yhat.

        Args:
            t0 (ndarray): time range
            y0 (ndarray): initial conditions

        Returns:
            list: list of ndarrays for time, y, and yhat
        """
        self.ysol = np.empty(0)
        self.yhatsol = np.empty(0)
        self.tsol = np.empty(0)

        self.ysol = np.append(self.ysol, y0)
        self.yhatsol = np.append(self.yhatsol, y0)
        self.tsol = np.append(self.tsol, t0)

        return self.tsol, self.ysol, self.yhatsol


###----------------------------------------###
