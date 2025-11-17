"""
Test for the specific mathematical query that was causing issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Model import FirstLayerDMM
from Backend.Mathematics import process_mathematical_query

def test_specific_math_query():
    """Test the specific query that was causing syntax errors"""
    
    print("🧪 Testing Specific Mathematical Query Fix")
    print("=" * 50)
    
    # The specific query that was causing issues
    query = "Differentiation of tan x with respect to x."
    
    print(f"Query: {query}")
    
    # Test decision making
    decision = FirstLayerDMM(query)
    print(f"Decision: {decision}")
    
    # Process mathematical queries
    if any('mathematics' in d for d in decision):
        for d in decision:
            if 'mathematics' in d:
                math_query = d.replace('mathematics', '').strip()
                print(f"Extracted Math Query: '{math_query}'")
                result = process_mathematical_query(math_query)
                print(f"Result: {result}")
                
                # Check if successful
                if not result.startswith("Error"):
                    print("\n✅ Success! The syntax error has been fixed.")
                else:
                    print("\n❌ Still encountering errors.")
    else:
        print("❌ Query not recognized as mathematical.")
    
    print("\n" + "=" * 50)
    print("Additional test cases:")
    
    # Test a few more similar cases
    test_cases = [
        "Differentiate sin x with respect to x",
        "Integration of cos x with respect to x",
        "differentiate tan x"
    ]
    
    for test_query in test_cases:
        print(f"\nQuery: {test_query}")
        decision = FirstLayerDMM(test_query)
        print(f"Decision: {decision}")
        
        if any('mathematics' in d for d in decision):
            for d in decision:
                if 'mathematics' in d:
                    math_query = d.replace('mathematics', '').strip()
                    result = process_mathematical_query(math_query)
                    print(f"Result: {result}")

if __name__ == "__main__":
    test_specific_math_query()