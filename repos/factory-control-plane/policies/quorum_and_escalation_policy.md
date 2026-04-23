# Quorum And Escalation Policy

## Internal-first rule
When uncertainty or conflict appears, resolve internally before human interaction.

## Quorum flow
1. Coordinator opens a `quorum_issue` contract.
2. At least two independent subagents respond.
3. Judge subagent selects decision with rationale and guardrail references.
4. Decision is binding and logged.

## Escalate to human only if all are true
1. Internal quorum did not converge OR confidence remains below threshold.
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
Every quorum and escalation event must be appended to runtime tracking logs.
