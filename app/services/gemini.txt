import os
import google.generativeai as genai
from dotenv import load_dotenv

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

    def send_message(self, customer_details: dict):
        message = f"""I have a customer profile with the following details:

    ID: {customer_details.get('ID', 'N/A')}
    Year of Birth: {customer_details.get('Year_Birth', 'N/A')}
    Education: {customer_details.get('Education', 'N/A')}
    Marital Status: {customer_details.get('Marital_Status', 'N/A')}
    Income: {customer_details.get('Income', 'N/A')}
    Number of Children: {customer_details.get('Kidhome', 'N/A')}
    Number of Teenagers: {customer_details.get('Teenhome', 'N/A')}
    Date of Enrollment: {customer_details.get('Dt_Customer', 'N/A')}
    Recency of Last Purchase: {customer_details.get('Recency', 'N/A')} days
    Amount spent on Wines: {customer_details.get('MntWines', 'N/A')}
    Amount spent on Fruits: {customer_details.get('MntFruits', 'N/A')}
    Amount spent on Meat: {customer_details.get('MntMeatProducts', 'N/A')}
    Amount spent on Fish: {customer_details.get('MntFishProducts', 'N/A')}
    Amount spent on Sweets: {customer_details.get('MntSweetProducts', 'N/A')}
    Amount spent on Gold: {customer_details.get('MntGoldProds', 'N/A')}
    Number of Deals Purchases: {customer_details.get('NumDealsPurchases', 'N/A')}
    Web Purchases: {customer_details.get('NumWebPurchases', 'N/A')}
    Catalog Purchases: {customer_details.get('NumCatalogPurchases', 'N/A')}
    Store Purchases: {customer_details.get('NumStorePurchases', 'N/A')}
    Web Visits Last Month: {customer_details.get('NumWebVisitsMonth', 'N/A')}
    Responded to Last Campaign: {"Yes" if customer_details.get('Response') == 1 else "No"}
    
    Based on this data, generate one personalized mobile notification. Mention:

    Their long-term relationship with the company (date of enrollment).
    Their purchasing patterns implying what platform they usually shop on(web, catalog, store purchases).
    Specific products they have bought frequently 
    Whether they responded to the last campaign.
    Encourage them to check the app and explore personalized offers.

Keep it concise and engaging not longer than 20 words, aiming to prompt action.

"""     
        response = self.chat_session.send_message(message)
        return response.text
       
    def get_history(self):
        return self.chat_session.history

# Usage example:
# if __name__ == "__main__":
#     chatbot = GeminiChatBot()
    
#     # Send a message and get response
#     response = chatbot.send_message("Hello, how are you?")
#     print("Bot:", response)
    
#     # Get chat history
#     history = chatbot.get_history()
#     print("Chat History:", history)