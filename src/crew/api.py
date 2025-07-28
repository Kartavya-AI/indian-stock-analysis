from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from conversation_crew import ConversationCrew
import sys

# Initialize FastAPI
app = FastAPI(
    title="NSE Stock Market Analysis API",
    description="Ask questions about Indian stocks, IPOs, or market data",
    version="1.0.0"
)

# Initialize the crew
crew = ConversationCrew()

# Request model
class StockQuery(BaseModel):
    question: str

# Response model  
class StockResponse(BaseModel):
    question: str
    result: str
    status: str

@app.post("/analyze-stock/", response_model=StockResponse)
async def analyze_stock(query: StockQuery):
    """
    Analyze stock market questions using the conversation crew
    
    Examples:
    - "Tell me about Reliance stock"
    - "LIC IPO performance" 
    - "Top gainers today"
    - "Current price of TCS"
    """
    
    if not query.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        # Run the crew analysis
        result = crew.crew().kickoff(inputs={'user_question': query.question})
        
        return StockResponse(
            question=query.question,
            result=str(result),
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )

@app.get("/")
async def root():
    return {
        "message": "NSE Stock Market Analysis System",
        "description": "Ask questions about Indian stocks, IPOs, or market data",
        "endpoint": "/analyze-stock/",
        "examples": [
            "Tell me about Reliance stock",
            "LIC IPO performance",
            "Top gainers today", 
            "Current price of TCS"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "NSE Stock Analysis API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)