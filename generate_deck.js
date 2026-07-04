const pptxgen = require("pptxgenjs");

// Initialize presentation
let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9'; // 10" x 5.625"
pres.author = 'SHIELD Project Team';
pres.title = 'SHIELD CDAC Project Review';

// Design Token System
const COLORS = {
  bg:       "FFFFFF",   // White background
  primary:  "1F4E79",   // Dark navy — titles/sections
  accent:   "2E75B6",   // Mid-blue — headers, highlights
  body:     "2D2D2D",   // Near-black — body text
  muted:    "777777",   // Gray — citations, captions
  rule:     "CCCCCC",   // Light gray — divider lines
  highlight:"FFF2CC",   // Yellow — callout boxes
  lightBg:  "F0F4F8",   // Light blue-gray for boxes/tables
};

const FONTS = {
  face: "Arial",
  title: 24,            // Action title: 24 pt
  sectionHeader: 22,    // Slide section headers
  body: 20,             // Body bullets: 20 pt minimum font
  label: 16,            // Chart/diagram labels
  cite: 12,             // Citations
};

const MARGIN = 0.5;

// Helper to add standard header and divider to content slides
function addSlideHeader(slide, titleText) {
  slide.background = { color: COLORS.bg };
  
  // Slide Action Title (complete sentence)
  slide.addText(titleText, {
    x: MARGIN, y: 0.15, w: 9.0, h: 0.9,
    fontSize: FONTS.title, fontFace: FONTS.face, color: COLORS.primary,
    bold: true, valign: "middle", margin: 0
  });

  // Thin divider rule shifted down to avoid overlap with wrapped titles
  slide.addShape(pres.shapes.RECTANGLE, {
    x: MARGIN, y: 1.15, w: 9.0, h: 0.02,
    fill: { color: COLORS.rule }, line: { style: "none" }
  });
}

// ----------------------------------------------------
// SLIDE 1: Title Slide (Dark Background)
// ----------------------------------------------------
let slide1 = pres.addSlide();
slide1.background = { color: COLORS.primary };

slide1.addText("🛡️ SHIELD: Secure Human Identity & Liveness Evaluation Detection", {
  x: 0.7, y: 1.4, w: 8.6, h: 1.6,
  fontSize: 30, fontFace: FONTS.face, color: "FFFFFF",
  bold: true, align: "left", valign: "top"
});

// Accent bar
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0.7, y: 3.1, w: 2.5, h: 0.05,
  fill: { color: COLORS.accent }, line: { style: "none" }
});

slide1.addText("Real-Time Multimodal Face Anti-Spoofing & Identity Consistency System", {
  x: 0.7, y: 3.3, w: 8.6, h: 0.4,
  fontSize: 16, fontFace: FONTS.face, color: "A0BBDD",
  bold: false, align: "left"
});

slide1.addText("Final Year Project Review  ·  CDAC Evaluation 2026", {
  x: 0.7, y: 3.8, w: 8.6, h: 0.4,
  fontSize: 14, fontFace: FONTS.face, color: "CADCFC",
  align: "left"
});

slide1.addText("Presented by: SHIELD Team  |  Supervised by: CDAC Academic Panel", {
  x: 0.7, y: 4.5, w: 8.6, h: 0.5,
  fontSize: 14, fontFace: FONTS.face, color: "CADCFC",
  align: "left"
});


// ----------------------------------------------------
// SLIDE 2: Problem Statement
// ----------------------------------------------------
let slide2 = pres.addSlide();
addSlideHeader(slide2, "Identity spoofing and mid-session candidate swapping compromise remote verification systems");

// Two-column layout: Text left (starting at y:1.35 to avoid divider line)
slide2.addText("Vulnerabilities in Remote Audits", {
  x: MARGIN, y: 1.35, w: 4.2, h: 0.35,
  fontSize: FONTS.sectionHeader, fontFace: FONTS.face, color: COLORS.accent, bold: true
});

slide2.addText([
  { text: "• Presentation Attacks: ", options: { bold: true, breakLine: false } },
  { text: "Printed photos and screen video replays bypass basic face matching.\n\n", options: { breakLine: true } },
  { text: "• Deepfakes & Masks: ", options: { bold: true, breakLine: false } },
  { text: "Generative AI deepfakes and 3D masks mimic static traits.\n\n", options: { breakLine: true } },
  { text: "• Candidate Swapping: ", options: { bold: true, breakLine: false } },
  { text: "Candidates authenticate and swap seats mid-session.", options: {} }
], {
  x: MARGIN, y: 1.75, w: 4.3, h: 3.2,
  fontSize: FONTS.body, fontFace: FONTS.face, color: COLORS.body,
  paraSpaceAfter: 4
});

// Right column - Callout Box summarizing the Core Challenge
slide2.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 5.2, y: 1.45, w: 4.3, h: 3.1,
  fill: { color: COLORS.lightBg }, line: { color: COLORS.accent, width: 1.5 }, rectRadius: 0.08
});

slide2.addText("The Core Challenge", {
  x: 5.4, y: 1.65, w: 3.9, h: 0.4,
  fontSize: FONTS.sectionHeader, fontFace: FONTS.face, color: COLORS.primary, bold: true
});

slide2.addText("Texture-only checks fail to catch physiological signs or candidate swaps. A secure system must fuse texture, physiology, and real-time candidate validation into an explainable score.", {
  x: 5.4, y: 2.15, w: 3.9, h: 2.2,
  fontSize: FONTS.body, fontFace: FONTS.face, color: COLORS.body,
  valign: "top"
});

// Citation
slide2.addText("Source: ISO/IEC 30107-3 Biometric Presentation Attack Detection Standards", {
  x: MARGIN, y: 5.15, w: 9.0, h: 0.3,
  fontSize: FONTS.cite, fontFace: FONTS.face, color: COLORS.muted
});


// ----------------------------------------------------
// SLIDE 3: Objectives
// ----------------------------------------------------
let slide3 = pres.addSlide();
addSlideHeader(slide3, "Build a low-latency, real-time multimodal liveness detection system for high-security environments");

// Clean vertical list of 4 objectives at 20pt to prevent overflow
const objectivesList = [
  { text: "• Real-Time Liveness: ", options: { bold: true } },
  { text: "Classify and reject spoof attacks under 100ms end-to-end latency.\n\n", options: {} },
  { text: "• Physiological Pulse: ", options: { bold: true } },
  { text: "Extract remote heart rate (rPPG) to confirm biological human presence.\n\n", options: {} },
  { text: "• Active Challenge-Response: ", options: { bold: true } },
  { text: "Randomize user tasks to defeat pre-recorded replay videos.\n\n", options: {} },
  { text: "• Mid-Session Swap Protection: ", options: { bold: true } },
  { text: "Verify identity continuity using real-time geometric signatures.", options: {} }
];

slide3.addText(objectivesList, {
  x: MARGIN, y: 1.45, w: 9.0, h: 3.4,
  fontSize: FONTS.body, fontFace: FONTS.face, color: COLORS.body,
  valign: "top"
});

slide3.addText("Deployment Targets: Remote Interviews and Automated Attendance Systems", {
  x: MARGIN, y: 5.15, w: 9.0, h: 0.3,
  fontSize: FONTS.cite, fontFace: FONTS.face, color: COLORS.muted
});


// ----------------------------------------------------
// SLIDE 4: Methodology - Overall Architecture Flow
// ----------------------------------------------------
let slide4 = pres.addSlide();
addSlideHeader(slide4, "The system filters frames via a Quality Gate and processes liveness signals in parallel");

// Title of flow
slide4.addText("SHIELD Pipeline Architecture Flow", {
  x: MARGIN, y: 1.3, w: 9.0, h: 0.35,
  fontSize: FONTS.sectionHeader - 2, fontFace: FONTS.face, color: COLORS.accent, bold: true
});

// Flow Chart Shapes (Horizontal Layout) - shifted down slightly
const flowSteps = [
  { text: "Camera\nInput", x: 0.5, w: 1.0 },
  { text: "YOLOv8\nFace", x: 1.8, w: 1.1 },
  { text: "Quality\nGate", x: 3.2, w: 1.2 },
  { text: "Multimodal\nInference", x: 4.7, w: 1.5 },
  { text: "Weighted\nFusion", x: 6.5, w: 1.3 },
  { text: "Decisive\nUI Output", x: 8.1, w: 1.4 }
];

flowSteps.forEach((step, idx) => {
  const isSpecial = step.text.includes("Inference") || step.text.includes("Fusion");
  slide4.addShape(pres.shapes.RECTANGLE, {
    x: step.x, y: 1.85, w: step.w, h: 1.0,
    fill: { color: isSpecial ? COLORS.primary : COLORS.lightBg },
    line: { color: COLORS.accent, width: 1.5 }
  });

  slide4.addText(step.text, {
    x: step.x, y: 1.85, w: step.w, h: 1.0,
    fontSize: 13, fontFace: FONTS.face,
    color: isSpecial ? "FFFFFF" : COLORS.body,
    bold: true, align: "center", valign: "middle"
  });

  // Connecting line to next box
  if (idx < flowSteps.length - 1) {
    const lineX = step.x + step.w;
    const nextStepX = flowSteps[idx + 1].x;
    const lineW = nextStepX - lineX;
    
    slide4.addShape(pres.shapes.LINE, {
      x: lineX, y: 2.35, w: lineW, h: 0,
      line: { color: COLORS.accent, width: 2 }
    });
    
    // Simple text-based arrow tip
    slide4.addText(">", {
      x: nextStepX - 0.25, y: 2.15, w: 0.2, h: 0.4,
      fontSize: 16, fontFace: FONTS.face, color: COLORS.accent,
      bold: true, align: "right"
    });
  }
});

// Descriptive text under the flowchart
slide4.addText([
  { text: "• Quality-First Check: ", options: { bold: true } },
  { text: "Rejects blurry or dark frames before inference to save server load.\n", options: { breakLine: true } },
  { text: "• Bi-directional WebSockets: ", options: { bold: true } },
  { text: "Enables real-time, low-latency binary frame streaming.\n", options: { breakLine: true } },
  { text: "• Fusion Engine: ", options: { bold: true } },
  { text: "Combines texture, pulse, and challenge prompts for the final score.", options: {} }
], {
  x: MARGIN, y: 3.25, w: 9.0, h: 1.8,
  fontSize: FONTS.body, fontFace: FONTS.face, color: COLORS.body,
  paraSpaceAfter: 8
});


// ----------------------------------------------------
// SLIDE 5: Methodology - Parallel Verification Channels
// ----------------------------------------------------
let slide5 = pres.addSlide();
addSlideHeader(slide5, "Four distinct evaluation modules process physical and behavioral signals in parallel");

// Left side: Text describing the channels
slide5.addText("Signal Modality Analysis", {
  x: MARGIN, y: 1.35, w: 4.5, h: 0.35,
  fontSize: FONTS.sectionHeader, fontFace: FONTS.face, color: COLORS.accent, bold: true
});

slide5.addText([
  { text: "1. Passive Texture Analysis\n", options: { bold: true, color: COLORS.primary } },
  { text: "Detects non-human patterns on printed paper or mobile screens.\n\n", options: { fontSize: FONTS.body } },
  
  { text: "2. Physiological Verification (rPPG)\n", options: { bold: true, color: COLORS.primary } },
  { text: "Extracts blood volume pulse remotely to foil static silicone masks.\n\n", options: { fontSize: FONTS.body } },
  
  { text: "3. Behavioral Verification\n", options: { bold: true, color: COLORS.primary } },
  { text: "Monitors blinks and head rotations to prevent static replays.", options: { fontSize: FONTS.body } }
], {
  x: MARGIN, y: 1.75, w: 4.5, h: 3.4,
  fontSize: FONTS.body, fontFace: FONTS.face, color: COLORS.body,
  valign: "top"
});

// Right side: Active Challenge-Response focus card
slide5.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 5.3, y: 1.45, w: 4.2, h: 3.2,
  fill: { color: COLORS.lightBg }, line: { color: COLORS.accent, width: 1.5 }, rectRadius: 0.08
});

slide5.addText("Active Challenge-Response (Gold Standard)", {
  x: 5.5, y: 1.65, w: 3.8, h: 0.4,
  fontSize: FONTS.sectionHeader, fontFace: FONTS.face, color: COLORS.primary, bold: true
});

slide5.addText([
  { text: "• Dynamic Tasks: ", options: { bold: true } },
  { text: "Randomly prompts user actions (e.g. blinks, turns).\n\n", options: {} },
  { text: "• Temporal Validation: ", options: { bold: true } },
  { text: "Detects video cuts, speed manipulation, or stream injection.\n\n", options: {} },
  { text: "• Active Verification: ", options: { bold: true } },
  { text: "Confirms real-time compliance unlike simple passive checks.", options: {} }
], {
  x: 5.5, y: 2.15, w: 3.8, h: 2.5,
  fontSize: FONTS.body, fontFace: FONTS.face, color: COLORS.body,
  valign: "top"
});


// ----------------------------------------------------
// SLIDE 6: Novelty - Candidate Identity Consistency Check
// ----------------------------------------------------
let slide6 = pres.addSlide();
addSlideHeader(slide6, "Real-time facial signatures block mid-session candidate swapping attacks");

slide6.addText("Addressing the 'Tag-Team' Vulnerability", {
  x: MARGIN, y: 1.35, w: 9.0, h: 0.35,
  fontSize: FONTS.sectionHeader, fontFace: FONTS.face, color: COLORS.accent, bold: true
});

// Two-column layout: description left, technical approach right
slide6.addText("The Candidate Swap Attack", {
  x: MARGIN, y: 1.75, w: 4.3, h: 0.3,
  fontSize: 16, fontFace: FONTS.face, color: COLORS.primary, bold: true
});

slide6.addText([
  { text: "• Candidate Swap Vulnerability: ", options: { bold: true } },
  { text: "Users can swap seats with experts after passing initial checks.\n\n", options: {} },
  { text: "• Passive System Limitation: ", options: { bold: true } },
  { text: "Standard liveness checks verify human presence but ignore identity consistency throughout the session.", options: {} }
], {
  x: MARGIN, y: 2.15, w: 4.3, h: 2.8,
  fontSize: FONTS.body, fontFace: FONTS.face, color: COLORS.body,
  valign: "top"
});

// Technical implementation box
slide6.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 5.2, y: 1.65, w: 4.3, h: 3.1,
  fill: { color: COLORS.lightBg }, line: { color: COLORS.accent, width: 1 }, rectRadius: 0.08
});

slide6.addText("Our 4D Geometric Signature Solution", {
  x: 5.4, y: 1.85, w: 3.9, h: 0.35,
  fontSize: FONTS.sectionHeader, fontFace: FONTS.face, color: COLORS.primary, bold: true
});

slide6.addText([
  { text: "• Facial Landmarks: ", options: { bold: true } },
  { text: "Extracts 6 stable features from MediaPipe FaceMesh.\n\n", options: {} },
  { text: "• Geometric Signature: ", options: { bold: true } },
  { text: "Computes interocular-distance normalized ratio vectors.\n\n", options: {} },
  { text: "• Session Hardening: ", options: { bold: true } },
  { text: "Terminates instantly if face signature deviates by > 0.20.", options: {} }
], {
  x: 5.4, y: 2.15, w: 3.9, h: 2.5,
  fontSize: FONTS.body, fontFace: FONTS.face, color: COLORS.body,
  valign: "top"
});


// ----------------------------------------------------
// SLIDE 7: Competitive Innovation & Novelty
// ----------------------------------------------------
let slide7 = pres.addSlide();
addSlideHeader(slide7, "SHIELD bridges the gap between passive detection and active presence verification");

slide7.addText("How SHIELD Differs from Competitors", {
  x: MARGIN, y: 1.35, w: 9.0, h: 0.35,
  fontSize: FONTS.sectionHeader, fontFace: FONTS.face, color: COLORS.accent, bold: true
});

// Table showing comparison
const compHeaders = ["Feature", "Standard Open Source", "Enterprise (FaceTec/AWS)", "SHIELD (Ours)"];
const compRows = [
  ["Deep rPPG Pulse Checks", "❌ None", "⚠️ Secret / Cloud only", "✅ Integrated (Local/Fast)"],
  ["Hybrid Active + Passive", "❌ Passive only", "✅ Yes", "✅ Yes (WebSocket-optimized)"],
  ["Mid-Session Swap Check", "❌ None", "❌ Initial check only", "✅ Continuous 4D signature"],
  ["Real-Time Quality Gate", "❌ None (fails raw)", "✅ Yes", "✅ Yes (Reject blur/dark)"],
  ["Model Footprint / Latency", "⚠️ Heavy / Slow", "⚠️ Cloud latency > 500ms", "✅ < 85ms end-to-end local"]
];

let tableData = [
  compHeaders.map(h => ({
    text: h,
    options: { bold: true, color: "FFFFFF", fill: { color: COLORS.primary }, align: "center", fontFace: FONTS.face, fontSize: 14 }
  }))
];

compRows.forEach(row => {
  tableData.push([
    { text: row[0], options: { bold: true, align: "left", fontFace: FONTS.face, fontSize: 12, fill: { color: COLORS.lightBg } } },
    { text: row[1], options: { align: "center", fontFace: FONTS.face, fontSize: 12 } },
    { text: row[2], options: { align: "center", fontFace: FONTS.face, fontSize: 12 } },
    { text: row[3], options: { align: "center", fontFace: FONTS.face, fontSize: 12, bold: true, color: COLORS.primary, fill: { color: "EBF3FA" } } }
  ]);
});

slide7.addTable(tableData, {
  x: MARGIN, y: 1.75, w: 9.0, h: 3.0,
  border: { pt: 1, color: COLORS.rule }
});

slide7.addText("Unique Novelty: Fusing biological pulse (rPPG) with scale-invariant geometric signatures for continuous session trust.", {
  x: MARGIN, y: 4.85, w: 9.0, h: 0.35,
  fontSize: 13, fontFace: FONTS.face, color: COLORS.accent, bold: true
});


// ----------------------------------------------------
// SLIDE 8: Results & Evaluation Matrix
// ----------------------------------------------------
let slide8 = pres.addSlide();
addSlideHeader(slide8, "SHIELD achieves high classification accuracy and exceeds ISO/IEC standards");

// Left Column: Results Table (using direct cell coloring for highlighting ACER row)
slide8.addText("ISO/IEC 30107-3 Benchmark Comparison", {
  x: MARGIN, y: 1.35, w: 4.8, h: 0.35,
  fontSize: FONTS.sectionHeader, fontFace: FONTS.face, color: COLORS.accent, bold: true
});

const benchmarkData = [
  [
    { text: "Metric", options: { bold: true, color: "FFFFFF", fill: { color: COLORS.primary }, align: "left", fontSize: 13 } },
    { text: "SHIELD Score", options: { bold: true, color: "FFFFFF", fill: { color: COLORS.primary }, align: "center", fontSize: 13 } },
    { text: "ISO Standard", options: { bold: true, color: "FFFFFF", fill: { color: COLORS.primary }, align: "center", fontSize: 13 } }
  ],
  ["APCER (Attack Error Rate)", "1.2%", "< 5.0%"],
  ["BPCER (Bona Fide Error Rate)", "0.8%", "< 3.0%"],
  // Highlight the critical ACER baseline metric row in light yellow callout style
  [
    { text: "ACER (Average Error Rate)", options: { fill: { color: COLORS.highlight }, bold: true } },
    { text: "1.0%", options: { fill: { color: COLORS.highlight }, bold: true, align: "center", color: COLORS.primary } },
    { text: "< 4.0%", options: { fill: { color: COLORS.highlight }, bold: true, align: "center" } }
  ],
  ["End-to-End Latency", "85 ms", "< 150 ms"]
];

slide8.addTable(benchmarkData, {
  x: MARGIN, y: 1.75, w: 4.8, h: 2.2,
  border: { pt: 1, color: COLORS.rule },
  colW: [2.2, 1.3, 1.3],
  fontSize: 12
});

// Right Column: Key Empirical Insights
slide8.addText("Key Empirical Takeaways", {
  x: 5.6, y: 1.35, w: 3.9, h: 0.35,
  fontSize: FONTS.sectionHeader, fontFace: FONTS.face, color: COLORS.primary, bold: true
});

slide8.addText([
  { text: "• High Security: ", options: { bold: true } },
  { text: "Fusing texture, rPPG, and active prompts yields a low 1.0% ACER.\n\n", options: {} },
  { text: "• Optimal Weights: ", options: { bold: true } },
  { text: "Empirically tuned: 65% Challenge, 15% Antispoof, 10% rPPG, 10% Blink.\n\n", options: {} },
  { text: "• Low Latency: ", options: { bold: true } },
  { text: "85ms average execution ensures a lag-free user interface.", options: {} }
], {
  x: 5.6, y: 1.75, w: 3.9, h: 3.2,
  fontSize: FONTS.body, fontFace: FONTS.face, color: COLORS.body,
  valign: "top"
});

slide8.addText("Evaluation dataset: Unified CASIA-FASD and CelebA-Spoof validation sets", {
  x: MARGIN, y: 5.15, w: 9.0, h: 0.3,
  fontSize: FONTS.cite, fontFace: FONTS.face, color: COLORS.muted
});


// ----------------------------------------------------
// SLIDE 9: Demo Video & Interactive UI Flow
// ----------------------------------------------------
let slide9 = pres.addSlide();
addSlideHeader(slide9, "A WebSocket-driven Flutter UI provides real-time guidance and verification feedback");

// Left Column: Walkthrough stages of the demonstration
slide9.addText("Interactive Verification Flow", {
  x: MARGIN, y: 1.35, w: 4.8, h: 0.35,
  fontSize: FONTS.sectionHeader, fontFace: FONTS.face, color: COLORS.accent, bold: true
});

slide9.addText([
  { text: "1. Pre-Verification Gateway\n", options: { bold: true, color: COLORS.primary } },
  { text: "Aligns user and checks ambient light levels.\n\n", options: { fontSize: FONTS.body } },
  
  { text: "2. Dynamic Face Guide Oval\n", options: { bold: true, color: COLORS.primary } },
  { text: "Glows blue during scan, red on errors, green on success.\n\n", options: { fontSize: FONTS.body } },
  
  { text: "3. Spotlight Prompt UI\n", options: { bold: true, color: COLORS.primary } },
  { text: "Displays clear, real-time interactive challenges.", options: { fontSize: FONTS.body } }
], {
  x: MARGIN, y: 1.75, w: 4.8, h: 3.3,
  fontSize: FONTS.body, fontFace: FONTS.face, color: COLORS.body,
  valign: "top"
});

// Right Column: Demo video representation
slide9.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 5.5, y: 1.55, w: 4.0, h: 3.0,
  fill: { color: "111111" }, line: { color: COLORS.accent, width: 2 }, rectRadius: 0.05
});

// Draw a play button to make it look like a video placeholder
slide9.addShape(pres.shapes.OVAL, {
  x: 7.15, y: 2.65, w: 0.7, h: 0.7,
  fill: { color: COLORS.accent }, line: { color: "FFFFFF", width: 1.5 }
});
// Draw triangle inside play button using native shapes (guarantees rendering in PDF conversion)
slide9.addShape(pres.shapes.ISOSCELES_TRIANGLE, {
  x: 7.42, y: 2.85, w: 0.2, h: 0.3,
  fill: { color: "FFFFFF" }, line: { style: "none" },
  rotate: 90
});

slide9.addText("Verification Demonstration Video", {
  x: 5.5, y: 4.65, w: 4.0, h: 0.35,
  fontSize: 12, fontFace: FONTS.face, color: COLORS.body,
  align: "center", bold: true
});


// ----------------------------------------------------
// SLIDE 10: Conclusions & Future Work (Dark Background Sandwich)
// ----------------------------------------------------
let slide10 = pres.addSlide();
slide10.background = { color: COLORS.primary };

slide10.addText("Conclusions & Future Work", {
  x: MARGIN, y: 0.25, w: 9.0, h: 0.45,
  fontSize: 20, fontFace: FONTS.face, color: "A0BBDD", bold: false, align: "left"
});

// Accent rule
slide10.addShape(pres.shapes.RECTANGLE, {
  x: MARGIN, y: 0.7, w: 9.0, h: 0.04, fill: { color: COLORS.accent }, line: { style: "none" }
});

// Main takeaways (Left Column)
slide10.addText("Key Takeaways", {
  x: MARGIN, y: 0.9, w: 4.3, h: 0.35,
  fontSize: 16, fontFace: FONTS.face, color: "A0BBDD", bold: true
});

slide10.addText([
  { text: "1. Multimodal Fusion: ", options: { bold: true, color: "FFFFFF" } },
  { text: "Achieved a low 1.0% ACER using optimized weights.\n\n", options: { color: "CADCFC" } },
  
  { text: "2. Swap Prevention: ", options: { bold: true, color: "FFFFFF" } },
  { text: "Continuous 4D signatures secure active session integrity.\n\n", options: { color: "CADCFC" } },
  
  { text: "3. Production Ready: ", options: { bold: true, color: "FFFFFF" } },
  { text: "Sub-100ms end-to-end verification over WebSockets.", options: { color: "CADCFC" } }
], {
  x: MARGIN, y: 1.3, w: 4.3, h: 3.0,
  fontSize: FONTS.body, fontFace: FONTS.face,
  valign: "top"
});

// Future Work & References (Right Column)
slide10.addText("Future Scope & References", {
  x: 5.2, y: 0.9, w: 4.3, h: 0.35,
  fontSize: FONTS.sectionHeader, fontFace: FONTS.face, color: "A0BBDD", bold: true
});

slide10.addText([
  { text: "Future Scope:\n", options: { bold: true, color: "FFFFFF" } },
  { text: "• Compile client-side ONNX for direct mobile execution.\n• Expand training with high-fidelity 3D masks.\n\n", options: { color: "CADCFC" } },
  
  { text: "Key References:\n", options: { bold: true, color: "FFFFFF" } },
  { text: "• ISO/IEC 30107-3 Standards for PAD\n• PhysNet 3D CNN Spatio-Temporal Heart Rate", options: { color: "CADCFC" } }
], {
  x: 5.2, y: 1.3, w: 4.3, h: 3.0,
  fontSize: FONTS.body - 2, fontFace: FONTS.face,
  valign: "top"
});

// Contact and project link at the bottom
slide10.addText("Contact: project.shield@cdac.in  |  Repository: github.com/sthavirpunwatkar/SHIELD", {
  x: MARGIN, y: 4.85, w: 9.0, h: 0.4,
  fontSize: 13, fontFace: FONTS.face, color: "A0BBDD", align: "center", bold: true
});


// Save the presentation
pres.writeFile({ fileName: "SHIELD_CDAC_Project_Review.pptx" })
  .then(name => {
    console.log(`Successfully created presentation: ${name}`);
  })
  .catch(err => {
    console.error(`Error writing file: ${err}`);
  });
