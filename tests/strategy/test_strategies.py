import pytest
from option_sim.strategy.strategies import Strategy
import numpy as np

class TestStrategies:
    def test_strategy(self):
        assert Strategy((1,2,3,'c')).legs_tuple == ((1,2,3,'c'),)
        assert Strategy((1,2,3,'c'),(1,2,3,'c')).legs_tuple == ((1,2,3,'c'),(1,2,3,'c'))

    def test_payoff(self):
        assert any(x < -1 for x in Strategy(1,100,1,'c').payoff()[:,1] ) == False

    def test_strategy_payoff(self):
        assert np.median(Strategy((1,100,1,'c'),(1,120,1,'c')).strategy_payoff(),axis=0)[0] == 110
        assert np.sum(Strategy(1,100,1,'p').payoff() - Strategy((1,100,1,'p')).strategy_payoff()) == 0