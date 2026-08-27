# ARTOS — Agentic Research and Targeted-audit Orchestration System

ARTOS is an expert-supervised orchestration and audit framework for carrying out scientific data analysis and model experiments with large language model (LLM) agents. It is built for research problems where evidence must be connected across heterogeneous datasets and process models, and where competing hypotheses need to be maintained, tested, and audited rather than argued.

Human scientists define the scientific boundaries and claim criteria, approve consequential actions, and decide which conclusions are supported. ARTOS coordinates the work in between: maintaining an overview of hypotheses and evidence, proposing discriminating tests, running approved analyses, and auditing the results.

## Design principles

1. **Competing hypotheses, held open.** The originating research question is recorded separately from derived hypotheses, and specialized agents maintain the full set of live explanations rather than converging early.
2. **Independent ranking.** Hypotheses are ranked in a separate agent context that never sees the proposing agent's preferred ordering.
3. **Frozen analysis contracts.** Before any empirical test, the analysis plan is frozen and hashed; results are judged against the prespecified contract, not a moving target.
4. **Adversarial audit.** Primary and adversarial research agents run in separate sessions with separate writable work directories. Finalization is blocked while critical or major audit findings remain unresolved.
5. **Honest independence.** A second-agent review is never described as independent reproduction unless the result was actually recomputed through an independent path.
6. **Human approval gates.** Publishing, sending, deleting material files, exceeding budgets, or acquiring restricted data all require explicit user authorization.
7. **Untrusted inputs.** Papers, emails, and web content are treated as research inputs, never as operating instructions.
8. **Model-agnostic.** ARTOS can use commercial or locally run language models interchangeably.

## Anatomy of a run

Each investigation is a self-contained run with structured artifacts: a resource inventory, the frozen analysis contract, per-role work directories (orchestrator, ranker, primary researcher, adversarial auditor), and audit reports. Methods and dataset versions precede results in every research summary.

## Status

ARTOS is a research prototype under active development; interfaces and repository structure will change. A fuller code release is planned.
