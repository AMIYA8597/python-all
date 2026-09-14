"""
# ==============================================================================
# LABORATORY: PROJECT-BASED LEARNING (STATE MACHINE ARCHITECTURE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer builds a text-based RPG. They write a 1,000-line `while` 
# loop containing a massive block of nested `if/elif` statements checking 
# the player's health, inventory, and location. When they try to add a new 
# enemy, they accidentally place an `if` inside the wrong block, mathematically 
# allowing the player to fight the dragon while simultaneously sleeping in the inn.
#
# A senior software architect builds an RPG using a "Finite State Machine" (FSM). 
# They mathematically isolate every location (Town, Forest, Boss) into an 
# independent, object-oriented "State" class. The main Game Loop does not contain 
# a single `if/elif` statement. It merely asks the current active State what to do, 
# and transitions flawlessly. If they want to add a new dungeon, they write a new 
# standalone Class and inject it into the Engine without touching the core routing.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Finite State Machine (FSM) architecture.
# - Execute Polymorphic routing (bypassing `if/elif` logic).
# - Understand the architecture of a continuous "Game Loop".
#
# ==============================================================================
"""

from abc import ABC, abstractmethod
import time
import sys

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE PLAYER STATE (THE PAYLOAD)
# ==============================================================================
# The Player object acts as a global payload passed between States.
class Player:
    def __init__(self, name: str):
        self.name = name
        self.hp = 100
        self.gold = 0
        self.is_alive = True


# ==============================================================================
# 4. THE FINITE STATE MACHINE (FSM) ARCHITECTURE
# ==============================================================================
class GameState(ABC):
    """
    THE ABSTRACT BASE CLASS (The Strategy Interface).
    Every single location in the game MUST inherit from this and implement `run`.
    The `run` method MUST mathematically return the String name of the NEXT state!
    """
    @abstractmethod
    def run(self, player: Player) -> str:
        pass


class MainMenuState(GameState):
    def run(self, player: Player) -> str:
        print("\n  [MAIN MENU]")
        print("  1. Start Adventure")
        print("  2. Exit Game")
        
        # In a real game, this would be an `input()`.
        # We hardcode the simulation to prevent the CI/CD pipeline from freezing!
        print("  > Auto-selecting '1'...")
        time.sleep(0.5)
        
        return "TOWN" # Mathematically transitions to the Town state!


class TownState(GameState):
    def run(self, player: Player) -> str:
        print(f"\n  [TOWN SQUARE] HP: {player.hp} | Gold: {player.gold}")
        print("  You are safe in the town. Where will you go?")
        print("  1. Go to the Dark Forest")
        print("  2. Sleep at the Inn (-10 Gold)")
        
        print("  > Auto-selecting '1' (Dark Forest)...")
        time.sleep(0.5)
        
        return "FOREST"


class ForestState(GameState):
    def run(self, player: Player) -> str:
        print(f"\n  [DARK FOREST] HP: {player.hp} | Gold: {player.gold}")
        print("  A Goblin ambushes you!")
        
        print("  > Mathematically simulating combat...")
        player.hp -= 30
        player.gold += 50
        
        if player.hp <= 0:
            player.is_alive = False
            print("  [DEATH] You were slain by the Goblin.")
            return "GAME_OVER"
            
        print(f"  [VICTORY] You killed the Goblin! Looted 50 Gold. You took 30 damage.")
        time.sleep(0.5)
        
        # We mathematically loop back to the Town!
        print("  > Retreating to Town...")
        return "TOWN"


class GameOverState(GameState):
    def run(self, player: Player) -> str:
        print("\n  [GAME OVER]")
        print(f"  Final Stats -> Name: {player.name} | Gold: {player.gold}")
        return "QUIT"


# ==============================================================================
# 5. THE GAME ENGINE (THE ROUTER)
# ==============================================================================
class GameEngine:
    def __init__(self):
        # The FSM Registry! The engine has NO IDEA what these states actually do.
        self.states = {
            "MENU": MainMenuState(),
            "TOWN": TownState(),
            "FOREST": ForestState(),
            "GAME_OVER": GameOverState()
        }
        self.current_state = "MENU"
        self.player = Player("Hero")

    def execute_game_loop(self):
        """
        THE INFINITE GAME LOOP.
        Notice there are absolutely zero `if/elif` statements checking where 
        the player is! This is architectural perfection.
        """
        section_header("FSM Execution: The Infinite Game Loop")
        
        # Limit the simulation to prevent an infinite loop in the lab
        turn_limit = 5
        current_turn = 0
        
        while self.current_state != "QUIT" and current_turn < turn_limit:
            # 1. We dynamically grab the current mathematical State object!
            active_state_object = self.states.get(self.current_state)
            
            if not active_state_object:
                print(f"  [CRITICAL ERROR] State '{self.current_state}' does not exist!")
                break
                
            # 2. We blindly execute the state and receive the pointer to the NEXT state!
            # The Engine does not care if it's the Forest, the Town, or a Boss fight.
            next_state_string = active_state_object.run(self.player)
            
            # 3. We mathematically shift the FSM!
            self.current_state = next_state_string
            current_turn += 1
            
        print("\n  [SHUTDOWN] Game Engine Terminated cleanly.")


def run_all_labs():
    engine = GameEngine()
    engine.execute_game_loop()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why did we mathematically force every GameState class to return a String (the next state) instead of just hardcoding `engine.current_state = 'TOWN'` inside the Forest class?"
   Senior Answer: "Architectural Coupling and Dependency Injection. If the `ForestState` class reaches out and modifies `engine.current_state` directly, the Forest becomes permanently coupled to the specific global `engine` object. You cannot mathematically Unit Test the Forest in isolation, because you would have to boot up the entire Game Engine just to test combat. By returning a pure String, the Forest class acts as a mathematically isolated function ($f(x) \\rightarrow y$). The Game Engine handles the routing, and the State handles the logic, achieving perfect Separation of Concerns."

2. Interviewer: "How does the Finite State Machine (FSM) architecture mathematically prevent the classic bug where a player opens their inventory while simultaneously fighting a dragon?"
   Senior Answer: "Mutual Exclusion. In a massive, monolithic `while` loop that relies on boolean flags (`if in_combat: ... if inventory_open: ...`), it is mathematically trivial for a developer to accidentally trigger two flags simultaneously, allowing code blocks to execute concurrently. An FSM mathematically guarantees absolute Mutual Exclusion. The `current_state` variable can only hold exactly one pointer at any given millisecond. If `current_state = 'DRAGON_COMBAT'`, the code inside the `INVENTORY` state physically cannot be executed, rendering race conditions and concurrent overlap bugs mathematically impossible."

3. Interviewer: "What is the architectural purpose of the 'Infinite Game Loop' (`while True:`) in game development, and why doesn't it instantly crash the CPU at $100\\%$ utilization?"
   Senior Answer: "Every video game on earth, from Pong to Cyberpunk 2077, runs inside a single infinite `while` loop. The loop handles three mathematical phases: 1) Process User Input, 2) Update Physics/State, 3) Render the Screen. If left unconstrained, this loop will execute millions of times per second, maxing out a CPU core at $100\\%$ and rendering $5,000$ Frames Per Second, instantly melting the GPU. Game Engines prevent this by calculating a 'Delta Time' at the end of every loop. If the math finished in $2$ milliseconds, but the game is capped at $60$ FPS (which requires exactly $16.6$ milliseconds per frame), the engine mathematically commands the OS to `sleep` the thread for the remaining $14.6$ milliseconds. This drops CPU utilization to near $0\\%$, keeping the hardware cool while maintaining a flawless 60 FPS lock."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Capstone Project (Game State Machine) Completed.")
