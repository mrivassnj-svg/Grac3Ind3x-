import gradio as gr
import json
import os
from utils.ai_core import AnalyzeSentiment, AdaptiveRefinementEngine
from utils.safety import CrisisDetector
from database.database import log_entry  # Using our high-performance SQLite logic

# Load Adaptive Pillar resources
with open("data/resources.json", "r") as f:
    RESOURCES = json.load(f)

# Initialize the Adaptive ML Engine
adaptive_engine = AdaptiveRefinementEngine()

def grace_engine_interface(user_input, user_uuid="STUB_USER_001"):
    """
    Core Pipeline: Executes the G.R.A.C.E. methodology.
    """
    # 1. PILLAR: RESPONSE (Sentiment & NLP)
    sentiment_report = AnalyzeSentiment(user_input)
    
    # 2. PILLAR: CARE (Immediate Crisis Detection)
    risk_level, safety_msg = CrisisDetector.evaluate(user_input)
    
    # 3. PILLAR: ADAPTIVE (Resource Recommendation)
    # If risk is critical, prioritize hotlines; otherwise, use ML-selected resource
    if risk_level == "🔴 CRITICAL":
        resource_pathway = f"**Emergency Protocol:** Contact {RESOURCES['crisis_contacts']['national_hotline']}"
    else:
        best_type = adaptive_engine.get_best_resource()
        # Fetch a random prompt from the recommended category
        if best_type == "grounding":
            resource_pathway = f"**Adaptive Suggestion:** {random.choice(RESOURCES['grounding_exercises'])}"
        else:
            resource_pathway = f"**Adaptive Suggestion:** {random.choice(RESOURCES['adaptive_prompts'])}"

    # 4. PILLAR: ENGINE (High-Performance Persistence)
    # Mapping dummy values for PHQ-9 and Velocity for this session
    mock_phq9 = 18 if risk_level == "🔴 CRITICAL" else 8
    mock_velocity = -2.5 # Simulated decline
    
    log_entry(
        user_uuid=user_uuid,
        score=mock_phq9,
        q9=1 if "suicide" in user_input.lower() else 0,
        sentiment=0.8 if "High" in sentiment_report else 0.2,
        velocity=mock_velocity,
        metadata={"raw_length": len(user_input), "resource_deployed": resource_pathway}
    )

    return (
        risk_level, 
        sentiment_report, 
        f"{safety_msg}\n\n---\n\n{resource_pathway}"
    )

# --- GRADIO INTERFACE DESIGN ---
with gr.Blocks(title="G.R.A.C.E. Systems", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📊 G.R.A.C.E. SYSTEMS")
    gr.Markdown("### Guided Response & Adaptive Care Engine | Clinician Oversight")
    
    with gr.Row():
        with gr.Column(scale=2):
            inp = gr.Textbox(
                label="Clinical Narrative / Patient Input",
                placeholder="Type session notes or patient reflections here...",
                lines=8
            )
            btn = gr.Button("🚀 Execute G.R.A.C.E. Analysis", variant="primary")
            
        with gr.Column(scale=1):
            out_risk = gr.Label(label="Safety Tier")
            out_sent = gr.Textbox(label="Sentiment Intelligence", interactive=False)

    gr.Markdown("---")
    gr.Markdown("### 🛠️ Intervention Pathway")
    out_alert = gr.Markdown(value="*Awaiting input analysis...*")
    
    btn.click(
        grace_engine_interface, 
        inputs=inp, 
        outputs=[out_risk, out_sent, out_alert]
    )

if __name__ == "__main__":
    # Ensure database exists before launch
    from database.database import init_db
    init_db()
    demo.launch()
