
** Developers:-
 Dhruv Khandelwal (BT24CSE073)
 Dhruv Gupta (BT24CSE009)
 Dhairya Singhal (BT24CSE070)
 Dev Pathak (BT24CSE030)
**





**please note that in .gitignore file , we have /venv .**


🌱 Sustainable Living Assistant
♻️ Project Overview
Sustainable Living Assistant is a Django-based web platform designed to guide users toward a more eco-friendly lifestyle. Through features like a Green Alternative Finder, a sustainability-focused chatbot, community contributions, gamified challenges, and streak tracking, users are empowered to reduce their carbon footprint in a fun and engaging way.

Our goal is to combine sustainability with interactivity, making green living simple, educational, and rewarding.

✅ Current Features
🔍 Green Alternative Finder (Text-Based, TensorFlow + Dataset)
Users can input a plastic-based product (e.g., "plastic cup"), and get instant sustainable alternatives.

Powered by a custom CSV dataset and backed by TensorFlow for simple text-based matching (more AI features planned).

🤖 Chatbot 
A friendly chatbot ) to answer questions related to sustainability and offer personalized suggestions.

🧮 Footprint Calculator
Users can input their habits to calculate their environmental footprint and compare it to previous data for tracking progress.

🌿 Community & Contributors
A section to highlight contributors who regularly participate in challenges or make green suggestions.

Users can connect and learn from others' choices.

🎯 Challenges & Gamification
Users can take on sustainability challenges and earn digital rewards.

Tracks streaks and encourages consistent eco-friendly behavior.

🛠️ Tech Stack
Backend: Django (Python)

Frontend: HTML, CSS, JavaScript

AI: TensorFlow (Text Matching)

Data: Custom CSV datasets for recommendations



🧪 How to Run Locally
Clone this repository

git clone https://github.com/your-username/sustainable-living.git
cd sustainable-living
Create and activate a virtual environment

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
Install required packages

pip install -r requirements.txt
Start the development server

python manage.py runserver
Open in your browser

http://127.0.0.1:8000/
📊 Dataset Used
recommendations.csv: Contains 100+ pairs of plastic products and their sustainable alternatives. Used for matching via TensorFlow logic.

