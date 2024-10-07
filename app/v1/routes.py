from fastapi import APIRouter,HTTPException, Query
from app.services.gemini import GeminiChatBot


router = APIRouter()
chatbot = GeminiChatBot()

@router.get("/generate-notification")
async def generate_notification(cust_id: str = Query(..., title="Customer ID", description="The ID of the customer to generate notification for")):
    try:
        notification = chatbot.send_message(cust_id)
        return {"notification": notification}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
