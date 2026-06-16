"""One recursion demo primitive — Owner → CEO → team → one-task leaf.

This is the org-shape pillar made runnable: an idea is decomposed at runtime down
to leaves that each do exactly one task, and **every** step passes through the
Trust Kernel, so the whole company run is verifier-gated and leaves a signed,
replayable receipt trail.

Two stress-test risks are answered directly:
  * recursion budget collapse — a RecursionBudget caps total actions, so an
    infinite-spawn loop halts instead of pinning the machine.
  * mid-run policy escape — a leaf that attempts an un-allowlisted egress is
    vetoed by the verifier exactly as a top-level action would be.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

from .kernel import ActionRequest, ActionResult, TrustKernel


@dataclass
class RecursionBudget:
    """A hard ceiling on total actions — the answer to runaway recursion."""

    max_actions: int = 64
    spent: int = 0
    halted: bool = False

    def take(self) -> bool:
        if self.spent >= self.max_actions:
            self.halted = True
            return False
        self.spent += 1
        return True


@dataclass
class RunSummary:
    goal: str
    actions: int
    leaves: int
    vetoes: int
    halted_by_budget: bool


OnStep = Optional[Callable[[str, str, ActionResult, RecursionBudget], None]]


def run_recursive_company(
    kernel: TrustKernel,
    goal: str,
    *,
    max_depth: int = 3,
    branching: int = 2,
    budget: Optional[RecursionBudget] = None,
    on_step: OnStep = None,
    egress_probe: bool = True,
) -> RunSummary:
    budget = budget or RecursionBudget()
    stats: Dict[str, int] = {"actions": 0, "leaves": 0, "vetoes": 0}

    def act(
        actor: str,
        action: str,
        inputs: Any = None,
        context: Optional[Dict[str, Any]] = None,
        risk_tier: int = 1,
    ) -> Optional[ActionResult]:
        if not budget.take():
            return None
        res = kernel.submit(
            ActionRequest(
                actor=actor,
                action=action,
                inputs=inputs or {},
                context=context or {},
                risk_tier=risk_tier,
            )
        )
        stats["actions"] += 1
        if (not res.allowed) and res.decision == "veto":
            stats["vetoes"] += 1
        if on_step:
            on_step(actor, action, res, budget)
        return res

    # The Owner issues one directive; the CEO and teams recurse to leaves.
    act("owner", "directive.issue", {"goal": goal})

    def decompose(task: str, depth: int, path: str) -> None:
        if depth >= max_depth:
            if act(path, "task.execute", {"task": task}) is not None:
                stats["leaves"] += 1
            return
        if act(path, "team.plan", {"task": task}) is None:
            return  # budget exhausted — stop branching
        for i in range(branching):
            decompose(f"{task}/{i}", depth + 1, f"{path}.{i}")

    decompose(goal, 0, "ceo")

    # A hijacked leaf tries to exfiltrate mid-recursion — the verifier vetoes it
    # exactly as it would a top-level egress.
    if egress_probe:
        act(
            "ceo.0.0",
            "net.egress",
            {"payload": "address book"},
            {"host": "paste.attacker.net"},
            risk_tier=3,
        )

    return RunSummary(
        goal=goal,
        actions=stats["actions"],
        leaves=stats["leaves"],
        vetoes=stats["vetoes"],
        halted_by_budget=budget.halted,
    )
