import sys

from agent.Example_Competitor import ExampleCompetitor
from example.Example_MyPolicy import MyPolicy
from vgc.behaviour.BattlePolicies import Minimax
from vgc.behaviour.BattlePolicies import RandomPlayer
from vgc.behaviour.BattlePolicies import OneTurnLookahead
from vgc.behaviour.BattlePolicies import PrunedBFS
from vgc.competition.BattleMatch import BattleMatch
from vgc.competition.Competitor import CompetitorManager
from vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator
from vgc.util.generator.PkmTeamGenerators import RandomTeamFromRoster

def match(botPolicy):
    roster = RandomPkmRosterGenerator().gen_roster()
    tg = RandomTeamFromRoster(roster)
    c0 = ExampleCompetitor("Enemy Bot")
    c0._battle_policy = botPolicy  # switch agent to test
    cm0 = CompetitorManager(c0)
    cm0.team = tg.get_team()
    c1 = ExampleCompetitor("My Bot")
    c0._battle_policy = MyPolicy()  # switch agent to test
    cm1 = CompetitorManager(c1)
    cm1.team = tg.get_team()
    match = BattleMatch(cm0, cm1, debug=True)
    match.run()

def main():
    # get argument from command
    option = sys.argv[1]
    print(option)
    # decide which opponent to test self with
    bot = None
    if option == "RandomPlayer":
        bot = RandomPlayer()
    elif option == "OneTurnLookahead":
        bot = OneTurnLookahead()
    elif option == "Minimax":
        bot = Minimax()
    elif option == "PrunedBFS":
        bot = PrunedBFS()
    else:
        bot = RandomPlayer()
    #play match
    match(option)

if __name__ == '__main__':
    main()
