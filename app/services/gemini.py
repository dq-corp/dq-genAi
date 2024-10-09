import os
import google.generativeai as genai
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta
from twilio.rest import Client

class GeminiChatBot:
    def __init__(self, model_name="gemini-1.5-flash"):
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

        #self.account_sid = os.environ['account_sid']
        #self.auth_token = os.environ['auth_token'] 
        # Twilio client for WhatsApp
        self.twilio_client = Client(os.environ['account_sid'], os.environ['auth_token'])
        
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
    
    def send_whatsapp_message(self, to, message):
        message = self.twilio_client.messages.create(
            body=message,
            from_='whatsapp:+14155238886',  # Replace with your Twilio WhatsApp number
            to=f'{to}'
        )
        return message.sid
    
    def send_product_notification(self, cust_id, product_data):
        # 1. Generate notification message with Gemini
        notification_message = self.generate_notification(product_data)

        # 2. Get customer's WhatsApp number
        phone_number = self.get_customer_phone_number(cust_id)  # Replace with your logic

        # 3. Send the notification through WhatsApp
        if phone_number:
            self.send_whatsapp_message(phone_number, notification_message)
    
    def process_incoming_message(self, from_number, message_body):
        # 1. Identify the customer (you might need to store phone numbers and cust_ids)
        cust_id = self.get_customer_id_from_number(from_number)  # Replace with your logic
        if not cust_id:
            # Handle case where number is not recognized
            return "Please create an account to start chatting!" 

        # 2. Get customer's recent scans
        scan_data = self.get_recent_scans(cust_id)

        # 3. Prepare context for Gemini (include chat history if needed)
        # For simplicity, we'll just use recent scans for now
        #context = f"Customer's recent scans:\n{scan_data}\n\n"
        context = f"Customer says: {message_body} You need to help the customer by providing adequate product support that will solve their issues. Limit yourself to less than 1600 characters"

        # 4. Start a new chat session for each customer interaction
        chat_session = self.model.start_chat(history=[])
        response = chat_session.send_message(context)

        # 5. Send the response back through WhatsApp
        self.send_whatsapp_message(from_number, response.text)

    # Placeholder functions for managing customer data
    def get_customer_id_from_number(self, from_number):
        # Replace with your logic to fetch cust_id based on phone number
        # Example:
        # customer = self.db["Customer"].find_one({"phone_number": from_number})
        # return customer.get("cust_id") 
        return "c786ddc5-b6f6-4fda-ab67-9337874a9594" # Placeholder

    def get_customer_phone_number(self, cust_id):
        # Replace with your logic to fetch phone number based on cust_id
        # Example:
        # customer = self.db["Customer"].find_one({"cust_id": cust_id})
        # return customer.get("phone_number")
        return "+1234567890" # Placeholder 

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