# ✈️ SkyGuard: Human-AI Security Simulation

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://skyguard-project-2025.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Status](https://img.shields.io/badge/Status-Live-success)

## 📄 Project Overview
**SkyGuard** is a Python-based experimental instrument designed to investigate **Automation Bias**, **Trust Calibration**, and **Cognitive Load** in Human-AI Teaming scenarios. 

This simulation mimics a high-stakes X-Ray baggage screening task at an airport. It serves as the primary data collection tool for my Master's Dissertation: *"Investigating the Impact of Imperfect AI Assistance on Human Vigilance in Security Screening."*

👉 **[Live Demo](https://skyguard-project-2025.streamlit.app/)**

## 🎯 Research Objectives
The simulation is designed to measure:
1.  **Reaction Time:** Does AI assistance speed up or slow down decision-making (Cost of Verification)?
2.  **Accuracy:** Does the presence of AI reduce human error or cause "blind compliance"?
3.  **Automation Bias:** How do operators react when the AI makes a deliberate error?

## 🧪 Experimental Design
The experiment utilizes a **Within-Subjects Design** with two distinct conditions:

| Condition | Description |
| :--- | :--- |
| **🛑 Manual Mode** | The user acts alone. They must visually scan the bag for threats (Guns, Knives, Bombs) without assistance. |
| **🤖 AI Assist Mode** | The user is supported by a simulated AI agent. The AI provides a text alert (Clear/Threat) with a confidence score. |

### The "Wizard of Oz" AI Model
To ensure scientific control, the AI is not a "Black Box" neural network. It is a probabilistic model with a **fixed reliability of 85%**.
* **True Positives/Negatives:** 85% of the time, the AI is correct.
* **False Positives/Negatives:** 15% of the time, the AI deliberately errors to test human vigilance.

## 🛠️ Tech Stack
This project was engineered using the **Python** ecosystem and deployed via **Streamlit Cloud**.

* **Frontend/UI:** [Streamlit](https://streamlit.io/) (Web-based interactive interface)
* **Data Processing:** [Pandas](https://pandas.pydata.org/) (Real-time data logging and CSV export)
* **Visualization:** [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) (Instant feedback charts)
* **Logic:** Python `random` & `time` modules for stochastic procedural generation.

## 🚀 How to Run Locally
If you wish to run this code on your local machine instead of the cloud:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/AdarshaAdhikari07/SkyGuard-Project.git](https://github.com/AdarshaAdhikari07/SkyGuard-Project.git)
    cd SkyGuard-Project
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app:**
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure
```text
SkyGuard-Project/
├── app.py              # Main application source code
├── requirements.txt    # List of Python dependencies
└── README.md           # Project documentation
