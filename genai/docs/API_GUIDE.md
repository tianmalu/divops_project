# TarotAI GenAI API Documentation

All endpoints are prefixed with `/genai`. All responses are in JSON format.

---

## 1. Health Check

**GET `/genai/health`**
- Checks service and Weaviate status.
- Response:
  - `status`: healthy/unhealthy
  - `timestamp`: current time
  - `version`: service version
  - `service`: service name
  - `weaviate_status`: Weaviate connection status
  - `feedback_collections`: feedback collection status

---

## 2. Simple Prediction

**GET `/genai/predict`**
- Parameters:
  - `question` (string, required): The question for prediction
  - `user_id` (string, optional): User ID
- Returns: Prediction result, question ID, discussion ID, etc.

---

## 3. Daily Tarot Reading

**GET `/genai/daily-reading`**
- Parameters:
  - `user_id` (string, optional): User ID
- Returns: Daily tarot reading result

---

## 4. User Discussions List

**GET `/genai/discussions/{user_id}`**
- Path Parameter:
  - `user_id` (string): User ID
- Returns: All discussions for the user

---

## 5. Discussion Details

**GET `/genai/discussion/{discussion_id}`**
- Path Parameter:
  - `discussion_id` (string): Discussion ID
- Returns: Discussion details, including drawn cards and history

---

## 6. Start New Discussion

**POST `/genai/discussion/start`**
- Body (JSON):
  - `user_id` (string): User ID
  - `initial_question` (string): Initial question
  - `topic` (string): Topic
- Returns: New discussion details, drawn cards, initial interpretation

---

## 7. Follow-up Question in Discussion

**POST `/genai/discussion/{discussion_id}/followup`**
- Path Parameter:
  - `discussion_id` (string): Discussion ID
- Body (JSON):
  - `question` (string): Follow-up question
- Returns: Follow-up response

---

## 8. Submit Discussion Feedback

**POST `/genai/discussion/{discussion_id}/feedback`**
- Path Parameter:
  - `discussion_id` (string): Discussion ID
- Body (JSON):
  - `user_id` (string): User ID
  - `feedback_text` (string): Feedback content
  - `rating` (integer): Rating
- Returns: Feedback processing result

---

## 9. Feedback Statistics

**GET `/genai/feedback/stats`**
- Parameters:
  - `user_id` (string, optional): Filter by user
- Returns: Feedback statistics

---

## 10. Get Feedback for a Discussion

**GET `/genai/feedback/discussion/{discussion_id}`**
- Path Parameter:
  - `discussion_id` (string): Discussion ID
- Returns: All feedback for the discussion

---

## 11. Context Statistics

**GET `/genai/feedback/contexts/stats`**
- Returns: Statistics about stored reading contexts

---

## 12. Enhanced Reading

**POST `/genai/reading/enhanced`**
- Body (JSON):
  - `question` (string): Question
  - `base_interpretation` (string): Base interpretation
  - `cards` (list): Card information
  - `user_id` (string): User ID
- Returns: Enhanced interpretation

---

## 13. Find Similar Contexts

**GET `/genai/feedback/contexts/similar`**
- Parameters:
  - `question` (string): Question
  - `cards` (string): Card information (JSON string)
  - `limit` (integer): Number of results
- Returns: Similar reading contexts

---

## Error Handling

- All endpoints return HTTP 4xx/5xx on error, with a `detail` field describing the issue.

---

For more details or example requests/responses, please refer to the source code or contact the development team.
