import pytest
from option_sim.model.strategies import Strategy


class TestStrategies:
    def test_strategy(self):
        assert Strategy((1,2,3)).legs == (1,2,3)
        assert Strategy((1,2,3),(1,2,3)).legs == ((1,2,3),(1,2,3))

    def test_payoff(self):
        assert any(x < -1 for x in Strategy().payoff(1,100,1)[:,1] ) == False