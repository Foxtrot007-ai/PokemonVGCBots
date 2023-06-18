from copy import deepcopy
from typing import List

import PySimpleGUI as sg
import numpy as np

from example.MonteCarloTreeSearchTemplate import MCTS
from vgc.behaviour import BattlePolicy
from vgc.datatypes.Constants import DEFAULT_PKM_N_MOVES, DEFAULT_PARTY_SIZE, TYPE_CHART_MULTIPLIER, DEFAULT_N_ACTIONS
from vgc.datatypes.Objects import PkmMove, GameState, Pkm, PkmTeam
from vgc.datatypes.Types import PkmStat, PkmStatus, PkmType, WeatherCondition
from vgc.engine import PkmBattleEnv

def estimate_damage(move_type: PkmType, pkm_type: PkmType, move_power: float, opp_pkm_type: PkmType,
                    attack_stage: int, defense_stage: int, weather: WeatherCondition) -> float:
    stab = 1.5 if move_type == pkm_type else 1.
    if (move_type == PkmType.WATER and weather == WeatherCondition.RAIN) or (
            move_type == PkmType.FIRE and weather == WeatherCondition.SUNNY):
        weather = 1.5
    elif (move_type == PkmType.WATER and weather == WeatherCondition.SUNNY) or (
            move_type == PkmType.FIRE and weather == WeatherCondition.RAIN):
        weather = .5
    else:
        weather = 1.
    stage_level = attack_stage - defense_stage
    stage = (stage_level + 2.) / 2 if stage_level >= 0. else 2. / (np.abs(stage_level) + 2.)
    damage = TYPE_CHART_MULTIPLIER[move_type][opp_pkm_type] * stab * weather * stage * move_power
    return damage

def known_moves(p : Pkm) -> List[PkmMove]:
    return list(filter(lambda m : m.name, p.moves))

def has_type_advantage(p1 : Pkm, p2: Pkm):
    return has_att_type_advantage(p1, p2) and not has_att_type_advantage(p2, p1)

def has_att_type_advantage(p1 : Pkm, p2 : Pkm):
    return TYPE_CHART_MULTIPLIER[p1.type][p2.type] == 2

def may_be_supereffective(p1 : Pkm, p2 : Pkm):
    return any(TYPE_CHART_MULTIPLIER[move.type][p2.type] == 2  for move in known_moves(p1))

def may_ohko(p1 : Pkm, p2 : Pkm, att_stage : int, def_stage : int, weather : WeatherCondition) -> bool:
    for move in p1.moves:
        if (estimate_damage(move.type, p1.type, move.power, p2.type, att_stage, def_stage, weather) >= p2.hp):
            return True
    return False

class WBukowskiBattlePolicy(BattlePolicy):
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

    def get_attack_boosting_move(self, p : Pkm) -> int:
        for i, move in enumerate(p.moves):
            if move.stat == PkmStat.ATTACK and move.stage > 0 and move.prob == 1:
                return i
        return None

    def find_best_for(self, t : PkmTeam, opp : Pkm, g : GameState) -> int:
        best_selection = None
        for i, pkm in enumerate([t.active] + t.party):
            if not may_be_supereffective(opp, pkm) and may_be_supereffective(pkm, opp):
                return i
            if may_be_supereffective(pkm, opp):
                best_selection = i
            elif best_selection is None and not may_be_supereffective(opp, pkm) :
                best_selection = i
        return best_selection if not best_selection is None else 0

    def get_action(self, g : GameState) -> int:
        weather = g.weather.condition

        my_team = g.teams[0]
        my_active = my_team.active
        my_party = my_team.party
        my_attack_stage = my_team.stage[PkmStat.ATTACK]
        my_defense_stage = my_team.stage[PkmStat.DEFENSE]

        opp_team = g.teams[1]
        opp_active = opp_team.active
        opp_not_fainted_pkms = len(opp_team.get_not_fainted())
        opp_attack_stage = opp_team.stage[PkmStat.ATTACK]
        opp_defense_stage = opp_team.stage[PkmStat.DEFENSE]

        my_type_advantage = TYPE_CHART_MULTIPLIER[my_active.type][opp_active.type]
        op_type_advantage = TYPE_CHART_MULTIPLIER[opp_active.type][my_active.type]

        damage: List[float] = []
        for move in my_active.moves:
            damage.append(estimate_damage(move.type, my_active.type, move.power, opp_active.type, my_attack_stage,
                                          opp_defense_stage, weather))
        most_damaging_move = int(np.argmax(damage))

        # knock-out if possible
        if damage[most_damaging_move] >= opp_active.hp:
            return most_damaging_move


        # if we know for sure that opp cannot knock us out  
        opp_known_moves = list(filter(lambda m: m.name, opp_active.moves))      
        all_moves_known = len(opp_known_moves) == 4
        if all_moves_known and all(estimate_damage(move.type, opp_active.type, move.power, my_active.type, opp_attack_stage, my_defense_stage, weather) < my_active.hp for move in opp_known_moves):
            boost = self.get_attack_boosting_move(my_active)
            if boost is not None:
                return boost
            return most_damaging_move
        
        # other mon can ohko opp
        for i, pkm in enumerate(my_team.party):
            if may_ohko(pkm, opp_active, 0, opp_defense_stage, weather) and not may_ohko(opp_active, pkm, opp_attack_stage, 0, weather):
                return i + 3

        # opp can be supereffective
        if may_be_supereffective(opp_active, my_active):
            to_switch = self.find_best_for(my_team, opp_active)
            if to_switch == 0:
                return most_damaging_move
            else:
                return to_switch + 3

        return most_damaging_move
    

