import sys

from agent.Example_Competitor import ExampleCompetitor
from example.Example_WBukowski import WBukowskiBattlePolicy
from example.Example_JMikolajczyk import JMikolajczykBattlePolicy
from example.Example_DBaziuk import DBaziukBattlePolicy
from vgc.behaviour.BattlePolicies import RandomPlayer, OneTurnLookahead, TypeSelector, Minimax, PrunedBFS
from vgc.competition.BattleMatch import BattleMatch
from vgc.competition.Competitor import CompetitorManager
from vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator
from vgc.util.generator.PkmTeamGenerators import RandomTeamFromRoster

def match(botPolicy, playerPolicy):
    roster = RandomPkmRosterGenerator().gen_roster()
    tg = RandomTeamFromRoster(roster)
    c0 = ExampleCompetitor("Enemy Bot")
    c0._battle_policy = botPolicy  # switch agent to test
    cm0 = CompetitorManager(c0)
    cm0.team = tg.get_team()
    c1 = ExampleCompetitor("My Bot")
    c1._battle_policy = playerPolicy  # switch agent to test
    cm1 = CompetitorManager(c1)
    cm1.team = tg.get_team()
    match = BattleMatch(cm0, cm1, debug=True)
    match.run()

def main():
    # get argument from command
    bot_option = sys.argv[1]
    player_option = sys.argv[2]
    number_of_matches = int(sys.argv[3])

    print(bot_option)
    print(" vs ")
    print(player_option)
    
    # decide which opponent to test self with
    bot = None
    if bot_option == "RandomPlayer":
        bot = RandomPlayer()
    elif bot_option == "OneTurnLookahead":
        bot = OneTurnLookahead()
    elif bot_option == "TypeSelector":
        bot = TypeSelector()
    elif bot_option == "Minimax":
        bot = Minimax()
    elif bot_option == "PrunedBFS":
        bot = PrunedBFS()
    elif bot_option == "WBukowski":
        bot = WBukowskiBattlePolicy()
    elif bot_option == "JMikolajczyk":
        bot = JMikolajczykBattlePolicy()
    elif bot_option == "DBaziuk":
        bot = DBaziukBattlePolicy()
    else:
        bot = RandomPlayer() #not implemented option

    # decide which player 
    player = None
    if player_option == "WBukowski":
        player = WBukowskiBattlePolicy()
    elif player_option == "JMikolajczyk":
        player = JMikolajczykBattlePolicy()
    elif player_option == "DBaziuk":
        player = DBaziukBattlePolicy()
    else:
        player = RandomPlayer() #not implemented option

    # start game
    for i in range(number_of_matches):
        match(bot, player)

if __name__ == '__main__':
    main()
