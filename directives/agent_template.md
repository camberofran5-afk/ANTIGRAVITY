# Agent Directive Template

## Agent Name
[Agent Name Here]

## Purpose
[Brief description of what this agent does]

## Goals
- Primary goal 1
- Primary goal 2
- Primary goal 3

## Inputs
| Input Name | Type | Description | Source |
|------------|------|-------------|--------|
| input_1 | string | Description | Layer/Source |
| input_2 | object | Description | Layer/Source |

## Outputs
| Output Name | Type | Description | Destination |
|-------------|------|-------------|-------------|
| output_1 | string | Description | Layer/Destination |
| output_2 | object | Description | Layer/Destination |

## Tools Available
- **Tool 1**: Description and when to use it
- **Tool 2**: Description and when to use it
- **Tool 3**: Description and when to use it

## Decision Logic
1. **IF** condition A **THEN** action X
2. **IF** condition B **THEN** action Y
3. **ELSE** default action Z

## Error Handling
- **Error Type 1**: Recovery strategy
- **Error Type 2**: Recovery strategy
- **Escalation**: When to escalate to orchestrator

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Dependencies
- Requires: [List of prerequisite agents/data]
- Provides to: [List of downstream consumers]

## Example Workflow
```
1. Receive input from [source]
2. Validate using [tool/method]
3. Process data via [logic]
4. Output result to [destination]
```

## Notes
- Additional context or special considerations
