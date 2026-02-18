========================================================================
HUMAN-IN-THE-LOOP AI SYSTEM:  A Comparative Study Of Manual and AI-Assisted Airport  Screening
========================================================================

1. PROJECT OVERVIEW
-------------------
This software is a 'Baggage Inspection System' developed in Python
(Streamlit) for research into "Automation Bias" and "Verification
Latency" in airport security screening. 

Instead of static images, the system uses a Stochastic Procedural Content 
Generation (PCG) engine to create randomized luggage bags for every trial, 
ensuring the assessment of true visual vigilance.

2. CORE FEATURES
----------------
* Stochastic PCG: Randomizes  luggage layouts using Unicode symbols 
  for threat and non-threat items.
* Imperfect AI Agent: Simulated assistant with 85% reliability (P=0.85) 
  to test trust calibration.
* Telemetry Logging: Captures reaction time (ms), decision accuracy, 
  and interaction mode into a structured CSV format.

3. TARGET THREATS
-----------------
Participants act as Security Officers to identify:
- Kinetic Weapons: Guns and Knives.
- Explosives: Bombs and Pyrotechnics.
- Hazardous Materials: Biohazards and Toxic Substances.

4. PROJECT TIMELINE
-------------------
- Phase 1 (Weeks 1-3): Development and  Monte Carlo Audit.
- Phase 2 (Weeks 4-6): Data Collection (N=30) and Statistical Analysis.
- Phase 3 (Weeks 7-8): Final Report Preparation (Deadline: April 13).

5. INSTALLATION & USAGE
-----------------------
Requirements: Python 3.9+, Streamlit, Pandas, NumPy, SciPy.

1. Install dependencies:
   pip install -r requirements.txt

2. Run the application:
   streamlit run app.py

6. ETHICAL CONSIDERATIONS
-------------------------
Project Ref: P192604.
The study uses 'Privacy by Design'—no personal identifiable information 
(PII) is captured. All participants must pass a 5-point 
informed consent checklist before beginning

7. CONTACT
----------
Student Name: Adarsha Adhikari 
