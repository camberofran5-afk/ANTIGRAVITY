# Agent Estimation Guidelines

## ⚡ CRITICAL: Compute Time, Not Human Time

**ALWAYS estimate in compute resources, not human hours:**

### Estimation Units:
- **Tool Calls**: Number of tool invocations needed
- **Tokens**: Estimated token consumption (input + output)
- **API Calls**: Number of external API requests
- **Compute Cycles**: Processing complexity

### Example Estimation:
```
❌ WRONG: "This will take 4 hours"
✅ CORRECT: "~50 tool calls, ~100K tokens, 20 API requests"
```

### Complexity Factors:
- **Simple**: 5-10 tool calls, 10-20K tokens
- **Medium**: 20-40 tool calls, 40-80K tokens
- **Complex**: 50-100 tool calls, 100-200K tokens
- **Very Complex**: 100+ tool calls, 200K+ tokens

### Parallel Work:
- Multiple agents can work simultaneously
- Total compute time = max(agent_times), not sum
- Coordination overhead: +10-20% tokens

---

**Remember**: We measure efficiency in compute resources, not wall-clock time!
