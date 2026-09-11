"""
Enhanced ROMAX Chatbot - Test Examples
This file demonstrates all new features of the chatbot
"""

from chatbot_responses import get_response


def test_matrix_operations():
    """Test all matrix operations"""
    print("\n" + "="*60)
    print("MATRIX OPERATIONS TESTS")
    print("="*60 + "\n")
    
    tests = [
        ("Matrix Addition", "matrix addition [[1,2],[3,4]] [[5,6],[7,8]]"),
        ("Matrix Subtraction", "matrix subtraction [[10,20],[30,40]] [[1,2],[3,4]]"),
        ("Matrix Multiplication", "matrix multiply [[1,2],[3,4]] [[5,6],[7,8]]"),
        ("Matrix Inverse", "matrix inverse [[4,7],[2,6]]"),
        ("Matrix Determinant", "determinant [[1,2],[3,4]]"),
        ("Solve Linear System", "solve equation [[2,1],[1,3]] [[8],[9]]"),
    ]
    
    for name, query in tests:
        print(f"Test: {name}")
        print(f"Input: {query}")
        result = get_response(query)
        print(f"Output:\n{result}\n")
        print("-" * 60 + "\n")


def test_calculus_operations():
    """Test calculus operations"""
    print("\n" + "="*60)
    print("CALCULUS OPERATIONS TESTS")
    print("="*60 + "\n")
    
    tests = [
        ("Simple Polynomial", "derivative of x**2 + 3*x"),
        ("Trigonometric", "derivative of sin(x) * cos(x)"),
        ("Exponential", "integral of exp(x)"),
        ("Rational Function", "derivative of 1/x"),
        ("Complex Expression", "integral of x**2 + sin(x)"),
        ("Logarithmic", "derivative of log(x)"),
    ]
    
    for name, query in tests:
        print(f"Test: {name}")
        print(f"Input: {query}")
        result = get_response(query)
        print(f"Output:\n{result}\n")
        print("-" * 60 + "\n")


def test_ai_concepts():
    """Test AI/ML concept explanations"""
    print("\n" + "="*60)
    print("AI/ML CONCEPT EXPLANATION TESTS")
    print("="*60 + "\n")
    
    concepts = [
        ("Machine Learning", "explain machine learning"),
        ("Deep Learning", "what is deep learning"),
        ("Neural Networks", "define neural networks"),
        ("NLP", "explain natural language processing"),
        ("Computer Vision", "what is computer vision"),
        ("Convolutional Neural Networks", "explain convolutional neural networks"),
        ("Transfer Learning", "what is transfer learning"),
        ("Data Science", "define data science"),
    ]
    
    for name, query in concepts:
        print(f"Test: {name}")
        print(f"Input: {query}")
        result = get_response(query)
        print(f"Output:\n{result}\n")
        print("-" * 60 + "\n")


def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n" + "="*60)
    print("EDGE CASES & ERROR HANDLING")
    print("="*60 + "\n")
    
    edge_cases = [
        ("Singular Matrix Inverse", "matrix inverse [[1,2],[2,4]]"),
        ("Dimension Mismatch", "matrix addition [[1,2],[3,4]] [[1,2,3]]"),
        ("Invalid Expression", "derivative of invalid_syntax()"),
        ("Unknown Concept", "explain quantum computing"),
    ]
    
    for name, query in edge_cases:
        print(f"Test: {name}")
        print(f"Input: {query}")
        result = get_response(query)
        print(f"Output:\n{result}\n")
        print("-" * 60 + "\n")


def test_mixed_operations():
    """Test realistic use cases combining multiple features"""
    print("\n" + "="*60)
    print("MIXED OPERATIONS (REALISTIC USE CASES)")
    print("="*60 + "\n")
    
    scenarios = [
        ("Learning Linear Algebra & AI",
         ["matrix multiply [[2,3],[1,4]] [[5],[6]]",
          "explain machine learning"]),
        ("Calculus Problem Solving",
         ["derivative of x**3 - 2*x**2 + 5*x - 3",
          "integral of x**2 + 2*x"]),
        ("System of Equations & AI",
         ["solve equation [[1,1],[2,3]] [[5],[8]]",
          "what is data science"]),
    ]
    
    for scenario_name, queries in scenarios:
        print(f"Scenario: {scenario_name}\n")
        for i, query in enumerate(queries, 1):
            print(f"Step {i}: {query}")
            result = get_response(query)
            print(f"Result: {result}\n")
        print("-" * 60 + "\n")


def test_basic_features():
    """Test that basic chatbot features still work"""
    print("\n" + "="*60)
    print("BASIC FEATURES TESTS (Backward Compatibility)")
    print("="*60 + "\n")
    
    basic_tests = [
        ("Greeting", "hello"),
        ("Identity", "who are you"),
        ("Math", "5 + 3"),
        ("Time", "what time is it"),
    ]
    
    for name, query in basic_tests:
        print(f"Test: {name}")
        print(f"Input: {query}")
        result = get_response(query)
        print(f"Output: {result}\n")
        print("-" * 60 + "\n")


if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   ENHANCED ROMAX CHATBOT - COMPREHENSIVE TEST SUITE       ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # Run all tests
    test_basic_features()
    test_matrix_operations()
    test_calculus_operations()
    test_ai_concepts()
    test_edge_cases()
    test_mixed_operations()
    
    print("\n" + "═"*60)
    print("✓ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("═"*60 + "\n")
