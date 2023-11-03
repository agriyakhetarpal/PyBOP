import pybop
import numpy as np
import pytest


class TestOptimisation:
    """
    A class to test the optimisation class.
    """

    @pytest.mark.unit
    def test_prior_sampling(self):
        # Tests prior sampling
        model = pybop.lithium_ion.SPM()

        Dataset = [
            pybop.Dataset("Time [s]", np.linspace(0, 3600, 100)),
            pybop.Dataset("Current function [A]", np.zeros(100)),
            pybop.Dataset("Terminal voltage [V]", np.ones(100)),
        ]

        param = [
            pybop.Parameter(
                "Negative electrode active material volume fraction",
                prior=pybop.Gaussian(0.75, 0.05),
                bounds=[0.73, 0.77],
            )
        ]

        signal = "Terminal voltage [V]"
        cost = pybop.RMSE()

        for i in range(10):
            opt = pybop.Optimisation(
                cost,
                model,
                optimiser=pybop.NLoptOptimize(n_param=len(param)),
                parameters=param,
                dataset=Dataset,
                signal=signal,
            )
            assert opt.x0 <= 0.77 and opt.x0 >= 0.73
