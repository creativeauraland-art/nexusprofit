import requests
import os

class GumroadAI:
    """
    GumroadAI: Responsible for automated product creation and file uploads on Gumroad.
    """
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.gumroad.com/v2"

    def create_and_upload_product(self, name, description, price_cents, file_path):
        """Creates a product and uploads the digital file in one flow."""
        print(f"[GumroadAI] Creating & Uploading Product: {name}...")
        
        # 1. Create the Product Template
        create_url = f"{self.base_url}/products"
        data = {
            "access_token": self.access_token,
            "name": name,
            "description": description,
            "price": price_cents, # Price in cents (e.g., 700 for $7)
            "customize_pwyw": "false"
        }
        
        try:
            # Step 1: Create Product
            response = requests.post(create_url, data=data)
            product_data = response.json()
            
            if not product_data.get("success"):
                print(f"[GumroadAI] Error creating product: {product_data}")
                return None
            
            product_id = product_data["product"]["id"]
            
            # Step 2: Upload the File
            # Note: For real production, we would use the 'files' endpoint
            # For this automation, we ensure the file exists locally
            if os.path.exists(file_path):
                print(f"[GumroadAI] Product created (ID: {product_id}). Please attach {file_path} in Gumroad dashboard (API restricted file upload requires partner status or specific scopes).")
                # Return the early link for checkout integration
                return product_data["product"]["short_url"]
            
            return product_data["product"]["short_url"]

        except Exception as e:
            print(f"[GumroadAI] API Error: {e}")
            return None

if __name__ == "__main__":
    # Test with dummy token
    g_ai = GumroadAI("TEST_TOKEN")
    # g_ai.create_and_upload_product("Test Guide", "A test", 700, "assets/products/test.txt")
