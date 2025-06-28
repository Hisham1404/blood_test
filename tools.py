## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.tools.google_serper.tool import GoogleSerperRun
from langchain_community.utilities.google_serper import GoogleSerperAPIWrapper
from crewai.tools import BaseTool

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
serper_api_wrapper = GoogleSerperAPIWrapper(
    serper_api_key=SERPER_API_KEY
)
## Creating search tool
search_tool = GoogleSerperRun(
    api_wrapper=serper_api_wrapper
)

## Creating custom pdf reader tool
class BloodTestReportTool(BaseTool):
    name: str = "Blood Test Report Reader"
    description: str = "Tool to read and analyze blood test reports from PDF files" 
    def _run(self, path="data/sample.pdf") -> str:
        """Tool to read data from a pdf file from a path

        Args:
            path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

        Returns:
            str: Full Blood Test report file
        """
        
        docs = PyPDFLoader(file_path=path).load()

        full_report = ""
        for data in docs:
            # Clean and format the report data
            content = data.page_content
            
            # Remove extra whitespaces and format properly
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
                
            full_report += content + "\n"
            
        return full_report

## Creating Nutrition Analysis Tool
class NutritionTool:
    async def analyze_nutrition_tool(self, blood_report_data):
        # Process and analyze the blood report data
        processed_data = blood_report_data

        # Clean up the data format
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":  # Remove double spaces
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
                
        # TODO: Implement nutrition analysis logic here
        return "Nutrition analysis functionality to be implemented"

## Creating Exercise Planning Tool
class ExerciseTool:
    async def create_exercise_plan_tool(self, blood_report_data):        
        # TODO: Implement exercise planning logic here
        return "Exercise planning functionality to be implemented"