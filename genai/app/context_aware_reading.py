"""
Context-aware reading enhancement module for TarotAI.
Uses stored feedback contexts to improve reading accuracy based on similar questions and card positions.
"""

# Standard library imports
import json
import os
import sys
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
import logging
from collections import Counter

# Add the server directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Local imports
from app.weaviate_client import get_weaviate_client
from app.models import TarotCard
from app.feedback import FeedbackProcessor
from app.logger_config import get_tarot_logger

# Set up logging
logger = get_tarot_logger(__name__)

class ContextAwareReader:
    """
    Enhances tarot readings by incorporating feedback from similar past readings.
    """
    
    def __init__(self):
        self.client = get_weaviate_client()
        self.feedback_processor = FeedbackProcessor()
        
    def enhance_reading_with_context(self, question: str, cards: List[TarotCard], 
                                   base_interpretation: str) -> Dict[str, str]:
        """
        Enhance a reading interpretation with context from similar past readings.
        
        Args:
            question: Current question
            cards: Cards drawn for current reading
            base_interpretation: Original AI interpretation
            
        Returns:
            Enhanced interpretation with context insights
        """
        try:
            # Prepare cards for similarity matching
            cards_in_positions = [
                {
                    "position": i,
                    "card_name": card.name
                }
                for i, card in enumerate(cards)
            ]
            
            # Get similar contexts
            similar_contexts = self.feedback_processor.get_similar_reading_contexts(
                question=question,
                cards_in_positions=cards_in_positions,
                limit=3
            )
            
            if not similar_contexts:
                return {
                    "enhanced_interpretation": base_interpretation,
                    "context_insights": "No similar readings found in feedback history.",
                    "confidence_boost": 0,
                    "similar_contexts_count": 0
                }
            
            # Generate context insights
            context_insights = self._generate_context_insights(similar_contexts, cards)
            
            # Enhance the interpretation
            enhanced_interpretation = self._enhance_interpretation(
                base_interpretation, context_insights, similar_contexts
            )
            
            # Calculate confidence boost
            confidence_boost = self._calculate_confidence_boost(similar_contexts)
            
            logger.info(f"Enhanced reading with {len(similar_contexts)} similar contexts")
            
            return {
                "enhanced_interpretation": enhanced_interpretation,
                "context_insights": context_insights,
                "confidence_boost": confidence_boost,
                "similar_contexts_count": len(similar_contexts),
                "similar_contexts": similar_contexts  # For debugging/transparency
            }
            
        except Exception as e:
            logger.error(f"Error enhancing reading with context: {str(e)}")
            return {
                "enhanced_interpretation": base_interpretation,
                "context_insights": f"Error retrieving context: {str(e)}",
                "confidence_boost": 0,
                "similar_contexts_count": 0
            }
    
    def _generate_context_insights(self, similar_contexts: List[Dict], current_cards: List[TarotCard]) -> str:
        """
        Generate insights based on similar contexts.
        
        Args:
            similar_contexts: List of similar reading contexts
            current_cards: Current cards drawn
            
        Returns:
            Context insights string
        """
        if not similar_contexts:
            return "No similar readings found."
        
        insights = []
        
        # Analyze patterns across similar contexts
        high_rated_contexts = [ctx for ctx in similar_contexts if ctx.get("rating", 0) >= 4]
        
        if high_rated_contexts:
            insights.append(f"Based on {len(high_rated_contexts)} similar high-rated readings:")
            
            # Common feedback themes
            feedback_themes = []
            for ctx in high_rated_contexts:
                feedback = ctx.get("user_feedback", "")
                if feedback:
                    feedback_themes.append(feedback[:100] + "..." if len(feedback) > 100 else feedback)
            
            if feedback_themes:
                insights.append("Previous users found these interpretations particularly accurate:")
                for i, theme in enumerate(feedback_themes[:2], 1):
                    insights.append(f"  {i}. {theme}")
        
        # Card-specific insights
        card_insights = self._analyze_card_patterns(similar_contexts, current_cards)
        if card_insights:
            insights.append("Card-specific insights from similar readings:")
            insights.extend(card_insights)
        
        return "\n".join(insights) if insights else "Similar readings found, but no specific patterns identified."
    
    def _analyze_card_patterns(self, similar_contexts: List[Dict], current_cards: List[TarotCard]) -> List[str]:
        """
        Analyze patterns for specific cards in similar positions.
        
        Args:
            similar_contexts: List of similar reading contexts
            current_cards: Current cards drawn
            
        Returns:
            List of card-specific insights
        """
        card_insights = []
        
        for position, card in enumerate(current_cards):
            # Find contexts where this card appeared in this position
            matching_contexts = []
            
            for ctx in similar_contexts:
                spread_info = ctx.get("spread_info", [])
                for spread_card in spread_info:
                    if (spread_card.get("position") == position and 
                        spread_card.get("card_name") == card.name):
                        matching_contexts.append(ctx)
                        break
            
            if matching_contexts:
                # Analyze what users said about this card in this position
                positive_feedback = []
                for ctx in matching_contexts:
                    if ctx.get("rating", 0) >= 4:
                        feedback = ctx.get("user_feedback", "")
                        if feedback:
                            positive_feedback.append(feedback)
                
                if positive_feedback:
                    card_insights.append(
                        f"  • {card.name} in position {position + 1}: Previous users appreciated interpretations focusing on {self._extract_key_themes(positive_feedback)}"
                    )
        
        return card_insights
    
    def _extract_key_themes(self, feedback_list: List[str]) -> str:
        """
        Extract key themes from feedback text.
        
        Args:
            feedback_list: List of feedback strings
            
        Returns:
            Summary of key themes
        """
        # Simple keyword extraction (could be enhanced with NLP)
        all_feedback = " ".join(feedback_list).lower()
        
        theme_keywords = {
            "accuracy": ["accurate", "correct", "right", "precise", "exact"],
            "insight": ["insightful", "deep", "meaningful", "profound", "revealing"],
            "guidance": ["helpful", "guidance", "direction", "advice", "clarity"],
            "resonance": ["resonated", "connected", "felt", "understood", "related"],
            "timing": ["timing", "when", "future", "soon", "time"],
            "practical": ["practical", "actionable", "useful", "applicable", "doable"]
        }
        
        found_themes = []
        for theme, keywords in theme_keywords.items():
            if any(keyword in all_feedback for keyword in keywords):
                found_themes.append(theme)
        
        return ", ".join(found_themes) if found_themes else "meaningful insights"
    
    def _enhance_interpretation(self, base_interpretation: str, context_insights: str, 
                              similar_contexts: List[Dict]) -> str:
        """
        Enhance the base interpretation with context insights.
        
        Args:
            base_interpretation: Original interpretation
            context_insights: Context insights from similar readings
            similar_contexts: List of similar contexts
            
        Returns:
            Enhanced interpretation
        """
        if not similar_contexts:
            return base_interpretation
        
        # Build enhanced interpretation
        enhanced_parts = [base_interpretation]
        
        # Add context-based confidence note if we have similar contexts
        if len(similar_contexts) >= 1:
            enhanced_parts.append(
                f"\n\n✨ **Context Enhancement**: This interpretation is supported by {len(similar_contexts)} similar reading{'s' if len(similar_contexts) > 1 else ''} that received high accuracy ratings from users."
            )
        
        # Add specific insights if available
        if context_insights and "No similar readings found" not in context_insights:
            enhanced_parts.append(f"\n\n📚 **Based on Similar Readings**:\n{context_insights}")
        
        return "\n".join(enhanced_parts)
    
    def _calculate_confidence_boost(self, similar_contexts: List[Dict]) -> float:
        """
        Calculate confidence boost based on similar contexts.
        
        Args:
            similar_contexts: List of similar reading contexts
            
        Returns:
            Confidence boost score (0-1)
        """
        if not similar_contexts:
            return 0.0
        
        # Base boost on number of similar contexts and their ratings
        total_score = 0.0
        for ctx in similar_contexts:
            rating = ctx.get("rating", 0)
            similarity = ctx.get("similarity_score", 0)
            
            # Weight by both rating and similarity
            context_score = (rating / 5.0) * similarity
            total_score += context_score
        
        # Normalize by number of contexts
        average_score = total_score / len(similar_contexts)
        
        # Cap at 1.0 and apply a scaling factor
        confidence_boost = min(1.0, average_score * 1.2)
        
        return round(confidence_boost, 2)
    
    def get_context_statistics(self) -> Dict:
        """
        Get statistics about stored reading contexts.
        
        Returns:
            Dictionary with context statistics
        """
        try:
            collection = self.client.collections.get("ReadingContext")
            
            try:
                result = collection.query.fetch_objects(limit=1000)
                contexts = result.objects
                
                if not contexts:
                    return {
                        "total_contexts": 0,
                        "question_types": {},
                        "average_rating": 0.0,
                        "most_common_cards": []
                    }
                
                # Analyze question types
                question_types = {}
                ratings = []
                all_cards = []
                
                for obj in contexts:
                    props = obj.properties
                    
                    # Count question types
                    q_type = props.get("question_type", "unknown")
                    question_types[q_type] = question_types.get(q_type, 0) + 1
                    
                    # Collect ratings
                    rating = props.get("rating", 0)
                    if rating:
                        ratings.append(rating)
                    
                    # Collect cards
                    try:
                        spread_info = json.loads(props.get("spread_info", "[]"))
                        for card_info in spread_info:
                            all_cards.append(card_info.get("card_name", ""))
                    except json.JSONDecodeError:
                        continue
                
                # Calculate statistics
                avg_rating = sum(ratings) / len(ratings) if ratings else 0.0
                
                # Most common cards
                card_counts = Counter(all_cards)
                most_common_cards = card_counts.most_common(5)
                
                return {
                    "total_contexts": len(contexts),
                    "question_types": question_types,
                    "average_rating": round(avg_rating, 2),
                    "most_common_cards": most_common_cards,
                    "total_ratings": len(ratings)
                }
                
            except Exception as query_error:
                logger.warning(f"Query error in context stats: {str(query_error)}")
                return {"error": str(query_error)}
                
        except Exception as e:
            logger.error(f"Error getting context statistics: {str(e)}")
            return {"error": str(e)}
    
    def close(self):
        """Close the client connection."""
        if hasattr(self, 'client') and self.client:
            self.client.close()
        if hasattr(self, 'feedback_processor') and self.feedback_processor.client:
            self.feedback_processor.client.close()


def enhance_reading_with_feedback_context(question: str, cards: List[TarotCard], 
                                        base_interpretation: str) -> Dict[str, str]:
    """
    Main function to enhance a reading with feedback context.
    
    Args:
        question: Current question
        cards: Cards drawn for current reading
        base_interpretation: Original AI interpretation
        
    Returns:
        Enhanced interpretation with context insights
    """
    reader = ContextAwareReader()
    try:
        return reader.enhance_reading_with_context(question, cards, base_interpretation)
    finally:
        reader.close()
