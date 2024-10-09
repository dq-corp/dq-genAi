from fastapi import APIRouter,HTTPException, Query, Request
from app.services.gemini import GeminiChatBot
import traceback


router = APIRouter()
chatbot = GeminiChatBot()

@router.post("/whatsapp-webhook")
async def whatsapp_webhook(request: Request):
    try:
        data = await request.form()
        from_number = data.get('From')
        message_body = data.get('Body')

        if not from_number or not message_body:
            raise HTTPException(status_code=400, detail="Invalid request data: Missing 'From' or 'Body'")

        response_text = chatbot.process_incoming_message(from_number, message_body)
        chatbot.send_whatsapp_message(from_number, response_text)
        return "OK" 

    except HTTPException as e:
        # These are exceptions you're raising intentionally for bad requests
        print(f"HTTPException: {e.status_code} - {e.detail}") 
        return {"error": e.detail}, e.status_code

    except Exception as e:
        # This will catch broader errors and print a stack trace
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        traceback.print_exc() # Print the full traceback
        return {"error": error_message}, 500 

@router.get("/generate-notification")
async def generate_notification(cust_id: str = Query(..., title="Customer ID", description="The ID of the customer to generate notification for")):
    try:
        notification = chatbot.send_message(cust_id)
        return {"notification": notification}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
