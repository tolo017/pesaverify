# File: generate_test_accounts.py
import pandas as pd
import random
from faker import Faker

def generate_test_accounts(num_accounts=1000):
    fake = Faker()
    banks = ['01', '02', '03', '04', '05']
    
    data = []
    for _ in range(num_accounts):
        data.append({
            'account_number': fake.bban(),
            'bank_code': random.choice(banks),
            'account_name': fake.name(),
            'amount': round(random.uniform(100, 10000), 2),
            'reference': fake.uuid4()
        })
    
    df = pd.DataFrame(data)
    df.to_csv('test_accounts.csv', index=False)
    print(f"Generated {num_accounts} test accounts in test_accounts.csv")

if __name__ == "__main__":
    generate_test_accounts(100)  # Generates 5000 test accounts