from faker import Faker
import random
import pandas as pd

# Initialize Faker with Swiss locales
fake = Faker(['de_CH', 'en_GB', 'fr_CH', 'it_CH', 'en_US'])
nationalities = ["Swiss", "German", "Italian", "French", "British", "American"]
unique_names = set()
unique_addresses = set()
client_id = 0
# Function to clean special characters and ensure proper encoding
def clean_text(text):
    try:
        return text.encode("utf-8", errors="ignore").decode("utf-8")  # Ignore problematic characters
    except Exception:
        return "Invalid Text"

# Function to generate a single client
def generate_client():
     global client_id 
     while True:
        # Generate name and address
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"
        address = fake.address().replace("\n", ", ")
        
        # Ensure uniqueness
        if full_name not in unique_names and address not in unique_addresses:
            client_id += 1 
            unique_names.add(full_name)
            unique_addresses.add(address)
            email = f"{clean_text(first_name).lower()}.{clean_text(last_name).lower()}@gmail.com"
    
            return {
                'client_id': client_id,
                'first name': clean_text(first_name),
                'last name': clean_text(last_name),
                'email': email,
                'address': clean_text(fake.address().replace("\n", ", ")),  
                'phone': clean_text(f"{fake.phone_number()}"),
                'nationality': random.choices(nationalities, k=1)[0],  # Directly return the string
                'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=80)
            }

# Generate 3000 clients
clients = [generate_client() for _ in range(3000)]

# Convert to DataFrame
clients_df = pd.DataFrame(clients)

# Save to CSV
clients_df.to_csv("clients_table.csv", index=False, encoding="utf-8")
print("Client data saved to 'clients_table.csv'")
