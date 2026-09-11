# This special function used for Chatbot responses
# This code is used for the Chatbot.py
# re: Detect math (or specific) expressions in the input
import re
import math
import random
from datetime import datetime
import numpy as np
from scipy import integrate, optimize
import sympy as sp
import requests
from typing import List, Tuple, Optional


# ============= MATRIX OPERATIONS =============
def parse_matrix_input(user_input: str) -> Optional[Tuple[np.ndarray, ...]]:
    """Parse matrix input from user (format: [[1,2],[3,4]])"""
    try:
        # Extract matrices from input (format: [[...], [...]])
        matrix_pattern = r'\[\s*\[.*?\]\s*\]'
        matrices_str = re.findall(matrix_pattern, user_input)
        if not matrices_str:
            return None
        matrices = [np.array(eval(m)) for m in matrices_str]
        return tuple(matrices) if len(matrices) > 1 else (matrices[0],)
    except:
        return None


def matrix_addition(a: np.ndarray, b: np.ndarray) -> str:
    """Perform matrix addition"""
    try:
        if a.shape != b.shape:
            return "Error: Matrices must have the same dimensions for addition."
        result = a + b
        return f"Matrix Addition Result:\n{result}\n\nNumerical:\n{result.tolist()}"
    except Exception as e:
        return f"Error in matrix addition: {str(e)}"


def matrix_subtraction(a: np.ndarray, b: np.ndarray) -> str:
    """Perform matrix subtraction"""
    try:
        if a.shape != b.shape:
            return "Error: Matrices must have the same dimensions for subtraction."
        result = a - b
        return f"Matrix Subtraction Result:\n{result}\n\nNumerical:\n{result.tolist()}"
    except Exception as e:
        return f"Error in matrix subtraction: {str(e)}"


def matrix_multiplication(a: np.ndarray, b: np.ndarray) -> str:
    """Perform matrix multiplication"""
    try:
        if a.shape[1] != b.shape[0]:
            return f"Error: Cannot multiply matrices with shapes {a.shape} and {b.shape}. Columns of first matrix must equal rows of second."
        result = np.dot(a, b)
        return f"Matrix Multiplication Result:\n{result}\n\nNumerical:\n{result.tolist()}"
    except Exception as e:
        return f"Error in matrix multiplication: {str(e)}"


def matrix_inverse(a: np.ndarray) -> str:
    """Compute matrix inverse"""
    try:
        if a.shape[0] != a.shape[1]:
            return "Error: Matrix must be square to compute inverse."
        det = np.linalg.det(a)
        if abs(det) < 1e-10:
            return f"Error: Matrix is singular (determinant ≈ 0). Inverse does not exist.\nDeterminant: {det}"
        result = np.linalg.inv(a)
        return f"Matrix Inverse:\n{result}\n\nNumerical:\n{result.tolist()}"
    except Exception as e:
        return f"Error in matrix inverse: {str(e)}"


def matrix_determinant(a: np.ndarray) -> str:
    """Compute matrix determinant"""
    try:
        if a.shape[0] != a.shape[1]:
            return "Error: Matrix must be square to compute determinant."
        det = np.linalg.det(a)
        return f"Determinant of the matrix: {det:.6f}"
    except Exception as e:
        return f"Error in determinant calculation: {str(e)}"


def solve_linear_system(a: np.ndarray, b: np.ndarray) -> str:
    """Solve system of linear equations Ax = b"""
    try:
        if a.shape[0] != a.shape[1]:
            return "Error: Coefficient matrix must be square."
        if a.shape[0] != b.shape[0]:
            return "Error: Coefficient matrix rows must match constant vector length."
        x = np.linalg.solve(a, b)
        return f"Solution to the system Ax = b:\n{x}\n\nNumerical:\n{x.tolist()}"
    except np.linalg.LinAlgError:
        return "Error: System has no unique solution (singular matrix)."
    except Exception as e:
        return f"Error solving system: {str(e)}"


# ============= CALCULUS OPERATIONS =============
def parse_calculus_expression(user_input: str) -> Optional[str]:
    """Extract mathematical expression from user input"""
    try:
        # Try to extract expression after keywords
        expr_patterns = [
            r'(?:derivative|derivative of|differentiate)\s+(?:of\s+)?([^?]+)',
            r'(?:integral|integral of|integrate)\s+(?:of\s+)?([^?]+)',
        ]
        for pattern in expr_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    except:
        return None


def compute_derivative(expr_str: str, return_equation: bool = True) -> str:
    """Compute derivative of an expression"""
    try:
        x = sp.Symbol('x')
        expr = sp.sympify(expr_str)
        derivative = sp.diff(expr, x)
        
        if return_equation:
            return f"Derivative of {expr}:\nd/dx({expr}) = {derivative}"
        else:
            return f"Derivative equation:\n{derivative}"
    except Exception as e:
        return f"Error computing derivative: {str(e)}\nMake sure to use valid expressions like: x**2, sin(x), exp(x), etc."


def compute_integral(expr_str: str, return_equation: bool = True) -> str:
    """Compute indefinite integral of an expression"""
    try:
        x = sp.Symbol('x')
        expr = sp.sympify(expr_str)
        integral = sp.integrate(expr, x)
        
        if return_equation:
            return f"Integral of {expr}:\n∫{expr}dx = {integral} + C"
        else:
            return f"Integral equation:\n{integral} + C"
    except Exception as e:
        return f"Error computing integral: {str(e)}\nMake sure to use valid expressions like: x**2, sin(x), cos(x), exp(x), etc."


# ============= AI CONCEPTS EXPLANATION =============
def get_ai_concept_from_geeksforgeeks(concept: str) -> Optional[str]:
    """Fetch AI concept explanation from GeeksforGeeks"""
    try:
        search_url = f"https://www.geeksforgeeks.org/search/?q={concept}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            # Try to extract meaningful content
            # GeeksforGeeks typically has articles about these topics
            if f"/{concept.replace(' ', '-').lower()}" in response.text:
                return f"Information about '{concept}' is available on GeeksforGeeks: {search_url}"
        return None
    except:
        return None


def get_ai_concept_from_wikipedia(concept: str) -> Optional[str]:
    """Fetch AI concept explanation from Wikipedia"""
    try:
        api_url = "https://en.wikipedia.org/api/rest_v1/page/summary"
        response = requests.get(f"{api_url}/{concept.replace(' ', '_')}", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if 'extract' in data:
                return data['extract']
        return None
    except:
        return None


def explain_ai_concept(concept: str) -> str:
    """Explain advanced AI/ML concepts using Wikipedia or built-in knowledge"""
    concept_lower = concept.lower()
    
    # Try to get from Wikipedia first
    wiki_explanation = get_ai_concept_from_wikipedia(concept)
    if wiki_explanation:
        return f"**{concept}** (from Wikipedia):\n{wiki_explanation}"
    
    # Fallback to built-in explanations for common concepts
    builtin_concepts = {
        'machine learning': 
            "Machine Learning (ML) is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.\n"
            "Key aspects:\n"
            "- Supervised Learning: Learn from labeled data (classification, regression)\n"
            "- Unsupervised Learning: Find patterns in unlabeled data (clustering)\n"
            "- Reinforcement Learning: Learn through trial and error with rewards/penalties",
        
        'deep learning':
            "Deep Learning is a subset of machine learning using artificial neural networks with multiple layers (deep networks).\n"
            "Key aspects:\n"
            "- Neural Networks: Mimic biological neurons\n"
            "- Backpropagation: Algorithm for training deep networks\n"
            "- Applications: Image recognition, NLP, speech recognition, autonomous vehicles",
        
        'natural language processing':
            "Natural Language Processing (NLP) is an AI technique that focuses on enabling computers to understand, interpret, and generate human language.\n"
            "Key tasks:\n"
            "- Sentiment Analysis: Determine emotions in text\n"
            "- Named Entity Recognition: Identify people, places, organizations\n"
            "- Machine Translation: Translate between languages\n"
            "- Question Answering: Systems that answer user questions",
        
        'computer vision':
            "Computer Vision is a field of AI that trains computers to interpret and understand the visual world.\n"
            "Key tasks:\n"
            "- Object Detection: Identify objects in images\n"
            "- Image Classification: Categorize images\n"
            "- Face Recognition: Identify individuals from faces\n"
            "- Semantic Segmentation: Assign labels to each pixel",
        
        'neural networks':
            "Neural Networks are computing systems inspired by biological neural networks in animal brains.\n"
            "Structure:\n"
            "- Input Layer: Receives data\n"
            "- Hidden Layers: Process information\n"
            "- Output Layer: Produces predictions\n"
            "- Activation Functions: Introduce non-linearity (ReLU, Sigmoid, Tanh)",
        
        'convolutional neural networks':
            "Convolutional Neural Networks (CNNs) are specialized neural networks for processing grid-like data, particularly images.\n"
            "Key components:\n"
            "- Convolutional Layers: Extract features using filters\n"
            "- Pooling Layers: Reduce spatial dimensions\n"
            "- Fully Connected Layers: Make predictions\n"
            "- Applications: Image classification, object detection, facial recognition",
        
        'recurrent neural networks':
            "Recurrent Neural Networks (RNNs) are neural networks designed for sequential data.\n"
            "Key types:\n"
            "- LSTM (Long Short-Term Memory): Handle long-term dependencies\n"
            "- GRU (Gated Recurrent Unit): Simplified LSTM variant\n"
            "- Applications: Time series, language modeling, machine translation",
        
        'transfer learning':
            "Transfer Learning is a technique where a model trained on one task is repurposed for another task.\n"
            "Benefits:\n"
            "- Reduced training time and data requirements\n"
            "- Better performance with limited data\n"
            "- Knowledge from one domain applied to another\n"
            "- Common in computer vision and NLP",
        
        'data science':
            "Data Science is an interdisciplinary field that uses scientific methods, processes, and systems to extract knowledge from data.\n"
            "Key areas:\n"
            "- Data Collection & Cleaning: Prepare data for analysis\n"
            "- Exploratory Data Analysis: Understand data patterns\n"
            "- Statistical Analysis: Test hypotheses\n"
            "- Machine Learning: Build predictive models\n"
            "- Data Visualization: Communicate insights",
    }
    
    for key, value in builtin_concepts.items():
        if key in concept_lower:
            return f"**{concept}**:\n{value}"
    
    # If not found, try GeeksforGeeks
    gfg_info = get_ai_concept_from_geeksforgeeks(concept)
    if gfg_info:
        return gfg_info
    
    return f"I don't have information about '{concept}'. Try asking about: Machine Learning, Deep Learning, Neural Networks, NLP, Computer Vision, Transfer Learning, or Data Science."


def get_response(user_input):
    user_input = user_input.lower().strip()

    # ============= MATRIX OPERATIONS PATTERNS =============
    if 'matrix addition' in user_input:
        matrices = parse_matrix_input(user_input)
        if matrices and len(matrices) >= 2:
            return matrix_addition(matrices[0], matrices[1])
        return "Please provide two matrices in format: matrix addition [[1,2],[3,4]] + [[5,6],[7,8]]"

    elif 'matrix subtraction' in user_input:
        matrices = parse_matrix_input(user_input)
        if matrices and len(matrices) >= 2:
            return matrix_subtraction(matrices[0], matrices[1])
        return "Please provide two matrices in format: matrix subtraction [[1,2],[3,4]] - [[5,6],[7,8]]"

    elif 'matrix multiply' in user_input or 'matrix multiplication' in user_input:
        matrices = parse_matrix_input(user_input)
        if matrices and len(matrices) >= 2:
            return matrix_multiplication(matrices[0], matrices[1])
        return "Please provide two matrices in format: matrix multiply [[1,2],[3,4]] * [[5,6],[7,8]]"

    elif 'matrix inverse' in user_input or 'inverse of matrix' in user_input:
        matrices = parse_matrix_input(user_input)
        if matrices:
            return matrix_inverse(matrices[0])
        return "Please provide a matrix in format: matrix inverse [[1,2],[3,4]]"

    elif 'determinant' in user_input:
        matrices = parse_matrix_input(user_input)
        if matrices:
            return matrix_determinant(matrices[0])
        return "Please provide a matrix in format: determinant [[1,2],[3,4]]"

    elif 'solve' in user_input and 'equation' in user_input or 'solve linear' in user_input:
        matrices = parse_matrix_input(user_input)
        if matrices and len(matrices) >= 2:
            return solve_linear_system(matrices[0], matrices[1])
        return "Please provide coefficient matrix and constant vector in format: solve equation [[1,2],[3,4]] [[5],[6]]"

    # ============= CALCULUS OPERATIONS PATTERNS =============
    elif 'derivative' in user_input or 'differentiate' in user_input:
        expr = parse_calculus_expression(user_input)
        if expr:
            return_eq = 'equation' not in user_input
            return compute_derivative(expr, return_eq)
        return "Please provide an expression. Example: derivative of x**2 + 3*x\nSupported: x**2, sin(x), cos(x), exp(x), log(x), sqrt(x)"

    elif 'integral' in user_input or 'integrate' in user_input:
        expr = parse_calculus_expression(user_input)
        if expr:
            return_eq = 'equation' not in user_input
            return compute_integral(expr, return_eq)
        return "Please provide an expression. Example: integral of x**2 + 3*x\nSupported: x**2, sin(x), cos(x), exp(x), log(x), sqrt(x)"

    # ============= AI CONCEPTS PATTERNS =============
    # Check for direct AI concept keywords (even without question words)
    ai_keywords_direct = ['machine learning', 'deep learning', 'neural network', 'nlp', 'natural language processing',
                          'computer vision', 'convolutional', 'cnn', 'recurrent', 'rnn', 'lstm', 'gru', 
                          'transfer learning', 'data science', 'reinforcement learning', 'supervised learning',
                          'unsupervised learning', 'clustering', 'classification', 'regression']
    for keyword in ai_keywords_direct:
        if keyword in user_input:
            return explain_ai_concept(keyword)
    
    if re.search(r'\b(explain|what is|define)\s+(.+)', user_input):
        match = re.search(r'\b(explain|what is|define)\s+(.+)', user_input)
        if match:
            concept = match.group(2).strip('?').strip()
            ai_keywords = ['machine learning', 'deep learning', 'neural network', 'nlp', 'natural language processing',
                          'computer vision', 'convolutional', 'cnn', 'recurrent', 'rnn', 'lstm', 'gru', 
                          'transfer learning', 'data science', 'reinforcement learning', 'supervised learning',
                          'unsupervised learning', 'clustering', 'classification', 'regression']
            if any(keyword in concept.lower() for keyword in ai_keywords):
                return explain_ai_concept(concept)

    elif user_input in ['hi', 'hello', 'hi there']:
        responses = ["Hello! How can I help you today?",
                     "Hi there! How can I help you?",
                     "Hello there! It is a great day today!!",
                     "Greetings! How can I assist you today?"]

    elif user_input in ['who are you', 'what is your name']:
        responses = ["I am ROMAX, your one and only assistant.",
                     "I am ROMAX, an AI assistant.",
                     "I am ROMAX, you can ask me anything."]

    elif user_input in ['how are you', 'how are you today', 'how are you feeling', 'how are you feeling today']:
        responses = ["I'm fine. Thank You!", "I'm doing great. Thanks!", "I'm feeling very good!!"]

    elif user_input in ['what time is it', 'what is the time', 'what is the current time',
                        'what is the time now', 'what is the time right now', 'time']:
        current_time = datetime.now().strftime('%I:%M %p')
        responses = [f"The current time is {current_time}.",
                     f"Right now, it is {current_time}.",
                     f"It is {current_time} right now."]

    elif re.search(r'\d+\s*([+\-*/%^])\s*\d+', user_input):
        try:
            cleaned_input = re.sub(r'[^0-9+\-*/%^.]', '', user_input)
            result = eval(cleaned_input)
            responses = [f"The result of {cleaned_input} is {result}.",
                         f"{cleaned_input} equals {result}.",
                         f"The answer to {cleaned_input} is {result}.",
                         f"It is {result}"]
        except ZeroDivisionError:
            responses = ["Division by zero is undefined"]
        except:
            responses = ["Sorry. I couldn't calculate that. Please enter a valid math expression."]

    elif re.search(r'square root of (-?\d+)', user_input):
        try:
            number = int(re.search(r'square root of (-?\d+)', user_input).group(1))
            if number < 0:
                responses = [f"{number} is a negative number. The square root is undefined.",
                             f"The square root of {number} is undefined since it is negative",
                             f"The square root cannot be computed since {number} < 0"]
            else:
                sqrt_result = math.sqrt(number)
                responses = [f"The square root of {number} is {sqrt_result:.9f}.",
                             f"√{number} equals {sqrt_result:.9f}.",
                             f"The square root of {number} is approximately {sqrt_result:.9f}."]
        except:
            responses = ["Sorry, there was an error calculating the square root. Try again."]

    elif re.search(r'(\d+)\s*power\s*by\s*(\d+)', user_input):
        try:
            match = re.search(r'(\d+)\s*power\s*by\s*(\d+)', user_input)
            base = int(match.group(1))
            exponent = int(match.group(2))
            result = base ** exponent
            responses = [f"{base} power by {exponent} is {result}.",
                         f"{base} raised to the power of {exponent} equals {result}.",
                         f"The result of {base} power by {exponent} is {result}."]
        except:
            responses = ["Sorry, there was an error calculating the power. Please try again.",
                         "Sorry, the number is too large, I cannot compute it."]

    elif re.search(r'\bpython\b', user_input):
        responses = ["Python is an interpreted, object-oriented, high-level programming language, "
                     "developed by Guido van Rossum, originally released in 1991. "
                     "It is widely used for backend web development, data science, AI, and automation.",
                     "Python is a programming language used for server-side, backend web development, "
                     "software development, solving mathematics, productivity tools, games, and desktop apps. "
                     "It's known for its simplicity and readability.",
                     "Python is one of the most popular programming languages today. "
                     "It's used in data science, machine learning, web development, and AI projects."]

    elif re.search(r'\bjava\b', user_input):
        responses = ["Java is a programming language used to develop mobile apps, "
                     "web apps, desktop apps, games and much more.",
                     "Java is a flexible language used to develop many software applications. "
                     "It is used in Big Data, AI, and IoT projects."]

    elif (re.search(r'c\s+and\s+c\+\+', user_input) or re.search(r'c\s+vs\s+c\+\+', user_input)
          or re.search(r'c\+\+\s+vs+\sc', user_input) or re.search(r'c\+\+\s+and+\sc', user_input)):
        responses = ["C++ was developed as an extension of C, and both languages have almost the same syntax. "
                     "The main difference between C and C++ is that C++ supports classes and objects, "
                     "while C does not.",
                     "C is a procedural language with a static system, "
                     "while C++ is a version extension of C, with support for object-oriented installations.",
                     "C++ is often viewed as a superset of C. "
                     "C++ is also known as a 'C with class'. "
                     "This was very nearly true when C++ was originally created, "
                     "but the two languages have evolved over time with "
                     "C picking up a number of features that either "
                     "weren't found in the contemporary version of C++ or "
                     "still haven't made it into any version of C++. "]

    elif 'c++' in user_input:
        responses = ["C++ is a high-performance, object-oriented programming language that extends C.",
                     "C++ is widely used in game development, systems programming, "
                     "and applications requiring real-time performance."]

    # Match compiler and interpreter comparisons
    elif re.search(r'\b(compilers?|interpreters?)\b.*\b(vs|and)\b.*\b(compilers?|interpreters?)\b', user_input):
        responses = ["Compilers and interpreters are both computer programs "
                     "that translate code created in a high-level language, but there are differences between them."
                     "\n- A compiler translates the entire source code into a machine-code file, "
                     "and the machine-code file is then executed."
                     "\n- An interpreter reads one statement from the source code, "
                     "translates it to the machine code or virtual machine code, "
                     "and then executes it right away."]

    # Match 'why is C popular' and similar C-focused queries
    elif re.search(r'\bwhy\s+(is|was)\s+c\b', user_input) or \
         re.search(r'\bwhat\s+makes\s+c\b', user_input) or \
         re.search(r'\bc\s+is\s+popular\b', user_input):
        responses = ["C is so popular because it is very fast compared to other programming languages, "
                     "like Java and Python.",
                     "C is very versatile, it can be used in both applications and technologies, "
                     "and it is usually much faster than Python."]

    # General C language response (moved to the bottom to avoid conflict with other checks)
    elif re.search(r'\bc\b', user_input):
        responses = ["C is a general-purpose programming language created by Dennis Ritchie at Bell Labs in 1972.",
                     "C is one of the most popular programming languages. "
                     "Its syntax forms the basis for many other languages.",
                     "C is the third letter of the English alphabet, but in computing, it's a powerful language."]

    elif re.search(r'\bruby\b', user_input):
        # Placeholder response for Ruby (to be handled by you later)
        responses = ["Ruby is a simple, open source, annotated language implementation with high performance. "
                     "It has a clean, friendly syntax and is easy to write.",
                     "Ruby might be referred to two concepts:"
                     "\nFirst, an invaluable gemstone whose color is visibly red."
                     "\nSecond, an interpreted, general-purpose programming language, "
                     "designed with the 'everything is an object' concept."]

    elif re.search(r'\bsql\s*server\b', user_input):
        # Placeholder response for SQL Server
        responses = ["SQL Server or Microsoft SQL Server is a relational data management system (RDBMS) "
                     "developed by Microsoft in 1988. It was used to create, maintain, "
                     "manage and deploy the RDBMS system.",
                     "SQL Server is one of the most popular database management systems "
                     "in the world and is widely used in businesses, "
                     "allowing users to query, manipulate and manage data effectively and safely."]

    elif re.search(r'\bmysql\b', user_input):
        # Placeholder response for MySQL
        responses = ["MySQL is an open source database management system used widely worldwide, "
                     "developed by Oracle Corporation and is currently being released for free.",
                     "MySQL is a relational database management system (RDBMS) open source, "
                     "widely used to store, manage and access data. "
                     "MySQL is completely free in the Lamp (Linux - Apache - MySQL - PHP) group."]

    elif re.search(r'\bsql', user_input):
        responses = ["SQL, short form of Structured Query Language, is a DBMS Language to work with database. "
                     "It is a programming language for storing and "
                     "processing information in the relational database. "
                     "The database of information storage in the form of a table "
                     "has rows and columns representing data attributes "
                     "and many different relationships between data values. "
                     "You can use SQL statements to store, update, remove, search "
                     "and retrieve information from the database. "
                     "You can also use SQL to maintain and optimize database performance.",
                     "The structural query language (SQL) is a common query language "
                     "used in all types of applications. "
                     "Analysts and developers develop and use SQL because "
                     "this language integrates effectively with many different programming languages."]

    else:
        responses = ["Sorry, I didn't quite get that."]

    return random.choice(responses)


if __name__ == "__main__":
    user_input = input("Enter a response: ")
    print(get_response(user_input))
