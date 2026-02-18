import gradio as gr
from utils.ai_core import AnalyzeSentiment, AdaptiveRefinementEngine
from utils.safety import CrisisDetector
from scoring import score_entry # <--- CRITICAL FIX: Linking your scoring logic

def grace_engine_interface(user_input, q1, q2, q3, q4, q5, q6, q7, q8, q9):
    # 1. Compile PHQ-9 Responses
    responses = {f"Q{i+1}": val for i, val in enumerate([q1, q2, q3, q4, q5, q6, q7, q8, q9])}
    
    # 2. RUN YOUR SCORING LOGIC (Pillar: Response)
    raw, weight, final, mood_class = score_entry(responses, user_input)
    
    # 3. RUN SAFETY CHECK (Pillar: Care)
    risk_level, safety_msg = CrisisDetector.evaluate(user_input, q9_score=q9)
    
    # 4. OVERRIDE Logic
    # If the score is high (Severe), force the risk to Critical even if keywords are missing
    if final >= 20:
        risk_level = "🔴 CRITICAL"
        safety_msg = "### ALERT: Severe PHQ-9 Score (20+). Immediate Triage Required."

    return risk_level, f"Mood: {mood_class} (Score: {final})", safety_msg

# UI Setup with sliders for the 9 questions
with gr.Blocks() as demo:
    gr.Markdown("# G.R.A.C.E. Systems Engine")
    with gr.Row():
        with gr.Column():
            inp = gr.Textbox(label="Session Narrative")
            # Adding sliders to feed the scoring.py logic
            qs = [gr.Slider(0, 3, step=1, label=f"PHQ-9 Q{i+1}") for i in range(9)]
        with gr.Column():
            out_risk = gr.Label(label="Safety Tier")
            out_mood = gr.Textbox(label="Clinical Verdict")
            out_path = gr.Markdown()
            
    btn = gr.Button("Analyze")
    btn.click(grace_engine_interface, inputs=[inp] + qs, outputs=[out_risk, out_mood, out_path])
