import pytest
from option_sim.model import bs_opt, delta, vega, theta, rho, gamma
from option_sim.model import implied_vol

class TestBS:
    def test_call(self):
        assert bs_opt(50, 50, 30/365, .5, .05, 1) == pytest.approx(2.954, rel=1e-2)

    def test_runtime_error_bs(self):
        with pytest.warns(RuntimeWarning, match='invalid value encountered'):
            bs_opt(50, 50, 0, .5, .05, 1)
        with pytest.warns(RuntimeWarning, match='divide by zero encountered in log'):
            bs_opt(0, 50, 30/365, .5, .05, 1)

    def test_zero_division_error_bs(self):
        with pytest.raises(ZeroDivisionError):
            bs_opt(50, 0, 30/365, .5, .05, 1)

    def test_delta(self):
        assert delta(50, 50, 30/365, .5, .05, 1) == pytest.approx(0.540 ,rel=1e-2)

    def test_vega(self):
        assert vega(50, 50, 30/365, .5, .05, 1) == pytest.approx(0.057, rel=1e-2)

    def test_theta(self):
        assert theta(50, 50, 30/365, .5, .05, 1) == pytest.approx(-0.0507, rel=1e-2)

    def test_rho(self):
        assert rho(50, 50, 30/365, .5, .05, 1) == pytest.approx(0.0197, rel=1e-2)

    def test_gamma(self):
        assert gamma(50, 50, 30/365, .5, .05, 1) == pytest.approx(0.0554, rel=1e-2)
    
    def test_imp_vol(self):
        assert implied_vol(50, 50, 30/365, 0.05, 1, 2.954) == pytest.approx(0.5, rel=1e-2)

    def test_runtime_error_implied_vol(self):
        with pytest.raises(ValueError):
            implied_vol(50, 50, 0, 0.05, 1, 2.954)