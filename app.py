import gradio as gr
import requests

API_URL = "http://localhost:8000/process_entry"

def grace_engine_interface(user_id, q1, q2, q3, q4, q5, q6, q7, q8, q9, narrative):
    # Prepare the payload for the Central API
    payload = {
        "user_id": user_id,
        "responses": {f"Q{i+1}": v for i, v in enumerate([q1, q2, q3, q4, q5, q6, q7, q8, q9])},
        "fill_word": narrative
    }
    
    # Send to the API
    response = requests.post(API_URL, json=payload)
    data = response.json()
    
    return data["risk_level"], data["mood_label"], data["intervention"]
