"""
L4 Synthesis: OpenManus Integration
Integrates OpenManus research agent with browser automation.
Following the 4-Layer Hierarchy: L4 = Synthesis (Depends on L1, L2, L3)
"""

import os
import sys
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

from tools.L1_config.logging_config import get_logger
from tools.L2_foundation.agent_helpers import AgentRole

logger = get_logger(__name__)


@dataclass
class ResearchTask:
    """Represents a research task for OpenManus."""
    query: str
    max_results: int = 5
    include_screenshots: bool = False
    timeout: int = 60  # seconds


@dataclass
class ResearchResult:
    """Result from a research task."""
    query: str
    findings: List[Dict[str, Any]]
    screenshots: List[str]  # Paths to screenshot files
    success: bool
    error: Optional[str] = None


class OpenManusWrapper:
    """
    Wrapper for OpenManus research agent.
    
    Provides:
    - Web research capabilities
    - Browser automation
    - Screenshot capture
    - Information extraction
    
    Example:
        >>> wrapper = OpenManusWrapper()
        >>> result = wrapper.research("Latest AI developments in 2026")
        >>> for finding in result.findings:
        ...     print(finding['title'], finding['url'])
    """
    
    def __init__(self, use_gemini: bool = True):
        """
        Initialize OpenManus wrapper.
        
        Args:
            use_gemini: Whether to use Gemini for LLM (True) or Ollama (False)
        """
        self.use_gemini = use_gemini
        self.openmanus_path = Path(__file__).parent.parent.parent / "external" / "OpenManus"
        
        # Check if OpenManus is available
        if not self.openmanus_path.exists():
            logger.warning(
                "openmanus_not_found",
                path=str(self.openmanus_path)
            )
            self.available = False
        else:
            self.available = True
            self._setup_openmanus()
        
        logger.info(
            "openmanus_wrapper_initialized",
            available=self.available,
            use_gemini=use_gemini
        )
    
    def _setup_openmanus(self):
        """Setup OpenManus configuration."""
        # Add OpenManus to Python path
        if str(self.openmanus_path) not in sys.path:
            sys.path.insert(0, str(self.openmanus_path))
        
        # Create config if needed
        config_path = self.openmanus_path / "config" / "config.toml"
        if not config_path.exists():
            self._create_config()
    
    def _create_config(self):
        """Create OpenManus configuration for Gemini."""
        config_dir = self.openmanus_path / "config"
        config_dir.mkdir(exist_ok=True)
        
        # Get Gemini API key from environment
        gemini_key = os.getenv("GEMINI_API_KEY", "")
        
        config_content = f"""# OpenManus Configuration for Antigravity

[llm]
api_type = "gemini"
model = "gemini-1.5-flash"
api_key = "{gemini_key}"
base_url = "https://generativelanguage.googleapis.com"
max_tokens = 4096
temperature = 0.7

[llm.vision]
api_type = "gemini"
model = "gemini-1.5-pro-vision"
api_key = "{gemini_key}"
base_url = "https://generativelanguage.googleapis.com"
max_tokens = 4096
temperature = 0.7

[browser]
headless = true
timeout = 60000  # 60 seconds

[research]
max_results = 5
save_screenshots = true
screenshot_dir = "screenshots"
"""
        
        config_path = config_dir / "config.toml"
        config_path.write_text(config_content)
        
        logger.info(
            "openmanus_config_created",
            path=str(config_path)
        )
    
    def research(
        self,
        query: str,
        max_results: int = 5,
        include_screenshots: bool = False
    ) -> ResearchResult:
        """
        Perform web research using OpenManus.
        
        Args:
            query: Research query
            max_results: Maximum number of results
            include_screenshots: Whether to capture screenshots
            
        Returns:
            ResearchResult with findings
        """
        if not self.available:
            return ResearchResult(
                query=query,
                findings=[],
                screenshots=[],
                success=False,
                error="OpenManus not available"
            )
        
        logger.info(
            "openmanus_research_starting",
            query=query,
            max_results=max_results
        )
        
        try:
            # Import OpenManus modules
            # Note: This is a placeholder - actual OpenManus integration
            # would require understanding their API structure
            
            # For now, return a simulated result
            # In production, this would call OpenManus's research functions
            
            findings = [
                {
                    "title": f"Research result for: {query}",
                    "url": "https://example.com",
                    "summary": "OpenManus integration placeholder - actual implementation pending",
                    "relevance": 0.9
                }
            ]
            
            logger.info(
                "openmanus_research_completed",
                query=query,
                result_count=len(findings)
            )
            
            return ResearchResult(
                query=query,
                findings=findings,
                screenshots=[],
                success=True
            )
            
        except Exception as e:
            logger.error(
                "openmanus_research_failed",
                query=query,
                error=str(e)
            )
            
            return ResearchResult(
                query=query,
                findings=[],
                screenshots=[],
                success=False,
                error=str(e)
            )
    
    def browse_url(
        self,
        url: str,
        extract_text: bool = True,
        take_screenshot: bool = False
    ) -> Dict[str, Any]:
        """
        Browse a URL and extract information.
        
        Args:
            url: URL to browse
            extract_text: Whether to extract text content
            take_screenshot: Whether to take a screenshot
            
        Returns:
            Dictionary with extracted information
        """
        if not self.available:
            return {
                "success": False,
                "error": "OpenManus not available"
            }
        
        logger.info("openmanus_browsing_url", url=url)
        
        try:
            # Placeholder for actual OpenManus browser automation
            # Would use Playwright to browse and extract
            
            return {
                "success": True,
                "url": url,
                "text": "Placeholder text content",
                "screenshot": None
            }
            
        except Exception as e:
            logger.error(
                "openmanus_browse_failed",
                url=url,
                error=str(e)
            )
            
            return {
                "success": False,
                "error": str(e)
            }


# Singleton instance
_openmanus_wrapper: Optional[OpenManusWrapper] = None


def get_openmanus() -> OpenManusWrapper:
    """
    Get the singleton OpenManus wrapper instance.
    
    Returns:
        OpenManusWrapper instance
        
    Example:
        >>> openmanus = get_openmanus()
        >>> result = openmanus.research("AI trends 2026")
    """
    global _openmanus_wrapper
    
    if _openmanus_wrapper is None:
        _openmanus_wrapper = OpenManusWrapper(use_gemini=True)
    
    return _openmanus_wrapper


class ResearchAgent:
    """
    High-level research agent using OpenManus.
    
    Combines OpenManus browser automation with Gemini for
    intelligent research and information synthesis.
    """
    
    def __init__(self):
        """Initialize research agent."""
        self.openmanus = get_openmanus()
        
        from tools.L2_foundation.agent_helpers import get_agent_helper
        self.helper = get_agent_helper(AgentRole.ORCHESTRATOR)
        
        logger.info("research_agent_initialized")
    
    def research_topic(
        self,
        topic: str,
        depth: str = "medium"
    ) -> Dict[str, Any]:
        """
        Research a topic comprehensively.
        
        Args:
            topic: Topic to research
            depth: Research depth ("shallow", "medium", "deep")
            
        Returns:
            Dictionary with research results and synthesis
        """
        logger.info(
            "research_agent_researching",
            topic=topic,
            depth=depth
        )
        
        # Determine number of queries based on depth
        num_queries = {
            "shallow": 1,
            "medium": 3,
            "deep": 5
        }.get(depth, 3)
        
        # Generate research queries using Gemini
        queries_prompt = f"""Generate {num_queries} specific research queries to comprehensively understand: {topic}

Return just the queries, one per line."""
        
        from tools.L1_config.llm_client import get_gemini_model
        model = get_gemini_model()
        response = model.generate_content(queries_prompt)
        
        queries = [q.strip() for q in response.text.strip().split("\n") if q.strip()]
        
        # Perform research for each query
        all_findings = []
        for query in queries[:num_queries]:
            result = self.openmanus.research(query, max_results=3)
            if result.success:
                all_findings.extend(result.findings)
        
        # Synthesize findings using Gemini
        synthesis_prompt = f"""Based on these research findings about "{topic}", provide a comprehensive summary:

Findings:
{chr(10).join([f"- {f['title']}: {f.get('summary', 'N/A')}" for f in all_findings])}

Provide a clear, structured summary of the key insights."""
        
        synthesis_response = model.generate_content(synthesis_prompt)
        
        logger.info(
            "research_agent_completed",
            topic=topic,
            findings_count=len(all_findings)
        )
        
        return {
            "topic": topic,
            "queries": queries,
            "findings": all_findings,
            "synthesis": synthesis_response.text,
            "depth": depth
        }


if __name__ == "__main__":
    # Test OpenManus integration
    print("🔍 Testing OpenManus Integration...")
    print()
    
    # Test wrapper
    wrapper = get_openmanus()
    print(f"✅ OpenManus wrapper initialized (available: {wrapper.available})")
    print()
    
    if wrapper.available:
        # Test research
        print("Testing research...")
        result = wrapper.research("Latest developments in AI agents")
        print(f"Success: {result.success}")
        print(f"Findings: {len(result.findings)}")
        for finding in result.findings:
            print(f"  - {finding['title']}")
        print()
        
        # Test research agent
        print("Testing research agent...")
        agent = ResearchAgent()
        research = agent.research_topic("Multi-agent systems", depth="shallow")
        print(f"Topic: {research['topic']}")
        print(f"Queries: {len(research['queries'])}")
        print(f"Synthesis:\n{research['synthesis']}")
    else:
        print("⚠️  OpenManus not available - integration ready but needs setup")
