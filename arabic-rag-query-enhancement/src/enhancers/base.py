"""
Base Query Enhancer Interface
All query enhancement techniques should inherit from this class
"""

from typing import List


class QueryEnhancer:
    """Base class for query enhancement techniques"""
    
    def enhance(self, query: str, query_id: str = None) -> str:
        """
        Enhance a single query
        
        Args:
            query: Original query text
            query_id: Optional query ID for logging/debugging
            
        Returns:
            Enhanced query text
        """
        raise NotImplementedError("Subclasses must implement enhance()")
    
    def enhance_batch(self, queries: List[str], query_ids: List[str] = None) -> List[str]:
        """
        Enhance multiple queries
        
        Args:
            queries: List of query texts
            query_ids: Optional list of query IDs
            
        Returns:
            List of enhanced query texts
        """
        if query_ids is None:
            query_ids = [None] * len(queries)
        
        return [self.enhance(q, qid) for q, qid in zip(queries, query_ids)]


class IdentityEnhancer(QueryEnhancer):
    """
    Identity enhancer - returns query unchanged
    Used for baseline experiments
    """
    
    def enhance(self, query: str, query_id: str = None) -> str:
        """Return query unchanged"""
        return query


# Example usage
if __name__ == "__main__":
    # Test identity enhancer
    enhancer = IdentityEnhancer()
    
    test_query = "من هو رئيس مصر؟"
    enhanced = enhancer.enhance(test_query)
    
    print(f"Original: {test_query}")
    print(f"Enhanced: {enhanced}")
    print(f"Same: {test_query == enhanced}")
