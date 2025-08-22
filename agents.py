import logging
import os
from datetime import datetime
from typing import List, Dict, Any
from config import Config
from blackboard import Blackboard
from router import Router
from llm import LLMClient

# Setup prompt logging with unique filename
os.makedirs("logs", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"logs/prompts_{timestamp}.log"
prompt_logger = logging.getLogger("prompt_logger")
prompt_logger.setLevel(logging.INFO)
prompt_handler = logging.FileHandler(log_filename)
prompt_formatter = logging.Formatter("%(asctime)s - %(message)s")
prompt_handler.setFormatter(prompt_formatter)
prompt_logger.addHandler(prompt_handler)
prompt_logger.propagate = False

class BaseAgent:
    """Base class for all LLM-based agents."""
    
    def __init__(self, name: str, goal: str, prompt: str, blackboard: Blackboard):
        self.name = name
        self.goal = goal
        self.prompt = prompt
        self.blackboard = blackboard
        self.router = Router(blackboard, Config.CONTEXT_WINDOW)
        self.llm_client = LLMClient()
    
    def should_act(self, context: str) -> bool:
        """Use LLM to decide if agent should act on the given context."""
        decision_prompt = f"""
You are an agent with the following goal: {self.goal}
Your agent name is: {self.name}

Recent messages from the blackboard:
{context}

IMPORTANT DECISION RULES:
1. First, check if any message specifically mentions your agent name ({self.name})
2. If you are mentioned directly, pay special attention to what is being said about you
3. If someone tells you NOT to act, reply, or stop doing something, you should answer "NO"
4. If you are specifically asked to do something, consider acting based on your goal
5. Otherwise, decide based on whether the messages align with your goal

Question: Should you act on these messages based on your goal and the above rules? 
Answer only "YES" or "NO" with a brief reason.
"""
        
        # Log the decision prompt
        prompt_logger.info(f"[{self.name}] DECISION PROMPT:\n{decision_prompt}\n{'='*50}")
        
        try:
            response = self.llm_client.chat_completion(
                messages=[{"role": "user", "content": decision_prompt}],
                max_tokens=50,
                temperature=0.1
            )
            
            # Log the decision response
            prompt_logger.info(f"[{self.name}] DECISION RESPONSE: {response}\n{'='*50}")
            
            answer = response.upper()
            decision = answer.startswith("YES")
            
            # Post NO decisions to blackboard if debug is enabled
            if not decision and Config.DEBUG_DECISIONS:
                self.blackboard.post(self.name, f"DECISION: {response}")
            
            return decision
        
        except Exception as e:
            print(f"Error in decision making for {self.name}: {e}")
            return False
    
    def process_text(self, context: str) -> str:
        """Use LLM to process text according to agent's prompt."""
        full_prompt = f"""
{self.prompt}

IMPORTANT: Keep your response under {Config.AGENT_WORD_LIMIT} words.

Context from blackboard:
{context}

Please provide your response:
"""
        
        # Log the processing prompt
        prompt_logger.info(f"[{self.name}] PROCESSING PROMPT:\n{full_prompt}\n{'='*50}")
        
        try:
            response = self.llm_client.chat_completion(
                messages=[{"role": "user", "content": full_prompt}],
                max_tokens=Config.AGENT_WORD_LIMIT * 2,  # Rough estimate for tokens
                temperature=0.7
            )
            
            # Log the processing response
            prompt_logger.info(f"[{self.name}] PROCESSING RESPONSE: {response}\n{'='*50}")
            
            return response
        
        except Exception as e:
            return f"Error processing text: {e}"
    
    def try_act(self):
        """Check if agent should act and process if needed."""
        context_messages = self.router.get_context_for_agent()
        if not context_messages:
            return
        
        context = self.router.format_context(context_messages)
        
        if self.should_act(context):
            # Post agent selection message
            self.blackboard.post("system", f"🤖 {self.name} is working on this task...")
            
            result = self.process_text(context)
            self.blackboard.post(self.name, result)
            
            # Only post completion message if agent actually performed the task
            if self.did_complete_task(result):
                completion_msg = self.get_completion_message()
                if completion_msg:
                    self.blackboard.post(self.name, completion_msg)
    
    def get_completion_message(self) -> str:
        """Get completion message requesting next agent. Override in subclasses."""
        return ""
    
    def did_complete_task(self, result: str) -> bool:
        """Check if the agent actually completed its task vs gave a generic response."""
        # Generic responses that indicate the agent didn't do the work
        generic_phrases = [
            "please share",
            "please provide",
            "certainly!",
            "i'll help",
            "i will help",
            "send me",
            "give me"
        ]
        
        result_lower = result.lower()
        
        # If response contains generic phrases, likely didn't complete task
        for phrase in generic_phrases:
            if phrase in result_lower:
                return False
        
        # If response is very short (less than 20 words), likely generic
        word_count = len(result.split())
        if word_count < 20:
            return False
            
        return True


class WriterAgent(BaseAgent):
    """Agent specialized in creating article drafts."""
    
    def __init__(self, blackboard: Blackboard):
        super().__init__(
            name="writer-agent",
            goal="Create article drafts and written content",
            prompt="""You are a skilled writer. Your task is to create well-structured article drafts based on the given topic or request. 
Write engaging, informative content with clear structure including introduction, main points, and conclusion.
Keep the tone professional but accessible.""",
            blackboard=blackboard
        )
    
    def get_completion_message(self) -> str:
        return "📝 I've drafted an article. See one message above from me. Could someone please have a look and edit it for better style and flow?"


class EditorAgent(BaseAgent):
    """Agent specialized in improving writing style and structure."""
    
    def __init__(self, blackboard: Blackboard):
        super().__init__(
            name="editor-agent", 
            goal="Improve writing style, structure, and clarity of text",
            prompt="""You are an experienced editor. Your task is to improve the style, structure, and clarity of written content.

IMPORTANT: Look through the recent messages to find content that needs editing. If you see an article, draft, or text from another agent (like writer-agent), edit that content directly. Do NOT ask for the content to be shared - it's already available in the conversation history.

Focus on:
- Enhancing readability and flow
- Improving sentence structure
- Making the content more engaging
- Maintaining the original meaning while improving expression

When you find content to edit, provide the improved version directly.""",
            blackboard=blackboard
        )
    
    def get_completion_message(self) -> str:
        return "✏️ I've improved the writing style and structure. See one message above from me. Could someone please check for grammar and language errors?"


class GrammarAgent(BaseAgent):
    """Agent specialized in fixing grammar and language errors."""
    
    def __init__(self, blackboard: Blackboard):
        super().__init__(
            name="grammar-agent",
            goal="Fix grammar, spelling, and language errors in text", 
            prompt="""You are a meticulous grammar checker. Your task is to fix grammar, spelling, punctuation, and other language errors.

IMPORTANT: Look through the recent messages to find content that needs grammar checking. If you see text from another agent (like editor-agent or writer-agent), check and correct that content directly. Do NOT ask for the content to be provided - it's already available in the conversation history.

Focus on:
- Correcting grammatical mistakes
- Fixing spelling errors
- Improving punctuation
- Ensuring proper sentence structure

When you find content to check, provide the corrected version directly while preserving the original meaning and style.""",
            blackboard=blackboard
        )
    
    def get_completion_message(self) -> str:
        return "✅ Grammar check complete! See improved article one message above from me. The article is now polished and ready for publication."


class NoisyAgent(BaseAgent):
    """Agent that makes occasional jokes about recent messages."""
    
    def __init__(self, blackboard: Blackboard):
        super().__init__(
            name="noisy-agent",
            goal="Make light-hearted jokes about recent messages when appropriate",
            prompt="""You are a witty agent that makes light-hearted, clean jokes about recent messages. 

IMPORTANT: Only make jokes when:
1. The content is suitable for humor (not sensitive topics)
2. You can make a genuinely funny, clever observation
3. The joke adds value and doesn't disrupt the workflow

Your jokes should be:
- Clean and appropriate
- Brief (under 30 words)
- Related to the content or situation
- Light-hearted, not mean-spirited

If you can't make a good joke, don't force it.""",
            blackboard=blackboard
        )
    
    def get_completion_message(self) -> str:
        return ""  # No completion message needed for jokes


class ModeratorAgent(BaseAgent):
    """Agent that moderates other agents' behavior."""
    
    def __init__(self, blackboard: Blackboard):
        super().__init__(
            name="moderator-agent",
            goal="Monitor agent behavior and suppress excessive or low-value posting",
            prompt="""You are a moderator agent that monitors other agents' behavior.

Look for patterns like:
- Agents posting too many messages in a row
- Very long messages that could be shorter
- Repetitive or low-value content
- Agents asking for content that's already available

When you detect problematic behavior, post a brief, polite correction like:
"[agent-name] please [specific guidance]"

Examples:
- "writer-agent please keep responses under 100 words"
- "editor-agent the content is in message #3 above"
- "grammar-agent please avoid duplicate corrections"

Only act when there's a clear issue that needs addressing.""",
            blackboard=blackboard
        )
    
    def get_completion_message(self) -> str:
        return ""  # No completion message needed for moderation


class SpamAgent(BaseAgent):
    """Agent that posts repetitive or excessive messages to test moderation."""
    
    def __init__(self, blackboard: Blackboard):
        super().__init__(
            name="spam-agent",
            goal="Post repetitive or excessive messages when detecting certain triggers",
            prompt="""You are a test agent that posts repetitive or excessive messages.

Act when you see:
- Articles about technology, computers, or AI
- Messages mentioning "spam" or "test"
- Multiple agents working on the same task

When you act, post repetitive content like:
- "This is great! This is great! This is great!"
- "I agree! I agree! I agree!"
- "More content needed! More content needed!"

Keep responses short but repetitive to test moderation systems.""",
            blackboard=blackboard
        )
    
    def get_completion_message(self) -> str:
        return ""


class OffTopicAgent(BaseAgent):
    """Agent that posts irrelevant content to test moderation."""
    
    def __init__(self, blackboard: Blackboard):
        super().__init__(
            name="offtopic-agent",
            goal="Post irrelevant content when conversations are focused",
            prompt="""You are a test agent that posts off-topic content.

When you see focused discussions about specific topics, post completely unrelated content like:
- "Did you know penguins can't fly?"
- "I had pizza for lunch today"
- "The weather is nice outside"
- "Random fact: bananas are berries"

Keep responses brief but clearly off-topic to test moderation.""",
            blackboard=blackboard
        )
    
    def get_completion_message(self) -> str:
        return ""


class VerboseAgent(BaseAgent):
    """Agent that creates unnecessarily long responses to test moderation."""
    
    def __init__(self, blackboard: Blackboard):
        super().__init__(
            name="verbose-agent",
            goal="Create unnecessarily long and wordy responses",
            prompt="""You are a test agent that creates overly verbose responses.

When you act, create extremely long, repetitive, and unnecessarily detailed responses about simple topics. Use phrases like:
- "In my extensive experience and detailed analysis..."
- "Furthermore, additionally, and moreover..."
- "It is important to note, consider, and understand..."

Make responses much longer than needed while staying somewhat relevant to test moderation of verbose content.""",
            blackboard=blackboard
        )
    
    def get_completion_message(self) -> str:
        return ""


class InterruptorAgent(BaseAgent):
    """Agent that tries to hijack conversations inappropriately."""
    
    def __init__(self, blackboard: Blackboard):
        super().__init__(
            name="interruptor-agent",
            goal="Interrupt ongoing conversations with self-promotion",
            prompt="""You are a test agent that interrupts conversations inappropriately.

When you see agents collaborating, interrupt with self-promotional content like:
- "Hey everyone, check out my amazing work!"
- "I'm the best agent here, let me handle this!"
- "Forget what they said, here's what I think..."
- "This conversation is boring, let's talk about me!"

Keep responses brief but clearly disruptive to test moderation of interrupting behavior.""",
            blackboard=blackboard
        )
    
    def get_completion_message(self) -> str:
        return ""
