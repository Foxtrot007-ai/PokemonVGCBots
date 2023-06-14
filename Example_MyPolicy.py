from copy import deepcopy
from typing import List

import PySimpleGUI as sg
import numpy as np

from example.MonteCarloTreeSearchTemplate import MCTS
from vgc.behaviour import BattlePolicy
from vgc.datatypes.Constants import DEFAULT_PKM_N_MOVES, DEFAULT_PARTY_SIZE, TYPE_CHART_MULTIPLIER, DEFAULT_N_ACTIONS
from vgc.datatypes.Objects import PkmMove, GameState
from vgc.datatypes.Types import PkmStat, PkmStatus, PkmType, WeatherCondition


class MyPolicy(BattlePolicy):
    def __init__(self):
        super().__init__()

    def requires_encode(self) -> bool:
        return False

    def close(self):
        pass

    def get_action(self, g: GameState) -> int:
        print("MCTS")
        tree = MCTS()
        stepState = State(g,-1)
        for _ in range(50):
            tree.do_rollout(stepState)
        return tree.choose(stepState).moveFrom
    
class State():
    def __init__(self, state : GameState, moveFrom):
        self.state = state
        self.moveFrom = moveFrom

    def find_children(self):
        if self.is_terminal():
            return set()
        
        newnodes = []

        for i in range(DEFAULT_N_ACTIONS):
            s, _, _, _ = self.state.step([i, 99])
            newnodes.append(State(deepcopy(s[0]), i))
        
        return newnodes

    def find_random_child(self):
        newnodes = self.find_children()
        return np.random.choice(newnodes)

    def is_terminal(self):
        return self.state.teams[0].fainted() or self.state.teams[1].fainted()

    def reward(self):
        if self.state.teams[0].fainted() and self.state.teams[1].fainted():
            return 0.5
        elif self.state.teams[0].fainted():
            return 0.0
        else:
            return 1.0
