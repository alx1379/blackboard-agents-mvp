import openai
from typing import List, Dict, Any
from config import Config
from blackboard import Blackboard
from router import Router

class BaseAgent:
    """Base class for all LLM-based agents."""
    
    def __init__(self, name: str, goal: str, prompt: str, blackboard: Blackboard):
        self.name = name
        self.goal = goal
        self.prompt = prompt
        self.blackboard = blackboard
        self.router = Router(blackboard)
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def should_act(self, context: str) -> bool:
        """Use LLM to decide if agent should act on the given context."""
        decision_prompt = f"""
You are an agent with the following goal: {self.goal}

Recent messages from the blackboard:
{context}

Question: Should you act on these messages based on your goal? 
Answer only "YES" or "NO" with a brief reason.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[{"role": "user", "content": decision_prompt}],
                max_tokens=50,
                temperature=0.1
            )
            
            answer = response.choices[0].message.content.strip().upper()
            return answer.startswith("YES")
        
        except Exception as e:
            print(f"Error in decision making for {self.name}: {e}")
            return False
    
    def process_text(self, context: str) -> str:
        """Use LLM to process text according to agent's prompt."""
        full_prompt = f"""
{self.prompt}

Context from blackboard:
{context}

Please provide your response:
"""
        
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[{"role": "user", "content": full_prompt}],
                max_tokens=Config.OPENAI_MAX_TOKENS,
                temperature=Config.OPENAI_TEMPERATURE
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return f"Error processing text: {e}"
    
    def try_act(self):
        """Check if agent should act and process if needed."""
        context_messages = self.router.get_context_for_agent()
        if not context_messages:
            return
        
        context = self.router.format_context(context_messages)
        
        if self.should_act(context):
            result = self.process_text(context)
            self.blackboard.post(self.name, result)


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


class EditorAgent(BaseAgent):
    """Agent specialized in improving writing style and structure."""
    
    def __init__(self, blackboard: Blackboard):
        super().__init__(
            name="editor-agent", 
            goal="Improve writing style, structure, and clarity of text",
            prompt="""You are an experienced editor. Your task is to improve the style, structure, and clarity of written content.
Focus on:
- Enhancing readability and flow
- Improving sentence structure
- Making the content more engaging
- Maintaining the original meaning while improving expression""",
            blackboard=blackboard
        )


class GrammarAgent(BaseAgent):
    """Agent specialized in fixing grammar and language errors."""
    
    def __init__(self, blackboard: Blackboard):
        super().__init__(
            name="grammar-agent",
            goal="Fix grammar, spelling, and language errors in text", 
            prompt="""You are a meticulous grammar checker. Your task is to fix grammar, spelling, punctuation, and other language errors.
Focus on:
- Correcting grammatical mistakes
- Fixing spelling errors
- Improving punctuation
- Ensuring proper sentence structure
Preserve the original meaning and style while making corrections.""",
            blackboard=blackboard
        )
