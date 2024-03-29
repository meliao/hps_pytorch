import pytest

cola = pytest.importorskip("cola")

import numpy as np
import pytest
from src.lippmann_schwinger_eqn.solver_utils import (
    greensfunction2,
    greensfunction3,
    getGscat2circ,
    find_diag_correction,
    _extend_1d_grid,
    get_extended_grid,
    _zero_pad_numpy,
)
from src.test_utils import check_arrays_close, check_scalars_close


class Test__extend_1d_grid:
    def test_0(self) -> None:
        """Make sure things run without error"""
        for n in [10, 20, 100, 200, 192]:
            for dx in [1 / n, 10 / n]:
                out = _extend_1d_grid(n, dx)

                s = f"Error on n={n}, dx={dx} "

                # Test for correct spacing
                spacing = out[1] - out[0]
                check_scalars_close(spacing, dx, msg=s + "spacing")

                # This tests for a power of 2. I just pulled this from chatGPT.
                l = out.shape[0]
                assert l > 0 and (l & (l - 1)) == 0, s + "power of 2"

                # Test for presence of 0 in the grid
                assert 0 in out, s + "presence of 0"


class Test_get_extended_grid:
    def test_0(self) -> None:
        for n in [10, 20, 100, 200, 400]:
            for dx in [1 / n, 10 / n]:
                out = get_extended_grid(n, dx)
                # print(out.shape)

                assert np.all(out[0, 0] == [0, 0])


class Test__zero_pad:
    def test_0(self) -> None:
        n1 = 3
        n2 = 5
        v = np.random.normal(size=(n1, n1))
        o = _zero_pad_numpy(v, n2)
        assert np.all(o[:n1, :n1] == v)
        check_scalars_close(v.sum(), o.sum())


if __name__ == "__main__":
    pytest.main()
