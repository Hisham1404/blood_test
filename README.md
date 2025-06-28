# Blood Test Analyser - AI-Powered Medical Report Analysis

A FastAPI-based application that uses CrewAI agents to analyze blood test reports and provide comprehensive health recommendations through nutrition and exercise planning.

## 🔧 Bugs Found and Fixes Applied

### **Critical Issues Resolved:**

#### 1. **Invalid Agent Parameters** (`agents.py`)
```python
doctor = Agent(
    memory=True,    # not correct as crewai doesnot use memory inside agents
)
```

```python
    tools=[BloodTestReportTool().read_tool....] #not correct way
    tools=[BloodTestReportTool()], #is the correct way

```

#### 2. **Import Errors** (`tools.py`)
**Problem:** Incorrect import paths for CrewAI tools and missing PDF loader
```python
#These imports don't exist
from crewai_tools import tools
from crewai_tools.tools.serper_dev_tool import SerperDevTool
# PDFLoader used but never imported
```

**Fix:** Corrected import paths
```python

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.tools.google_serper.tool import GoogleSerperRun
from langchain_community.utilities.google_serper import GoogleSerperAPIWrapper
from crewai.tools import BaseTool
```

#### 3. **Incorrect BaseTool Implementation** (`tools.py`)
**Problem:** Custom method names instead of required `_run` method
```python
class BloodTestReportTool(BaseTool):
    async def read_data_tool(path="data/sample.pdf"):  # Missing self and wrong method used
```

**Fix:** Implemented proper BaseTool pattern
```python
class BloodTestReportTool(BaseTool):
    name: str = "Blood Test Report Reader"
    description: str = "Tool to read and analyze blood test reports from PDF files"
    
    def _run(self, path="data/sample.pdf") -> str:
        # Implementation with proper self parameter
```

#### 4. **Tool Usage Pattern Error** (`task.py`)
**Problem:** Attempting to access non-existent method from class instead of using instance
```python
tools=[BloodTestReportTool.read_data_tool]  # Method doesn't exist
```

**Fix:** Use proper tool instances
```python
tools=[BloodTestReportTool()]  
```

#### 5. **Missing Self Parameters** (`tools.py`)
**Problem:** Instance methods missing required `self` parameter
```python
async def read_data_tool(path="data/sample.pdf"): 
async def analyze_nutrition_tool(blood_report_data):
```

**Fix:** Added proper `self` parameters
```python
def _run(self, path="data/sample.pdf") -> str:   #used create instance _run()
def analyze_nutrition_tool(self, blood_report_data):
```


## 🚀 Setup and Usage Instructions

### **Prerequisites**
- Python 3.8 or higher
- Openrouter API used kimi model

### **Installation**

1. **Clone the repository:**
```bash
git clone https://github.com/Hisham1404/blood_test.git
cd blood_test
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Environment Configuration:**
Create a `.env` file in the root directory:
```env
Openrouter_api_key=your_openrouter_api_key_here
```

### **Running the Application**

#### **Start the FastAPI Server:**
```bash
python main.py
```
The server will start on `http://0.0.0.0:8000` with auto-reload enabled.

#### **Alternative using uvicorn directly:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### **Accessing the API**
- **Health Check:** `GET http://localhost:8000/`
- **API Documentation:** `http://localhost:8000/docs`
- **Analysis Endpoint:** `POST http://localhost:8000/analyze`


### **AI Agents Workflow**

The system uses 4 specialized CrewAI agents working in sequence:

1. **Doctor Agent**: Analyzes blood test data and provides medical insights
2. **Nutritionist Agent**: Creates personalized nutrition recommendations
3. **Exercise Specialist Agent**: Develops appropriate exercise plans
4. **Verifier Agent**: Reviews and validates all recommendations

## 🛠 Project Structure

```
blood-test-analyser-debug/
├── main.py              # FastAPI application and entry point
├── agents.py            # CrewAI agent definitions
├── task.py              # Task definitions for agents
├── tools.py             # Custom tools for PDF processing
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── data/               # Directory for uploaded files
├── outputs/            # Output directory for processed results
└── __pycache__/        # Python cache files
```
