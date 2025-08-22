"""LLM abstraction layer supporting multiple providers."""

import openai
from typing import Optional, Dict, Any
from config import Config

class LLMProvider:
    """Base class for LLM providers."""
    
    def chat_completion(self, messages: list, max_tokens: int = None, temperature: float = None) -> str:
        """Generate chat completion."""
        raise NotImplementedError
    
    def is_available(self) -> bool:
        """Check if provider is properly configured."""
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider."""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY) if Config.OPENAI_API_KEY else None
    
    def chat_completion(self, messages: list, max_tokens: int = None, temperature: float = None) -> str:
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        response = self.client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=messages,
            max_tokens=max_tokens or Config.OPENAI_MAX_TOKENS,
            temperature=temperature or Config.OPENAI_TEMPERATURE
        )
        
        return response.choices[0].message.content.strip()
    
    def is_available(self) -> bool:
        return Config.OPENAI_API_KEY is not None


class GeminiProvider(LLMProvider):
    """Google Gemini provider."""
    
    def __init__(self):
        try:
            import google.generativeai as genai
            if Config.GEMINI_API_KEY:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
            else:
                self.model = None
        except ImportError:
            self.model = None
    
    def chat_completion(self, messages: list, max_tokens: int = None, temperature: float = None) -> str:
        if not self.model:
            raise ValueError("Gemini not available - check API key and google-generativeai package")
        
        # Convert OpenAI format to Gemini format
        prompt = self._convert_messages_to_prompt(messages)
        
        # Configure generation
        generation_config = {
            'max_output_tokens': max_tokens or Config.GEMINI_MAX_TOKENS,
            'temperature': temperature or Config.GEMINI_TEMPERATURE,
        }
        
        response = self.model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        return response.text.strip()
    
    def _convert_messages_to_prompt(self, messages: list) -> str:
        """Convert OpenAI message format to simple prompt."""
        prompt_parts = []
        for msg in messages:
            if msg["role"] == "user":
                prompt_parts.append(msg["content"])
            elif msg["role"] == "system":
                prompt_parts.append(f"System: {msg['content']}")
        return "\n".join(prompt_parts)
    
    def is_available(self) -> bool:
        return self.model is not None


class LLMClient:
    """Main LLM client that routes to configured provider."""
    
    def __init__(self):
        self.providers = {
            "openai": OpenAIProvider(),
            "gemini": GeminiProvider()
        }
        self.current_provider = self._get_active_provider()
    
    def _get_active_provider(self) -> LLMProvider:
        """Get the configured active provider."""
        provider_name = Config.LLM_PROVIDER.lower()
        
        if provider_name in self.providers and self.providers[provider_name].is_available():
            return self.providers[provider_name]
        
        # Fallback to first available provider
        for provider in self.providers.values():
            if provider.is_available():
                return provider
        
        raise ValueError("No LLM provider is properly configured")
    
    def chat_completion(self, messages: list, max_tokens: int = None, temperature: float = None) -> str:
        """Generate chat completion using active provider."""
        return self.current_provider.chat_completion(messages, max_tokens, temperature)
    
    def get_provider_name(self) -> str:
        """Get name of current provider."""
        for name, provider in self.providers.items():
            if provider == self.current_provider:
                return name
        return "unknown"
