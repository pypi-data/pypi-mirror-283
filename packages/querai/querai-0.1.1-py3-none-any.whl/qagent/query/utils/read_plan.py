import json

from qagent.query.core import QueryPlan


def read_qplan(planfile: str, plantext: str) -> QueryPlan:
    """Reads a query plan from a file."""
    assert plantext or planfile
    if planfile:
        with open(planfile, 'r') as f:
            qplan = json.load(f)
    else:
        qplan = json.loads(plantext)
    # print(f"QPLANFROMFILE: {qplan}")
    return QueryPlan(**qplan)
