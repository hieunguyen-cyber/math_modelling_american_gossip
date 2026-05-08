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

    def run(self, victim: int, originator: int, max_steps: Optional[int] = None) -> Dict:
        """Run constrained BFS from originator limited to neighbors of victim.

        Returns a result dict containing history, reached set and timesteps.
        """
        # Induced subgraph among neighbors of victim
        neighbors = set(self.G.neighbors(victim))
        if originator not in neighbors:
            # if originator is not in neighborhood, cannot start propagation
            return {"history": [], "reached": set(), "timesteps": 0}

        sub_nodes = neighbors
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
        return {"history": self.history, "reached": visited, "timesteps": self.timesteps}

    def replay(self) -> List[Set[int]]:
        """Return a copy of the propagation history (frontiers per timestep)."""
        return [set(s) for s in self.history]
