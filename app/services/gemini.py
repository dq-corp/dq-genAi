import os
import google.generativeai as genai
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta

class GeminiChatBot:
    def __init__(self, model_name="gemini-1.5-pro"):
        load_dotenv()
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=self.generation_config,
        )
        self.chat_session = self.model.start_chat(history=[])
        
        # MongoDB connection
        self.client = MongoClient(os.environ['MONGO_URI'])
        self.db = self.client["data"]
        
    def get_recent_scans(self, cust_id, days=30):
        scan_collection = self.db["Scan"]
        product_collection = self.db["Product"]
        
        # Get recent scans
        cutoff_date = datetime.now() - timedelta(days=days)
        scans = scan_collection.find({
            "cust_id": cust_id,
        })
        
        scan_data = []
        for scan in list(scans)[:100]:
            product = product_collection.find_one({
                "upc": scan["upc"],
                "store_id": scan["store_id"]
            })
            if product:
                scan_data.append({
                    "upc": scan["upc"],
                    "store_id": scan["store_id"],
                    "date": scan["date"],
                    "product_name": product.get("name"),
                    "product_category": product.get("category"),
                    "product_price": product.get("price"),
                    "product_sku": product.get("sku"),
                    "product_description": product.get("description"),
                    "product_discounted_price": product.get("discounted_price"),
                    "product_brand": product.get("brand")
                })
        
        return scan_data

    def send_message(self, cust_id: str):
        scan_data = self.get_recent_scans(cust_id)
        
        if not scan_data:
            return "No recent scans found for this customer."

        message = f"""I have a customer profile with the following recent scans:
{scan_data}

Based on this data, generate one personalized mobile notification. Let it be attention-grabbing. Mention:
1. The product details and why it might be best for them.
2. Specific products they have bought frequently.
3. Encourage them to check the app and explore personalized offers.

Keep it concise and engaging, not longer than 20 words, aiming to prompt action.
"""
        response = self.chat_session.send_message(message)
        return response.text

    def get_history(self):
        return self.chat_session.history

# Usage example:
if __name__ == "__main__":
    '''
    #chatbot = GeminiChatBot()
    # Send a message and get response
    response = chatbot.send_message("c786ddc5-b6f6-4fda-ab67-9337874a9594")
    print("Bot:", response)
    # Get chat history
    history = chatbot.get_history()
    print("Chat History:", history)
    '''