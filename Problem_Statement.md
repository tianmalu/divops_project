# 🧙‍♀️ TarotAI - GenAI-Powered Tarot Reading Assistant

## 1. Problem Statement

### 🔍 What Problem Does This Application Solve?

Many users seek guidance or emotional insight through tarot readings, but traditional tarot apps often feel rigid, overly mechanical, or too abstract. Our app aims to bridge the mystical elements of tarot with the conversational power of Generative AI, offering a personalized, emotionally resonant experience.

---

### 🎯 What is the Main Functionality?

- **Daily Tarot**: Personalized daily reading tailored to your past patterns.
- **Natural Language Tarot Reading**: Users ask questions in their own words; the system responds with relevant card readings powered by GenAI.
- **AI-Enhanced Interpretation**: Each card drawn is accompanied by a rich narrative-style explanation, tone-adapted to the user's question.
- **User Feedback Adaptation**: The app continuously learns from feedback to refine keyword associations in the vector database.
- **Optional Features**:
  - Weekly summary of draws ("Your Destiny Journal")
  - Chat channel for users
  - Picture generation for visualizing anwsers (via image AI)

---

### 👥 Who Are the Intended Users?

- Individuals interested in tarot, astrology, or spiritual insight
- Casual users seeking a fun, gamified introspective tool
- Wellness app users who seek mental clarity or journaling prompts

---

### 🤖 How Will You Integrate GenAI Meaningfully?

- **LLM for Response Generation**: Generate human-like, emotionally resonant tarot interpretations.
- **Embedding + Vector DB**: Use semantic search to match questions with relevant tarot symbols.
- **Feedback Loop**: Use user thumbs-up/down or comment feedback to update keywords in vector DB for more accurate future matches.
- **Optional Image Gen**: GenAI can create unique visuals based on the reading to enhance user immersion.

---

### 📖 Example Scenarios

#### 🔮 Scenario 1: Casual Daily Use
- **User**: Click the "Daily Tarot" button.
- **App**: Draws 1 or 3 cards, gives a narrative: "Today are The Magician... A chance awaits you to use your full potential..."

#### 💔 Scenario 2: Emotional Decision
- **User**: "Should I give them another chance?"
- **App**: Pulls a reversed Lovers card, explains with AI-generated empathy: "Your heart seeks clarity, but the signs hint toward imbalance..."

#### 📈 Scenario 3: Data-Driven Learning
- **User**: Gives feedback: "This reading didn’t feel accurate."
- **App**: Logs vector embedding and updates keyword weighting for future refinement.


---

> TarotAI isn’t just a reading tool — it’s a reflective companion that adapts, learns, and grows with its user.

