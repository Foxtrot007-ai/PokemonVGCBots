from copy import deepcopy
from typing import List

import PySimpleGUI as sg
import numpy as np

from vgc.behaviour import BattlePolicy
from vgc.datatypes.Constants import DEFAULT_PKM_N_MOVES, DEFAULT_PARTY_SIZE, TYPE_CHART_MULTIPLIER, DEFAULT_N_ACTIONS
from vgc.datatypes.Objects import PkmMove, GameState, Pkm
from vgc.datatypes.Types import PkmStat, PkmStatus, PkmType, WeatherCondition, PkmEntryHazard


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


def max_dmg_move(attack_pkm: Pkm, deff_pkm: Pkm, attack, deff, weather):
    damage = []
    for move in attack_pkm.moves:
        damage.append(
            estimate_damage(move.type, attack_pkm.type, move.power, deff_pkm.type, attack, deff, weather))

    maxI = int(np.argmax(damage))
    return maxI, damage


def can_be_paralyze(pkm: Pkm):
    return pkm.type != PkmType.ELECTRIC and pkm.type != PkmType.GROUND and \
           pkm.status != PkmStatus.PARALYZED


def can_be_poisoned(pkm: Pkm):
    return pkm.type != PkmType.POISON and pkm.type != PkmType.STEEL and \
           pkm.status != PkmStatus.POISONED


def effect_score(pkm: Pkm, move: PkmMove):
    if move.status == PkmStatus.POISONED:
        return move.prob * 3 if can_be_poisoned(pkm) else 0
    elif move.status == PkmStatus.PARALYZED:
        return move.prob * 1 if can_be_paralyze(pkm) else 0
    elif move.status == PkmStatus.SLEEP:
        return move.prob * 2 if pkm.status != PkmStatus.SLEEP else 0
    elif move.status == PkmStatus.BURNED:
        return move.prob * 3 if pkm.status != PkmStatus.BURNED else 0
    elif move.status == PkmStatus.CONFUSED:
        return move.prob * 4 if pkm.status != PkmStatus.CONFUSED else 0
    else:
        return 0


class JMikolajczykBattlePolicy(BattlePolicy):
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
        print("JM")
        weather = g.weather.condition

        # get my pkms
        my_team = g.teams[0]
        my_active = my_team.active
        my_party = my_team.party
        my_attack_stage = my_team.stage[PkmStat.ATTACK]
        my_defense_stage = my_team.stage[PkmStat.DEFENSE]
        my_type = my_active.type

        # get opp team
        opp_team = g.teams[1]
        opp_active = opp_team.active
        opp_not_fainted_pkms = len(opp_team.get_not_fainted())
        opp_attack_stage = opp_team.stage[PkmStat.ATTACK]
        opp_defense_stage = opp_team.stage[PkmStat.DEFENSE]
        opp_type = opp_active.type

        my_type_mul = TYPE_CHART_MULTIPLIER[my_type][opp_type]
        opp_type_mul = TYPE_CHART_MULTIPLIER[opp_type][my_type]

        # get most damaging move
        max_id, damage = max_dmg_move(my_active, opp_active, my_attack_stage, opp_defense_stage, weather)

        if damage[max_id] >= opp_active.hp:
            print("KO")
            return max_id

        move_score = []
        for pkm in [my_active] + my_party:
            if pkm.fainted():
                continue
            for move in pkm.moves:
                dmg = estimate_damage(move.type, pkm.type, move.power, opp_type, my_attack_stage, opp_defense_stage,
                                      weather)
                recovery_score = move.recover / my_active.max_hp * 5 if my_active.hp / my_active.max_hp < .5 else move.recover / my_active.max_hp
                effect = effect_score(opp_active, move)
                if move.hazard == PkmEntryHazard.SPIKES and opp_team.entry_hazard[PkmEntryHazard.SPIKES] < 3:
                    spikes = move.prob * 10 if opp_team.entry_hazard[PkmEntryHazard.SPIKES] == 0 else move.prob * 3
                else:
                    spikes = 0
                score = 3 * dmg * move.acc + 2 * recovery_score + 5 * effect * move.acc + spikes * move.acc * 5
                move_score.append(score)

        active_best = np.argmax(move_score[:4])
        best_swap = np.argmax(move_score[4:])

        swap_idx = best_swap > 3
        if opp_type_mul == 2 and opp_active.status != PkmStatus.SLEEP and opp_active.status != PkmStatus.CONFUSED:
            print("NEED SWAP")
            if TYPE_CHART_MULTIPLIER[opp_type][my_party[swap_idx]] != 2.:
                return swap_idx + 4
            elif TYPE_CHART_MULTIPLIER[opp_type][my_party[not swap_idx]] != 2.:
                return not swap_idx + 4

        if move_score[active_best] * 2 > move_score[best_swap]:
            print("ACTIVE BEST MOVE score:", move_score[active_best])
            return active_best
        else:
            print("SWAP BEST MOVE score: ", move_score[best_swap])
            return swap_idx + 4
