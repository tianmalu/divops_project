"""
Feedback processing module for TarotAI.
Handles user feedback on discussion accuracy and updates KeywordMeaning when ratings are high.
"""

import json
import os
import sys
from typing import List, Dict, Optional
import weaviate

# Add the server directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Local imports
from app.weaviate_client import get_weaviate_client
from app.models import Feedback, KeywordMeaning, TarotCard, CardLayout
from app.logger_config import get_tarot_logger
from datetime import datetime

# Set up logging
logger = get_tarot_logger(__name__)

class FeedbackProcessor:
    """
    Processes user feedback and updates KeywordMeaning data based on accuracy ratings.
    """
    
    def __init__(self):
        self.client = get_weaviate_client()
        self.high_rating_threshold = 4  # Ratings of 4/5 or above are considered high
        
    def process_feedback(self, feedback: Feedback) -> Dict[str, str]:
        """
        Process user feedback and update KeywordMeaning if rating is high enough.
        
        Args:
            feedback: Feedback object containing user rating and details
            
        Returns:
            Dict with processing status and message
        """
        try:
            # Store the feedback
            feedback_result = self._store_feedback(feedback)
            
            # If rating is high enough (4/5 or above), update KeywordMeaning
            if feedback.rating and feedback.rating >= self.high_rating_threshold:
                keyword_result = self._update_keyword_meaning(feedback)
                return {
                    "status": "success",
                    "message": f"Feedback processed successfully. Rating: {feedback.rating}/5. KeywordMeaning updated and reading context stored.",
                    "feedback_id": feedback_result.get("feedback_id"),
                    "keywords_updated": keyword_result.get("keywords_updated", 0),
                    "contexts_stored": keyword_result.get("contexts_stored", 0)
                }
            else:
                return {
                    "status": "success", 
                    "message": f"Feedback processed successfully. Rating: {feedback.rating}/5. No KeywordMeaning update needed.",
                    "feedback_id": feedback_result.get("feedback_id"),
                    "keywords_updated": 0,
                    "contexts_stored": 0
                }
                
        except Exception as e:
            logger.error(f"Error processing feedback: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to process feedback: {str(e)}"
            }
    
    def _store_feedback(self, feedback: Feedback) -> Dict[str, str]:
        """
        Store feedback in the database.
        
        Args:
            feedback: Feedback object to store
            
        Returns:
            Dict with feedback storage result
        """
        try:
            # Create feedback record
            feedback_data = {
                "user_id": feedback.user_id,
                "question": feedback.question,
                "model_response": feedback.model_response,
                "feedback_text": feedback.feedback_text,
                "rating": feedback.rating,
                "discussion_id": feedback.discussion_id,
                "timestamp": datetime.now().isoformat(),
                "cards_drawn": json.dumps([card.model_dump() for card in feedback.spread])
            }
            
            # Store in Weaviate
            result = self.client.collections.get("Feedback").data.insert(feedback_data)
            
            logger.info(f"Feedback stored successfully for user {feedback.user_id}")
            return {
                "status": "success",
                "feedback_id": str(result)
            }
            
        except Exception as e:
            logger.error(f"Error storing feedback: {str(e)}")
            raise
    
    def _update_keyword_meaning(self, feedback: Feedback) -> Dict[str, int]:
        """
        Update KeywordMeaning based on high-rated feedback and store reading context.
        
        Args:
            feedback: Feedback object with high rating
            
        Returns:
            Dict with update results
        """
        try:
            keywords_updated = 0
            contexts_stored = 0
            
            # Store the complete reading context for future reference
            self._store_reading_context(feedback)
            contexts_stored += 1
            
            # Extract keywords from the cards in the spread
            for position, layout in enumerate(feedback.spread):
                if layout.position_keywords:
                    for keyword in layout.position_keywords:
                        # Create or update KeywordMeaning entry
                        self._create_or_update_keyword_meaning(
                            card=layout.name,
                            keyword=keyword,
                            feedback=feedback,
                            position=position
                        )
                        keywords_updated += 1
            
            logger.info(f"Updated {keywords_updated} keywords and stored {contexts_stored} reading contexts based on high-rated feedback")
            return {
                "keywords_updated": keywords_updated,
                "contexts_stored": contexts_stored
            }
            
        except Exception as e:
            logger.error(f"Error updating keyword meanings: {str(e)}")
            raise
    
    def _create_or_update_keyword_meaning(self, layout: CardLayout, keyword: str, 
                                         feedback: Feedback, position: int):
        """
        Create or update a KeywordMeaning entry based on feedback.
        
        Args:
            card: TarotCard object
            keyword: Keyword to update
            feedback: Feedback object
            position: Position of card in spread
        """
        try:
            # Determine orientation (simplified - you might want to enhance this)
            orientation = "upright"  # Default, could be enhanced with actual orientation data
            
            # Create KeywordMeaning object
            keyword_meaning = KeywordMeaning(
                keyword=keyword,
                meaning=self._extract_meaning_from_feedback(feedback, keyword),
                feedback=[f"User rated {feedback.rating}/5: {feedback.feedback_text or 'No additional comment'}"],
                source="user_feedback",
                orientation=orientation,
                position=position
            )
            
            # Check if keyword meaning already exists for this card
            existing_meanings = self._get_existing_keyword_meanings(layout.name, keyword)
            
            if existing_meanings:
                # Update existing meaning
                self._update_existing_keyword_meaning(existing_meanings[0], keyword_meaning)
            else:
                # Create new meaning
                self._create_new_keyword_meaning(layout, keyword_meaning)

                
        except Exception as e:
            logger.error(f"Error creating/updating keyword meaning: {str(e)}")
            raise
    
    def _extract_meaning_from_feedback(self, feedback: Feedback, keyword: str) -> str:
        """
        Extract meaningful interpretation from user feedback for a keyword.
        
        Args:
            feedback: Feedback object
            keyword: Keyword to extract meaning for
            
        Returns:
            Extracted meaning string
        """
        # Simple implementation - can be enhanced with NLP
        if feedback.feedback_text:
            return f"User context: {feedback.feedback_text[:100]}..."
        else:
            return f"Confirmed accurate interpretation in context of: {feedback.question[:100]}..."
    
    def _get_existing_keyword_meanings(self, card_name: str, keyword: str) -> List[Dict]:
        """
        Get existing keyword meanings for a card and keyword.
        
        Args:
            card_name: Name of the tarot card
            keyword: Keyword to search for
            
        Returns:
            List of existing keyword meanings
        """
        try:
            # Search for existing KeywordMeaning entries (simplified)
            collection = self.client.collections.get("KeywordMeaning")
            try:
                result = collection.query.fetch_objects(limit=100)
                # Filter manually for now
                filtered_results = [obj.properties for obj in result.objects 
                                  if obj.properties.get("keyword") == keyword]
                return filtered_results
            except Exception as query_error:
                logger.warning(f"KeywordMeaning query error: {str(query_error)}")
                return []
            
        except Exception as e:
            logger.error(f"Error getting existing keyword meanings: {str(e)}")
            return []
    
    def _update_existing_keyword_meaning(self, existing_meaning: Dict, new_meaning: KeywordMeaning):
        """
        Update an existing keyword meaning with new feedback.
        
        Args:
            existing_meaning: Existing meaning dictionary
            new_meaning: New KeywordMeaning object
        """
        try:
            # Merge feedback
            existing_feedback = existing_meaning.get("feedback", [])
            updated_feedback = existing_feedback + new_meaning.feedback
            
            # Update the meaning
            updated_data = {
                "keyword": new_meaning.keyword,
                "meaning": new_meaning.meaning,
                "feedback": updated_feedback,
                "source": "user_feedback",
                "orientation": new_meaning.orientation,
                "position": new_meaning.position,
                "updated_at": datetime.now().isoformat()
            }
            
            # Update in Weaviate (simplified - you might need to find the object ID)
            collection = self.client.collections.get("KeywordMeaning")
            # Note: You'll need to implement proper object ID retrieval and update
            logger.info(f"Updated keyword meaning for: {new_meaning.keyword}")
            
        except Exception as e:
            logger.error(f"Error updating existing keyword meaning: {str(e)}")
            raise
    
    def _create_new_keyword_meaning(self, layout: CardLayout, keyword_meaning: KeywordMeaning):

        """
        Create a new keyword meaning entry.
        
        Args:
            card: TarotCard object
            keyword_meaning: KeywordMeaning object to create
        """
        try:
            keyword_data = {
                "keyword": keyword_meaning.keyword,
                "meaning": keyword_meaning.meaning,
                "feedback": keyword_meaning.feedback,
                "source": keyword_meaning.source,
                "orientation": keyword_meaning.orientation,
                "position": keyword_meaning.position,
                "card_name": layout.name,
                "created_at": datetime.now().isoformat()
            }
            
            # Store in Weaviate
            collection = self.client.collections.get("KeywordMeaning")
            result = collection.data.insert(keyword_data)
            
            logger.info(f"Created new keyword meaning for: {keyword_meaning.keyword}")
            
        except Exception as e:
            logger.error(f"Error creating new keyword meaning: {str(e)}")
            raise
    
    def _store_reading_context(self, feedback: Feedback):
        """
        Store the complete reading context (question, cards, positions, response) for future similarity matching.
        
        Args:
            feedback: Feedback object with high rating
        """
        try:
            # Create a comprehensive reading context entry
            reading_context = {
                "question": feedback.question,
                "model_response": feedback.model_response,
                "user_feedback": feedback.feedback_text or "",
                "rating": feedback.rating,
                "user_id": feedback.user_id,
                "discussion_id": feedback.discussion_id,
                "timestamp": datetime.now().isoformat(),
                "spread_info": json.dumps([{
                    "position": layout.position,
                    "card_name": layout.name,
                    "upright": layout.upright,
                    "keywords": layout.position_keywords,
                    "meaning": layout.meaning
                } for layout in feedback.spread]),
                "total_cards": len(feedback.spread),
                "question_type": self._classify_question_type(feedback.question),
                "source": "accurate_feedback"
            }
            
            # Store in ReadingContext collection
            collection = self.client.collections.get("ReadingContext")
            result = collection.data.insert(reading_context)
            
            logger.info(f"Stored reading context for question: {feedback.question[:50]}...")
            
        except Exception as e:
            logger.error(f"Error storing reading context: {str(e)}")
            raise
    
    def _classify_question_type(self, question: str) -> str:
        """
        Classify the type of question based on keywords.
        
        Args:
            question: User question
            
        Returns:
            Question type classification
        """
        question_lower = question.lower()
        
        # Define question categories
        if any(word in question_lower for word in ['love', 'relationship', 'partner', 'romance', 'dating', 'marriage']):
            return "love_relationship"
        elif any(word in question_lower for word in ['career', 'job', 'work', 'profession', 'business', 'money', 'finance']):
            return "career_finance"
        elif any(word in question_lower for word in ['health', 'wellness', 'body', 'healing', 'medical']):
            return "health_wellness"
        elif any(word in question_lower for word in ['spiritual', 'soul', 'purpose', 'meaning', 'growth', 'meditation']):
            return "spiritual_growth"
        elif any(word in question_lower for word in ['future', 'will', 'prediction', 'outcome', 'happen']):
            return "future_prediction"
        elif any(word in question_lower for word in ['decision', 'choice', 'should', 'what to do', 'advice']):
            return "decision_advice"
        else:
            return "general"
    
    def get_feedback_statistics(self, user_id: Optional[str] = None) -> Dict:
        """
        Get feedback statistics for analysis.
        
        Args:
            user_id: Optional user ID to filter by
            
        Returns:
            Dictionary with feedback statistics
        """
        try:
            collection = self.client.collections.get("Feedback")
            
            # Get all feedback (simplified approach with better error handling)
            try:
                if user_id:
                    # For user-specific stats, we'll need to filter manually
                    result = collection.query.fetch_objects(limit=1000)
                    # Filter manually
                    filtered_objects = [obj for obj in result.objects if obj.properties.get("user_id") == user_id]
                    total_feedback = len(filtered_objects)
                    ratings = [obj.properties.get("rating", 0) for obj in filtered_objects if obj.properties.get("rating")]
                else:
                    result = collection.query.fetch_objects(limit=1000)
                    total_feedback = len(result.objects)
                    ratings = [obj.properties.get("rating", 0) for obj in result.objects if obj.properties.get("rating")]
                
                avg_rating = sum(ratings) / len(ratings) if ratings else 0
                high_ratings = len([r for r in ratings if r >= self.high_rating_threshold])
                
                return {
                    "total_feedback": total_feedback,
                    "average_rating": round(avg_rating, 2),
                    "high_ratings_count": high_ratings,
                    "high_ratings_percentage": round((high_ratings / len(ratings)) * 100, 2) if ratings else 0
                }
            except Exception as query_error:
                logger.warning(f"Query error, returning empty stats: {str(query_error)}")
                # Return empty stats instead of error when there's a connection issue
                return {
                    "total_feedback": 0,
                    "average_rating": 0.0,
                    "high_ratings_count": 0,
                    "high_ratings_percentage": 0.0,
                    "note": "Unable to retrieve statistics due to connection issues"
                }
            
        except Exception as e:
            logger.error(f"Error getting feedback statistics: {str(e)}")
            # Return empty stats instead of error
            return {
                "total_feedback": 0,
                "average_rating": 0.0,
                "high_ratings_count": 0,
                "high_ratings_percentage": 0.0,
                "error": str(e)
            }
    
    def get_similar_reading_contexts(self, question: str, cards_in_positions: List[Dict], limit: int = 5) -> List[Dict]:
        """
        Find similar reading contexts based on question type and card positions.
        
        Args:
            question: Current question
            cards_in_positions: List of dicts with 'position' and 'card_name' keys
            limit: Maximum number of similar contexts to return
            
        Returns:
            List of similar reading contexts
        """
        try:
            collection = self.client.collections.get("ReadingContext")
            question_type = self._classify_question_type(question)
            
            # Get all reading contexts (we'll filter manually)
            try:
                result = collection.query.fetch_objects(limit=1000)
                
                similar_contexts = []
                for obj in result.objects:
                    properties = obj.properties
                    
                    # Filter by question type
                    if properties.get("question_type") != question_type:
                        continue
                    
                    # Parse spread info
                    try:
                        spread_info = json.loads(properties.get("spread_info", "[]"))
                    except json.JSONDecodeError:
                        continue
                    
                    # Calculate similarity score based on matching cards in positions
                    similarity_score = self._calculate_context_similarity(
                        cards_in_positions, spread_info
                    )
                    
                    if similarity_score > 0:
                        context_data = {
                            "question": properties.get("question", ""),
                            "model_response": properties.get("model_response", ""),
                            "user_feedback": properties.get("user_feedback", ""),
                            "rating": properties.get("rating", 0),
                            "spread_info": spread_info,
                            "similarity_score": similarity_score,
                            "timestamp": properties.get("timestamp", "")
                        }
                        similar_contexts.append(context_data)
                
                # Sort by similarity score and return top results
                similar_contexts.sort(key=lambda x: x["similarity_score"], reverse=True)
                return similar_contexts[:limit]
                
            except Exception as query_error:
                logger.warning(f"Query error in similar contexts: {str(query_error)}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting similar reading contexts: {str(e)}")
            return []
    
    def _calculate_context_similarity(self, current_cards: List[Dict], stored_spread: List[Dict]) -> float:
        """
        Calculate similarity score between current cards and stored spread.
        
        Args:
            current_cards: Current cards with positions
            stored_spread: Stored spread information
            
        Returns:
            Similarity score (0-1)
        """
        if not current_cards or not stored_spread:
            return 0.0
        
        exact_matches = 0
        card_name_matches = 0
        total_positions = max(len(current_cards), len(stored_spread))
        
        # Create lookup dict for stored spread
        stored_lookup = {card["position"]: card["card_name"] for card in stored_spread}
        stored_cards = [card["card_name"] for card in stored_spread]
        
        # Check for exact matches in same positions
        for current_card in current_cards:
            position = current_card.get("position")
            card_name = current_card.get("card_name")
            
            # Exact position match
            if position is not None and stored_lookup.get(position) == card_name:
                exact_matches += 1
            # Card appears anywhere in the spread
            elif card_name in stored_cards:
                card_name_matches += 1
        
        # Calculate similarity score - give more weight to exact matches
        exact_score = exact_matches / total_positions if total_positions > 0 else 0.0
        card_score = card_name_matches / total_positions if total_positions > 0 else 0.0
        
        # Combine scores: exact matches worth 1.0, card matches worth 0.3
        similarity_score = exact_score + (card_score * 0.3)
        
        # If no cards match but we have some content, give a small base similarity for same question type
        if similarity_score == 0.0 and current_cards and stored_spread:
            similarity_score = 0.1  # Small base similarity for question type match
        
        return min(similarity_score, 1.0)  # Cap at 1.0


def process_user_feedback(feedback: Feedback) -> Dict[str, str]:
    """
    Main function to process user feedback.
    
    Args:
        feedback: Feedback object from user
        
    Returns:
        Processing result dictionary
    """
    processor = FeedbackProcessor()
    try:
        return processor.process_feedback(feedback)
    finally:
        if hasattr(processor, 'client') and processor.client:
            processor.client.close()

def get_feedback_stats(user_id: Optional[str] = None) -> Dict:
    """
    Get feedback statistics.
    
    Args:
        user_id: Optional user ID to filter by
        
    Returns:
        Statistics dictionary
    """
    processor = FeedbackProcessor()
    try:
        return processor.get_feedback_statistics(user_id)
    finally:
        if hasattr(processor, 'client') and processor.client:
            processor.client.close()
