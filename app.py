import gradio as gr
from scoring import detect_crisis, calculate_slope, get_clinical_verdict, WEIGHTS, WORD_SCORES

init_db()

def process_submission(user_id, *inputs):
    responses = {f"Q{i+1}": val for i, val in enumerate(inputs[:10])}
    fill_word = inputs[10]
    
    # 1. Base Scoring
    weighted = sum(responses[q] * WEIGHTS.get(q, 1.0) for q in responses)
    final_score = weighted + WORD_SCORES.get(fill_word.lower(), 0)
    
    # 2. Clinical Safety Check
    is_crisis = detect_crisis(fill_word)
    history = save_entry_and_get_history(user_id, final_score, responses)
    slope = calculate_slope(final_score, history)
    
    severity, msg = get_clinical_verdict(final_score, slope, is_crisis)
    
    # 3. Escalation
    if severity != "STABLE":
        # In a real app, this triggers an SMTP/SMS alert to a doctor
        log_clinician_alert(user_id, severity)
        
    return f"VERDICT: {msg}\nSTABILITY INDEX: {final_score:.2f}\nSLOPE: {slope:.2f}"

# --- THEME (Protective Angelic Inquisition) ---
custom_css = """
.gradio-container { background: #f4f1ea; border: 5px solid #d4af37; }
.gr-header { color: #8b0000; font-family: 'serif'; text-align: center; }
"""

with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("# 🪽 THE PROTECTIVE WATCH 🪽")
    gr.Markdown("### Private Secure Portal for Psychological Monitoring")
    
    with gr.Row():
        u_id = gr.Textbox(label="Authorized Patient ID")
        f_word = gr.Textbox(label="Current Reflection (Fill Word)")

    sliders = [gr.Slider(-2, 2, step=1, label=f"Metric {i+1}") for i in range(10)]
    
    btn = gr.Button("SUBMIT TO THE ARCHIVE")
    output = gr.Textbox(label="System Status / Guidance")

    btn.click(process_submission, inputs=[u_id] + sliders + [f_word], outputs=output)

demo.launch(share=True)
