import gradio as gr
from utils.ai_core import AnalyzeSentiment
from utils.safety import CrisisDetector

def grace_engine_interface(user_input):
    # Pillar: Response (Sentiment Analysis)
    sentiment = AnalyzeSentiment(user_input)
    
    # Pillar: Care (Safety Detection)
    risk_level, alert = CrisisDetector.evaluate(user_input)
    
    # Pillar: Adaptive (Resource Mapping)
    # logic to pull from resources.json would go here
    
    return f"Risk Level: {risk_level}", f"AI Sentiment: {sentiment}", alert

with gr.Blocks(title="G.R.A.C.E. Systems") as demo:
    gr.Markdown("# G.R.A.C.E. Systems Engine")
    with gr.Row():
        inp = gr.Textbox(placeholder="Enter patient narrative or session notes...")
        out_risk = gr.Label(label="Risk Assessment")
    
    out_sent = gr.Textbox(label="Sentiment Analysis")
    out_alert = gr.Markdown()
    
    btn = gr.Button("Analyze Entry")
    btn.click(grace_engine_interface, inputs=inp, outputs=[out_risk, out_sent, out_alert])
if __name__ == "__main__":
    demo.launch()
