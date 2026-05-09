from __future__ import annotations
from typing import Dict, List, Set, Optional
import networkx as nx
from collections import deque

class GossipPropagationEngine:
    """Constrained gossip propagation engine.

    Propagation is constrained to the victim's neighborhood induced subgraph G[N(v)].

    This engine supports deterministic BFS-like spreading with timestep recording
    and full replay of the infection history.
    """

    def __init__(self, G: nx.Graph):
        self.G = G
        self.history: List[Set[int]] = []
        self.timesteps: int = 0

    def run(self, victim: int, originator: int, max_steps: Optional[int] = None, constrain_to_neighbors: bool = True) -> Dict:
        """Run BFS from originator. If constrain_to_neighbors is True, limits to neighbors of victim."""
        neighbors = set(self.G.neighbors(victim))
        
        if constrain_to_neighbors:
            sub_nodes = set(neighbors) | {victim}
        else:
            sub_nodes = set(self.G.nodes())

        if originator not in sub_nodes:
            return {"history": [], "reached": set(), "timesteps": 0}
        visited: Set[int] = set()
        q = deque()
        q.append(originator)
        visited.add(originator)
        self.history = [set(visited)]
        t = 0

        while q:
            if max_steps is not None and t >= max_steps:
                break
            t += 1
            next_frontier: Set[int] = set()
            for _ in range(len(q)):
                u = q.popleft()
                # spread only to neighbors within the victim's neighbor set
                for w in self.G.neighbors(u):
                    if w in sub_nodes and w not in visited:
                        visited.add(w)
                        next_frontier.add(w)
            for node in next_frontier:
                q.append(node)
            if next_frontier:
                self.history.append(set(next_frontier))
        self.timesteps = len(self.history) - 1 if len(self.history) > 0 else 0
        # compute reached friends (exclude victim from reached friends)
        reached_friends = set(visited) & set(self.G.neighbors(victim))
        return {"history": self.history, "reached": reached_friends, "timesteps": self.timesteps, "visited": visited}

    def replay(self) -> List[Set[int]]:
        """Return a copy of the propagation history (frontiers per timestep)."""
        return [set(s) for s in self.history]
