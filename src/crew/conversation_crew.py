import os
import os
from crewai import Agent, Task, Crew, LLM, Process
from crewai.project import agent, task, crew, CrewBase
from crewai_tools import SerperDevTool
from src.crew.tools.nse_tools import get_all_nse_tools
from dotenv import load_dotenv

load_dotenv()

# Initialize tools once
nse_tools = get_all_nse_tools()
serper_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY", "demo"))

os.getenv("GEMINI_API_KEY")
llm = LLM(model="gemini/gemini-2.0-flash")
@CrewBase
class ConversationCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def indian_stock_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['indian_stock_researcher'],
            llm=llm,
            tools=[serper_tool]
        )
    
    @agent
    def nse_data_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['nse_data_analyst'],
            llm=llm,
            tools=nse_tools
        )
    
    @agent
    def response_coordinator(self) -> Agent:
        return Agent(
            config=self.agents_config['response_coordinator'],
            llm=llm,
            tools=[]
        )

    @task
    def research_indian_stock_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_indian_stock_task'],
            agent=self.indian_stock_researcher()
        )
    
    @task
    def analyze_nse_data_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_nse_data_task'],
            agent=self.nse_data_analyst()
        )
    
    @task
    def coordinate_response_task(self) -> Task:
        return Task(
            config=self.tasks_config['coordinate_response_task'],
            agent=self.response_coordinator()
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the simplified conversation crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
    
