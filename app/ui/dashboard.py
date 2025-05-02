import streamlit as st
import pandas as pd
import io
from pathlib import Path
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.append(str(Path(__file__).parent.parent.parent))
from app.core.validator import AccountValidator

MOCK_API_URL = "http://localhost:5000/validate"
CHUNK_SIZE = 200  # Optimal chunk size for validation
MAX_WORKERS = 6   # Balanced concurrency

def validate_chunk(chunk, validator, api_url):
    """Validate a chunk of accounts with proper API URL"""
    return validator.validate_bulk(chunk.to_dict("records"), api_url)

def show_dashboard():
    st.set_page_config(page_title="PesaVerify", layout="wide")
    
    st.title("🔍 PesaVerify - Bulk Account Validation")
    
    # File Upload Section
    uploaded_file = st.file_uploader(
        "Upload payment batch (CSV/JSON)", 
        type=["csv", "json"]
    )
    
    if uploaded_file:
        try:
            # Read file
            with st.spinner("Analyzing file..."):
                file_bytes = uploaded_file.read()
                try:
                    data = pd.read_csv(io.BytesIO(file_bytes))
                except:
                    data = pd.read_json(io.BytesIO(file_bytes))
                
                st.success(f"✅ Loaded {len(data)} accounts")

            if st.button("Validate Accounts"):
                # Setup validation
                progress_bar = st.progress(0)
                status_text = st.empty()
                validator = AccountValidator(max_workers=MAX_WORKERS)
                results = []
                
                # Process in chunks
                chunks = [data.iloc[i:i + CHUNK_SIZE] 
                         for i in range(0, len(data), CHUNK_SIZE)]
                
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    futures = []
                    for chunk in chunks:
                        futures.append(executor.submit(
                            validate_chunk, 
                            chunk, 
                            validator,
                            MOCK_API_URL  # Pass API URL here
                        ))
                    
                    for i, future in enumerate(as_completed(futures)):
                        results.extend(future.result())
                        progress = min((i + 1) / len(chunks), 1.0)
                        progress_bar.progress(progress)
                        status_text.text(f"Processed {min((i + 1) * CHUNK_SIZE, len(data))}/{len(data)}")
                
                # Process results
                data["is_valid"] = [r["valid"] for r in results]
                data["reason"] = [r["reason"] for r in results]
                
                # Display results
                st.success("Validation Complete!")
                st.dataframe(data)

        except Exception as e:
            st.error(f"Validation failed: {str(e)}")

if __name__ == "__main__":
    show_dashboard()