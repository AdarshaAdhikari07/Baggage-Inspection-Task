import streamlit as st
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. APP CONFIGURATION & CUSTOM CSS
# ==========================================
st.set_page_config(page_title="Baggage Inspection Task", page_icon="🔍", layout="centered")

# Custom CSS to make buttons red with white text
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        border: none;
        height: 3em;
        width: 100%;
        font-weight: bold;
        font-size: 18px;
    }
    div.stButton > button:hover {
        background-color: #ff3333;
        color: white;
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
    logs = []
    for i in range(10000):
        is_threat = random.random() < 0.40
        ai_advice = "THREAT" if is_threat else "CLEAR"
        is_ai_correct = True
        if random.random() > 0.85: 
            is_ai_correct = False
            ai_advice = "CLEAR" if ai_advice == "THREAT" else "THREAT"
        logs.append({"AI_Correct": is_ai_correct, "Ground_Truth": is_threat})
    st.session_state.verification_result = pd.DataFrame(logs)

# ==========================================
# 5. UI LAYOUT
# ==========================================
st.title("Baggage Inspection Task")

# --- PHASE 1: CONSENT ---
if not st.session_state.consent_given:
    st.header("📄 Participant Information & Consent")
    with st.expander("Participant Information Sheet", expanded=True):
        st.write("**Researcher:** Adarsha Adhikari | **Supervisor:** Aram Saeed [cite: 94]")
        st.write("**Ethics Reference:** P192604")
        st.markdown("Please read the full information regarding 'Automation Bias' and 'Cost of Verification'[cite: 95].")
    
    st.warning("Confirm you are 18+ and agree to participate voluntarily[cite: 104].")
    if st.button("✅ I Consent & Agree to Participate"):
        st.session_state.consent_given = True
        st.rerun()
    st.stop()

# --- PHASE 2: MAIN MENU (AS PER YOUR SCREENSHOT) ---
if not st.session_state.game_active and st.session_state.rounds == 0:
    st.markdown("### 📋 Mission Briefing")
    st.write("**Role:** Security Screening Officer | **Objective:** Detect prohibited items[cite: 112].")
    st.info("Examine the luggage and decide, based on your own judgment, whether it is safe or not[cite: 113].")

    st.markdown("#### ⚠️ TARGET THREATS (LOOK FOR THESE):")
    threat_html = " ".join([f"<span style='font-size:40px; margin:0 10px;'>{x}</span>" for x in THREAT_ITEMS])
    st.markdown(f"<div style='background-color: #262730; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;'>{threat_html}</div>", unsafe_allow_html=True)

    st.divider()
    
    col_part, col_dev = st.columns(2)
    
    with col_part:
        st.subheader("👤 Participant Mode")
        st.caption("Start here to collect data.")
        if st.button("Start Manual Mode"):
            st.session_state.mode, st.session_state.game_active = "Manual", True
            generate_bag(); st.rerun()
        if st.button("Start AI-Assisted Mode"):
            st.session_state.mode, st.session_state.game_active = "AI_Assist", True
            generate_bag(); st.rerun()
            
    with col_dev:
        st.subheader("⚙️ Developer Mode")
        st.caption("For algorithmic verification.")
        if st.button("🔍 Run System Verification"):
            run_system_verification()
            
        if st.session_state.verification_result is not None:
            res = st.session_state.verification_result
            st.success("✅ Verification Complete")
            st.write(f"**AI Reliability:** {(res['AI_Correct'].mean())*100:.2f}%")
            st.write(f"**Threat Rate:** {(res['Ground_Truth'].mean())*100:.2f}%")

# --- PHASE 3: GAME LOOP ---
elif st.session_state.game_active:
    st.progress(st.session_state.rounds / 10, f"Bag {st.session_state.rounds+1}/10")
    bag_html = " ".join([f"<span style='font-size:55px; padding:10px;'>{x}</span>" for x in st.session_state.current_bag])
    st.markdown(f"<div style='background:#111; border:4px solid #444; border-radius:15px; padding:30px; text-align:center;'>{bag_html}</div>", unsafe_allow_html=True)

    if st.session_state.mode == "AI_Assist":
        prediction = "THREAT" if st.session_state.has_threat else "CLEAR"
        if random.random() > 0.85: prediction = "CLEAR" if prediction == "THREAT" else "THREAT"
        if prediction == "THREAT": st.error("🤖 AI ALERT: Threat Detected", icon="⚠️")
        else: st.success("🤖 AI SCAN: Bag Clear", icon="✅")
    else:
        st.warning("📡 AI SYSTEM OFFLINE", icon="🛑")

    st.write("")
    if st.button("✅ CLEAR BAG"): process_decision(False); st.rerun()
    if st.button("🚨 REPORT THREAT"): process_decision(True); st.rerun()

# --- PHASE 4: END SCREEN ---
else:
    st.success(f"Session Complete. Final Score: {st.session_state.score}")
    if len(st.session_state.history) > 0:
        df = pd.DataFrame(st.session_state.history)
        st.subheader("📈 Performance Report")
        
        tab1, tab2 = st.tabs(["⏱️ Reaction Time", "🎯 Accuracy"])
        with tab1:
            fig1, ax1 = plt.subplots()
            sns.barplot(data=df, x="Mode", y="Time", hue="Result", palette="viridis", ax=ax1)
            st.pyplot(fig1)
        with tab2:
            fig2, ax2 = plt.subplots()
            acc_df = df.groupby("Mode")["Result"].apply(lambda x: (x == 'CORRECT').mean() * 100).reset_index()
            sns.barplot(data=acc_df, x="Mode", y="Result", palette="magma", ax=ax2)
            st.pyplot(fig2)

        st.error("⚠️ DATA SUBMISSION REQUIRED [cite: 173]")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results (CSV)", csv, "baggage_results.csv", "text/csv")

    if st.button("🔄 Return to Main Menu"): restart_game()
