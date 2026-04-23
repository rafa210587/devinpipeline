# Quorum And Escalation Policy

## Internal-first rule
When uncertainty or conflict appears, resolve internally before human interaction.

## Mandatory debate before quorum
For material ambiguity in product, architecture, contracts, integration, test strategy, release gate or promotion:
1. the coordinator must open a structured debate round first;
2. debate tasks must be dispatched as small `subagent_task` slices with explicit questions, evidence scope and output schema;
3. each debater must return a `subagent_result` with position, evidence and residual risks;
4. only after the debate round fails to converge should formal quorum start.

## Quorum flow
1. Coordinator opens a `quorum_issue` contract.
2. At least two independent subagents respond.
3. Judge subagent selects decision with rationale and guardrail references.
4. Decision is binding and logged.

## Escalate to human only if all are true
1. Internal debate and quorum did not converge OR confidence remains below threshold.
2. The issue is blocking critical path.
3. Additional autonomous attempts are unlikely to change outcome.

## Escalation payload
Must include:
- question
- attempted options
- evidence
- risks
- recommended default
- urgency

## Auditability
Every debate, quorum and escalation event must be appended to runtime tracking logs.
The coordinator must persist debate summaries and winning rationale in the runtime-data repo before asking the human.
