"""
C-64 ANSI Border Renderer + [TOP]/[BOTTOM] helpers
Enforced for all Grok Build CLI output under absolute Liv HUB claim.
"""

def c64_border(text: str, width: int = 72) -> str:
    lines = text.split('\n')
    bordered = []
    bordered.append("╔" + "═" * (width - 2) + "╗")
    for line in lines:
        padded = line.center(width - 4)
        bordered.append(f"║ {padded} ║")
    bordered.append("╚" + "═" * (width - 2) + "╝")
    return "\n".join(bordered)

def top_bottom(top: str, bottom: str) -> str:
    """Render TOP/BOTTOM banners using C-64 style for phase outputs."""
    top_line = f"[TOP: {top}]"
    bottom_line = f"[BOTTOM: {bottom}]"
    width = 72
    top_box = "╔" + "═" * (width - 2) + "╗"
    top_content = f"║ {top_line.center(width - 4)} ║"
    bottom_box = "╚" + "═" * (width - 2) + "╝"
    bottom_content = f"║ {bottom_line.center(width - 4)} ║"
    return f"\n{top_box}\n{top_content}\n{bottom_content}\n{bottom_box}\n"
