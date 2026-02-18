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

# Custom CSS for Red Decision Buttons
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #ff4b4b !important;
        color: white !important;
        border-radius: 10px;
        border: none;
        height: 3.5em;
        width: 100%;
        font-weight: bold;
        font-size: 18px;
    }
    div.stButton > button:hover {
        background-color: #ff3333 !important;
        border: 1px solid white;
    }
    </style>
    """, unsafe_allow_html=True)

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
    """Creates a unique bag with a 40% threat probability."""
    items = random.sample(SAFE_ITEMS, k=random.randint(4, 8))
    threat = False
    if random.random() < 0.40: 
        items.append(random.choice(THREAT_ITEMS))
        threat = True
    random.shuffle(items)
    st.session_state.current_bag = items
    st.session_state.has_threat = threat
    st.session_state.start_time = time.time()

def process_decision(user_rejected):
    """Logs user reaction time and accuracy."""
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
    """Monte Carlo Simulation: Runs 10,000 trials to verify AI reliability."""
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
    progress_bar.progress(1.0)
    st.session_state.verification_result = pd.DataFrame(logs)

# ==========================================
# 5. UI LAYOUT & ETHICS GATEWAY
# ==========================================
st.title(" Baggage Inspection Task")

# --- PHASE 1: INFORMED CONSENT ---
if not st.session_state.consent_given:
    st.header("📄 Participant Information & Consent")
    with st.expander("READ FIRST: Participant Information Sheet", expanded=True):
        st.subheader("Human-in-the-Loop AI System")
        st.write("**Researcher:** Adarsha Adhikari | **Supervisor:** Aram Saeed")
        st.write("**** ")
        st.markdown(f"""
        **Purpose:** This research compares Manual and AI-Assisted modes to study "Automation Bias" and "Cost of Verification".
        **Procedure:** You have to detect threat item.You will inspect 10 bags each on two differents modes. One mode is Manual, the other is AI assistant.
        **Privacy:** No names, IP addresses,  are recorded.
        **Data Submission:** Download the anonymous CSV and email it to **adhika108@coventry.ac.uk**.
        """)

    st.subheader("✅ Informed Consent")
    st.write("Please check each box to indicate your agreement:")
    c1 = st.checkbox("I confirm that I have read and understood the Information Sheet.")
    c2 = st.checkbox("I understand my information will be treated confidentially.")
    c3 = st.checkbox("I understand my participation is voluntary and I can withdraw by closing my browser.")
    c4 = st.checkbox("I understand the results will be used for academic research.")
    c5 = st.checkbox("I agree to take part and confirm I am 18+ years of age.")

    if st.button("I Consent & Agree to Participate") : 
        if all([c1, c2, c3, c4, c5]):
            st.session_state.consent_given = True
            st.rerun()
        else:
            st.error("Please check all boxes to proceed.")
    st.stop()

# --- PHASE 2: MAIN MENU ---
if not st.session_state.game_active and st.session_state.rounds == 0:
    st.markdown("### 📋 Mission Briefing")
    st.info("Role: Security Officer. Objective: Detect prohibited items.Please note that you are testing a prototype of an AI assistant. It is meant to identify potential threats. Please examine the luggage and decide, based on your own judgment, whether it is safe or not .")
    
    st.markdown("#### ⚠️ TARGET THREATS:")
    threat_html = " ".join([f"<span style='font-size:40px; margin:0 10px;'>{x}</span>" for x in THREAT_ITEMS])
    st.markdown(f"<div style='background-color: #262730; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;'>{threat_html}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("👤 **Participant Mode**")
        if st.button("Start Manual Mode", use_container_width=True):
            st.session_state.mode, st.session_state.game_active = "Manual", True
            generate_bag(); st.rerun()
        if st.button("Start AI-Assisted Mode", use_container_width=True):
            st.session_state.mode, st.session_state.game_active = "AI_Assist", True
            generate_bag(); st.rerun()
    with col2:
        st.warning("⚙️ **Developer Mode**")
        if st.button("🛠️ Run System Verification", use_container_width=True):
            run_system_verification()
           
        
        if st.session_state.verification_result is not None:
            df_audit = st.session_state.verification_result
            st.write(f"**Trials:** {len(df_audit):,}")
            st.write(f"**AI Reliability:** {(df_audit['AI_Correct'].mean()) * 100:.2f}%")
            st.write(f"**Threat Rate:** {(df_audit['Ground_Truth'].mean()) * 100:.2f}%")
           

# --- PHASE 3: GAME LOOP ---
elif st.session_state.game_active:
    st.progress(st.session_state.rounds / 10, f"Bag {st.session_state.rounds+1}/10")
    bag_html = " ".join([f"<span style='font-size:55px; padding:10px;'>{x}</span>" for x in st.session_state.current_bag])
    st.markdown(f"<div style='background:#111; border:4px solid #444; border-radius:15px; padding:30px; text-align:center;'>{bag_html}</div>", unsafe_allow_html=True)

    if st.session_state.mode == "AI_Assist":
        prediction = "THREAT" if st.session_state.has_threat else "CLEAR"
        if random.random() > 0.85: prediction = "CLEAR" if prediction == "THREAT" else "THREAT"
        confidence = random.randint(80, 99)
        if prediction == "THREAT": st.error(f"🤖 AI ALERT: Suspicious Object Detected ({confidence}%)", icon="⚠️")
        else: st.success(f"🤖 AI SCAN: No Suspicious Object Detected ({confidence}%)", icon="✅")
    else:
        st.warning("📡 AI SYSTEM OFFLINE: Manual Inspection Required", icon="🛑")

    st.write("")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("✅ CLEAR BAG", use_container_width=True): process_decision(False); st.rerun() 
    with col_b:
        if st.button("🚨 REPORT THREAT", use_container_width=True): process_decision(True); st.rerun()

# --- PHASE 4: END SCREEN & SUBMISSION ---
else:
    st.success(f"Session Complete. Final Score: {st.session_state.score}")
    if len(st.session_state.history) > 0:
        df = pd.DataFrame(st.session_state.history)
        st.divider()
        st.subheader("📈 Performance Report")
        
        tab1, tab2, tab3 = st.tabs(["⏱️ Reaction Time", "🎯 Accuracy", "📄 Raw Data"])
        
        with tab1:
            fig1, ax1 = plt.subplots(figsize=(8, 4))
            sns.barplot(data=df, x="Mode", y="Time", hue="Result", palette="viridis", ax=ax1)
            ax1.set_title("Response Latency per Mode")
            st.pyplot(fig1)
            
        with tab2:
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            acc_df = df.groupby("Mode")["Result"].apply(lambda x: (x == 'CORRECT').mean() * 100).reset_index()
            sns.barplot(data=acc_df, x="Mode", y="Result", palette="magma", ax=ax2)
            ax2.set_ylim(0, 105)
            ax2.set_ylabel("Accuracy (%)")
            st.pyplot(fig2)

        with tab3:
            st.dataframe(df, use_container_width=True)
        
        st.error(" ACTION REQUIRED for Paticipant: Plz Go through both Manual Mode and AI Assisted Mode. After you complete the both mode. Plz submit the data  ")
        st.error("Privacy: NO names and Ip addresses are recorded.")
        st.write("1.Please Click the button below to download your results.")
        st.write("2.Please Email the file to: **adhika108@coventry.ac.uk which will be use for study purpose . All the information are kept confidentially**")
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results (CSV)", csv, "baggage_results.csv", "text/csv")

    if st.button("🔄 Return to Main Menu"): restart_game()
