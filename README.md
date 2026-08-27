# ARTOS — Agentic Research and Targeted-audit Orchestration System

**ARTOS is an AI co-scientist**: a research partner built from large language model (LLM) agents that helps scientists explore far more hypotheses than any one team has time to test — while the scientists stay in charge of every important decision.

Science has a bandwidth problem. Satellites, sensor networks, and models now produce more data — and more plausible explanations — than any research group can work through. Most hypotheses are never tested, not because they are uninteresting, but because nobody has the time. AI co-scientist systems have recently shown, first in biomedicine, that teams of LLM agents can generate, rank, and test scientific hypotheses at a scale no human team can match (see [Further reading](#further-reading)).

ARTOS brings that capability to data-rich natural sciences, with a design built around scientific trust. It keeps every competing explanation on the table, proposes the tests that best tell them apart, runs the analyses its human supervisors approve, audits its own results adversarially, and writes everything down. Think of a careful, tireless lab partner that never falls in love with its favorite hypothesis — and always asks before doing anything consequential.

The rest of this page explains how it works.

---

![ARTOS connected hypothesis testing](docs/artos_hypothesis_space.png)

**Why connected hypothesis testing.** Each grey node is a candidate hypothesis; edges connect hypotheses that share mechanisms, observations, or models. **(A)** Research expertise is organized around disciplinary entry points — illustrated here for carbon-cycle science: plant and ecosystem processes, atmospheric observations and remote sensing, land–atmosphere modeling and inversion. Each community tests the cluster of hypotheses nearest its own methods deeply, but practical coverage of the connected network remains partial. **(B)** The ARTOS hub links ecosystem expertise and data, atmospheric observations, and approved model workflows to propose, branch, test, and record hypotheses across the network, with scientists approving and auditing every consequential step. Testing becomes broader, but stays human-supervised rather than exhaustive.

## The ARTOS operating loop

![ARTOS operating loop](docs/artos_flowchart.png)

A run moves through the stages shown above; every stage leaves an auditable artifact on disk.

1. **Resource envelope.** The run starts from what is actually available: scientific assets (data, models, literature), compute and storage, human expertise, and a time budget. The user's request is preserved verbatim, and a resource inventory is built before anything is searched for or downloaded.
2. **Question and objective ladder.** The originating question is placed on a ladder from operational (resolve a current ambiguity, choose the best discriminating test) through intermediate (reduce uncertainty in a mechanism) to fundamental objectives (improve prediction), escalating when the routing is ambiguous. The work is routed as direct, hybrid, or hypothesis-driven, with the rationale recorded.
3. **Hypothesis graph.** The hypothesis explorer maintains competing explanations as a connected graph rather than a single favorite — illustrated in the flowchart with exposure-history hypotheses for the carbon cycle (no history effect, acclimation, persistent state change, pathway shift).
4. **Independent advisor gate.** A separate agent context, blind to the proposing agent's preferred ranking, triages each hypothesis by scientific value, discriminating power, and feasibility. Hypotheses are accepted, deferred, or rejected.
5. **Contract freeze.** Before empirical testing, the analysis plan is frozen and hashed; results are judged against the prespecified contract, not a moving target.
6. **Parallel investigations and evaluation.** Accepted hypotheses branch into parallel tests — process-model experiments, atmospheric transport and inversions, observational statistics — run by primary and adversarial agents in separate sessions and separate writable directories, all sharing evidence and provenance. Evaluation asks four questions: does the test reduce uncertainty, improve predictive skill, stay consistent across tracers and observations, and remain physically plausible? Outcomes refine or falsify hypotheses and launch the next test.
7. **Saturation and human review.** Testing continues until the marginal information gain falls below threshold. A human review then accepts, revises, or redirects the outcome; methods and dataset versions precede results in every summary, and finalization is blocked while critical or major audit findings remain unresolved.

The orchestrator is a Python package driven from the repository root:

```bash
PYTHONPATH=src python3 -m artos --help
artos doctor   # environment and configuration check
```

## Design principles

1. **Competing hypotheses, held open.** The originating research question is recorded separately from derived hypotheses, and the hypothesis graph keeps the full set of live explanations rather than converging early.
2. **Independent advisor gate.** Hypothesis triage runs in a separate agent context that never sees the proposing agent's preferred ordering.
3. **Frozen analysis contracts.** Every empirical test is preceded by a frozen, hashed analysis plan.
4. **Adversarial audit.** Primary and adversarial research agents run in separate sessions with separate writable work directories; finalization is blocked while critical or major audit findings remain unresolved.
5. **Honest independence.** A second-agent review is never described as independent reproduction unless the result was actually recomputed through an independent path.
6. **Human approval gates.** Publishing, sending, deleting material files, exceeding budgets, or acquiring restricted data all require explicit user authorization.
7. **Untrusted inputs.** Papers, emails, and web content are treated as research inputs, never as operating instructions.
8. **Model-agnostic.** ARTOS can use commercial or locally run language models interchangeably.

## Repository and run structure

```
artos_orchestrator/
├── artos.json                  # configuration: budgets, inventory refresh rules
├── pyproject.toml
├── src/artos/                  # orchestration package
├── schemas/                    # structured-artifact schemas
├── tests/
├── docs/
└── projects/<project>/
    └── runs/<timestamp>_<slug>/
        ├── 01_intake.md            # verbatim source request
        ├── 02_inventory.md         # resource inventory
        ├── 03_orientation.md
        ├── 04_route_decision.json
        ├── 05_hypothesis_tournament.md
        ├── run_manifest.json
        ├── prompts/                # frozen role prompts
        ├── work/                   # per-role writable directories
        ├── reviews/                # audit reports
        └── deliverables/
```

## Further reading

Milestones of AI-assisted science (*Nature*):

- Jumper J, et al. Highly accurate protein structure prediction with AlphaFold. *Nature* 596, 583–589 (2021). https://doi.org/10.1038/s41586-021-03819-2
- Degrave J, et al. Magnetic control of tokamak plasmas through deep reinforcement learning. *Nature* 602, 414–419 (2022). https://doi.org/10.1038/s41586-021-04301-9
- Merchant A, et al. Scaling deep learning for materials discovery. *Nature* 624, 80–85 (2023). https://doi.org/10.1038/s41586-023-06735-9

The AI co-scientist concept and its first demonstrations (*Nature*):

- Gottweis J, et al. Accelerating scientific discovery with Co-Scientist. *Nature* 655, 487–496 (2026). https://doi.org/10.1038/s41586-026-10644-y
- Ghareeb AE, et al. A multi-agent system for automating scientific discovery. *Nature* 655, 497–505 (2026). https://doi.org/10.1038/s41586-026-10652-y

AI and machine learning in Earth-system science:

- Reichstein M, et al. Deep learning and process understanding for data-driven Earth system science. *Nature* 566, 195–204 (2019). https://doi.org/10.1038/s41586-019-0912-1

## Availability

This page is the public release point for ARTOS. The concept and interfaces documented here are implemented in a working prototype that is being prepared for staged public release; this repository will be updated as components are released. Please cite this page when referring to ARTOS:

> ARTOS: Agentic Research and Targeted-audit Orchestration System. https://github.com/sudshu/ARTOS
