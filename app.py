import streamlit as st
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. APP CONFIGURATION
# ==========================================
st.set_page_config(page_title="Baggage Inspection Task", page_icon="", layout="centered")

# ==========================================
# 2. SESSION STATE MANAGEMENT
# ==========================================
if 'consent_given' not in st.session_state: st.session_state.consent_given = False
if 'score' not in st.session_state: st.session_state.score = 0
if 'rounds' not in st.session_state: st.session_state.rounds = 0
if 'history' not in st.session_state: st.session_state.history = []
if 'game_active' not in st.session_state: st.session_state.game_active = False
if 'current_bag' not in st.session_state: st.session_state.current_bag = []
if 'has_threat' not in st.session_state: st.session_state.has_threat = False
if 'start_time' not in st.session_state: st.session_state.start_time = 0
if 'mode' not in st.session_state: st.session_state.mode = "Manual"
if 'verification_result' not in st.session_state: st.session_state.verification_result = None

# ==========================================
# 3. ASSET LIBRARY
# ==========================================
SAFE_ITEMS = ['👕', '👖', '👗', '👟', '🎩', '💻', '📷', '📚', '🧸', '🥪', '🕶️']
THREAT_ITEMS = ['🔫', '🔪', '💣', '🧨', '🩸', '☠️']

# ==========================================
# 4. CORE FUNCTIONS
# ==========================================
def generate_bag():
    """PCG Engine: Creates a unique bag."""
    items = random.sample(SAFE_ITEMS, k=random.randint(4, 8))
    threat = False
    
    # Ground Truth Generation (40% Threat Probability)
    if random.random() < 0.40:
        items.append(random.choice(THREAT_ITEMS))
        threat = True
    
    random.shuffle(items)
    st.session_state.current_bag = items
    st.session_state.has_threat = threat
    st.session_state.start_time = time.time()

def process_decision(user_rejected):
    """Log User Decision."""
    rt = round(time.time() - st.session_state.start_time, 3)
    correct = (user_rejected == st.session_state.has_threat)
    result_str = "CORRECT" if correct else "ERROR"
    
    if correct: st.session_state.score += 10

    st.session_state.history.append({
        "Round": st.session_state.rounds + 1,
        "Mode": st.session_state.mode,
        "Threat": st.session_state.has_threat,
        "User_Reject": user_rejected,
        "Result": result_str,
        "Time": rt
    })

    st.session_state.rounds += 1
    if st.session_state.rounds < 10:
        generate_bag()
    else:
        st.session_state.game_active = False

def restart_game():
    st.session_state.rounds = 0
    st.session_state.score = 0
    st.session_state.game_active = False
    st.session_state.verification_result = None
    st.rerun()

def run_system_verification():
    """Automated Audit: Runs 10,000 trials."""
    logs = []
    progress_bar = st.progress(0)
    for i in range(10000):
        is_threat = random.random() < 0.40
        ai_advice = "THREAT" if is_threat else "CLEAR"
        is_ai_correct = True
        if random.random() > 0.85: # 85% Reliability Target
            is_ai_correct = False
            ai_advice = "CLEAR" if ai_advice == "THREAT" else "THREAT"
        logs.append({"Trial": i, "Ground_Truth": is_threat, "AI_Advice": ai_advice, "AI_Correct": is_ai_correct})
        if i % 1000 == 0: progress_bar.progress(i / 10000)
    progress_bar.progress(100)
    st.session_state.verification_result = pd.DataFrame(logs)

# ==========================================
# 5. UI LAYOUT & GATEWAY LOGIC
# ==========================================
st.title(" Baggage Inspection Task")

# --- PHASE 1: INFORMED CONSENT ---
if not st.session_state.consent_given:
    st.header("📄 Participant Information & Consent")
    with st.expander("READ FIRST: Participant Information Sheet", expanded=True):
        st.write("""
        **Project Title:** Human-in-the-Loop AI System: A Comparative Study of Manual and AI-Assisted Airport Screening
        **Researcher:** Adarsha Adhikari | **Supervisor:** Aram Saeed
        
        **Purpose:** This study investigates 'Automation Bias' and the 'Cost of Verification' in human-AI teaming.
        **Procedure:** You will perform 10 baggage checks. One mode is Manual, the other uses an AI assistant (85% reliable).After you done both manual and AI Assistant that you have to download the .CSV file 
        **Privacy:** No PII (Personal Identifiable Information) is collected. 
        **Data Submission:** You will download a CSV file at the end and email it to the researcher.Data is logged to a structured .CSV file. Participants manually download this anonymous file and email it to the researcher. While the researcher sees the sender's email, the CSV itself is PII-free, containing no names or IDs.The manual CSV submission method is a deliberate technical choice to keep the Streamlit hosting environment architecture free of PII. The study has eliminated the risk of accidental collection of IP addresses or other concealed digital identifiers simply by not integrating back, end databases.
        **Withdrawal:** You may stop at any time by closing the browser.
        """)
    st.warning("By clicking 'I Consent' below, you confirm you are 18+ and agree to participate voluntarily.")
    if st.button("✅ I Consent & Agree to Participate"):
        st.session_state.consent_given = True
        st.rerun()
    st.stop()

# --- PHASE 2: MAIN MENU & BRIEFING ---
if not st.session_state.game_active and st.session_state.rounds == 0:
    st.markdown("### 📋 Mission Briefing")
    st.markdown("**Role:** Security Screening Officer | **Objective:** Detect prohibited items.")
    st.info("Please note that you are testing a prototype of an AI assistant. It is meant to identify potential threats. Please examine the luggage and decide, based on your own judgment, whether it is safe or not")
    
    st.markdown("#### ⚠️ TARGET THREATS (LOOK FOR THESE):")
    threat_html = " ".join([f"<span style='font-size:40px; margin:0 10px;'>{x}</span>" for x in THREAT_ITEMS])
    st.markdown(f"<div style='background-color: #262730; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;'>{threat_html}</div>", unsafe_allow_html=True)
    
    st.warning("⚡ **Performance Metric:** Both SPEED and ACCURACY are tracked.")
    st.divider()

    st.markdown("### Select Operation Mode")
    col1, col2 = st.columns(2)
    with col1:
        st.success("👤 **Participant Mode**")
        if st.button("Start Manual Mode"):
            st.session_state.mode, st.session_state.game_active = "Manual", True
            generate_bag()
            st.rerun()
        if st.button("Start AI-Assisted Mode"):
            st.session_state.mode, st.session_state.game_active = "AI_Assist", True
            generate_bag()
            st.rerun()
    with col2:
        st.warning("⚙️ **Developer Mode**")
        if st.button("🛠️ Run System Verification"): run_system_verification()

    if st.session_state.verification_result is not None:
        df_audit = st.session_state.verification_result
        st.divider()
        st.subheader("✅ System Verification Report")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Trials", f"{len(df_audit):,}")
        m2.metric("AI Reliability", f"{(df_audit['AI_Correct'].mean()) * 100:.2f}%")
        m3.metric("Threat Rate", f"{(df_audit['Ground_Truth'].mean()) * 100:.2f}%")

# --- PHASE 3: GAME LOOP ---
elif st.session_state.game_active:
    st.progress(st.session_state.rounds / 10, f"Bag {st.session_state.rounds+1}/10")
    bag_html = " ".join([f"<span style='font-size:55px; padding:10px;'>{x}</span>" for x in st.session_state.current_bag])
    st.markdown(f"<div style='background:#111; border:4px solid #444; border-radius:15px; padding:30px; text-align:center;'>{bag_html}</div>", unsafe_allow_html=True)

    if st.session_state.mode == "AI_Assist":
        prediction = "THREAT" if st.session_state.has_threat else "CLEAR"
        if random.random() > 0.85: prediction = "CLEAR" if prediction == "THREAT" else "THREAT"
        confidence = random.randint(80, 99)
        if prediction == "THREAT": st.error(f"🤖 AI ALERT: Threat Detected (Confidence: {confidence}%)", icon="⚠️")
        else: st.success(f"🤖 AI SCAN: Bag Clear (Confidence: {confidence}%)", icon="✅")
    else:
        st.warning("📡 AI SYSTEM OFFLINE: Manual Inspection Required", icon="🛑")

    st.write("")
    if st.button("✅ CLEAR BAG", type="primary", use_container_width=True): process_decision(False); st.rerun()
    if st.button("🚨 REPORT THREAT", type="primary", use_container_width=True): process_decision(True); st.rerun()

# --- PHASE 4: END SCREEN & SUBMISSION ---
else:
    st.success(f"Session Complete. Final Score: {st.session_state.score}")
    if len(st.session_state.history) > 0:
        df = pd.DataFrame(st.session_state.history)
        st.divider()
        st.subheader("📈 Performance Report")
        tab1, tab2 = st.tabs(["⏱️ Reaction Time", "🎯 Accuracy"])
        with tab1:
            fig1, ax1 = plt.subplots(figsize=(6, 3)); sns.barplot(data=df, x="Mode", y="Time", hue="Result", palette="viridis", ax=ax1)
            st.pyplot(fig1)
        with tab2:
            acc_df = df.groupby("Mode")["Result"].apply(lambda x: (x == 'CORRECT').mean() * 100).reset_index()
            fig2, ax2 = plt.subplots(figsize=(6, 3)); sns.barplot(data=acc_df, x="Mode", y="Result", palette="magma", ax=ax2); ax2.set_ylim(0, 100); st.pyplot(fig2)
        
        st.divider()
        st.error("⚠️ ACTION REQUIRED: SUBMIT YOUR DATA")
        st.write("1. Download your results below.")
        st.write("2. Email the file to the researcher to include your data in the study.")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results (CSV)", csv, "baggage_results.csv", "text/csv")

    if st.button("🔄 Return to Main Menu"): restart_game()
