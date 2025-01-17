from crewai.knowledge.source.base_knowledge_source import BaseKnowledgeSource
from crewai_tools.tools.scrape_website_tool.scrape_website_tool import ScrapeWebsiteTool

class CrewAiKnowledgeSource(BaseKnowledgeSource):    
    
    def load_content(self) -> str:
        try:
            site_url = "https://docs.crewai.com"
            scrape_tool = ScrapeWebsiteTool(website=site_url)
            response = scrape_tool.run()
            return response
        except Exception as e:
            raise ValueError(f"An error occurred while loading content: {e}")
        
    def add(self) -> None:
        content = self.load_content()
        for _, text in content.items():
            chunks = self._chunk_text(text)
            self.chunks.extend(chunks)
        
        self.save_documents()
        
    
            
            