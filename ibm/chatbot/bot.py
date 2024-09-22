# bot.py

import re
from collections import deque
from chatbot.settings import Settings
from chatbot.llm import LLM
from chatbot.prompts import react_prompt, search_prompt
from chatbot.cart_database import CartDatabase
from chatbot.catalog_database import CatalogDatabase

class Chatbot:
    def __init__(self, 
            business: str, 
            business_description: str, 
            products: list[dict],
            ibm_api_key: str,
            ibm_project_id: str,
            model_id: str = "mistralai/mistral-large",
            history_limit=3
        ):
        self.business = business
        self.business_description = business_description
        self.catalog_db = CatalogDatabase(products)
        self.cart_db = CartDatabase()
        self.llm = LLM(ibm_api_key, ibm_project_id, model_id)
        self.history_limit = history_limit  # Maximum number of turns to keep in history
        self.conversation_history = deque(maxlen=history_limit * 2)  # Each turn has user and bot message

    def search_products(self, query: str) -> str:
        # Include the catalog data in the prompt and ask LLM to find matching products
        catalog_prompt = self.catalog_db.get_catalog_prompt()
        prompt = search_prompt.format(
            catalog=catalog_prompt,
            query=query
        )
        response = self.llm.generate_text(prompt)

        # The LLM returns the matching products as a string
        return response.strip()

    def update_cart(self, action_input: str) -> str:
        # Parse the action input to determine 'Add' or 'Remove' and the products
        action_input = action_input.strip('"').strip()
        try:
            operation, products_str = action_input.split(' ', 1)
        except ValueError:
            return "Invalid cart input format. Please specify the operation and products."

        operation = operation.lower()

        if operation not in ["add", "remove"]:
            return "Invalid cart operation. Use 'Add' or 'Remove'."

        # Split the products string by commas to get individual product entries
        product_entries = [p.strip() for p in products_str.split(',')]

        messages = []

        for entry in product_entries:
            # Expecting format: quantity x product_name
            try:
                # Split each entry into quantity and product name
                quantity_part, product_name = entry.split(' x ', 1)
                quantity = int(quantity_part.strip())
                product_name = product_name.strip()

                if operation == "add":
                    result = self.cart_db.add_product(product_name, quantity)
                elif operation == "remove":
                    result = self.cart_db.remove_product(product_name)
                messages.append(f"{product_name}: {result}")
            except ValueError:
                messages.append(f"Invalid format for entry: '{entry}'. Expected 'quantity x product_name'.")

        return "\n".join(messages)


    def finalize_order(self) -> str:
        # Simulate order finalization
        cart_items = self.cart_db.get_cart()
        if cart_items:
            return "Your order has been finalized and placed. Thank you for shopping with us!"
        else:
            return "Your cart is empty. Cannot finalize the order."

    def generate_response(self, action_input: str) -> str:
        # Simply return the action input as the response to the user
        return action_input.strip('"')

    def build_conversation_history(self):
        # Build conversation history string from the deque
        return "\n".join(self.conversation_history)

    def determine_action(self, message: str, processing_steps: list = []) -> tuple:

        # Build the prompt with limited conversation history
        conversation_history = self.build_conversation_history()

        # Build the prompt including the conversation history and any current processing steps
        prompt = react_prompt.format(
            business=self.business,
            business_description=self.business_description,
            conversation_history=conversation_history,
            user_message=message
        )

        if processing_steps:
            prompt += "\n" + "\n".join(processing_steps)

        prompt += "\nThought:"
        response = self.llm.generate_text(prompt)

        # Extract the action, action input, thought, and observation using regex
        thought_pattern = r'\s*(.*?)\s*Action:'
        action_pattern = r'Action:\s*(.*?)\n'
        action_input_pattern = r'Action Input:\s*(.*?)(?:\n|$)'

        action_match = re.search(action_pattern, response, re.DOTALL)
        action_input_match = re.search(action_input_pattern, response, re.DOTALL)
        thought_match = re.search(thought_pattern, response, re.DOTALL)

        action = action_match.group(1).strip() if action_match else None
        action_input = action_input_match.group(1).strip() if action_input_match else None
        thought = thought_match.group(1).strip() if thought_match else None

        print("Thought:", thought)
        print("Action:", action)
        print("Action Input:", action_input)

        return action, action_input, thought

    def get_response(self, message: str) -> str:
        action, action_input, thought = self.determine_action(message)

        # Keep all ReAct steps during current processing
        current_processing_steps = []

        # Process actions in a loop until a response is ready to be sent to the user
        while True:

            if thought:
                current_processing_steps.append(f"Thought: {thought}")

            if action == 'search':
                observation = self.search_products(action_input)

            elif action == 'cart':
                observation = self.update_cart(action_input)
                
            elif action == 'finish':
                response = self.finalize_order()
                break
            
            elif action == 'response':
                response = action_input
                break                
            
            else:
                response_text = "I'm sorry, I didn't understand that. Could you please rephrase?"
                self.conversation_history.append(f"Bot Response: {response_text}")
                return response_text
            
            print(f"Observation: {observation}\n\n")
            current_processing_steps.append(f"Action: {action}\nAction Input: {action_input}\nObservation: {observation}")

            # Determine the next action based on the observation
            action, action_input, thought = self.determine_action(message, current_processing_steps)
                        
        self.conversation_history.append(f"User Message: {message}")
        self.conversation_history.append(f"Bot Response: {response}")

        return response

    def start_chat(self):
        print(f"{self.business} virtual sales assistant: Hello! How can I assist you today?")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                print(f"{self.business} virtual sales assistant: Thank you for visiting. Have a great day!")
                break
            response = self.get_response(user_input)
            print(f"{self.business} virutal sales assistant: {response}")

# Example usage:
if __name__ == "__main__":
    chatbot = Chatbot(
        business="Seven-Eleven Grocery Store",
        business_description="A grocery store selling a variety of products.",
        products=[
            {"name": "AA Batteries Pack of 4", "price": 5.99},
            {"name": "AAA Batteries Pack of 6", "price": 7.99},
            {"name": "Free-range Eggs Dozen Pack", "price": 3.99},
            {"name": "Whole Milk Gallon", "price": 2.99},
            {"name": "Skim Milk Gallon", "price": 2.99},
            {"name": "Organic Orange Juice", "price": 4.99},
            {"name": "Brand A Orange Juice", "price": 3.49},
            {"name": "Brand B Orange Juice", "price": 3.79},
            {"name": "Vegan Cheddar Cheese", "price": 5.49},
            {"name": "Vegan Mozzarella Cheese", "price": 5.49},
        ],
        history_limit=5  # Keep the last 5 user-bot exchanges
    )
    chatbot.start_chat()
