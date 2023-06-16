from copy import deepcopy
from typing import List

import PySimpleGUI as sg
import numpy as np

from example.MonteCarloTreeSearchTemplate import MCTS
from vgc.behaviour import BattlePolicy
from vgc.datatypes.Constants import DEFAULT_PKM_N_MOVES, DEFAULT_PARTY_SIZE, TYPE_CHART_MULTIPLIER, DEFAULT_N_ACTIONS
from vgc.datatypes.Objects import PkmMove, GameState
from vgc.datatypes.Types import PkmStat, PkmStatus, PkmType, WeatherCondition


class DBaziukBattlePolicy(BattlePolicy):
    """
    Agent that selects actions randomly.
    """
    def __init__(self, switch_probability: float = .15, n_moves: int = DEFAULT_PKM_N_MOVES,
                 n_switches: int = DEFAULT_PARTY_SIZE):
        super().__init__()
        self.n_actions: int = n_moves + n_switches
        self.pi: List[float] = ([(1. - switch_probability) / n_moves] * n_moves) + (
                [switch_probability / n_switches] * n_switches)

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, g: GameState) -> int:
        print("DBaziuk")
        return np.random.choice(self.n_actions, p=self.pi)
    

