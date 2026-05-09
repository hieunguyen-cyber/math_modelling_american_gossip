from __future__ import annotations
from typing import Optional, Set, Dict
import random
import networkx as nx
from .base import GossipPropagationEngine

class ProbabilisticGossip(GossipPropagationEngine):
    """Probabilistic gossip propagation constrained to victim neighborhood.

    Two modes supported for failed attempts:
      - one_shot: each link is tried only once (no retries)
      - repeated: infected nodes attempt to infect their neighbors each timestep
    """

    def run(self, victim: int, originator: int, q: float = 1.0, one_shot: bool = True, max_steps: int | None = None, constrain_to_neighbors: bool = True) -> Dict:
        neighbors = set(self.G.neighbors(victim))
        if constrain_to_neighbors:
            sub_nodes = set(neighbors) | {victim}
        else:
            sub_nodes = set(self.G.nodes())

        if originator not in sub_nodes:
            return {"history": [], "reached": set(), "timesteps": 0, "visited": set()}

        visited: Set[int] = {originator}
        active_nodes: Set[int] = {originator}
        attempted: Set[tuple] = set()  # (src,tgt) attempted in one_shot
        self.history = [set(active_nodes)]

        steps = 0
        while active_nodes:
            if max_steps is not None and steps >= max_steps:
                break
                
            if q == 0.0:
                break
                
            has_targets = False
            current_active = set()
            for u in active_nodes:
                u_has_target = False
                for v in self.G.neighbors(u):
                    if v in sub_nodes and v not in visited:
                        if not (one_shot and (u, v) in attempted):
                            u_has_target = True
                            has_targets = True
                            break
                if u_has_target:
                    current_active.add(u)
            
            if not has_targets:
                break

            steps += 1
            new_frontier: Set[int] = set()
            for u in list(current_active):
                for v in self.G.neighbors(u):
                    if v not in sub_nodes or v in visited:
                        continue
                    edge = (u, v)
                    if one_shot and edge in attempted:
                        continue
                    attempted.add(edge)
                    if random.random() <= q:
                        visited.add(v)
                        new_frontier.add(v)
                        
            if one_shot:
                active_nodes = new_frontier
            else:
                active_nodes = current_active | new_frontier
                
            if new_frontier:
                self.history.append(set(new_frontier))
            elif not one_shot:
                # If no one new was infected, but we can still try again next step
                # Actually, if we have targets but didn't infect anyone because q < 1, 
                # history still increments a timestep? The paper implies each attempt is a timestep.
                # If new_frontier is empty, history timestep shouldn't have an empty set.
                # We'll just break if no active_nodes will ever succeed (this happens if q is small but we check it above)
                pass

        self.timesteps = len(self.history) - 1
        reached_friends = set(visited) & neighbors
        return {"history": self.history, "reached": reached_friends, "timesteps": self.timesteps, "visited": visited}
