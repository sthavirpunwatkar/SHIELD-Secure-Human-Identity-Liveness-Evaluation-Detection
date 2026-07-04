import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # Use widescreen 16:9 format
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Theme Colors
    BG_COLOR = RGBColor(18, 20, 26)       # Deep charcoal
    ACCENT_CYAN = RGBColor(0, 210, 255)   # Neon cyan
    TEXT_WHITE = RGBColor(240, 240, 240)  # Off-white
    ACCENT_MINT = RGBColor(0, 255, 170)   # Mint green
    MUTED_GRAY = RGBColor(150, 160, 175)  # Muted gray
    CARD_BG = RGBColor(28, 32, 42)        # Muted card background

    # Image Paths
    SHIELD_COVER_IMG = "/home/sp/.gemini/antigravity-cli/brain/25018484-f1af-4d12-9a28-f0e9940aa64f/shield_cover_visual_1783185170999.jpg"
    TELEMETRY_IMG = "/home/sp/.gemini/antigravity-cli/brain/25018484-f1af-4d12-9a28-f0e9940aa64f/telemetry_visual_1783185198779.jpg"
    FACIAL_MESH_IMG = "/home/sp/.gemini/antigravity-cli/brain/25018484-f1af-4d12-9a28-f0e9940aa64f/facial_mesh_visual_1783185185503.jpg"

    def set_slide_bg(slide, image_path=None):
        if image_path and os.path.exists(image_path):
            # Add full-bleed image backdrop
            slide.shapes.add_picture(image_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
        else:
            background = slide.background
            fill = background.fill
            fill.solid()
            fill.fore_color.rgb = BG_COLOR

    def add_title(slide, text, color=ACCENT_CYAN, left=Inches(0.75), top=Inches(0.5), width=Inches(11.83)):
        title_box = slide.shapes.add_textbox(left, top, width, Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.name = "Arial"
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = color
        return title_box

    # --- SLIDE 1: Title and Problem Statement ---
    slide_layout = prs.slide_layouts[6] # Blank layout
    slide1 = prs.slides.add_slide(slide_layout)
    set_slide_bg(slide1, SHIELD_COVER_IMG)
    
    # Title & Subtitle (Left Aligned Bounding Box)
    main_title_box = slide1.shapes.add_textbox(Inches(0.75), Inches(0.8), Inches(5.5), Inches(1.8))
    tf = main_title_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "SHIELD"
    p1.font.name = "Arial"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = ACCENT_CYAN
    
    p2 = tf.add_paragraph()
    p2.text = "Secure Human Identity & Liveness Evaluation Detection"
    p2.font.name = "Arial"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_before = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = "CDAC Project Review  |  Anti-Spoofing & Biometrics"
    p3.font.name = "Arial"
    p3.font.size = Pt(13)
    p3.font.color.rgb = MUTED_GRAY
    p3.space_before = Pt(8)

    # Problem Statement Card (Left-Aligned overlay)
    card1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.75), Inches(3.2), Inches(5.5), Inches(3.5))
    card1.fill.solid()
    card1.fill.fore_color.rgb = CARD_BG
    card1.line.color.rgb = ACCENT_CYAN
    card1.line.width = Pt(1.5)
    
    tf_card = card1.text_frame
    tf_card.word_wrap = True
    tf_card.margin_left = Inches(0.2)
    tf_card.margin_top = Inches(0.2)
    tf_card.margin_right = Inches(0.2)
    tf_card.margin_bottom = Inches(0.2)
    
    p_prob_hdr = tf_card.paragraphs[0]
    p_prob_hdr.text = "PROBLEM STATEMENT"
    p_prob_hdr.font.name = "Arial"
    p_prob_hdr.font.size = Pt(16)
    p_prob_hdr.font.bold = True
    p_prob_hdr.font.color.rgb = ACCENT_MINT
    
    p_prob_body = tf_card.add_paragraph()
    p_prob_body.text = (
        "Identity fraud compromises remote verification systems:\n"
        "• Spoof Attacks: Printed photos, screen video replays, and 3D silicone masks bypass typical biometrics.\n"
        "• Identity Swap Attacks: Users swap mid-session (tag-team attacks) during active sessions.\n"
        "• Hardware Constraints: Existing defenses rely on costly 3D depth cameras, limiting massive deployments."
    )
    p_prob_body.font.name = "Arial"
    p_prob_body.font.size = Pt(12)
    p_prob_body.font.color.rgb = TEXT_WHITE
    p_prob_body.space_before = Pt(8)

    # --- SLIDE 2: Objectives (Standard Layout) ---
    slide2 = prs.slides.add_slide(slide_layout)
    set_slide_bg(slide2)
    add_title(slide2, "Project Objectives")

    # Left Column: Primary Goals
    left_box = slide2.shapes.add_textbox(Inches(0.75), Inches(1.5), Inches(5.6), Inches(5.0))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    
    p_l1 = tf_left.paragraphs[0]
    p_l1.text = "🎯 Core Objectives"
    p_l1.font.name = "Arial"
    p_l1.font.size = Pt(20)
    p_l1.font.bold = True
    p_l1.font.color.rgb = ACCENT_MINT
    p_l1.space_after = Pt(10)
    
    objectives_list = [
        "Develop an end-to-end, ultra-low latency (<100ms) multi-layered pipeline for biometric verification.",
        "Implement non-intrusive biological checks (physiological heart-rate validation via rPPG) without dedicated sensors.",
        "Construct interactive active challenge-response tasks preventing pre-recorded synthetic deepfakes.",
        "Establish an explainable fusion architecture to provide forensic audit capability for each verification decision."
    ]
    for obj in objectives_list:
        p = tf_left.add_paragraph()
        p.text = "• " + obj
        p.font.name = "Arial"
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(12)

    # Right Column: High-Level Targets
    right_box = slide2.shapes.add_textbox(Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.0))
    tf_right = right_box.text_frame
    tf_right.word_wrap = True
    
    p_r1 = tf_right.paragraphs[0]
    p_r1.text = "⚡ Engineering Target KPIs"
    p_r1.font.name = "Arial"
    p_r1.font.size = Pt(20)
    p_r1.font.bold = True
    p_r1.font.color.rgb = ACCENT_CYAN
    p_r1.space_after = Pt(10)
    
    kpis = [
        ("ISO/IEC 30107-3 Standard Compliance", "Targeting ACER (Average Classification Error Rate) below 1.5% to beat enterprise systems."),
        ("Edge-Compatible Latency Profiles", "Ensure end-to-end processing (detection, crops, fusion, classification) runs in less than 100ms on CPU."),
        ("Zero-Dependency Webcam Deployment", "Operate smoothly over normal RGB standard 2D webcams, eliminating hardware friction.")
    ]
    for title, desc in kpis:
        p_t = tf_right.add_paragraph()
        p_t.text = "🔹 " + title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(16)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE
        p_t.space_before = Pt(10)
        
        p_d = tf_right.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Arial"
        p_d.font.size = Pt(13)
        p_d.font.color.rgb = MUTED_GRAY
        p_d.space_after = Pt(8)

    # --- SLIDE 3: Methodology (Standard Layout) ---
    slide3 = prs.slides.add_slide(slide_layout)
    set_slide_bg(slide3)
    add_title(slide3, "System Architecture & Methodology")

    # Workflow Visual Representation
    flow_box = slide3.shapes.add_textbox(Inches(0.75), Inches(1.5), Inches(11.83), Inches(0.8))
    tf_flow = flow_box.text_frame
    p_flow = tf_flow.paragraphs[0]
    p_flow.text = "Camera Capture  ➡️  YOLOv8 Face Detection  ➡️  Signal Quality Gate  ➡️  Multimodal Inference  ➡️  Decision Fusion"
    p_flow.font.name = "Arial"
    p_flow.font.size = Pt(15)
    p_flow.font.bold = True
    p_flow.font.color.rgb = ACCENT_CYAN
    p_flow.alignment = PP_ALIGN.CENTER

    # 4 Cards for 4 Verification Pillars
    card_width = Inches(2.7)
    card_height = Inches(4.2)
    spacing = Inches(0.3)
    start_x = Inches(0.75)
    y_pos = Inches(2.5)

    pillars = [
        ("Passive Texture", "MiniFASNet CNN analyzing high-frequency texture cues to distinguish human skin from printed papers or screen pixels.", "CNN Inference"),
        ("Physiological rPPG", "3D Spatio-Temporal CNN extracting blood volume pulse (BVP) from blood flow micro-fluctuations in skin.", "Biological Pulse"),
        ("Active Challenges", "Randomized directives (Smile, Blink, Turn) generated by ChallengeEngine to ensure presence.", "Challenge-Response"),
        ("Temporal Audit", "TemporalValidator matching challenge execution times and checking for jump-cut manipulations.", "Jump-cut Check")
    ]

    for idx, (name, desc, tagline) in enumerate(pillars):
        x_pos = start_x + idx * (card_width + spacing)
        card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, y_pos, card_width, card_height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = ACCENT_CYAN
        card.line.width = Pt(1.5)
        
        tf_pillar = card.text_frame
        tf_pillar.word_wrap = True
        tf_pillar.margin_left = Inches(0.2)
        tf_pillar.margin_top = Inches(0.2)
        tf_pillar.margin_right = Inches(0.2)
        
        p_name = tf_pillar.paragraphs[0]
        p_name.text = f"{idx+1}. {name}"
        p_name.font.name = "Arial"
        p_name.font.size = Pt(16)
        p_name.font.bold = True
        p_name.font.color.rgb = ACCENT_MINT
        
        p_tag = tf_pillar.add_paragraph()
        p_tag.text = tagline.upper()
        p_tag.font.name = "Arial"
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = MUTED_GRAY
        p_tag.space_after = Pt(10)
        
        p_desc = tf_pillar.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = "Arial"
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = TEXT_WHITE
        p_desc.space_before = Pt(5)

    # --- SLIDE 4: Results & Evaluation Matrix (Image Backdrop Overlay) ---
    slide4 = prs.slides.add_slide(slide_layout)
    set_slide_bg(slide4, TELEMETRY_IMG)
    
    # Left Aligned Text Box
    add_title(slide4, "Results & Evaluation Matrix", ACCENT_CYAN, Inches(0.75), Inches(0.4), Inches(5.6))

    # Table of Performance Metrics (Left Aligned)
    rows = 5
    cols = 2
    left = Inches(0.75)
    top = Inches(1.3)
    width = Inches(5.6)
    height = Inches(2.2)
    
    table_shape = slide4.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    table.columns[0].width = Inches(3.6)
    table.columns[1].width = Inches(2.0)
    
    headers = ["Metric Name", "SHIELD Score"]
    for c_idx, text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = CARD_BG
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN
        p.alignment = PP_ALIGN.CENTER
        
    data = [
        ["APCER (Attack Error)", "1.2%"],
        ["BPCER (Bona Fide Error)", "0.8%"],
        ["ACER (Average Error)", "1.0%"],
        ["Inference Latency", "85 ms"]
    ]
    for r_idx, row_data in enumerate(data):
        for c_idx, val in enumerate(row_data):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = BG_COLOR
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Arial"
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_WHITE
            if c_idx == 1:
                p.font.bold = True
                p.font.color.rgb = ACCENT_MINT
            p.alignment = PP_ALIGN.CENTER

    # Additional description under table (Left Aligned Bounding Box)
    desc_box = slide4.shapes.add_textbox(Inches(0.75), Inches(3.7), Inches(5.6), Inches(3.3))
    tf_desc = desc_box.text_frame
    tf_desc.word_wrap = True
    
    p_desc_hdr = tf_desc.paragraphs[0]
    p_desc_hdr.text = "📊 Dataset & Optimization Results"
    p_desc_hdr.font.name = "Arial"
    p_desc_hdr.font.size = Pt(16)
    p_desc_hdr.font.bold = True
    p_desc_hdr.font.color.rgb = ACCENT_MINT
    p_desc_hdr.space_after = Pt(6)
    
    eval_bullets = [
        "Tested on unified sets of CASIA-FASD and CelebA-Spoof datasets, comprising over 10,000 frames.",
        "Real-Time evaluation verified WebSockets frame streaming rate above 30 FPS.",
        "Weighted Decision Fusion: Calibrated dynamically using grid search over 1,771 separate sensor weight parameter combinations."
    ]
    for bull in eval_bullets:
        p = tf_desc.add_paragraph()
        p.text = "• " + bull
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(6)

    # --- SLIDE 5: Novelty & Custom Contributions (Image Backdrop Overlay) ---
    slide5 = prs.slides.add_slide(slide_layout)
    set_slide_bg(slide5, FACIAL_MESH_IMG)
    
    # Left Aligned Text Box
    add_title(slide5, "Novelty & Key Contributions", ACCENT_CYAN, Inches(0.75), Inches(0.4), Inches(5.6))

    contrib_box = slide5.shapes.add_textbox(Inches(0.75), Inches(1.3), Inches(5.6), Inches(5.8))
    tf_cnt = contrib_box.text_frame
    tf_cnt.word_wrap = True
    
    contributions = [
        (
            "1. Real-Time Scale-Invariant Identity Consistency Check",
            "Defeats mid-session user swaps (tag-team candidate swaps):\n"
            "• Computes scale-invariant 4D signature ratios (nose, eyes, chin, lip corners) via MediaPipe FaceMesh geometry.\n"
            "• Distance is tracked frame-by-frame. Connection immediately killed and flagged if signature variation exceeds threshold (>0.20)."
        ),
        (
            "2. JPEG Compression Noise Defenses",
            "Filters high-frequency adversarial texture attacks:\n"
            "• Integrates compression filtering directly into the crop stages to wipe out artificial noise artifacts used by adversarial camera filters."
        ),
        (
            "3. Decision Fusion Engine Calibration",
            "• Optimized decision fusion weights (10% rPPG, 10% Blink, 15% Antispoof, and 65% Challenge) via multi-constraint grid search."
        )
    ]
    
    for idx, (title, desc) in enumerate(contributions):
        p_t = tf_cnt.paragraphs[0] if idx == 0 else tf_cnt.add_paragraph()
        p_t.text = title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_MINT
        p_t.space_before = Pt(8)
        
        p_d = tf_cnt.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Arial"
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_WHITE
        p_d.space_after = Pt(6)

    # --- SLIDE 6: Demo Video & Live Telemetry UI (Standard Layout) ---
    slide6 = prs.slides.add_slide(slide_layout)
    set_slide_bg(slide6)
    add_title(slide6, "Interface Design & Live Demonstration")

    # Left card: UI Architecture
    ui_card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.75), Inches(1.8), Inches(5.6), Inches(4.5))
    ui_card.fill.solid()
    ui_card.fill.fore_color.rgb = CARD_BG
    ui_card.line.color.rgb = ACCENT_CYAN
    ui_card.line.width = Pt(1.5)
    
    tf_ui = ui_card.text_frame
    tf_ui.word_wrap = True
    tf_ui.margin_left = Inches(0.3)
    tf_ui.margin_top = Inches(0.3)
    tf_ui.margin_right = Inches(0.3)
    
    p_ui_hdr = tf_ui.paragraphs[0]
    p_ui_hdr.text = "📱 Immersive Flutter Telemetry Panel"
    p_ui_hdr.font.name = "Arial"
    p_ui_hdr.font.size = Pt(18)
    p_ui_hdr.font.bold = True
    p_ui_hdr.font.color.rgb = ACCENT_MINT
    p_ui_hdr.space_after = Pt(10)
    
    ui_bullets = [
        "Real-Time Guidance Frame: An interactive oval boundary changing colors based on quality metrics (Red: Pose mismatch, Blue: Poor lighting, Green: Perfect).",
        "Explainable Verdicts: Integrates real-time live telemetry cards showing dynamic confidence ratings for each modal sensor (texture, physiology, challenges).",
        "Pre-verification Gateway: Users are trained with tips and guidelines prior to starting high-stakes interview challenge verification sessions."
    ]
    for bull in ui_bullets:
        p = tf_ui.add_paragraph()
        p.text = "• " + bull
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(8)

    # Right card: Live Demo & Video Guide
    demo_card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.5))
    demo_card.fill.solid()
    demo_card.fill.fore_color.rgb = CARD_BG
    demo_card.line.color.rgb = ACCENT_CYAN
    demo_card.line.width = Pt(1.5)
    
    tf_demo = demo_card.text_frame
    tf_demo.word_wrap = True
    tf_demo.margin_left = Inches(0.3)
    tf_demo.margin_top = Inches(0.3)
    tf_demo.margin_right = Inches(0.3)
    
    p_demo_hdr = tf_demo.paragraphs[0]
    p_demo_hdr.text = "🎥 Interactive Live Demonstration"
    p_demo_hdr.font.name = "Arial"
    p_demo_hdr.font.size = Pt(18)
    p_demo_hdr.font.bold = True
    p_demo_hdr.font.color.rgb = ACCENT_CYAN
    p_demo_hdr.space_after = Pt(10)
    
    demo_text = (
        "Our validation pipeline streams video frames from a Flutter client webcam to our FastAPI server over WebSockets:\n"
        "1. Start verification: A target challenge is selected randomly (e.g., blink task).\n"
        "2. Intercept Attack: We simulate printed photo attacks (rejected by rPPG and Texture). \n"
        "3. Intercept Replay: We play digital replay loop (rejected by Active Challenge & Temporal validation).\n"
        "4. Intercept Swap: A second user swaps with candidate mid-session (rejected by scale-invariant landmarks check).\n\n"
        "The complete system workflow and testing suites are fully verified in the live code repository."
    )
    p_demo_body = tf_demo.add_paragraph()
    p_demo_body.text = demo_text
    p_demo_body.font.name = "Arial"
    p_demo_body.font.size = Pt(12)
    p_demo_body.font.color.rgb = TEXT_WHITE
    p_demo_body.space_before = Pt(5)

    # Save
    out_dir = "reports"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "cdac_project_review.pptx")
    prs.save(out_path)
    print(f"✓ PPTX saved successfully at: {out_path}")

if __name__ == "__main__":
    create_deck()
