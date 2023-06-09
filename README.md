# PokemonVGCBots

## Contents

- [Usage](#usage)
- [Observations & Tips](#tips)
- [Test results](#tests)

## <a name="usage"> Usage

Few bots for Pokemon-vgc-engine
How to use this repository
### Download PokemonVGCBots Engine:
  ```
  https://gitlab.com/DracoStriker/pokemon-vgc-engine/-/wikis/home
  ```
### Setting up enviroment for tests (linux version):
In terminal get into pokemon-vgc-engine-master directory.
Then do:
  ```
  python3 -m venv venv
  source ./venv/bin/activate
  pip install -r requirements.txt
  ```
  
In case of error during installation of `elo` do: 
  ```
  pip install wheel anyjson "setuptools<58.0.0"
  ```

### Applying routes for enviroment:
  ```
  pip install virtualenvwrapper
  source ./venv/bin/virtualenvwrapper.sh
  add2virtualenv .
  ```
### Trying some examples:
  ```
  python3 example/Example_BattleEcosystem.py 
  ```
### Example_Match_All_bots.py
Choose player to compete against bot.
Use Example_Match_All_bots.py as:
```
python3 example/Example_Match_All_bots.py <BotName> <PlayerName> <NumberOfMatches>
```
**BotName** = {"RandomPlayer" "OneTurnLookahead" "Minimax" "PrunedBFS" "WBukowski" "JMikolajczyk" "DBaziuk"}

**PlayerName** = { "WBukowski" "JMikolajczyk" "DBaziuk"}

Choose player to compete against bot.

**Number of battles in one match is defined in /vgc/datatypes/Constats.py as DEFAULT_MATCH_N_BATTLES** !!!

### Using TestBot.sh
TestBot.sh is simple bash script that starts battles with bots defined in myArray.
It uses **Example_Match_All_bots.py** with arguments from myArray, so you can define which bot you want to battle with. 

Put it in **pokemon-vgc-engine-master** directory.
Also create **TestOutput/output.txt** for logging.
Use it like this with virtualenvwrapper and venv configured:
```
./TestBot.sh <PlayerName> <NumberOfMatches>
```
PlayerName = { "WBukowski", "JMikolajczyk", "DBaziuk"}

**TestOutput/output.txt**:
```
  Fri Jun 16 08:12:11 PM UTC 2023
    RandomPlayer Bot vs DBaziuk Bot
       MATCH RESULTS [35, 51]
    OneTurnLookahead Bot vs DBaziuk Bot
       MATCH RESULTS [51, 17]
    Minimax Bot vs DBaziuk Bot
       MATCH RESULTS [51, 7]
    PrunedBFS Bot vs DBaziuk Bot
       MATCH RESULTS [51, 48]
    WBukowski Bot vs DBaziuk Bot
       MATCH RESULTS [51, 7]
    JMikolajczyk Bot vs DBaziuk Bot
       MATCH RESULTS [30, 51]
    DBaziuk Bot vs DBaziuk Bot
       MATCH RESULTS [33, 51]

```
### Player files
There is a bot defined in **Example_|PlayerName|.py** for each tournament participant.

**Example_Match_All_bots.py** uses these files to manage matches.

**Put this files into example directory** !!!

**Remember to modify only your file** !!!

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

## <a name="tips"> Observations & Tips

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

### Pokemon moves

 - We are guaranteed that every Pokemon has at least 1 STAB move.

### Status
status can be overwritten except confused
#### POISONED
  - Poison and Steel types are immune to it
  - deals 12.5% max health at end of turn
  - is permanent
#### PARALYZED
  - Electric and Ground types are immune to it
  - will try to make a move with probability 75%
  - is permanent
#### SLEEP
  - can't move till removed
  - maximum duration is 4 turns, chance to wake up every turn with 50% probability (before attack)
#### BURNED
  - deals 12.% max health at end of turn
  - is permanent
#### (special) CONFUSED
  - can appear with any other effect
  - 1/3 chance of hitting yourselves (with 12.5% max health damage) instead of target
  - maximum duration is 4 turns, chance to snap out of confusion every turn with 50% probability (before attack)
  - disappears when pokemon is switched

### Weather

- set before attack
- damage from weather is applied at the end of turn
- lasts 6 turns

#### SUNNY
- boosts Fire attacks (1.5 * dmg) and debuffs Water attacks (0.5 * dmg)

#### RAIN
- boost Water attacks (1.5 * dmg) and debuffs Water attacks (0.5 * dmg)

#### SANDSTORM
- deals 12.5% max pokemon health every turn
- doesn't damage Rock, Ground and Steel types

#### HAIL
- deals 12.5% max pokemon health every turn
- doesn't damage Ice types

### Entry hazard

#### SPIKES
1/8 1/6 1/4 
- stack up to three
- deal 1/8, 1/6, 1/4 max health depending on stackage when Pokemon switches in
- don't damage Flying types
- cannot be removed

### Bugs

- Frozen status has no effect (there's no single check for it) and cannot even be inflicted
- Burn status cannot be inflicted

## <a name="tests"> Tests

### Our bots stats against each other:
Tested with /example/Example_Match_All_bots.py (DEFAULT_MATCH_N_BATTLES = 3, we will change it to 100 or 1000 for better data)

For 1000 games:
|                | **JMikolajczyk** | **DBaziuk** | **WBukowski**
|----------------|------------------|-------------|--------------
|**JMikołajczyk**|         X        | 484 vs 516  |544 vs 456
|   **DBaziuk**  |     516 vs 484   |       X     |560 vs 440
| **WBukowski**  |     456 vs 544   | 440 vs 560  |    X

For 10'000 games:
|                | **JMikolajczyk** | **DBaziuk** | **WBukowski**
|----------------|------------------|-------------|--------------
|**JMikołajczyk**|        X         | 4771 vs 5229|5405 vs 4595
|   **DBaziuk**  |     5229 vs 4771 |       X     |5501 vs 4499
| **WBukowski**  |   4595 vs 5405   |5501 vs 4499 |    X


### Random bot:
```
Random  93 vs 907 JMikolajczyk 
Random 134 vs 866 DBaziuk 
Random  95 vs 905 WBukowski 
```
### OneTurnLookahead bot:
```
OneTurnLookahed 416 vs 584 JMikolajczyk 
OneTurnLookahed 369 vs 631 DBaziuk 
OneTurnLookahed 468 vs 532 WBukowski 
```
### TypeSelector bot:
```
TypeSelector 160 vs 840 JMikolajczyk 
TypeSelector 162 vs 838 DBaziuk 
TypeSelector 288 vs 712 WBukowski 
```
### Minimax bot:
```
Minimax 201 vs 799 JMikolajczyk 
Minimax 201 vs 799 DBaziuk 
Minimax 218 vs 782 WBukowski 
```
### PrunedBFS bot:
```
PrunedBFS 169 vs 831 JMikolajczyk 
PrunedBFS 213 vs 787 DBaziuk 
PrunedBFS 192 vs 808 WBukowski 
```
### Dominik's Bot with MCTS
I managed to create bot with Battle Policies based on Monte Carlo Tree Search.

It is based on minimal MCTS template: https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1

I modified it first for Tik-Tac-Toe to study the MCTS heuristic search algorithm, and I applied it
as Battle Policy. 

Node expansion assumes that the opponent is doing a bad action, which narrows a number of nodes to possible expansion.

It is defined in **Example_MyPolicy.py**

### Stats for MCTS bot against others:
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
