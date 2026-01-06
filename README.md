# ⚡ Smart Meter Privacy Dashboard

An **interactive Streamlit dashboard** that simulates household electricity consumption and demonstrates the **trade-off between data utility and user privacy** in smart metering systems. The project visualizes how different privacy-preserving techniques—especially **differential privacy**—affect energy analytics and appliance-level inference (NILM).

---

## 🚀 Project Overview

Smart meters provide fine-grained energy data that is useful for analytics but can also reveal **sensitive personal information**, such as daily routines or electric vehicle (EV) usage. This project simulates realistic household energy consumption and shows:

* How energy usage varies across different household profiles
* How privacy mechanisms modify smart meter data
* How appliance usage (e.g., EV charging) can be inferred or hidden depending on noise levels

The dashboard is designed for **educational, research, and demonstration purposes** in smart grids, privacy engineering, and data security.

---

## ✨ Key Features

### 🏠 Household Consumption Simulation

* Simulates **hourly electricity usage** over 24 hours
* Multiple household profiles:

  * Family
  * Student
  * Retired
  * Working couple
* Realistic peak-hour behavior (morning & evening loads)

### 🔐 Privacy-Preserving Techniques

* **Raw Hourly Data** (no privacy)
* **Daily Aggregation** (coarse-grained privacy)
* **Differential Privacy** using Laplace noise

### ⚖️ Privacy vs Utility Visualization

* Side-by-side comparison of original vs private data
* Adjustable noise scale to observe privacy impact in real time

### 🚗 NILM (Non-Intrusive Load Monitoring)

* Synthetic appliance-level energy traces:

  * Fridge
  * Lights
  * Washing machine
  * Electric Vehicle (EV)
* Demonstrates how EV usage can be detected or hidden
* Shows privacy leakage risks with low-noise data

### 📊 Interactive Visualizations

* Line charts and area plots using Plotly
* Live simulation playback
* User-controlled parameters via sidebar

---

## 🛠 Tech Stack

* **Language:** Python
* **Web Framework:** Streamlit
* **Data Processing:** Pandas, NumPy
* **Visualization:** Plotly
* **Privacy Mechanism:** Differential Privacy (Laplace noise)

---

## 📁 Project Structure

```
project-root/
│
├── smart_meter_dashboard.py   # Streamlit application
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/smart-meter-privacy-dashboard.git
cd smart-meter-privacy-dashboard
```

### 2️⃣ Install Dependencies

```bash
pip install streamlit pandas numpy plotly
```

---

## ▶️ Running the Dashboard

```bash
streamlit run smart_meter_dashboard.py
```

The app will open automatically in your browser at:

```
http://localhost:8501
```

---

## 🎛 Dashboard Sections

### 🏠 Simulation Tab

* Select household profile
* View hourly consumption
* Play live consumption animation

### 🔐 Privacy vs Utility Tab

* Choose privacy method
* Adjust noise level
* Compare original vs private data

### 🚗 NILM (Appliance Detection) Tab

* View appliance-level ground truth
* Apply unified privacy noise
* Observe EV detection or masking

---

## 🧪 Key Concepts Demonstrated

* Smart meter data privacy risks
* Differential privacy trade-offs
* Energy disaggregation (NILM)
* Privacy leakage through fine-grained data

---

## ⚠️ Limitations

* Uses **synthetic data**, not real smart meter readings
* EV detection logic is simplified for demonstration
* Not intended for production deployment

---

## 🔮 Future Enhancements

* Real smart meter dataset integration
* Formal privacy-utility metrics
* More appliance types
* User authentication & data export
* Policy-based privacy controls

---

## 👨‍💻 Author

**Prince Harsha**
Smart Grid, Privacy & Data Security Enthusiast

---

## 📜 License

This project is licensed under the **MIT License**.

---

⭐ If you find this project useful, consider giving it a star on GitHub!
