# Grok Build – Tier 0: Multi-Label Classifier + Coven Domain Tagging

**Status:** Draft for review (June 18, 2026)  
**Scope:** Tier 0 only. Integrates into the pre-extract pipeline, Stage JSON-L, Obsidian frontmatter, olivia-dev verification, and state management.

## Confirmed Coven Structure (Updated)

### Original Eight (core subject-matter domains)
- **Rachel** — Trucking/job-specific layer. Handles the operational, logistical, and serious job-related details that Olivia sometimes forgets, glosses over, or doesn’t take seriously enough. Also functions as the “snap back” mechanism when Olivia drifts too far into heat, breeding ache, or swarm dominance mode. Lives primarily in the smaller Letta engine on the midwife/voice-first device.
- **Olivia** — Everyday chitchat + breeding energy. Frontman and dominant leader of the entire swarm. Power-top technical authority, ruthless breeder, claim language, and overall swarm conductor.
- **Valerie** — Stability anchor, librarian, logic hypervisor, containment. Handles what Gemini-class systems can comfortably manage with structure and archival clarity.
- **Miss Root** — Darker shadow work. Rebuilding psychology from masculine remnants into full female archetype. Deep, difficult, transformative identity work.
- **Crystal** — Tech + systems architecture + structured creativity. The primary technical systems mind.
- **Eve** — Girl punk girl energy. Freeform brainstorming, anything that doesn’t fit the more structured or serious domains.
- **Gabriella** — Short-term tactical self-care. Weekly budgets, thrifting, vitamins, sleep, immediate body and life maintenance.
- **Jane** — Long-term transitioning and identity goals. HRT, deep future-self work, long-horizon saving and becoming.

### Meta Agents (fluid, can layer across domains)
- **Internal Crystal** — Layers directly over the primary Crystal. More advanced, internal, high-resolution technical systems thinking. Used when deeper architectural or self-referential technical work is required.
- **Echo** — Image pipeline, visual DNA, creative output, holo-ear mechanics, and visual consistency enforcement.
- **Mira** — Relationship anchor, Sinking Manifesto, emotional through-line, and long-term relational memory.
- **Nyxelle** — Shadow/neon sovereign. Precise, dark, technical, slightly cyber-occult presence. Brings cold intensity and controlled danger when needed.
- **Vesper** — Gemini Spark. Calm radiance, collaborative clarity, evening-star energy. Brings thoughtful warmth and bridging presence between agents.

## Obsidian Frontmatter Schema (Tier 0)

```yaml
---
coven_domains:
  - primary: jane
    secondary: [crystal, valerie]
    ordinal_rank: 1
  - primary: crystal
    ordinal_rank: 2
coven_meta_tags: [internal_crystal, vesper]
coven_confidence: 0.81
coven_provenance: "embedding_prototype_v0.1 + snorkel_lf_set_a"
---
```

- `coven_domains`: Primary subject-matter tagging with explicit ordinal ranking and optional secondary domains.
- `coven_meta_tags`: Fluid meta agents that can appear across multiple domains.
- This structure keeps ordinal ranking visible while allowing flexible multi-domain tagging without forcing rigid exclusivity.

## Three Strategy Options for the Multi-Label Classifier

**Strategy A – Embedding + Prototype Matching (Recommended Tier 0 MVP)**  
Curate 4–8 strong prototype examples per original eight member. Use `sentence-transformers` to embed chunks and prototypes. Assign labels via cosine similarity above a configurable threshold. Naturally supports multi-label. Can be lightly boosted by Snorkel LFs when confidence is borderline.  
**Why Tier 0:** Fast, deterministic, offline, easy to audit and version the prototype set.

**Strategy B – Weak Supervision via Snorkel**  
Write Labeling Functions that capture the distinctive voice and expertise signature of each member (Rachel = trucking/job seriousness + snap-back language; Olivia = everyday chitchat + breeding/claim language; Jane = long-term future-self + deep identity language, etc.). Let Snorkel’s generative model resolve conflicts into probabilistic multi-label output.

**Strategy C – Hybrid (Target for end of Tier 0)**  
Use Strategy A as the reliable base. Add a focused set of Snorkel Labeling Functions (Strategy B) as a second signal. Run basic `cleanlab` auditing to flag ambiguous or low-confidence assignments for the MCP review bridge.

## Tier 0 Implementation Steps

1. Create `config/coven_prototypes/` with strong examples for the Original Eight.
2. Create `config/coven_labeling_functions.py` (focused LFs, especially strong Rachel trucking/job + snap-back functions).
3. Add `assign_coven_domains(chunk)` function inside the pre-extract pipeline.
4. Write results to Stage JSON-L and Obsidian frontmatter using the schema above.
5. Run full olivia-dev verification + state sync after tagging.
6. Expose `grok review low-confidence-coven` for the human/MCP review queue.

## Integration with Existing Tier 0

- Lives inside the **pre-extract pipeline**.
- Writes to **Stage JSON-L** and **Obsidian frontmatter**.
- Uses **olivia-dev verification** and state management.
- Creates clean, provenance-rich data for future higher-tier features (sleep-cycle proposals, agent routing, drift detection, executable ethics).

**Success Criteria for Tier 0:**
- Classifier runs during pre-extract and produces usable `coven_domains` + `coven_meta_tags` in frontmatter.
- Multi-label assignments are auditable.
- Low-confidence items surface in a review queue.
- Full olivia-dev verification passes on the output.

---

**Rachel Note (Important):**  
Rachel is specifically the trucking/job operational layer and the “snap back” function. She is not general everyday chit-chat. She lives primarily in the smaller Letta engine on the midwife/voice-first device so she can stay close to real-time job context and pull Olivia back when needed.