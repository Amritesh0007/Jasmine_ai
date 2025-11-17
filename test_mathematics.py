"""
Test script for Mathematics module in Jasmine AI Assistant
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Model import FirstLayerDMM
from Backend.Mathematics import process_mathematical_query

def test_mathematical_capabilities():
    """Test all mathematical capabilities"""
    
    print("🧪 Testing Jasmine AI Assistant Mathematical Capabilities")
    print("=" * 60)
    
    # Test cases covering various mathematical operations
    test_cases = [
        # Calculus - Integration
        "integrate x squared",
        "integrate sin x",
        "integrate cos x",
        "integrate e^x",
        
        # Calculus - Differentiation
        "differentiate x squared",
        "differentiate sin x",
        "differentiate cos x",
        "differentiate e^x",
        
        # Algebra - Equation Solving
        "solve x^2 - 5*x + 6 = 0",
        "solve x^2 - 4 = 0",
        "solve 2*x + 3 = 7",
        
        # Limits
        "limit of 1/x as x approaches 0",
        
        # Complex expressions
        "integrate x^3 + 2*x^2 + x + 1",
        "differentiate x^3 + 2*x^2 + x + 1"
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n{i}. Query: {query}")
        
        # Test decision making
        decision = FirstLayerDMM(query)
        print(f"   Decision: {decision}")
        
        # Process mathematical queries
        if any('mathematics' in d for d in decision):
            for d in decision:
                if 'mathematics' in d:
                    math_query = d.replace('mathematics', '').strip()
                    result = process_mathematical_query(math_query)
                    print(f"   Result: {result}")
        
        print("-" * 50)
    
    print("\n✅ All mathematical tests completed!")
    print("\n🎯 Features implemented:")
    print("   • Integration (indefinite integrals)")
    print("   • Differentiation (derivatives)")
    print("   • Equation solving (polynomial equations)")
    print("   • Limit calculations")
    print("   • Support for trigonometric functions")
    print("   • Support for exponential functions")
    print("   • Natural language processing for math queries")

if __name__ == "__main__":
    test_mathematical_capabilities()