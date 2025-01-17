from tabnanny import verbose
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import (
    FileReadTool,
    ScrapeWebsiteTool,
    SerperDevTool,
    WebsiteSearchTool
)
from crewai_tools.tools import DallETool

from scripted_ai.models.post_data import PostData
from scripted_ai.tools.gcp_image_uploader import GCPImageUploaderTool
from scripted_ai.tools.image_downloader import ImageDownloaderTool
from scripted_ai.tools.wordpress_tool import WordpressTool
from scripted_ai.knowledge.crew_ai_knowledge_source import CrewAiKnowledgeSource
from bs4 import BeautifulSoup

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ScriptedAi():
	"""ScriptedAi crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
 
	search_tool = SerperDevTool()
	scrape_tool = ScrapeWebsiteTool(website="{main_font}")
	web_rag_tool = WebsiteSearchTool(website="{main_font}")
	file_reader = FileReadTool()
	wordpress_tool = WordpressTool()
	image_downloader = ImageDownloaderTool()
	image_uploader = GCPImageUploaderTool()
	
	
 
	# crewai_base_knowledge = CrewAiKnowledgeSource()
 
	dalle_tool = DallETool(model="dall-e-3",
						size="1024x1024",
						quality="standard",
						n=1)

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			verbose=True,
			# knowledge_sources=[self.crewai_base_knowledge],
		)

	@agent
	def writer(self) -> Agent:
		return Agent(
			config=self.agents_config['writer'],
			verbose=True,
			llm="gpt-4o",   
		)
  
	@agent
	def html_page_developer(self) -> Agent:
		return Agent(
			config=self.agents_config['html_page_developer'],
			verbose=True,
			
		)
  
	@agent
	def json_developer(self) -> Agent:
		return Agent(
			config=self.agents_config['json_developer'],
			verbose=True,
			
		)
	@agent
	def image_designer(self) -> Agent:
		return Agent(
			config=self.agents_config['image_designer'],
			verbose=True,
		)
  
	@agent
	def wordpress_publisher(self) -> Agent:
		return Agent(
			config=self.agents_config['wordpress_publisher'],
			verbose=True,			
		)
  
	def content_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['content_manager'],
			verbose=True,
			allow_delegation=False,
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			tools=[
    			self.scrape_tool,
				# self.search_tool,
				self.web_rag_tool
			]
		)

	@task
	def writing_task(self) -> Task:
		return Task(
			config=self.tasks_config['writing_task'],
			output_file='post.md',
			context=[
				self.research_task()
			],
		)
  
	@task
	def image_generation_task(self) -> Task:
		return Task(
			config=self.tasks_config['image_generation_task'],
			context=[
				self.research_task()
			],
			tools=[
				self.dalle_tool
			],
		)
	
	@task
	def image_download_task(self) -> Task:
		return Task(
			config=self.tasks_config['image_download_task'],
			context=[
				self.image_generation_task()
			],
			tools=[
				self.image_downloader
			],
		)
  
	@task
	def image_uploader_task(self) -> Task:
		return Task(
			config=self.tasks_config['image_uploader_task'],
			context=[
				self.image_download_task()
			],
			tools=[
				self.image_uploader
			],
		)

	@task
	def html_development_task(self) -> Task:
		return Task(
			config=self.tasks_config['html_development_task'],
			output_file='post.html',
			context=[
				self.writing_task(),
				self.image_generation_task(),
				self.image_uploader_task()
			]
		)

	@task
	def json_development_task(self) -> Task:
		return Task(
			config=self.tasks_config['json_development_task'],			
			context=[
				self.html_development_task()
			],
			outputs={"json_result": "{output}"},
			output_validation=PostData
		)
  
	@task
	def post_publishing_task(self) -> Task:
		return Task(
			config=self.tasks_config['post_publishing_task'],
			tools=[
				self.wordpress_tool
			],
			context=[
				self.json_development_task()
			],
   
			context_inputs={
				"title": "{json_result[title]}",
				"content": "{json_result[content]}",
				"status": "{json_result[status]}"
			}
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ScriptedAi crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			memory=True,
			# manager_agent=self.content_manager(),
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
