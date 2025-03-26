# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
A simple and effective ML model which detects Anomaly based on account transaction history and UI to search for any acccount and its details for validations

## 🎥 Demo
🖼️ Screenshots:
1> Sample History Data created using python
![image](https://github.com/user-attachments/assets/26d55a5e-9d4d-4d65-a293-52c5d9d69764)

2> Snap of output from ML model based on history data
![image](https://github.com/user-attachments/assets/490d97b3-996c-457f-b81e-f7da3ed421ce)

3> Snap of UI search and results
![image](https://github.com/user-attachments/assets/bb04e76c-3778-440a-b510-4d1e4d76ab97)


## 💡 Inspiration
As we are facing lot of reconciliation problems in our project, this problem statement looks interesting and we thought if we get some hands-on here same we could apply to real time project 

## ⚙️ What It Does
The key features and functionalities of our project.
1. It creates data for ML model, this data is almost like real time data
2. As No Labeled Data: stated that we don't have labeled data for anomalies. Reinforcement Learning can work in environments where we don't have explicit examples of what constitutes an anomaly.
3. Using IsolationForest, it is deriving the comments and Anomaly for each account
4. Simple UI to search for accounts and is it comes under Anomaly or not and its history in same page

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/ewfx/sradg-data-visionaries.git 
   ```
2. Install dependencies  
   ```sh
   pip install -r requirements.txt
   ```
3. Run the project  
   ```sh
   python generate_data.py
   python predict_anomaly.py
   python search_and_disply.py
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: python
- 🔹 Backend: python
- 🔹 Database: filess
- 🔹 Other: ML,Pandas

## 👥 Team
- **Kailas K M** - 
- **Chintu Babu Raparthi** - 
