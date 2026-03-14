"""
Context Management for Oil Agent
Optimizes token usage by managing conversation history and context.
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime

log = logging.getLogger(__name__)


class HistoryCompressor:
    """Compresses conversation history to reduce token usage."""
    
    def __init__(self, compression_ratio: float = 0.15):
        """
        Args:
            compression_ratio: Target compression ratio (0.0-1.0)
        """
        self.compression_ratio = compression_ratio
    
    def compress_history(self, history: List[Dict]) -> str:
        """
        Compresses conversation history into a compact summary.
        
        Args:
            history: List of conversation turns
            
        Returns:
            Compressed summary string
        """
        if not history:
            return ""
        
        # Extract key information from history
        key_points = []
        for turn in history[-10:]:  # Only last 10 turns
            if 'role' in turn and 'content' in turn:
                content = turn['content']
                # Keep only essential information
                if len(content) > 200:
                    # Truncate and keep first 200 chars
                    key_points.append(content[:200] + "...")
                else:
                    key_points.append(content)
        
        # Create compressed summary
        summary = " | ".join(key_points)
        return summary


class SlidingWindowManager:
    """Manages a sliding window of recent context."""
    
    def __init__(self, window_size: int = 3, max_tokens: int = 8000):
        """
        Args:
            window_size: Number of recent steps to keep
            max_tokens: Maximum tokens for window content
        """
        self.window_size = window_size
        self.max_tokens = max_tokens
        self.history: List[Dict] = []
        self.compressed_history: Optional[Dict] = None
    
    def add_step(self, step_data: Dict):
        """
        Adds a new step to the window.
        
        Args:
            step_data: Dictionary containing step information
        """
        self.history.append(step_data)
        
        # Keep only the most recent steps
        if len(self.history) > self.window_size:
            self.history = self.history[-self.window_size:]
    
    def get_window_summary(self) -> str:
        """
        Returns a summary of the current window.
        
        Returns:
            Summary string of recent steps
        """
        if not self.history:
            return "No recent context available."
        
        summary_parts = []
        for i, step in enumerate(self.history):
            if 'tool' in step:
                summary_parts.append(f"Step {i+1}: Used {step['tool']}")
            elif 'result' in step:
                result_preview = step['result'][:100] if len(step['result']) > 100 else step['result']
                summary_parts.append(f"Step {i+1}: Result: {result_preview}...")
        
        return " | ".join(summary_parts)
    
    def clear_old(self):
        """Clears old entries beyond window size."""
        if len(self.history) > self.window_size:
            self.history = self.history[-self.window_size:]
    
    def compress_window(self, compressor: HistoryCompressor) -> Dict:
        """
        Compresses the current window history.
        
        Args:
            compressor: HistoryCompressor instance
            
        Returns:
            Dictionary with compressed summary and metadata
        """
        if not self.history:
            return None
        
        # Create summary from history
        summary_parts = []
        for step in self.history:
            if 'tool' in step:
                summary_parts.append(f"Used {step['tool']}")
            elif 'result' in step:
                summary_parts.append(f"Result: {step['result'][:100]}...")
        
        summary = " | ".join(summary_parts)
        
        self.compressed_history = {
            'summary': summary,
            'steps_count': len(self.history),
            'timestamp': datetime.now().isoformat()
        }
        
        return self.compressed_history


class MemoryCleaner:
    """Cleans memory by removing redundant or low-value content."""
    
    def __init__(self):
        self.cache: Dict[str, any] = {}
    
    def clean_content(self, content) -> str:
        """
        Cleans content by removing duplicates and low-value text.
        
        Args:
            content: Raw content (string or dict)
            
        Returns:
            Cleaned content string
        """
        # Handle dict input (from agent results)
        if isinstance(content, dict):
            # Convert dict to string representation
            content = str(content)
        
        # Ensure content is a string
        if not isinstance(content, str):
            return str(content)
        
        # Split into lines
        lines = content.split('\n')
        cleaned_lines = []
        seen_lines = set()
        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue
            
            # Skip duplicates
            line_hash = hash(line.strip())
            if line_hash in seen_lines:
                continue
            seen_lines.add(line_hash)
            
            # Keep line
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def deduplicate_events(self, events: List[Dict]) -> List[Dict]:
        """
        Removes duplicate events from a list.
        
        Args:
            events: List of event dictionaries
            
        Returns:
            Deduplicated list of events
        """
        seen = set()
        deduplicated = []
        
        for event in events:
            # Create a unique identifier
            if 'title' in event:
                event_id = f"{event.get('title', '')}_{event.get('category', '')}"
                if event_id not in seen:
                    seen.add(event_id)
                    deduplicated.append(event)
            else:
                deduplicated.append(event)
        
        return deduplicated


class AgentState:
    """Tracks agent state and statistics."""
    
    def __init__(self, max_steps: int = 10):
        """
        Args:
            max_steps: Maximum number of steps allowed
        """
        self.max_steps = max_steps
        self.current_step = 0
        self.total_tokens_input = 0
        self.total_tokens_output = 0
        self.events_detected = 0
        self.start_time = datetime.now()
        
        # Phase 2: Extended tracking attributes
        self.tools_used = set()  # Set of tool names used
        self.detected_events = []  # List of all detected events
        self.high_impact_events = []  # List of high-impact events (impact >= 7)
        self.compression_savings = 0  # Tokens saved through compression
    
    def increment_step(self):
        """Increments current step counter."""
        self.current_step += 1
    
    def add_tokens(self, input_tokens: int, output_tokens: int):
        """
        Adds token usage to statistics.
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
        """
        self.total_tokens_input += input_tokens
        self.total_tokens_output += output_tokens
    
    def add_event(self):
        """Increments events detected counter."""
        self.events_detected += 1
    
    def add_tool_usage(self, tool_name: str):
        """
        Records that a tool was used.
        
        Args:
            tool_name: Name of the tool used
        """
        self.tools_used.add(tool_name)
    
    def add_detected_event(self, event: dict):
        """
        Adds a detected event to the tracking list.
        
        Args:
            event: Event dictionary
        """
        self.detected_events.append(event)
        
        # Track high-impact events (impact >= 7)
        impact_score = event.get('impact_score', 0)
        if impact_score >= 7:
            self.high_impact_events.append(event)
            # Keep only last 10 high-impact events
            if len(self.high_impact_events) > 10:
                self.high_impact_events = self.high_impact_events[-10:]
    
    def add_compression_savings(self, tokens_saved: int):
        """
        Adds tokens saved through compression.
        
        Args:
            tokens_saved: Number of tokens saved
        """
        self.compression_savings += tokens_saved
    
    def get_summary(self) -> str:
        """
        Returns a summary of agent state.
        
        Returns:
            Summary string
        """
        duration = datetime.now() - self.start_time
        
        summary = f"""Agent State Summary:
 - Steps: {self.current_step}/{self.max_steps}
 - Total Input Tokens: {self.total_tokens_input:,}
 - Total Output Tokens: {self.total_tokens_output:,}
 - Events Detected: {self.events_detected}
 - Duration: {duration}
 - Average Input/Step: {self.total_tokens_input // self.current_step if self.current_step > 0 else 0:,}
 - Average Output/Step: {self.total_tokens_output // self.current_step if self.current_step > 0 else 0:,}
 - Tools Used: {len(self.tools_used)}
 - High Impact Events: {len(self.high_impact_events)}
 - Compression Savings: {self.compression_savings:,} tokens
"""
        return summary
    
    def is_complete(self) -> bool:
        """Returns True if agent has completed all steps."""
        return self.current_step >= self.max_steps


def build_optimized_prompt_context(
    state: AgentState,
    window_manager: SlidingWindowManager,
    current_date: str,
    current_datetime: str
) -> str:
    """
    Builds an optimized prompt context with minimal token usage.
    
    Args:
        state: Agent state object
        window_manager: Sliding window manager
        current_date: Current date string
        current_datetime: Current datetime string
        
    Returns:
        Optimized prompt context string
    """
    context_parts = []
    
    # Add current context
    context_parts.append(f"Date: {current_date}")
    context_parts.append(f"Time: {current_datetime}")
    context_parts.append(f"Step: {state.current_step}/{state.max_steps}")
    
    # Add compressed history if available
    if window_manager.compressed_history:
        context_parts.append("=== COMPRESSED HISTORY ===")
        context_parts.append(window_manager.compressed_history['summary'])
    
    # Add high-impact events if available
    if state.high_impact_events:
        context_parts.append("=== HIGH IMPACT EVENTS ===")
        for event in state.high_impact_events[-5:]:  # Last 5 events
            context_parts.append(f"- {event.get('title', 'Unknown')} (impact: {event.get('impact_score', 0)})")
    
    # Add window summary if available
    window_summary = window_manager.get_window_summary()
    if window_summary and window_summary != "No recent context available.":
        context_parts.append(f"Recent Context: {window_summary}")
    
    # Add token usage stats
    if state.total_tokens_input > 0:
        ratio = state.total_tokens_output / state.total_tokens_input if state.total_tokens_input > 0 else 0
        context_parts.append(f"Token Usage: {state.total_tokens_input:,} in → {state.total_tokens_output:,} out (ratio: {ratio:.2f})")
    
    # Add compression savings if available
    if state.compression_savings > 0:
        context_parts.append(f"Compression Savings: {state.compression_savings:,} tokens")
    
    # Join all parts
    optimized_context = "\n".join(context_parts)
    
    return optimized_context
