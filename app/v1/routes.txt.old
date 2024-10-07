from fastapi import APIRouter,HTTPException
from app.models.customer_model import CustomerModel
from app.services.gemini import GeminiChatBot
from app.services.fetch import KaggleDatasetDownloader

router = APIRouter()
chatbot = GeminiChatBot()
downloader = KaggleDatasetDownloader()

@router.post("/generate-notification")
async def generate_notification(customer_details: CustomerModel):
    try:
        customer_data = customer_details.dict()
        notification = chatbot.send_message(customer_data)
        return {"notification": notification}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.get("/get-customer-model/{customer_id}", response_model=CustomerModel)
async def get_customer_model(customer_id: int):
    try:
        # Download and load the dataset
        df = downloader.download_dataset("imakash3011", "customer-personality-analysis", "1", "marketing_campaign.csv")
        
        # Search for the customer by ID
        customer_data = df[df['ID'] == customer_id].to_dict(orient='records')

        if not customer_data:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Convert the result to the CustomerModel (assuming only one result is found)
        return CustomerModel(**customer_data[0])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")