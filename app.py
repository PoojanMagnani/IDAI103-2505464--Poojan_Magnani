import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Any
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ArtRestorer AI - Cultural Heritage Preservation",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== OPENAI API CONFIGURATION ====================
openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    st.error("❌ OpenAI API key not found! Please add OPENAI_API_KEY to your .env file")
    st.stop()

openai_client = OpenAI(api_key=openai_api_key)

# ==================== GLOBAL CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

    :root {
        --midnight: #0a0e1a;
        --deep-navy: #111827;
        --navy: #1a2540;
        --navy-light: #243050;
        --gold: #c9a84c;
        --gold-light: #e4c47e;
        --gold-pale: #f5e6c8;
        --teal: #2dd4bf;
        --teal-dark: #14b8a6;
        --cream: #faf7f2;
        --text-primary: #f0ece4;
        --text-muted: #9ba3b4;
        --text-dark: #1e2535;
        --border: rgba(201,168,76,0.25);
        --card-bg: rgba(26,37,64,0.6);
        --glow: 0 0 40px rgba(201,168,76,0.15);
    }

    /* ========== GLOBAL RESETS ========== */
    .stApp {
        background: var(--midnight);
        font-family: 'DM Sans', sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* ========== HEADER ========== */
    .site-header {
        background: linear-gradient(180deg, rgba(10,14,26,0.98) 0%, rgba(17,24,39,0.95) 100%);
        border-bottom: 1px solid var(--border);
        padding: 1.2rem 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(20px);
        position: relative;
        margin: -6rem -6rem 2rem -6rem;
    }
    .site-header::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--gold), transparent);
    }
    .header-logo {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--gold);
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .header-tagline {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.75rem;
        color: var(--text-muted);
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 0.2rem;
        text-align: center;
    }

    /* ========== HERO ========== */
    .hero-wrapper {
        position: relative;
        padding: 5rem 2rem 6rem;
        text-align: center;
        overflow: hidden;
    }
    .hero-bg-orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(120px);
        opacity: 0.18;
        pointer-events: none;
    }
    .hero-bg-orb-1 {
        width: 600px; height: 600px;
        background: var(--gold);
        top: -200px; left: -100px;
    }
    .hero-bg-orb-2 {
        width: 500px; height: 500px;
        background: var(--teal);
        bottom: -150px; right: -100px;
    }
    .hero-eyebrow {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        color: var(--teal);
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border: 1px solid rgba(45,212,191,0.3);
        border-radius: 20px;
        background: rgba(45,212,191,0.05);
    }
    .hero-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(3.5rem, 8vw, 6.5rem);
        font-weight: 300;
        color: var(--text-primary);
        line-height: 1.05;
        margin: 0 0 0.3rem 0;
        letter-spacing: -1px;
    }
    .hero-title-accent {
        color: var(--gold);
        font-style: italic;
        font-weight: 400;
    }
    .hero-subtitle {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.15rem;
        color: var(--text-muted);
        margin: 1.5rem auto 3rem auto;
        max-width: 600px;
        line-height: 1.7;
        font-weight: 300;
        text-align: center;
    }
    .hero-divider {
        width: 80px;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--gold), transparent);
        margin: 0 auto 3rem;
    }

    /* ========== FEATURE GRID ========== */
    .features-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        color: var(--text-muted);
        letter-spacing: 4px;
        text-transform: uppercase;
        text-align: center;
        margin: 3rem 0 2rem;
    }
    .feature-card-dark {
        background: rgba(26,37,64,0.5);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        height: 220px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .feature-card-dark::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--gold), transparent);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    .feature-card-dark:hover {
        background: rgba(36,48,80,0.85);
        border-color: rgba(201,168,76,0.5);
        transform: translateY(-6px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 30px rgba(201,168,76,0.1);
    }
    .feature-card-dark:hover::before { opacity: 1; }
    .feature-icon-dark {
        font-size: 2.2rem;
        margin-bottom: 1rem;
        display: block;
        transition: transform 0.3s ease;
    }
    .feature-card-dark:hover .feature-icon-dark {
        transform: scale(1.15);
    }
    .feature-card-dark h3 {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.15rem;
        font-weight: 600;
        color: var(--gold-light);
        margin: 0 0 0.6rem 0;
        letter-spacing: 0.5px;
    }
    .feature-card-dark p {
        color: var(--text-muted);
        font-size: 0.82rem;
        line-height: 1.5;
        margin: 0;
    }

    /* ========== WHY SECTION ========== */
    .why-card {
        background: rgba(26,37,64,0.4);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        backdrop-filter: blur(10px);
        height: 280px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }
    .why-card:hover {
        border-color: rgba(45,212,191,0.4);
        background: rgba(26,37,64,0.7);
    }
    .why-card-icon {
        font-size: 2.8rem;
        margin-bottom: 1.2rem;
        display: block;
    }
    .why-card h3 {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.4rem;
        color: var(--text-primary);
        margin: 0 0 0.8rem 0;
    }
    .why-card p {
        color: var(--text-muted);
        font-size: 0.9rem;
        line-height: 1.6;
        margin: 0;
    }

    /* ========== CTA SECTION ========== */
    .cta-block {
        background: linear-gradient(135deg, rgba(201,168,76,0.12) 0%, rgba(45,212,191,0.08) 100%);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 4rem 2rem;
        text-align: center;
        margin: 4rem 0 2rem;
        position: relative;
        overflow: hidden;
    }
    .cta-block::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--gold), var(--teal), transparent);
    }
    .cta-block h2 {
        font-family: 'Cormorant Garamond', serif;
        font-size: 3rem;
        font-weight: 300;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }
    .cta-block p {
        color: var(--text-muted);
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
    }

    /* ========== BUTTONS ========== */
    .stButton > button {
        background: linear-gradient(135deg, var(--gold) 0%, #b8932f 100%);
        color: var(--midnight);
        border: none;
        padding: 0.9rem 2.5rem;
        font-size: 0.95rem;
        font-weight: 600;
        border-radius: 10px;
        cursor: pointer;
        font-family: 'DM Sans', sans-serif;
        letter-spacing: 0.5px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(201,168,76,0.25);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(201,168,76,0.4);
        background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 100%);
    }

    /* ========== WELCOME CARD ========== */
    .welcome-card {
        background: rgba(26,37,64,0.6);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 3rem 2.5rem;
        max-width: 720px;
        margin: 0 auto;
        backdrop-filter: blur(20px);
    }
    .welcome-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.8rem;
        font-weight: 300;
        color: var(--text-primary);
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .welcome-subtitle {
        text-align: center;
        color: var(--text-muted);
        font-size: 1rem;
        margin-bottom: 2.5rem;
    }

    /* ========== FORM INPUTS ========== */
    .stTextInput > label,
    .stSelectbox > label,
    .stTextArea > label {
        color: var(--text-muted) !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        font-family: 'DM Mono', monospace !important;
    }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background: rgba(17,24,39,0.8) !important;
        border: 1px solid rgba(201,168,76,0.3) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.95rem !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 2px rgba(201,168,76,0.15) !important;
    }
    .stSelectbox > div > div > div {
        color: var(--text-primary) !important;
    }

    /* ========== TABS ========== */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(17,24,39,0.8);
        border-radius: 12px;
        padding: 0.4rem;
        gap: 0.3rem;
        border: 1px solid var(--border);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: var(--text-muted);
        padding: 0.7rem 1.4rem;
        font-size: 0.85rem;
        font-weight: 500;
        border-radius: 8px;
        font-family: 'DM Sans', sans-serif;
        letter-spacing: 0.3px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(201,168,76,0.2), rgba(201,168,76,0.1)) !important;
        color: var(--gold-light) !important;
        border: 1px solid rgba(201,168,76,0.4) !important;
    }

    /* ========== USER GREETING ========== */
    .user-greeting {
        background: linear-gradient(135deg, rgba(201,168,76,0.12), rgba(45,212,191,0.08));
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    .greeting-avatar {
        width: 52px; height: 52px;
        background: linear-gradient(135deg, var(--gold), #b8932f);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        flex-shrink: 0;
        color: var(--midnight);
        font-weight: bold;
        font-family: 'Cormorant Garamond', serif;
    }
    .greeting-text h3 {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.5rem;
        color: var(--text-primary);
        margin: 0 0 0.3rem 0;
    }
    .greeting-text p {
        color: var(--text-muted);
        font-size: 0.85rem;
        margin: 0;
    }

    /* ========== MAIN CARD ========== */
    .glass-card {
        background: rgba(26,37,64,0.5);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(15px);
    }
    .glass-card h2 {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.8rem;
        font-weight: 400;
        color: var(--gold-light);
        margin-top: 0;
        letter-spacing: 0.5px;
    }

    /* ========== FEATURE SELECTOR ========== */
    .feature-selector {
        background: rgba(17,24,39,0.6);
        border: 1px solid rgba(45,212,191,0.2);
        border-radius: 14px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }
    .feature-selector h3 {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.2rem;
        color: var(--teal);
        margin: 0 0 1rem 0;
        letter-spacing: 0.5px;
    }

    /* ========== TEMPERATURE SLIDER ========== */
    .slider-container {
        background: rgba(17,24,39,0.6);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
    }
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, var(--navy-light), var(--gold), var(--teal)) !important;
        height: 6px !important;
        border-radius: 6px !important;
    }
    .stSlider > div > div > div > div > div {
        background: white !important;
        border: 3px solid var(--gold) !important;
        width: 22px !important;
        height: 22px !important;
        box-shadow: 0 2px 10px rgba(201,168,76,0.5) !important;
    }
    .stSlider > label {
        color: var(--text-muted) !important;
        font-size: 0.78rem !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        font-family: 'DM Mono', monospace !important;
    }

    /* ========== RESULT BOX ========== */
    .result-box {
        background: rgba(17,24,39,0.8);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2.5rem;
        backdrop-filter: blur(20px);
    }
    .result-box h3 {
        font-family: 'Cormorant Garamond', serif;
        color: var(--gold-light);
        font-size: 1.8rem;
        margin-top: 0;
    }
    .result-text {
        line-height: 2;
        color: #d0cbbc;
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
    }
    .result-text h2 {
        color: var(--gold-light);
        font-family: 'Cormorant Garamond', serif;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-size: 1.7rem;
        font-weight: 400;
    }
    .result-text h3 {
        color: var(--teal);
        font-family: 'Cormorant Garamond', serif;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        font-size: 1.35rem;
        font-weight: 400;
    }
    .result-text strong { color: var(--gold-light); font-weight: 600; }
    .result-text ul, .result-text li { margin: 0.5rem 0; line-height: 1.8; }

    /* ========== SECTION LABELS ========== */
    .section-eyebrow {
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        color: var(--teal);
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
        display: block;
    }
    .section-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.2rem;
        font-weight: 300;
        color: var(--text-primary);
        margin: 0 0 0.8rem 0;
    }

    /* ========== INSIGHTS ========== */
    .insight-header {
        background: linear-gradient(135deg, rgba(201,168,76,0.15), rgba(45,212,191,0.08));
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* ========== TIMELINE PLANNER ========== */
    .timeline-card {
        background: rgba(26,37,64,0.5);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        position: relative;
        transition: all 0.3s ease;
    }
    .timeline-card:hover {
        border-color: rgba(201,168,76,0.4);
        background: rgba(36,48,80,0.7);
    }
    .timeline-phase-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        color: var(--teal);
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .timeline-phase-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.35rem;
        color: var(--gold-light);
        margin: 0 0 0.5rem 0;
    }
    .timeline-duration-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(201,168,76,0.2), rgba(201,168,76,0.1));
        border: 1px solid rgba(201,168,76,0.3);
        color: var(--gold-light);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-family: 'DM Mono', monospace;
        margin-bottom: 0.8rem;
    }
    .phase-task {
        background: rgba(17,24,39,0.5);
        border-left: 2px solid var(--teal);
        padding: 0.6rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        color: #b0bbc8;
        font-size: 0.88rem;
    }
    .priority-high { border-left-color: #ef4444; }
    .priority-medium { border-left-color: var(--gold); }
    .priority-low { border-left-color: var(--teal); }
    .timeline-connector {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0.5rem 0;
        color: var(--text-muted);
        font-size: 1.3rem;
    }
    .milestone-dot {
        width: 12px; height: 12px;
        background: var(--gold);
        border-radius: 50%;
        box-shadow: 0 0 12px rgba(201,168,76,0.5);
        display: inline-block;
        margin-right: 0.5rem;
        flex-shrink: 0;
    }
    .risk-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.72rem;
        font-family: 'DM Mono', monospace;
        margin-left: 0.5rem;
    }
    .risk-high { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
    .risk-medium { background: rgba(201,168,76,0.15); color: var(--gold-light); border: 1px solid rgba(201,168,76,0.3); }
    .risk-low { background: rgba(45,212,191,0.15); color: var(--teal); border: 1px solid rgba(45,212,191,0.3); }

    .summary-stat {
        background: rgba(17,24,39,0.8);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.5rem;
        text-align: center;
    }
    .summary-stat .stat-value {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.5rem;
        color: var(--gold-light);
        font-weight: 400;
        line-height: 1;
        margin-bottom: 0.4rem;
    }
    .summary-stat .stat-label {
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-family: 'DM Mono', monospace;
    }

    /* ========== QUIZ (FEATURE GALLERY) ========== */
    .quiz-header {
        background: linear-gradient(135deg, rgba(26,37,64,0.8), rgba(17,24,39,0.9));
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
    }
    .quiz-header h3 {
        font-family: 'Cormorant Garamond', serif;
        color: var(--gold-light);
        font-size: 1.5rem;
        margin: 0 0 0.3rem 0;
    }
    .quiz-header p {
        color: var(--text-muted);
        font-size: 0.88rem;
        margin: 0;
    }

    /* ========== RADIO BUTTONS ========== */
    .stRadio > div > label {
        background: rgba(26,37,64,0.5) !important;
        border: 1px solid rgba(201,168,76,0.2) !important;
        border-radius: 10px !important;
        padding: 0.8rem 1.2rem !important;
        color: var(--text-primary) !important;
        transition: all 0.2s ease !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
    }
    .stRadio > div > label:hover {
        border-color: rgba(201,168,76,0.5) !important;
        background: rgba(36,48,80,0.7) !important;
    }

    /* ========== FILE UPLOADER ========== */
    .stFileUploader > div {
        background: rgba(17,24,39,0.6) !important;
        border: 1px dashed rgba(201,168,76,0.3) !important;
        border-radius: 12px !important;
    }

    /* ========== SLIDER MULTISELECT ========== */
    .stMultiSelect > div > div {
        background: rgba(17,24,39,0.8) !important;
        border: 1px solid rgba(201,168,76,0.3) !important;
        border-radius: 10px !important;
    }
    .stMultiSelect > div > div > div {
        color: var(--text-primary) !important;
    }

    /* ========== NUMBER INPUT ========== */
    .stNumberInput > div > div > input {
        background: rgba(17,24,39,0.8) !important;
        border: 1px solid rgba(201,168,76,0.3) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }

    /* ========== FEEDBACK FORM ========== */
    .feedback-modal-inner {
        background: rgba(26,37,64,0.95);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 3rem 2.5rem;
        backdrop-filter: blur(20px);
        margin: 2rem 0;
    }

    /* ========== FOOTER ========== */
    .site-footer {
        border-top: 1px solid var(--border);
        padding: 2rem 1rem;
        text-align: center;
        margin-top: 4rem;
        color: var(--text-muted);
        font-size: 0.82rem;
        font-family: 'DM Mono', monospace;
    }
    .site-footer span {
        color: var(--gold);
    }

    /* ========== MISC ========== */
    .divider-gold {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
        margin: 2rem 0;
    }
    .badge-teal {
        display: inline-block;
        background: rgba(45,212,191,0.1);
        border: 1px solid rgba(45,212,191,0.3);
        color: var(--teal);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-family: 'DM Mono', monospace;
        letter-spacing: 1px;
    }
    .badge-gold {
        display: inline-block;
        background: rgba(201,168,76,0.1);
        border: 1px solid rgba(201,168,76,0.3);
        color: var(--gold-light);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-family: 'DM Mono', monospace;
        letter-spacing: 1px;
    }

    /* Streamlit specific overrides */
    [data-testid="stMarkdownContainer"] p { color: #c5bfb4; }
    [data-testid="stMarkdownContainer"] p.hero-subtitle { text-align: center !important; margin-left: auto !important; margin-right: auto !important; }
    .hero-wrapper p { text-align: center !important; }
    div[data-testid="metric-container"] {
        background: rgba(26,37,64,0.5);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1rem;
    }
    .stSelectbox svg { color: var(--gold) !important; }
    .stSpinner { color: var(--gold) !important; }

</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'result_text' not in st.session_state:
    st.session_state.result_text = ""

# ==================== FEATURE DESCRIPTIONS ====================
feature_descriptions = {
    'period': 'Expert restoration guidance for Baroque and Renaissance artworks using historically accurate techniques',
    'cultural': 'Restore and enhance traditional patterns from Mughal, Islamic, Celtic, Asian, and indigenous arts',
    'sculptural': 'Reconstruct eroded or damaged features in sculptures, statues, and three-dimensional artifacts',
    'textile': 'Expert restoration for tapestries, embroidery, historical fabrics, and woven artifacts',
    'abstract': 'Restore contemporary, abstract, expressionist, and modern artworks',
    'manuscript': 'Restore illuminated manuscripts, scrolls, codices, and historical documents',
    'mural': 'Restore wall paintings, cave art, frescoes, and architectural murals',
    'ceramic': 'Restore pottery, porcelain, ceramic vessels, and glazed artifacts',
    'symbol': 'Decode and restore symbolic elements, religious imagery, inscriptions, and cultural icons',
    'educational': 'Create engaging museum descriptions, exhibition content, and educational materials'
}

def render_header():
    st.markdown("""
    <div class="site-header">
        <div>
            <div class="header-logo">⬡ ArtRestorer AI</div>
            <div class="header-tagline">Cultural Heritage Preservation Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== LANDING PAGE ====================
if st.session_state.page == 'landing':
    render_header()

    # Hero
    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero-bg-orb hero-bg-orb-1"></div>
        <div class="hero-bg-orb hero-bg-orb-2"></div>
        <div class="hero-eyebrow">AI · Heritage · Preservation</div>
        <h1 class="hero-title">Restore the Past,<br><span class="hero-title-accent">Preserve Forever</span></h1>
        <div class="hero-divider"></div>
        <p class="hero-subtitle" style="text-align: center !important; margin-left: auto !important; margin-right: auto !important;">
            Advanced AI analysis meets centuries of artistic tradition. Expert guidance for conservators, curators, historians and collectors worldwide.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Features label
    st.markdown('<p class="features-label">— Core Capabilities —</p>', unsafe_allow_html=True)

    features_showcase = [
        {"icon": "🎭", "title": "Period-Specific Restoration", "desc": "Baroque, Renaissance, Gothic — historically accurate techniques"},
        {"icon": "🕌", "title": "Cultural Pattern Enhancement", "desc": "Mughal, Islamic, Celtic and indigenous design restoration"},
        {"icon": "🗿", "title": "Sculptural Reconstruction", "desc": "3D artifacts, statues — detailed erosion and loss analysis"},
        {"icon": "🧵", "title": "Textile & Tapestry Repair", "desc": "Historical fabrics, embroidery and woven artifact restoration"},
        {"icon": "🎨", "title": "Modern Art Recovery", "desc": "Abstract and contemporary works, innovative approaches"},
        {"icon": "📜", "title": "Manuscript Conservation", "desc": "Ancient scrolls, illuminated texts and fragile documents"},
        {"icon": "🏛️", "title": "Mural & Fresco Revival", "desc": "Cave paintings, frescoes and architectural murals"},
        {"icon": "🏺", "title": "Ceramic Restoration", "desc": "Pottery, porcelain and glazed artifact reconstruction"},
        {"icon": "🔯", "title": "Symbol Interpretation", "desc": "Religious imagery, inscriptions and cultural iconography"}
    ]

    for i in range(0, len(features_showcase), 3):
        cols = st.columns(3, gap="medium")
        for j in range(3):
            if i + j < len(features_showcase):
                f = features_showcase[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="feature-card-dark">
                        <span class="feature-icon-dark">{f['icon']}</span>
                        <h3>{f['title']}</h3>
                        <p>{f['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)

    # Why Choose
    st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
    st.markdown("""
    <p class="features-label">— Why ArtRestorer AI —</p>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown("""
        <div class="why-card">
            <span class="why-card-icon">🔬</span>
            <h3>Expert Analysis</h3>
            <p>AI-powered insights rooted in historical research and global conservation best practices.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="why-card">
            <span class="why-card-icon">⚡</span>
            <h3>Instant Guidance</h3>
            <p>Comprehensive restoration analysis delivered in seconds, not days of manual research.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="why-card">
            <span class="why-card-icon">🌍</span>
            <h3>Global Heritage</h3>
            <p>Deep support for diverse cultural traditions spanning every continent and era.</p>
        </div>
        """, unsafe_allow_html=True)

    # CTA
    st.markdown("""
    <div class="cta-block">
        <h2>Begin Your Restoration Journey</h2>
        <p>Join conservators and art enthusiasts worldwide in preserving cultural heritage.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Enter Application →", key="landing_continue"):
            st.session_state.page = 'welcome'
            st.rerun()

    st.markdown("""
    <div class="site-footer">
        <span>ArtRestorer AI</span> · Powered by OpenAI · Cultural Heritage Preservation
    </div>
    """, unsafe_allow_html=True)


# ==================== WELCOME PAGE ====================
elif st.session_state.page == 'welcome':
    render_header()

    st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="welcome-card">
        <div class="welcome-title">Welcome</div>
        <p class="welcome-subtitle">Tell us about yourself to personalise your experience</p>
    """, unsafe_allow_html=True)

    user_name = st.text_input("Your Name", placeholder="Enter your full name", key="name_input")

    artwork_type = st.selectbox(
        "Artwork Type",
        ["", "Painting (Oil, Acrylic, Watercolor)", "Sculpture (Stone, Bronze, Wood)",
         "Textile (Tapestry, Fabric, Embroidery)", "Manuscript (Scrolls, Books, Documents)",
         "Mural/Fresco (Wall Painting)", "Ceramic/Pottery (Vessels, Tiles)",
         "Mixed Media/Contemporary Art", "Other Heritage Artifact"],
        key="artwork_input"
    )

    user_role = st.selectbox(
        "Your Role",
        ["", "Professional Conservator/Restorer", "Museum Curator", "Art Historian/Researcher",
         "Student (Art/Conservation)", "Private Collector", "Artist",
         "Art Enthusiast/Hobbyist", "Educator/Teacher"],
        key="role_input"
    )

    user_goal = st.selectbox(
        "Primary Goal",
        ["", "Physical restoration guidance", "Digital restoration/reconstruction",
         "Artwork analysis and documentation", "Educational content creation",
         "Academic research", "Preventive conservation", "Exhibition planning"],
        key="goal_input"
    )

    st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)

    if st.button("Begin Analysis →", key="begin_btn"):
        if user_name and artwork_type and user_role and user_goal:
            st.session_state.user_data = {
                'name': user_name,
                'artwork_type': artwork_type,
                'role': user_role,
                'goal': user_goal
            }
            st.session_state.page = 'main'
            st.rerun()
        else:
            st.error("Please complete all fields to continue.")

    st.markdown('</div>', unsafe_allow_html=True)


# ==================== MAIN APPLICATION ====================
elif st.session_state.page == 'main':
    render_header()
    st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🖼️  Restoration Assistant",
        "📚  Feature Gallery",
        "🏛️  Cultural Insights",
        "🗓️  Timeline Planner"
    ])

    # ==================== TAB 1: RESTORATION ASSISTANT ====================
    with tab1:
        user = st.session_state.user_data
        initials = user['name'][0].upper() if user.get('name') else "?"
        st.markdown(f"""
        <div class="user-greeting">
            <div class="greeting-avatar">{initials}</div>
            <div class="greeting-text">
                <h3>Hello, {user.get('name', '')} 👋</h3>
                <p>{user.get('artwork_type', '')} &nbsp;·&nbsp; {user.get('role', '')}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h2>Art Restoration Analysis</h2>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<span class="section-eyebrow">Upload Image (Optional)</span>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], key="image_upload", label_visibility="collapsed")
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded Artwork", use_container_width=True)

        with col2:
            artwork_description = st.text_area(
                "Artwork Description",
                placeholder="Describe the artwork: medium, period, visible damage, dimensions, provenance...",
                height=200,
                key="description_input"
            )

        # Feature Selector
        st.markdown('<div class="feature-selector">', unsafe_allow_html=True)
        st.markdown('<h3>Select Analysis Type</h3>', unsafe_allow_html=True)
        feature_select = st.selectbox(
            "Analysis Type",
            [
                "1. 🎭 Period-Specific Restoration (Baroque/Renaissance)",
                "2. 🕌 Cultural Pattern Enhancement (Traditional Arts)",
                "3. 🗿 Sculptural Reconstruction",
                "4. 🧵 Textile & Tapestry Repair",
                "5. 🎨 Abstract & Modern Art Recovery",
                "6. 📜 Ancient Manuscript Conservation",
                "7. 🏛️ Mural & Fresco Revival",
                "8. 🏺 Ceramic & Pottery Reconstruction",
                "9. 🔯 Symbol & Iconography Interpretation",
                "10. 🎓 Educational Content Generation"
            ],
            key="feature_select",
            label_visibility="collapsed"
        )
        feature_key = ['period', 'cultural', 'sculptural', 'textile', 'abstract', 'manuscript', 'mural', 'ceramic', 'symbol', 'educational'][int(feature_select[0]) - 1]
        st.markdown(f'<p style="color: var(--text-muted); font-size: 0.88rem; font-style: italic; margin-top: 0.5rem;">{feature_descriptions[feature_key]}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        col3, col4, col5 = st.columns(3)
        with col3:
            art_style_options = [
                "Baroque", "Renaissance", "Gothic", "Neoclassical", "Rococo",
                "Romantic", "Impressionist", "Expressionist", "Art Deco", "Art Nouveau",
                "Indian Mughal", "Indian Rajput", "Indian Pahari", "Indian Madhubani",
                "Persian Miniature", "Islamic Geometric", "Byzantine", "Japanese Ukiyo-e",
                "Chinese Ming Dynasty", "Aboriginal", "Egyptian", "Greek/Roman Classical"
            ]
            art_style = st.selectbox("Art Style / Period", [""] + art_style_options, key="style_input")

        with col4:
            damage_type_options = [
                "Water damage/stains", "Fire damage/smoke residue",
                "Fading from sunlight/UV exposure", "Erosion/weathering",
                "Cracks/structural damage", "Flaking/peeling paint",
                "Mold/biological growth", "Scratches/surface abrasions",
                "Missing sections/losses", "Discoloration/yellowing",
                "Torn fabric/textile damage", "Broken/fragmented pieces",
                "Oxidation/corrosion", "Insect damage", "Previous poor restoration"
            ]
            damage_type = st.selectbox("Damage Type", [""] + damage_type_options, key="damage_input")

        with col5:
            cultural_context_options = [
                "Italian Renaissance", "French Baroque", "Spanish Colonial",
                "Flemish/Dutch", "British Victorian", "Indian Mughal",
                "Indian Rajput", "Indian Temple Art", "Persian/Iranian",
                "Ottoman Turkish", "Chinese Imperial", "Japanese Edo Period",
                "Egyptian Pharaonic", "Greek Classical", "Roman Imperial",
                "Byzantine Eastern Orthodox", "African Tribal", "Native American"
            ]
            cultural_context = st.selectbox("Cultural Context", [""] + cultural_context_options, key="context_input")

        # Temperature Slider
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        st.markdown('<span class="section-eyebrow">AI Creativity Level</span>', unsafe_allow_html=True)

        temperature = st.slider("Creativity Level", 0.0, 1.0, 0.6, 0.05, key="temp_slider", label_visibility="collapsed")

        if temperature <= 0.3:
            ind_color = "#60a5fa"; ind_icon = "🎯"; ind_title = "Highly Conservative"; ind_sub = "Strict Historical Accuracy"
            desc = "Ultra-precise restoration focusing purely on documented historical evidence and proven conservation techniques."
        elif temperature <= 0.5:
            ind_color = "#93c5fd"; ind_icon = "📚"; ind_title = "Conservative & Methodical"; ind_sub = "Evidence-Based Approach"
            desc = "Careful restoration based on historical research and comparative analysis with minimal speculation."
        elif temperature <= 0.7:
            ind_color = "#c9a84c"; ind_icon = "⚖️"; ind_title = "Balanced & Professional"; ind_sub = "Art + Science"
            desc = "Balanced approach combining historical accuracy with thoughtful creative suggestions. Ideal for most projects."
        elif temperature <= 0.85:
            ind_color = "#a78bfa"; ind_icon = "🎨"; ind_title = "Creative & Exploratory"; ind_sub = "Artistic Interpretation"
            desc = "Imaginative restoration suggestions exploring multiple creative possibilities while respecting historical context."
        else:
            ind_color = "#e879f9"; ind_icon = "✨"; ind_title = "Highly Creative"; ind_sub = "Bold Artistic Vision"
            desc = "Maximum creativity with bold artistic interpretations. Generates innovative ideas that push boundaries."

        st.markdown(f"""
        <div style="background: rgba(17,24,39,0.8); border: 1px solid {ind_color}40; border-radius: 14px; padding: 1.5rem 2rem; margin-top: 1.5rem; display: flex; align-items: center; gap: 1.5rem;">
            <div style="font-size: 2.5rem; flex-shrink: 0;">{ind_icon}</div>
            <div>
                <div style="font-family: 'Cormorant Garamond', serif; font-size: 1.3rem; color: {ind_color}; font-weight: 500;">{ind_title} &nbsp;<span style="font-size: 0.75rem; font-family: 'DM Mono', monospace; letter-spacing: 2px; opacity: 0.7;">{ind_sub}</span></div>
                <div style="color: var(--text-muted); font-size: 0.88rem; margin-top: 0.3rem; line-height: 1.5;">{desc}</div>
            </div>
            <div style="margin-left: auto; font-family: 'DM Mono', monospace; font-size: 1.6rem; color: {ind_color}; font-weight: 500; flex-shrink: 0;">{temperature:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Generate Button
        st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
        if st.button("Generate AI Restoration Analysis →", key="generate_btn"):
            if artwork_description:
                with st.spinner("Analysing artwork and generating expert restoration guidance..."):
                    import time
                    time.sleep(3)
                    st.session_state.page = 'results'
                    creativity_level = ["highly conservative", "conservative and methodical", "balanced and professional", "creative and exploratory", "highly creative and innovative"][min(int(temperature / 0.2), 4)]

                    st.session_state.result_text = f"""COMPREHENSIVE RESTORATION ANALYSIS
══════════════════════════════════════════════════════════

ARTWORK DETAILS:
{artwork_description}

STYLE/PERIOD: {art_style or 'Not specified'}
DAMAGE TYPE: {damage_type or 'general wear'}
CULTURAL CONTEXT: {cultural_context or 'Not specified'}
ANALYSIS TYPE: {feature_select}
AI CREATIVITY LEVEL: {temperature} ({creativity_level})

══════════════════════════════════════════════════════════

EXPERT RESTORATION GUIDANCE:

1. HISTORICAL CONTEXT & SIGNIFICANCE

   Based on the provided description and the {art_style or 'specified'} period, this artwork represents a significant example of its time. The {cultural_context or 'general'} cultural context suggests traditional techniques and materials that were commonly employed during this era.

2. CONDITION ASSESSMENT

   The {damage_type or 'general wear'} presents specific challenges that require careful consideration:

   • Primary concerns include structural integrity and aesthetic coherence
   • Surface analysis reveals patterns consistent with environmental exposure
   • Original materials and techniques must be preserved where possible
   • Documentation of current state is essential before intervention

3. RESTORATION METHODOLOGY

   Step-by-step approach for conservation:

   a) DOCUMENTATION PHASE
      - Comprehensive photography (visible light, UV, infrared)
      - Detailed condition mapping
      - Material analysis and identification
      - Historical research and comparative studies

   b) STABILIZATION PHASE
      - Consolidation of loose or flaking areas
      - Structural support where needed
      - Environmental stabilization
      - Protection from further deterioration

   c) CLEANING PHASE
      - Surface cleaning using appropriate methods
      - Removal of discolored varnish or overpainting
      - pH testing and adjustment
      - Gradual approach with constant monitoring

   d) RESTORATION PHASE
      - Loss compensation using reversible materials
      - Color matching to original palette
      - Texture recreation matching original techniques
      - Integration with surrounding original material

4. MATERIALS & TECHNIQUES

   Recommended conservation-grade materials:

   • Adhesives: Reversible synthetic polymers
   • Consolidants: Tested for compatibility with original materials
   • Inpainting media: Watercolors or conservation acrylics
   • Protective coatings: UV-filtering, breathable varnishes

   Traditional techniques:
   • Period-appropriate brushwork patterns
   • Layering methodology consistent with {art_style or 'period'} style
   • Color mixing using historically accurate pigment knowledge

5. CULTURAL & HISTORICAL CONSIDERATIONS

   Respect for {cultural_context or "the artwork's"} traditions:
   • Consultation with cultural heritage experts
   • Understanding of symbolic and religious significance
   • Preservation of authentic character and patina
   • Balance between restoration and historical integrity

6. TECHNICAL SPECIFICATIONS

   Color Palette Recommendations:
   • Earth tones: Raw umber, burnt sienna, yellow ochre
   • Primary colors adjusted for period accuracy
   • Consideration of natural pigment aging

   Application Techniques:
   • Brushstroke direction following original patterns
   • Layering sequence respecting traditional methods
   • Glazing techniques for depth and luminosity

7. CONSERVATION CHALLENGES & SOLUTIONS

   Challenge 1: {damage_type or 'damage'} extent
   Solution: Gradual intervention with regular assessment

   Challenge 2: Material compatibility
   Solution: Comprehensive testing on sample areas

   Challenge 3: Color matching aged surfaces
   Solution: Create reference samples and account for natural aging

   Challenge 4: Maintaining authenticity
   Solution: Document all interventions, use distinguishable but harmonious restoration

8. PREVENTIVE CONSERVATION

   Environmental Controls:
   • Temperature: 18-22°C (64-72°F)
   • Relative humidity: 45-55%
   • Light levels: <150 lux for sensitive materials
   • UV filtration on all light sources

   Handling & Display:
   • Proper mounting and support systems
   • Protection from physical contact
   • Regular monitoring and condition checks

9. ETHICAL CONSIDERATIONS

   Following international conservation ethics (ICOM-CC, AIC):
   • Minimal intervention principle
   • Reversibility of all treatments
   • Documentation of all procedures
   • Respect for original artist's intent

10. DOCUMENTATION & REPORTING

    Essential records to maintain:
    • Before, during, and after treatment photographs
    • Written treatment reports
    • Material samples and analysis results
    • Conservation decision rationale

══════════════════════════════════════════════════════════

CONCLUSION:

This restoration project requires a balanced approach combining historical accuracy, technical expertise, and cultural sensitivity. The {damage_type or 'damage'} can be addressed through systematic conservation methods while preserving the artwork's integrity.

All treatments should prioritize long-term stability and maintain the artwork's research and cultural value.

══════════════════════════════════════════════════════════

IMPORTANT DISCLAIMER:
This analysis is advisory only. All physical restoration work must be performed by certified professional conservators following appropriate institutional guidelines.

══════════════════════════════════════════════════════════
"""
                    st.rerun()
            else:
                st.error("Please provide an artwork description to proceed.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ==================== TAB 2: FEATURE GALLERY ====================
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<span class="section-eyebrow">All Capabilities</span>', unsafe_allow_html=True)
        st.markdown('<h2 style="font-family: \'Cormorant Garamond\', serif; font-size: 2rem; color: var(--gold-light); margin-top: 0;">Feature Gallery</h2>', unsafe_allow_html=True)

        features = [
            {"icon": "🎭", "title": "Period-Specific Restoration",
             "desc": "Expert restoration guidance for Baroque and Renaissance artworks using historically accurate techniques",
             "cases": ["Renaissance portraits with sfumato technique", "Baroque paintings with dramatic chiaroscuro", "Dutch Golden Age realistic lighting", "Rococo delicate pastels and gold leaf"]},
            {"icon": "🕌", "title": "Cultural Pattern Enhancement",
             "desc": "Restore and enhance traditional patterns from Mughal, Islamic, Celtic, Asian, and indigenous arts",
             "cases": ["Mughal miniature floral borders", "Islamic geometric tessellations", "Celtic knotwork patterns", "Japanese ukiyo-e wave patterns"]},
            {"icon": "🗿", "title": "Sculptural Reconstruction",
             "desc": "Reconstruct eroded or damaged features in sculptures, statues, and three-dimensional artifacts",
             "cases": ["Greek/Roman marble statues", "Indian temple sculptures", "Egyptian hieroglyphic carvings", "Mayan stele reconstructions"]},
            {"icon": "🧵", "title": "Textile & Tapestry Repair",
             "desc": "Expert restoration for tapestries, embroidery, historical fabrics, and woven artifacts",
             "cases": ["Medieval tapestries (Bayeux style)", "Chinese silk embroidery", "Indian Banarasi sarees", "Persian carpets"]},
            {"icon": "🎨", "title": "Abstract & Modern Art Recovery",
             "desc": "Restore contemporary, abstract, expressionist, and modern artworks",
             "cases": ["Pollock drip paintings", "Rothko color fields", "Abstract impressionism texture recovery", "Minimalist hard-edge works"]},
            {"icon": "📜", "title": "Ancient Manuscript Conservation",
             "desc": "Restore illuminated manuscripts, scrolls, codices, and historical documents",
             "cases": ["Book of Kells style illuminations", "Arabic/Persian calligraphy scrolls", "Sanskrit palm leaf manuscripts", "Dead Sea Scrolls preservation"]},
            {"icon": "🏛️", "title": "Mural & Fresco Revival",
             "desc": "Restore wall paintings, cave art, frescoes, and architectural murals",
             "cases": ["Ajanta/Ellora cave paintings", "Roman Pompeii frescoes", "Mexican muralism (Diego Rivera style)", "Aboriginal rock art"]},
            {"icon": "🏺", "title": "Ceramic & Pottery Reconstruction",
             "desc": "Restore pottery, porcelain, ceramic vessels, and glazed artifacts",
             "cases": ["Chinese Ming dynasty porcelain", "Greek amphoras and pottery", "Native American pottery", "Japanese raku ceramics"]},
            {"icon": "🔯", "title": "Symbol & Iconography Interpretation",
             "desc": "Decode and restore symbolic elements, religious imagery, inscriptions, and cultural icons",
             "cases": ["Egyptian hieroglyphics interpretation", "Christian iconography (Byzantine style)", "Hindu temple symbolism", "Mayan glyph decoding"]},
            {"icon": "🎓", "title": "Educational Content Generation",
             "desc": "Create engaging museum descriptions, exhibition content, and educational materials",
             "cases": ["Museum placard content", "Virtual exhibition descriptions", "Educational tour scripts", "Accessibility-friendly art explanations"]}
        ]

        def safe_rerun():
            if hasattr(st, 'experimental_rerun'):
                try:
                    st.experimental_rerun()
                    return
                except Exception:
                    pass
            try:
                from streamlit.runtime.scriptrunner import RerunException
                raise RerunException()
            except Exception:
                st.session_state['_rerun_trigger'] = not st.session_state.get('_rerun_trigger', False)

        cases = []
        for f in features:
            for case in f['cases']:
                cases.append({"case": case, "feature": f['title']})

        import random

        if 'quiz_questions' not in st.session_state:
            pool = cases.copy()
            num_q = min(6, max(3, len(pool)))
            sample = random.sample(pool, num_q)
            titles = [f['title'] for f in features]
            questions = []
            for s in sample:
                correct = s['feature']
                wrongs = [t for t in titles if t != correct]
                choices = random.sample(wrongs, min(3, len(wrongs))) + [correct]
                random.shuffle(choices)
                questions.append({'prompt': s['case'], 'correct': correct, 'choices': choices})
            st.session_state.quiz_questions = questions
            st.session_state.q_index = 0
            st.session_state.score = 0

        st.markdown("""
        <div class="quiz-header">
            <h3>Knowledge Quiz</h3>
            <p>Match each use case to the correct AI restoration feature.</p>
        </div>
        """, unsafe_allow_html=True)

        questions = st.session_state.quiz_questions
        qidx = st.session_state.q_index

        if qidx < len(questions):
            q = questions[qidx]
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                <span class="badge-gold">Question {qidx+1} of {len(questions)}</span>
                <span class="badge-teal">Score: {st.session_state.score}</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background: rgba(17,24,39,0.6); border: 1px solid var(--border); border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1.5rem; color: var(--text-primary); font-size: 1.05rem; font-style: italic; border-left: 3px solid var(--gold);">
                "{q['prompt']}"
            </div>
            """, unsafe_allow_html=True)

            selected = st.radio('Which feature best matches this use case?', q['choices'], key=f'choice_{qidx}')
            if st.button('Submit Answer →', key=f'submit_{qidx}'):
                if selected == q['correct']:
                    st.session_state.score += 1
                    st.success('✓ Correct — well done!')
                else:
                    st.error(f"✗ The correct answer was: {q['correct']}")
                st.session_state.q_index += 1
                safe_rerun()
        else:
            total = len(questions)
            score = st.session_state.score
            pct = int((score / total) * 100)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(201,168,76,0.12), rgba(45,212,191,0.08)); border: 1px solid var(--border); border-radius: 16px; padding: 2rem; text-align: center; margin-bottom: 1.5rem;">
                <div style="font-family: 'Cormorant Garamond', serif; font-size: 3.5rem; color: var(--gold-light); line-height: 1;">{score}/{total}</div>
                <div style="color: var(--text-muted); font-family: 'DM Mono', monospace; font-size: 0.75rem; letter-spacing: 3px; text-transform: uppercase; margin-top: 0.5rem;">Quiz Complete · {pct}% Accuracy</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button('Play Again', key='quiz_restart'):
                del st.session_state.quiz_questions
                del st.session_state.q_index
                del st.session_state.score
                safe_rerun()

        with st.expander('View Full Feature Gallery'):
            for feature in features:
                cases_html = "".join([f"<li style='color: #9ba3b4; font-size: 0.88rem;'>{case}</li>" for case in feature['cases']])
                st.markdown(f"""
                <div style="background: rgba(17,24,39,0.6); border: 1px solid var(--border); border-radius: 14px; padding: 1.5rem; margin-bottom: 1rem; border-left: 3px solid var(--gold);">
                    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.8rem;">
                        <span style="font-size: 1.8rem;">{feature['icon']}</span>
                        <div>
                            <div style="font-family: 'Cormorant Garamond', serif; font-size: 1.2rem; color: var(--gold-light);">{feature['title']}</div>
                            <div style="color: var(--text-muted); font-size: 0.82rem; margin-top: 0.2rem;">{feature['desc']}</div>
                        </div>
                    </div>
                    <ul style="margin: 0; padding-left: 1.2rem;">{cases_html}</ul>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ==================== TAB 3: CULTURAL INSIGHTS ====================
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<span class="section-eyebrow">Heritage Knowledge Base</span>', unsafe_allow_html=True)
        st.markdown('<h2 style="font-family: \'Cormorant Garamond\', serif; font-size: 2rem; color: var(--gold-light); margin-top: 0;">Cultural & Historical Insights</h2>', unsafe_allow_html=True)

        insight_type = st.selectbox(
            "Select Art Period or Cultural Tradition",
            ["Renaissance (Italian)", "Baroque (European)", "Rococo (French)",
             "Indian Mughal Art", "Indian Rajput Painting", "Islamic Art & Calligraphy",
             "Japanese Ukiyo-e", "Chinese Ming Dynasty", "Byzantine Art",
             "Egyptian Art", "Greek Classical Art", "Aboriginal Australian Art"],
            key="cultural_insight_select"
        )

        cultural_insights = {
            "Renaissance (Italian)": {
                "emoji": "🎨", "period": "14th–17th Century",
                "background": "The Renaissance marked a cultural rebirth in Europe, emphasizing humanism, naturalism, and classical learning. Artists like Leonardo da Vinci, Michelangelo, and Raphael revolutionized art with techniques like linear perspective, sfumato, and anatomical accuracy.",
                "importance": "Renaissance art represents a pivotal shift from medieval symbolism to realistic representation. It laid the foundation for Western art and introduced techniques still used today. The period's emphasis on individual expression and scientific observation changed how humans viewed themselves.",
                "restoration": "Renaissance paintings require extreme care due to fragile egg tempera and oil layers. Restoration must preserve original glazing techniques, gold leaf applications, and the delicate balance of light and shadow. Modern conservators use non-invasive imaging before any intervention.",
                "techniques": ["Linear Perspective", "Sfumato (Leonardo's technique)", "Chiaroscuro (light/shadow)", "Contrapposto (natural poses)", "Oil glazing layers"],
                "famous_works": ["Mona Lisa", "The Last Supper", "Sistine Chapel Ceiling", "The Birth of Venus"]
            },
            "Baroque (European)": {
                "emoji": "✨", "period": "17th–18th Century",
                "background": "Baroque art emerged as a dramatic, emotional response to the Protestant Reformation. Characterized by intense emotion, movement, and theatrical lighting, it was used by the Catholic Church to inspire faith through grandeur and spectacle.",
                "importance": "Baroque art revolutionized emotional expression in painting and sculpture. Artists like Caravaggio, Rembrandt, and Rubens created works with unprecedented drama and realism.",
                "restoration": "Baroque works often feature heavy impasto, dramatic chiaroscuro, and dark varnish layers. Restoration requires careful varnish removal to reveal original colors while preserving the intentional darkness that creates dramatic effects.",
                "techniques": ["Tenebrism (dramatic contrast)", "Dynamic composition", "Rich color palette", "Emotional intensity", "Movement and energy"],
                "famous_works": ["The Night Watch", "Ecstasy of Saint Teresa", "Las Meninas", "The Calling of St Matthew"]
            },
            "Rococo (French)": {
                "emoji": "🌸", "period": "18th Century",
                "background": "Rococo emerged as a lighter, more playful reaction to Baroque grandeur. Characterized by pastel colors, delicate ornamentation, and themes of romance and leisure, it flourished in French aristocratic salons.",
                "importance": "Rococo art captured the elegance and refinement of 18th-century aristocratic culture. Its emphasis on pleasure, intimacy, and decorative beauty influenced interior design, fashion, and the decorative arts.",
                "restoration": "Rococo works often feature delicate pastel pigments, gold leaf, and intricate detail. Restoration requires preserving the lightness and airiness of the style while addressing fading and deterioration of fragile materials.",
                "techniques": ["Pastel color palette", "Asymmetric curves", "Gold leaf detailing", "Delicate brushwork", "Playful subject matter"],
                "famous_works": ["The Swing", "Pilgrimage to Cythera", "Diana Leaving Her Bath", "Rococo interiors of Versailles"]
            },
            "Indian Mughal Art": {
                "emoji": "🕌", "period": "16th–19th Century",
                "background": "Mughal miniature paintings blend Persian, Indian, and Islamic artistic traditions. Created for royal courts, these intricate works depicted historical events, court life, flora, and fauna with meticulous detail and vibrant colors.",
                "importance": "Mughal art represents a unique synthesis of diverse cultural influences, documenting historical events and showcasing the sophistication of Mughal court culture.",
                "restoration": "Mughal miniatures are painted on paper with natural pigments and gold. Restoration must address insect damage, pigment fading, and paper deterioration while preserving delicate gold leaf work.",
                "techniques": ["Fine brushwork (single hair brushes)", "Natural mineral pigments", "Gold leaf application", "Intricate border patterns", "Layered composition"],
                "famous_works": ["Hamzanama manuscripts", "Akbarnama", "Padshahnama", "Baburnama illustrations"]
            },
            "Indian Rajput Painting": {
                "emoji": "🎭", "period": "16th–19th Century",
                "background": "Rajput paintings from various royal courts depicted Hindu mythology, poetry, and courtly life. These works are known for bold colors, emotional expression, and spiritual themes, particularly illustrations of Krishna and Radha.",
                "importance": "Rajput art preserved Hindu religious narratives and courtly culture. Each school developed distinctive styles contributing to India's diverse artistic heritage.",
                "restoration": "Similar to Mughal art but with distinctive regional techniques. Rajput works often use more vibrant colors and thicker paper. Conservation must respect religious symbolism.",
                "techniques": ["Bold flat colors", "Expressive faces and gestures", "Symbolic use of color", "Poetry-inspired compositions", "Regional stylistic variations"],
                "famous_works": ["Bani Thani (Kishangarh)", "Ragamala paintings", "Krishna Lila series", "Mewar Ramayana"]
            },
            "Islamic Art & Calligraphy": {
                "emoji": "🕌", "period": "7th Century–Present",
                "background": "Islamic art emphasizes geometric patterns, arabesques, and calligraphy due to religious restrictions on figurative representation. Quranic verses become art through elaborate scripts like Kufic, Naskh, and Thuluth.",
                "importance": "Islamic art demonstrates how religious principles can inspire mathematical precision and aesthetic beauty. Calligraphy elevates written language to divine art.",
                "restoration": "Islamic manuscripts and architectural decorations require specialized knowledge of Arabic scripts and geometric principles. Symmetry and pattern integrity must be preserved.",
                "techniques": ["Sacred geometry", "Arabesque patterns", "Illuminated manuscripts", "Tilework (zellige)", "Various calligraphic scripts"],
                "famous_works": ["Blue Quran", "Alhambra decorations", "Topkapi manuscripts", "Isfahan mosque tiles"]
            },
            "Japanese Ukiyo-e": {
                "emoji": "🎌", "period": "17th–19th Century",
                "background": "Ukiyo-e are woodblock prints depicting kabuki actors, beautiful women, landscapes, and everyday life in Edo-period Japan. Artists like Hokusai and Hiroshige influenced Western Impressionism.",
                "importance": "Ukiyo-e democratized art in Japan and profoundly influenced European artists like Van Gogh and Monet, showcasing masterful composition and color gradation.",
                "restoration": "Woodblock prints are vulnerable to light damage, foxing, and paper degradation. Restoration requires understanding traditional Japanese papermaking and printing techniques.",
                "techniques": ["Woodblock printing", "Bokashi (color gradation)", "Bold outlines", "Flat color areas", "Asymmetric composition"],
                "famous_works": ["The Great Wave", "Thirty-Six Views of Mt. Fuji", "Fifty-Three Stations of Tokaido", "Beauties of the Yoshiwara"]
            },
            "Chinese Ming Dynasty": {
                "emoji": "🐉", "period": "14th–17th Century",
                "background": "Ming Dynasty art revived classical Chinese traditions. Known for blue and white porcelain, landscape paintings, and calligraphy, Ming artists emphasized harmony between humans and nature.",
                "importance": "Ming art represents the pinnacle of Chinese ceramic production and landscape painting. The period's artistic output influenced global trade and aesthetic preferences worldwide.",
                "restoration": "Ming ceramics require specialized knowledge of high-fire techniques and cobalt pigments. Paintings on silk demand extreme care due to material fragility.",
                "techniques": ["Blue and white porcelain", "Monochrome ink landscapes", "Calligraphic painting", "Scholar's rocks", "Court painting traditions"],
                "famous_works": ["Ming vases", "Shen Zhou landscapes", "Tang Yin paintings", "Imperial porcelain"]
            },
            "Byzantine Art": {
                "emoji": "☦️", "period": "4th–15th Century",
                "background": "Byzantine art served the Eastern Orthodox Church, creating iconic religious images with gold backgrounds, frontal poses, and spiritual symbolism. Mosaics and icons were designed to inspire devotion.",
                "importance": "Byzantine art preserved classical traditions through the medieval period and established the visual language of Orthodox Christianity.",
                "restoration": "Byzantine mosaics and icons require specialized conservation of gold leaf, tempera on wood panels, and glass tesserae. Religious protocols must be observed.",
                "techniques": ["Gold leaf backgrounds", "Egg tempera", "Mosaic tesserae", "Hierarchical scaling", "Symbolic color use"],
                "famous_works": ["Hagia Sophia mosaics", "Vladimir Mother of God", "Ravenna mosaics", "Christ Pantocrator"]
            },
            "Egyptian Art": {
                "emoji": "🏛️", "period": "3000–30 BCE",
                "background": "Ancient Egyptian art served religious and political purposes, depicting gods, pharaohs, and the afterlife. The strict artistic conventions lasted for millennia, demonstrating extraordinary cultural continuity.",
                "importance": "Egyptian art provides insight into one of history's longest-lasting civilizations. Tomb paintings, sculptures, and hieroglyphics preserved knowledge for over 3,000 years.",
                "restoration": "Egyptian artifacts require climate control due to their age. Pigments derived from minerals need careful stabilization. Many works involve stone, papyrus, or plaster.",
                "techniques": ["Hierarchical scale", "Composite view", "Register composition", "Symbolic color", "Relief carving"],
                "famous_works": ["Tutankhamun's mask", "Nefertiti bust", "Tomb of Nefertari", "Book of the Dead papyri"]
            },
            "Greek Classical Art": {
                "emoji": "🏛️", "period": "5th–4th Century BCE",
                "background": "Classical Greek art emphasized ideal beauty, proportion, and naturalism. Sculptors like Phidias and Praxiteles created works embodying philosophical ideals of harmony and balance.",
                "importance": "Greek classical art established standards of beauty and proportion that shaped Western civilization, influencing art, architecture, and aesthetics for millennia.",
                "restoration": "Ancient Greek sculptures often survive as Roman copies or fragments. Restoration involves careful cleaning of marble and ethical decisions about reconstruction.",
                "techniques": ["Contrapposto stance", "Golden ratio proportions", "Idealized naturalism", "Bronze hollow-casting", "Polychrome marble"],
                "famous_works": ["Parthenon sculptures", "Discobolus", "Venus de Milo", "Winged Victory"]
            },
            "Aboriginal Australian Art": {
                "emoji": "🪃", "period": "40,000+ years–Present",
                "background": "Aboriginal art is one of the world's oldest continuous art traditions, depicting Dreamtime stories, ancestral beings, and connection to land. Rock paintings and dot paintings encode spiritual knowledge.",
                "importance": "Aboriginal art represents humanity's oldest living art tradition, preserving tens of thousands of years of cultural knowledge inseparable from spiritual beliefs and connection to country.",
                "restoration": "Aboriginal art restoration requires consultation with traditional owners and respect for sacred content. Rock art conservation must consider environmental exposure.",
                "techniques": ["Dot painting", "X-ray art (showing internal organs)", "Natural ochre pigments", "Symbolic mapping", "Layered narratives"],
                "famous_works": ["Bradshaw paintings", "X-ray art (Kakadu)", "Papunya Tula movement", "Wandjina spirit figures"]
            }
        }

        if insight_type in cultural_insights:
            insight = cultural_insights[insight_type]
            st.markdown(f"""
            <div class="insight-header">
                <div style="font-size: 3rem; margin-bottom: 0.8rem;">{insight['emoji']}</div>
                <div style="font-family: 'Cormorant Garamond', serif; font-size: 2.2rem; color: var(--text-primary); font-weight: 300;">{insight_type}</div>
                <div style="margin-top: 0.5rem;"><span class="badge-teal">📅 {insight['period']}</span></div>
            </div>
            """, unsafe_allow_html=True)

            sections = [
                ("📖", "Historical Background", insight['background'], "var(--gold)"),
                ("⭐", "Cultural Importance", insight['importance'], "var(--teal)"),
                ("🛠️", "Restoration Considerations", insight['restoration'], "#a78bfa"),
            ]
            for icon, title, content, color in sections:
                st.markdown(f"""
                <div style="background: rgba(17,24,39,0.6); border: 1px solid {color}25; border-left: 3px solid {color}; border-radius: 12px; padding: 1.5rem 2rem; margin-bottom: 1.2rem;">
                    <div style="font-family: 'Cormorant Garamond', serif; font-size: 1.1rem; color: {color}; margin-bottom: 0.8rem; letter-spacing: 0.5px;">{icon} {title}</div>
                    <p style="color: #b0bbc8; font-size: 0.92rem; line-height: 1.75; margin: 0;">{content}</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div style="font-family: 'Cormorant Garamond', serif; font-size: 1.1rem; color: var(--gold-light); margin: 1.5rem 0 1rem 0; letter-spacing: 0.5px;">🎨 Key Artistic Techniques</div>
            """, unsafe_allow_html=True)
            cols = st.columns(2)
            for idx, technique in enumerate(insight['techniques']):
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div style="background: rgba(17,24,39,0.5); border: 1px solid var(--border); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.8rem;">
                        <div class="milestone-dot"></div>
                        <span style="color: var(--text-primary); font-size: 0.9rem;">{technique}</span>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("""
            <div style="font-family: 'Cormorant Garamond', serif; font-size: 1.1rem; color: var(--gold-light); margin: 1.5rem 0 1rem 0;">🖼️ Famous Masterpieces</div>
            """, unsafe_allow_html=True)
            for work in insight['famous_works']:
                st.markdown(f"""
                <div style="background: rgba(17,24,39,0.5); border: 1px solid var(--border); border-radius: 10px; padding: 0.8rem 1.2rem; margin-bottom: 0.6rem; display: flex; align-items: center; gap: 1rem;">
                    <span style="color: var(--gold); font-size: 1.1rem;">◆</span>
                    <span style="color: var(--text-primary); font-size: 0.92rem; font-family: 'Cormorant Garamond', serif; font-size: 1.05rem;">{work}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ==================== TAB 4: AI RESTORATION TIMELINE PLANNER ====================
    with tab4:
        st.markdown("""
        <div style="background:rgba(26,37,64,0.5);border:1px solid rgba(201,168,76,0.25);border-radius:20px;padding:2.5rem;margin-bottom:2rem;backdrop-filter:blur(15px);">
            <span style="font-family:'DM Mono',monospace;font-size:0.65rem;color:#2dd4bf;letter-spacing:4px;text-transform:uppercase;margin-bottom:0.8rem;display:block;">Project Planning Tool</span>
            <div style="font-family:'Cormorant Garamond',serif;font-size:2rem;color:#e4c47e;margin-top:0;">AI Restoration Timeline Planner</div>
            <p style="color:#9ba3b4;font-size:0.92rem;margin-top:0.8rem;line-height:1.6;">Configure your project parameters and receive a detailed phase-by-phase restoration timeline with risk assessments, milestones, and scheduling recommendations.</p>
        </div>
        """, unsafe_allow_html=True)

        # ---- INPUTS ----
        st.markdown("""
        <div style="background:rgba(17,24,39,0.6);border:1px solid rgba(201,168,76,0.25);border-radius:16px;padding:1.5rem 2rem;margin-bottom:1.5rem;">
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:#2dd4bf;margin-bottom:0.5rem;">Project Parameters</div>
        </div>
        """, unsafe_allow_html=True)

        tl_col1, tl_col2 = st.columns(2)
        with tl_col1:
            tl_artwork_type = st.selectbox("Artwork Type", [
                "Oil Painting", "Watercolor on Paper", "Stone Sculpture",
                "Bronze Sculpture", "Textile / Tapestry", "Illuminated Manuscript",
                "Mural / Fresco", "Ceramic / Pottery", "Mixed Media"
            ], key="tl_art_type")
            tl_damage_severity = st.select_slider("Damage Severity", options=[
                "Minimal (surface dust/light scratches)",
                "Moderate (fading, minor losses)",
                "Significant (structural cracks, major losses)",
                "Severe (major structural damage, 50%+ loss)",
                "Critical (near-total deterioration)"
            ], value="Moderate (fading, minor losses)", key="tl_damage")
            tl_size = st.selectbox("Artwork Scale", [
                "Small (< 30cm)", "Medium (30-100cm)", "Large (100-200cm)",
                "Very Large (> 200cm)", "Monumental (architectural scale)"
            ], key="tl_size")

        with tl_col2:
            tl_urgency = st.selectbox("Project Urgency", [
                "Flexible (timeline open)", "Standard (6-12 months)",
                "Priority (3-6 months)", "Urgent (< 3 months)"
            ], key="tl_urgency")
            tl_team_size = st.select_slider("Conservation Team Size", options=[
                "Solo conservator", "2-3 specialists", "4-6 person team", "Large institutional team (7+)"
            ], value="2-3 specialists", key="tl_team")
            tl_goals = st.multiselect("Restoration Goals", [
                "Stabilisation only", "Full visual restoration",
                "Scientific documentation", "Public exhibition prep",
                "Digital archiving", "Loan/transport preparation",
                "Educational reproduction", "Insurance documentation"
            ], default=["Stabilisation only", "Full visual restoration"], key="tl_goals")

        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

        if st.button("Generate Restoration Timeline →", key="gen_timeline"):
            damage_map = {
                "Minimal (surface dust/light scratches)": (1, "LOW"),
                "Moderate (fading, minor losses)": (2, "MEDIUM"),
                "Significant (structural cracks, major losses)": (3, "HIGH"),
                "Severe (major structural damage, 50%+ loss)": (4, "HIGH"),
                "Critical (near-total deterioration)": (5, "HIGH")
            }
            size_map = {
                "Small (< 30cm)": 0.7, "Medium (30-100cm)": 1.0,
                "Large (100-200cm)": 1.4, "Very Large (> 200cm)": 1.8,
                "Monumental (architectural scale)": 2.5
            }
            urgency_map = {
                "Flexible (timeline open)": 1.0, "Standard (6-12 months)": 0.85,
                "Priority (3-6 months)": 0.65, "Urgent (< 3 months)": 0.45
            }
            team_map = {
                "Solo conservator": 1.3, "2-3 specialists": 1.0,
                "4-6 person team": 0.75, "Large institutional team (7+)": 0.55
            }

            dmg_level, risk_base = damage_map[tl_damage_severity]
            size_f = size_map[tl_size]
            urg_f = urgency_map[tl_urgency]
            team_f = team_map[tl_team_size]

            def calc_weeks(base_w):
                return max(1, round(base_w * (dmg_level / 2) * size_f * urg_f * team_f))

            phases = [
                {
                    "phase": "Phase 01", "icon": "🔬",
                    "title": "Assessment & Documentation",
                    "weeks": calc_weeks(3),
                    "color": "#2dd4bf",
                    "tasks": [
                        ("Comprehensive visual inspection and condition mapping", "HIGH", "#ef4444"),
                        ("UV fluorescence, X-radiography, infrared reflectography", "HIGH", "#ef4444"),
                        ("Material sampling and scientific analysis", "MEDIUM", "#c9a84c"),
                        ("Historical research, provenance and archival study", "MEDIUM", "#c9a84c"),
                        ("Photographic documentation (raking light, multispectral)", "LOW", "#2dd4bf"),
                    ],
                    "milestone": "Condition Report & Treatment Proposal approved by stakeholders",
                    "deliverable": "Detailed Condition Report"
                },
                {
                    "phase": "Phase 02", "icon": "🛡️",
                    "title": "Emergency Stabilisation",
                    "weeks": calc_weeks(2),
                    "color": "#ef4444",
                    "tasks": [
                        ("Consolidation of flaking or delaminating paint layers", "HIGH", "#ef4444"),
                        ("Structural support for fragile or cracked substrate", "HIGH", "#ef4444"),
                        ("Local facing of vulnerable areas prior to treatment", "MEDIUM", "#c9a84c"),
                        ("Climate and environmental stabilisation measures", "LOW", "#2dd4bf"),
                    ],
                    "milestone": "Artwork structurally stable and safe to proceed",
                    "deliverable": "Stabilisation Report"
                },
                {
                    "phase": "Phase 03", "icon": "🧹",
                    "title": "Surface Cleaning & Preparation",
                    "weeks": calc_weeks(4),
                    "color": "#c9a84c",
                    "tasks": [
                        ("Dry mechanical cleaning — removal of surface deposits", "LOW", "#2dd4bf"),
                        ("Solvent-based cleaning of discoloured varnish layers", "HIGH", "#ef4444"),
                        ("Aqueous cleaning where appropriate (pH controlled)", "MEDIUM", "#c9a84c"),
                        ("Removal of previous incompatible restorations or overpaints", "HIGH", "#ef4444"),
                        ("Final surface preparation and assessment of revealed original", "MEDIUM", "#c9a84c"),
                    ],
                    "milestone": "Original surface fully accessible and documented",
                    "deliverable": "Cleaning Test Records & Solubility Maps"
                },
                {
                    "phase": "Phase 04", "icon": "🔧",
                    "title": "Structural Conservation",
                    "weeks": calc_weeks(3) if dmg_level >= 3 else 0,
                    "color": "#a78bfa",
                    "tasks": [
                        ("Structural consolidation of substrate (relining, cradling)", "HIGH", "#ef4444"),
                        ("Loss filling with conservation-grade fills", "MEDIUM", "#c9a84c"),
                        ("Surface texture work to match surrounding original", "MEDIUM", "#c9a84c"),
                        ("Adhesive consolidation of all previously loose elements", "LOW", "#2dd4bf"),
                    ],
                    "milestone": "Structural integrity fully restored",
                    "deliverable": "Structural Treatment Report"
                },
                {
                    "phase": "Phase 05", "icon": "🎨",
                    "title": "Aesthetic Restoration & Inpainting",
                    "weeks": calc_weeks(5),
                    "color": "#c9a84c",
                    "tasks": [
                        ("Colour matching and reference sample creation", "HIGH", "#ef4444"),
                        ("Inpainting of losses using reversible conservation media", "HIGH", "#ef4444"),
                        ("Texture recreation to integrate losses with original surface", "HIGH", "#ef4444"),
                        ("Intermediate varnish application for visual unification", "MEDIUM", "#c9a84c"),
                        ("Chromatic reintegration review with client / curator", "MEDIUM", "#c9a84c"),
                    ],
                    "milestone": "Visual reintegration approved — aesthetic integrity restored",
                    "deliverable": "Inpainting Log & Photographic Record"
                },
                {
                    "phase": "Phase 06", "icon": "✅",
                    "title": "Final Varnishing, Review & Handover",
                    "weeks": calc_weeks(2),
                    "color": "#2dd4bf",
                    "tasks": [
                        ("Application of final protective varnish (reversible, UV-stable)", "MEDIUM", "#c9a84c"),
                        ("Full post-treatment documentation photography", "LOW", "#2dd4bf"),
                        ("Preparation of final conservation treatment report", "HIGH", "#ef4444"),
                        ("Client review, sign-off and handover", "LOW", "#2dd4bf"),
                        ("Long-term care and preventive conservation guidance issued", "LOW", "#2dd4bf"),
                    ],
                    "milestone": "Project complete — artwork delivered with full documentation",
                    "deliverable": "Final Conservation Report & Certificate"
                }
            ]

            active_phases = [p for p in phases if p["weeks"] > 0]
            total_weeks = sum(p["weeks"] for p in active_phases)
            total_months = round(total_weeks / 4.3, 1)

            # ---- SUMMARY STATS ----
            st.markdown("""
            <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(201,168,76,0.3),transparent);margin:1.5rem 0;"></div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.5rem;color:#f0ece4;margin-bottom:1rem;font-weight:300;">Project Summary</div>
            """, unsafe_allow_html=True)

            s1, s2, s3, s4 = st.columns(4)
            for col, val, lbl in [(s1, f"{total_weeks}w", "Total Duration"),
                                   (s2, f"{total_months}mo", "Est. Months"),
                                   (s3, str(len(active_phases)), "Phases"),
                                   (s4, risk_base, "Risk Level")]:
                with col:
                    st.markdown(f"""
                    <div style="background:rgba(17,24,39,0.8);border:1px solid rgba(201,168,76,0.25);border-radius:14px;padding:1.5rem;text-align:center;">
                        <div style="font-family:'Cormorant Garamond',serif;font-size:2.5rem;color:#e4c47e;line-height:1;">{val}</div>
                        <div style="font-size:0.7rem;color:#9ba3b4;text-transform:uppercase;letter-spacing:2px;font-family:'DM Mono',monospace;margin-top:0.5rem;">{lbl}</div>
                    </div>
                    """, unsafe_allow_html=True)

            if tl_urgency == "Urgent (< 3 months)" and total_weeks > 12:
                st.warning(f"Urgent timeline selected but estimated duration is {total_weeks} weeks. Consider expanding team size or reducing scope.")

            # ---- PHASE CARDS using native Streamlit ----
            st.markdown("""
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.5rem;color:#f0ece4;margin:2rem 0 1rem;font-weight:300;">Phase-by-Phase Timeline</div>
            """, unsafe_allow_html=True)

            running_week = 0
            for i, phase in enumerate(active_phases):
                start_w = running_week + 1
                end_w = running_week + phase["weeks"]
                running_week = end_w
                bar_pct = int((phase["weeks"] / max(total_weeks, 1)) * 100)
                ph_color = phase["color"]

                # Phase header
                st.markdown(f"""
                <div style="background:rgba(26,37,64,0.55);border:1px solid {ph_color}44;border-left:4px solid {ph_color};border-radius:14px;padding:1.4rem 1.8rem;margin-top:1rem;">
                    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;">
                        <div>
                            <div style="font-family:'DM Mono',monospace;font-size:0.6rem;color:{ph_color};letter-spacing:3px;text-transform:uppercase;">{phase["phase"]} &nbsp;·&nbsp; {phase["icon"]}</div>
                            <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:#e4c47e;margin:0.3rem 0;">{phase["title"]}</div>
                            <div style="display:inline-block;background:rgba(201,168,76,0.12);border:1px solid rgba(201,168,76,0.3);color:#e4c47e;padding:0.2rem 0.7rem;border-radius:20px;font-size:0.75rem;font-family:'DM Mono',monospace;">
                                Weeks {start_w}–{end_w} &nbsp;·&nbsp; {phase["weeks"]} week{"s" if phase["weeks"] != 1 else ""}
                            </div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:0.65rem;color:#9ba3b4;font-family:'DM Mono',monospace;letter-spacing:2px;text-transform:uppercase;">Share of total</div>
                            <div style="font-family:'Cormorant Garamond',serif;font-size:2rem;color:{ph_color};">{bar_pct}%</div>
                        </div>
                    </div>
                    <div style="height:5px;background:rgba(10,14,26,0.5);border-radius:4px;margin:1rem 0;overflow:hidden;">
                        <div style="width:{bar_pct}%;height:100%;background:linear-gradient(90deg,{ph_color}66,{ph_color});border-radius:4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Tasks
                for task_text, priority, t_color in phase["tasks"]:
                    st.markdown(f"""
                    <div style="background:rgba(10,14,26,0.45);border-left:2px solid {t_color};padding:0.55rem 1rem;border-radius:0 8px 8px 0;margin:0.4rem 1rem 0.4rem 2rem;display:flex;align-items:center;justify-content:space-between;gap:1rem;">
                        <span style="color:#9ba3b4;font-size:0.83rem;">{task_text}</span>
                        <span style="background:rgba(0,0,0,0.3);border:1px solid {t_color}55;color:{t_color};padding:0.15rem 0.55rem;border-radius:20px;font-size:0.68rem;font-family:'DM Mono',monospace;white-space:nowrap;">{priority}</span>
                    </div>
                    """, unsafe_allow_html=True)

                # Milestone + Deliverable
                st.markdown(f"""
                <div style="background:rgba(201,168,76,0.05);border:1px dashed rgba(201,168,76,0.25);border-radius:10px;padding:0.75rem 1.2rem;margin:0.8rem 1rem 0 1rem;display:flex;align-items:center;gap:0.8rem;">
                    <div style="width:10px;height:10px;background:#c9a84c;border-radius:50%;box-shadow:0 0 10px rgba(201,168,76,0.5);flex-shrink:0;"></div>
                    <div>
                        <div style="font-family:'DM Mono',monospace;font-size:0.58rem;color:#c9a84c;letter-spacing:2px;text-transform:uppercase;">Milestone</div>
                        <div style="color:#f0ece4;font-size:0.85rem;margin-top:0.15rem;">{phase["milestone"]}</div>
                    </div>
                </div>
                <div style="margin:0.5rem 1rem 0.8rem 1rem;">
                    <span style="color:#9ba3b4;font-size:0.7rem;font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;">Deliverable → </span>
                    <span style="background:rgba(45,212,191,0.1);border:1px solid rgba(45,212,191,0.3);color:#2dd4bf;padding:0.2rem 0.6rem;border-radius:20px;font-size:0.72rem;font-family:'DM Mono',monospace;">{phase["deliverable"]}</span>
                </div>
                """, unsafe_allow_html=True)

                if i < len(active_phases) - 1:
                    st.markdown("""
                    <div style="text-align:center;color:#9ba3b4;font-size:1.2rem;margin:0.3rem 0;">↓</div>
                    """, unsafe_allow_html=True)

            # ---- RECOMMENDATIONS ----
            st.markdown("""
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.5rem;color:#f0ece4;margin:2rem 0 1rem;font-weight:300;">Planning Recommendations</div>
            """, unsafe_allow_html=True)

            rec_items = []
            if dmg_level >= 4:
                rec_items.append(("🚨", "HIGH", "#ef4444", "Immediate structural stabilisation is critical. Do not proceed to cleaning before securing all fragile elements."))
            if "Scientific documentation" in tl_goals:
                rec_items.append(("🔬", "MEDIUM", "#c9a84c", "Allow additional 2-3 weeks for laboratory analysis. Partner with a university conservation science department."))
            if "Public exhibition prep" in tl_goals:
                rec_items.append(("🖼️", "MEDIUM", "#c9a84c", "Build a 4-week buffer before exhibition date. Final varnish requires 2 weeks to cure under stable conditions."))
            if tl_urgency in ["Priority (3-6 months)", "Urgent (< 3 months)"]:
                rec_items.append(("⚡", "HIGH", "#ef4444", "Compressed timeline increases risk. Consider expanding team size or reducing scope to critical interventions only."))
            rec_items.append(("📋", "LOW", "#2dd4bf", "Document every intervention in a running treatment log. Photographs before, during and after each phase are mandatory."))
            rec_items.append(("🌡️", "LOW", "#2dd4bf", "Maintain stable environment throughout: 18-22°C, 45-55% RH. Fluctuations can undo treatment gains."))
            if "Digital archiving" in tl_goals:
                rec_items.append(("💾", "LOW", "#2dd4bf", "Schedule multispectral imaging at end of Phase 3 (cleaned but pre-inpainted) for the highest-quality archive record."))

            for r_icon, r_priority, r_color, r_text in rec_items:
                st.markdown(f"""
                <div style="background:rgba(17,24,39,0.6);border:1px solid {r_color}30;border-left:3px solid {r_color};border-radius:10px;padding:0.9rem 1.2rem;margin-bottom:0.7rem;display:flex;align-items:flex-start;gap:0.9rem;">
                    <span style="font-size:1.2rem;flex-shrink:0;">{r_icon}</span>
                    <div>
                        <span style="background:rgba(0,0,0,0.3);border:1px solid {r_color}55;color:{r_color};padding:0.15rem 0.55rem;border-radius:20px;font-size:0.68rem;font-family:'DM Mono',monospace;">{r_priority}</span>
                        <p style="color:#b0bbc8;font-size:0.86rem;margin:0.4rem 0 0 0;line-height:1.6;">{r_text}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ---- DOWNLOAD ----
            timeline_export = f"""ARTRESTORER AI - RESTORATION TIMELINE PLAN
Generated: {datetime.now().strftime("%B %d, %Y at %H:%M")}
Project: {st.session_state.user_data.get("name", "N/A")} | {tl_artwork_type}

PARAMETERS
Artwork Type:    {tl_artwork_type}
Damage:          {tl_damage_severity}
Scale:           {tl_size}
Team:            {tl_team_size}
Urgency:         {tl_urgency}
Goals:           {", ".join(tl_goals)}

SUMMARY
Total Duration:  {total_weeks} weeks (~{total_months} months)
Phases:          {len(active_phases)}
Risk Level:      {risk_base}

PHASES
"""
            rw = 0
            for ph in active_phases:
                sw = rw + 1; ew = rw + ph["weeks"]; rw = ew
                timeline_export += f"\n{ph['phase']}: {ph['title']}\nWeeks {sw}-{ew} ({ph['weeks']}w)\n"
                for t, p, _ in ph["tasks"]:
                    timeline_export += f"  [{p}] {t}\n"
                timeline_export += f"Milestone: {ph['milestone']}\nDeliverable: {ph['deliverable']}\n"

            st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
            st.download_button(
                label="📥 Download Timeline Plan",
                data=timeline_export,
                file_name=f"Timeline_{tl_artwork_type.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                key="dl_timeline"
            )

        st.markdown('</div>', unsafe_allow_html=True)


# ==================== RESULTS PAGE ====================
elif st.session_state.page == 'results':
    render_header()
    st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-bottom: 2.5rem;">
        <span class="section-eyebrow">Analysis Complete</span>
        <div class="section-title">Restoration Report</div>
        <p style="color: var(--text-muted); font-size: 1rem; max-width: 500px; margin: 0 auto;">Expert AI guidance generated for your artwork</p>
    </div>
    """, unsafe_allow_html=True)

    user = st.session_state.user_data
    initials = user['name'][0].upper() if user.get('name') else "?"
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(201,168,76,0.1), rgba(45,212,191,0.06)); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem 2rem; margin-bottom: 2rem; display: flex; align-items: center; gap: 1.5rem; flex-wrap: wrap;">
        <div style="width: 48px; height: 48px; background: linear-gradient(135deg, var(--gold), #b8932f); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'Cormorant Garamond', serif; font-size: 1.4rem; color: var(--midnight); font-weight: 600; flex-shrink: 0;">{initials}</div>
        <div style="flex: 1; min-width: 200px;">
            <div style="font-family: 'Cormorant Garamond', serif; font-size: 1.3rem; color: var(--text-primary);">{user.get('name', '')}</div>
            <div style="color: var(--text-muted); font-size: 0.82rem; margin-top: 0.2rem;">{user.get('artwork_type', '')} &nbsp;·&nbsp; {user.get('role', '')} &nbsp;·&nbsp; {user.get('goal', '')}</div>
        </div>
        <div><span class="badge-teal">📅 {datetime.now().strftime('%b %d, %Y')}</span></div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([5, 1])
    with col_a:
        st.markdown('<div style="font-family: \'Cormorant Garamond\', serif; font-size: 1.5rem; color: var(--gold-light); margin-bottom: 0.5rem;">Detailed Analysis Report</div>', unsafe_allow_html=True)
    with col_b:
        st.download_button(
            label="📥 Export",
            data=f"""ARTRESTORER AI — RESTORATION ANALYSIS REPORT
══════════════════════════════════════════════════════
PREPARED FOR: {user.get('name', '')}
ROLE: {user.get('role', '')} | TYPE: {user.get('artwork_type', '')}
DATE: {datetime.now().strftime('%B %d, %Y')}

{st.session_state.result_text}

══════════════════════════════════════════════════════
Generated by ArtRestorer AI · Cultural Heritage Preservation
This analysis is advisory only. Always consult certified conservators.
""",
            file_name=f"ArtRestorer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            key="download_report"
        )

    st.markdown('<hr class="divider-gold">', unsafe_allow_html=True)

    # Format result
    formatted = st.session_state.result_text
    formatted = formatted.replace("COMPREHENSIVE RESTORATION ANALYSIS",
        "<div style='font-family: Cormorant Garamond, serif; font-size: 1.6rem; color: var(--gold-light); font-weight: 400; letter-spacing: 1px;'>Comprehensive Restoration Analysis</div>")
    formatted = formatted.replace("EXPERT RESTORATION GUIDANCE:",
        "<div style='font-family: Cormorant Garamond, serif; font-size: 1.4rem; color: var(--teal); margin: 2rem 0 0.8rem; font-weight: 300; letter-spacing: 0.5px;'>Expert Restoration Guidance</div>")
    formatted = formatted.replace("CONCLUSION:",
        "<div style='font-family: Cormorant Garamond, serif; font-size: 1.3rem; color: var(--gold-light); margin: 2rem 0 0.5rem;'>Conclusion</div>")
    formatted = formatted.replace("IMPORTANT DISCLAIMER:",
        "<div style='font-family: DM Mono, monospace; font-size: 0.7rem; color: #ef4444; letter-spacing: 3px; text-transform: uppercase; margin: 1.5rem 0 0.5rem;'>Important Disclaimer</div>")
    formatted = formatted.replace("══════════════════════════════════════════════════════════",
        "<hr style='border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(201,168,76,0.3), transparent); margin: 1.5rem 0;'>")

    st.markdown(f"""
    <div class="result-box">
        <div class="result-text" style="font-size: 0.93rem; line-height: 1.9;">{formatted}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="margin-top: 2rem; text-align: center;"></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("← Analyse Another Artwork", key="back_btn"):
            st.session_state.page = 'main'
            st.rerun()

    # Feedback
    st.markdown("""
    <div style="text-align: center; margin: 4rem 0 1rem;">
        <div style="font-family: 'Cormorant Garamond', serif; font-size: 2rem; color: var(--text-primary); font-weight: 300;">Share Your Experience</div>
        <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 0.5rem;">Help us improve ArtRestorer AI</p>
    </div>
    """, unsafe_allow_html=True)

    col_fb1, col_fb2, col_fb3 = st.columns([1, 1, 1])
    with col_fb2:
        if st.button("📝 Open Feedback Form", key="open_feedback_results"):
            st.session_state.show_feedback_results = True

    if 'show_feedback_results' not in st.session_state:
        st.session_state.show_feedback_results = False

    if st.session_state.show_feedback_results:
        st.markdown('<div class="feedback-modal-inner">', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-family: 'Cormorant Garamond', serif; font-size: 2rem; color: var(--gold-light); font-weight: 300;">We Value Your Feedback</div>
            <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 0.5rem;">Your input shapes the future of ArtRestorer AI</p>
        </div>
        """, unsafe_allow_html=True)

        col_fb1, col_fb2 = st.columns(2)
        with col_fb1:
            feedback_name = st.text_input("Your Name", key="feedback_name_results", placeholder="Enter your name")
            feedback_email = st.text_input("Email (Optional)", key="feedback_email_results", placeholder="your@email.com")
            feedback_rating = st.select_slider(
                "Overall Rating",
                options=["⭐ Poor", "⭐⭐ Fair", "⭐⭐⭐ Good", "⭐⭐⭐⭐ Very Good", "⭐⭐⭐⭐⭐ Excellent"],
                value="⭐⭐⭐ Good", key="feedback_rating_results"
            )
        with col_fb2:
            feedback_category = st.selectbox(
                "Feedback Category",
                ["General Feedback", "Feature Request", "Bug Report", "Accuracy of Analysis", "User Experience", "Other"],
                key="feedback_category_results"
            )
            feedback_recommend = st.radio(
                "Would you recommend ArtRestorer AI?",
                ["👍 Yes", "🤔 Maybe", "👎 No"],
                horizontal=True, key="feedback_recommend_results"
            )

        feedback_comments = st.text_area(
            "Your Comments & Suggestions",
            placeholder="Share your thoughts or report issues...",
            height=150, key="feedback_comments_results"
        )

        col_fb_btn1, col_fb_btn2, col_fb_btn3 = st.columns([1, 1, 1])
        with col_fb_btn1:
            if st.button("Cancel", key="cancel_feedback_results"):
                st.session_state.show_feedback_results = False
                st.rerun()
        with col_fb_btn2:
            if st.button("Submit Feedback →", key="submit_feedback_results"):
                if feedback_name and feedback_comments:
                    st.success("✅ Thank you for your feedback! It helps us improve.")
                    st.balloons()
                    import time; time.sleep(2)
                    st.session_state.show_feedback_results = False
                    st.rerun()
                else:
                    st.error("Please provide your name and comments.")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="site-footer">
        <span>ArtRestorer AI</span> · Powered by OpenAI · Cultural Heritage Preservation
    </div>
    """, unsafe_allow_html=True)
