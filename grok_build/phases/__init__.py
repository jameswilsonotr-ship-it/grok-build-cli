"""
Grok Build Phases Package
Each phase is a stub module with execute() and test() for interactive completion.
Phase 3 includes VALERIE V5.0 ingestion pipeline as core deliverable.
"""

from . import phase_01_environment
from . import phase_02_mcp_antigravity
from . import phase_03_letta_valerie_ingestion
from . import phase_04_swarm_iron_pearl
from . import phase_05_overlap_mining
from . import phase_06_redteam_security
from . import phase_07_voice_irt_prep

def get_phase(num: int):
    modules = {
        1: phase_01_environment,
        2: phase_02_mcp_antigravity,
        3: phase_03_letta_valerie_ingestion,
        4: phase_04_swarm_iron_pearl,
        5: phase_05_overlap_mining,
        6: phase_06_redteam_security,
        7: phase_07_voice_irt_prep,
    }
    return modules[num]
