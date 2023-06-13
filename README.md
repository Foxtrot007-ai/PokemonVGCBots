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
## My bot, some simple heuristics
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
```
to do
```
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
