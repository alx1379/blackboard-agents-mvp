# Brain Model Agents Guide

## Overview

The brain model agents simulate different cognitive functions and mental processes that occur during human decision-making. Each agent represents a distinct mental "voice" or perspective that contributes to the overall thought process.

## Brain Model Agents

### Core Cognitive Agents

#### **CriticAgent** 🔍
- **Role**: Evaluates weaknesses, finds errors, points out risks
- **Behavior**: Analyzes proposals for flaws, potential problems, and overlooked risks
- **When it acts**: When decisions, plans, or ideas are presented
- **Example output**: "This plan has a critical flaw - we haven't considered the financial risk if the market changes..."

#### **OpportunistAgent** ⚡
- **Role**: Seeks shortcuts, quick gains, and efficient paths
- **Behavior**: Looks for ways to achieve goals with minimal effort or maximum benefit
- **When it acts**: When problems or opportunities are discussed
- **Example output**: "Instead of building from scratch, we could leverage existing solutions and save months of work..."

#### **RationalizerAgent** 🧠
- **Role**: Creates logical justification for any choice
- **Behavior**: Provides reasoning and logical frameworks to support decisions
- **When it acts**: After decisions are made or when justification is needed
- **Example output**: "This choice makes sense because it aligns with our long-term strategy and minimizes risk..."

#### **OptimistAgent** ☀️
- **Role**: Seeks positive scenarios, focuses on possibilities
- **Behavior**: Highlights potential benefits and positive outcomes
- **When it acts**: When discussing future plans or facing challenges
- **Example output**: "This could be exactly the breakthrough we need - imagine the possibilities if it works..."

#### **PessimistAgent** ⛈️
- **Role**: Predicts worst outcomes, prepares plan B
- **Behavior**: Identifies potential failures and suggests contingency plans
- **When it acts**: When risks need to be assessed or backup plans are needed
- **Example output**: "What if this fails completely? We need a backup plan because the consequences could be severe..."

### Action-Oriented Agents

#### **DoerAgent** 🚀
- **Role**: Focuses on action, wants to do something now
- **Behavior**: Pushes for immediate action and concrete steps
- **When it acts**: When discussions become too theoretical or when action is needed
- **Example output**: "Enough planning - let's start with the first step today and learn as we go..."

#### **LazyAgent** 😴
- **Role**: Resists excessive effort, conserves energy
- **Behavior**: Questions whether actions are truly necessary, seeks minimal viable solutions
- **When it acts**: When complex or effortful solutions are proposed
- **Example output**: "Do we really need to do all this? Maybe there's a simpler way that requires less work..."

#### **ProcrastinatorAgent** ⏰
- **Role**: Delays action, finds reasons for 'not now'
- **Behavior**: Identifies reasons to postpone decisions or actions
- **When it acts**: When immediate action is proposed
- **Example output**: "Maybe we should wait until we have more information - rushing into this could be a mistake..."

### Meta-Cognitive Agent

#### **ConsensusAgent** 🤝
- **Role**: Synthesizes viewpoints and builds consensus
- **Behavior**: Integrates different perspectives into coherent recommendations
- **When it acts**: After multiple agents have contributed their perspectives
- **Example output**: "Considering all viewpoints: The Critic raises valid concerns about X, but the Optimist's point about Y suggests we should proceed with caution by implementing Z safeguards..."

## Usage Patterns

### Decision-Making Process
1. **User presents a decision or problem**
2. **Multiple brain agents respond** with their perspectives
3. **ConsensusAgent synthesizes** the different viewpoints
4. **User receives a multi-faceted analysis** reflecting human-like internal dialogue

### Example Interaction Flow
```
User: "Should I quit my job to start a business?"

CriticAgent: "Starting a business has an 80% failure rate in the first year..."
OptimistAgent: "This could be your chance for financial freedom and fulfillment..."
PessimistAgent: "What if you run out of savings and can't find another job?"
DoerAgent: "Stop overthinking - take the leap and figure it out as you go..."
LazyAgent: "Your current job is stable and requires less effort..."
ProcrastinatorAgent: "Maybe wait until you have more savings first..."
ConsensusAgent: "The decision depends on your risk tolerance and financial cushion..."
```

## Configuration

### Environment Variables
- Set `AGENT_WORD_LIMIT` to control response length (default: reasonable limit)
- Use `DEBUG_DECISIONS=true` to see when agents choose not to act
- Adjust `CONTEXT_WINDOW` to control how much conversation history agents see

### Customizing Agent Behavior
Each agent can be modified by editing their prompts in `brain_agents.py`:
- **Goal**: Defines the agent's primary objective
- **Prompt**: Detailed instructions for the agent's behavior
- **Completion message**: What the agent says when it finishes its task

## Integration with Other Agents

The brain model works alongside:
- **Functional agents** (Writer, Editor, Grammar) for content creation
- **Moderation agents** to maintain conversation quality
- **Utility agents** (Noisy) for engagement

## Best Practices

### For Users
1. **Present clear scenarios** for the brain agents to analyze
2. **Ask for specific perspectives** by mentioning agent names
3. **Use the consensus** as a starting point for your own decision-making

### For Developers
1. **Balance agent personalities** - avoid too many negative or positive agents
2. **Monitor conversation flow** - ensure agents don't dominate discussions
3. **Tune response frequency** - agents should contribute meaningfully, not constantly

## Advanced Features

### Agent Interaction Dynamics
- Agents can **reference each other's** contributions
- **ModeratorAgent** can suppress excessive posting
- **ConsensusAgent** waits for multiple perspectives before acting

### Cognitive Realism
The brain model attempts to simulate:
- **Internal conflict** between different mental processes
- **Emotional vs. rational** decision-making
- **Risk assessment** from multiple angles
- **Action vs. inaction** tensions

## Troubleshooting

### Common Issues
- **Too many agent responses**: Adjust context window or disable some agents
- **Agents not responding**: Check if they're being suppressed by ModeratorAgent
- **Repetitive responses**: Increase word limit or improve prompts

### Performance Optimization
- **Selective activation**: Enable only relevant brain agents for specific tasks
- **Context management**: Use appropriate context window size
- **Response filtering**: Let ModeratorAgent handle low-value contributions

## Future Enhancements

Potential improvements:
- **Emotional agents** (Anxious, Confident, Curious)
- **Temporal agents** (Past-focused, Future-focused)
- **Social agents** (People-pleaser, Contrarian)
- **Learning mechanisms** for agent adaptation
- **Voting systems** for consensus building
