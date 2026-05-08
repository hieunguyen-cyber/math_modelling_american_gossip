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

    def run(self, victim: int, originator: int, q: float = 1.0, one_shot: bool = True, max_steps: int | None = None) -> Dict:
        neighbors = set(self.G.neighbors(victim))
        if originator not in neighbors:
            return {"history": [], "reached": set(), "timesteps": 0}

        visited: Set[int] = {originator}
        frontier: Set[int] = {originator}
        attempted: Set[tuple] = set()  # (src,tgt) attempted in one_shot
        self.history = [set(frontier)]

        steps = 0
        while frontier:
            if max_steps is not None and steps >= max_steps:
                break
            steps += 1
            new_frontier: Set[int] = set()
            for u in list(frontier):
                for v in self.G.neighbors(u):
                    if v not in neighbors or v in visited:
                        continue
                    edge = (u, v)
                    if one_shot and edge in attempted:
                        continue
                    attempted.add(edge)
                    if random.random() <= q:
                        visited.add(v)
                        new_frontier.add(v)
            frontier = new_frontier if one_shot else (frontier | new_frontier)
            if frontier:
                self.history.append(set(frontier))

        self.timesteps = len(self.history) - 1
        return {"history": self.history, "reached": visited, "timesteps": self.timesteps}
