# PokemonVGCBots
Few bots for Pokemon-vgc-engine

## Setting up enviroment for tests:
  ```
  python3 -m venv venv
  source ./venv/bin/active
  pip install -r requirements.txt
  ```
## Applying routes for enviroment:
  ```
  pip install virtualenvwrapper
  source ./venv/bin/virtualenvwrapper.sh
  add2virtualenv .
  ```
## Trying some examples:
  ```
  python3 example/Example_BattleEcosystem.py 
  ```
## Example_Match_All_bots.py
I modified **Example_Match.py**, so now I can define what bots will fight.
I use only this four bots for now.
```
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
```

## Using TestBot.sh
TestBot.sh is simple bash script that starts battles with bots defined in myArray.
It uses **Example_Match_All_bots.py** with arguments from myArray.

Put it in **pokemon-vgc-engine-master** directory.
Use it like this with virtualenvwrapper and venv configured:
```
./TestBot.sh
```
Also create **TestOutput/output.txt** for logging.
## Battle policy problem
Example bots defined in BattlePolicies.py use TeamPredictions or Public information:
>Forward Model
>The GameState provided to you is in reality a PkmBattleEnv object (which inherits from GameState), so you can
>forward the game state using the openAI gym method step providing the joint action. Note that only public or predicted
>information will be available (if a move is unknown it will be replaced by a normal type PkmMove, and same for the
>Pkm), with no effects and a base move power and hp.
>   ```
>   def get_action(self, g) -> int:  # g: PkmBattleEnv
>     my_action = 0
>     opp_action = 0
>     s, _, _, _ = g.step([my_action, opp_action])
>     g = s[0]  # my game state view (first iteration)
>     my_action = 1
>     opp_action = 1
>     s, _, _, _ = g.step([my_action, opp_action])
>     g = s[0]  # my game state view (second iteration)
>  ```
So in my opinion, MinMax example and BFS example bots are quite useless at start, but may be useful 
in battles with a lot of pokemon switches.
## Information we know for 100%
### My pokemon team info:
We know every thing. For example:
- Stats, status, list of moves, type and stages for active pokemon
- And of course for the rest of them in team.

So with this knowledge we can calculate a lot.
### Worst part - information about enemy team.
At the beginning, we only know:
- opponent active pokemon: type, stage, status, hp
and that's all :)

Of course more information about opponent will be revealed during battle,
but I can hardly see to use this information for an averaged bot 
that must demonstrate the ability to use random teams
### The most shocking decision by the developers of the API (for me)
Probably most simple and useful strategy is not possible to implement.
When I was playing in some pokemon games, I often used my low hp pokemon to tank enemy attack
and when it went fainted, I switched it to pokemon with resistance or type advantage.
And what API does with it? If your pokemon faints, the next active pokemon will be a random one.
It is written in /engine/PkmBattleEnv.py
```
 def __switch_fainted_pkm(self) -> Tuple[float, float]:
    damage0, damage1 = 0., 0.
        self.switched = [False, False]
        team0 = self.teams[0]
        team1 = self.teams[1]
        pkm0 = self.teams[0].active
        pkm1 = self.teams[1].active
        if pkm0.fainted():
            if self.debug:
                self.log += 'FAINTED: %s\n' % (str(pkm0))
                self.commands.append(('event', ['log', f'Trainer 0 active fainted.']))
            new_active, _, pos = team0.switch(-1) <- Problem!!!
            if self.debug:
                if pos != -1:
                    self.commands.append(('switch', [0, pos, new_active.hp,
                                                     new_active.moves[0].power,
                                                     new_active.moves[1].power,
                                                     new_active.moves[2].power,
                                                     new_active.moves[3].power]))
```
Switch function with argument -1 is random switch.
## My Policy bot, some simple heuristics
I put here some simple hierarchy of decisions. 
For example, if some action is not effective or useless due to e.g. using a damaging move with a resisted type, checking will drop one level lower in hierarchy.
## Hierarchy for know:
## Stats for Hierarchy bot against others:
Tested with /example/Example_Match.py (DEFAULT_MATCH_N_BATTLES = 3, we will change it to 100 or 1000 for better data)
### Random bot:
```
to do
```
### OneTurnLookahead bot:
```
to do
```
### Minimax bot:
```
to do
```
### PrunedBFS bot:
```
to do
```
## My Bot with MCTS
I managed to create bot with Battle Policies based on Monte Carlo Tree Search.

It is based on minimal MCTS template: https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1

I modified it first for Tik-Tac-Toe to study the MCTS heuristic search algorithm, and I applied it
as Battle Policy. 

Node expansion assumes that the opponent is doing a bad action, which narrows a number of nodes to possible expansion.

## Stats for MCTS bot against others:
Tested with /example/Example_Match_All_bots.py (DEFAULT_MATCH_N_BATTLES = 100)

Fights with all bots lasted an average of 6 minutes each, so It's quite painful to test.
And It's good to know that I only do 50 do_rollout()'s. 

Wed Jun 14 09:08:47 PM UTC 2023
### Random bot:
```
RandomPlayer Bot vs MyPolicy Bot
  MATCH RESULTS [40, 51]
```
### OneTurnLookahead bot:
```
OneTurnLookahead Bot vs MyPolicy Bot
  MATCH RESULTS [51, 0]
```
### Minimax bot:
```
Minimax Bot vs MyPolicy Bot
  MATCH RESULTS [51, 13]
```
### PrunedBFS bot:
```
PrunedBFS Bot vs MyPolicy Bot
  MATCH RESULTS [51, 34]
```
