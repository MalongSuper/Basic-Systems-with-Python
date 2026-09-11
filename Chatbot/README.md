# ROMAX Chatbot

An intelligent AI assistant that combines **basic conversational abilities** with **advanced mathematical computing** and **AI/ML educational capabilities**.

## What It Does

ROMAX is a multi-purpose chatbot that helps you with:

### **Basic Chat Features** (Original Functionality)
Conversational AI with practical utilities:
- **Greetings & Identity**: Ask who ROMAX is or greet the chatbot
- **Arithmetic Operations**: Perform basic calculations
- **Mathematical Functions**: Compute square roots and powers
- **Time Information**: Get current date and time
- **Programming Knowledge**: Learn about programming languages

```
Input:  hello
Output: Hello! How can I help you today?

Input:  5 + 3
Output: The result of 5+3 is 8.

Input:  square root of 16
Output: √16 equals 4.0

Input:  2 power by 5
Output: 2 raised to the power of 5 equals 32.

Input:  what time is it
Output: The current time is 2:30 PM.

Input:  what is python
Output: Python is an interpreted, object-oriented, high-level programming language...
```

---
### **Matrix Operations** (Linear Algebra)
Perform complex matrix computations using NumPy:
- Addition, Subtraction, Multiplication
- Matrix Inverse & Determinant
- Solve Systems of Linear Equations

```
Input:  matrix addition [[1,2],[3,4]] [[5,6],[7,8]]
Output: [[6,8],[10,12]]

Input:  solve equation [[2,1],[1,3]] [[8],[9]]
Output: [2.6, 2.8]
```

### **Calculus Operations** (Derivatives & Integrals)
Compute symbolic derivatives and integrals using SymPy:
- Derivatives of polynomials, trigonometric, exponential functions
- Indefinite integrals with step-by-step results
- Support for complex expressions

```
Input:  derivative of x**2 + 3*x
Output: d/dx(...) = 2*x + 3

Input:  integral of sin(x)
Output: ∫sin(x)dx = -cos(x) + C
```

### **AI/ML Concepts** (Educational Knowledge Base)
Learn about 12+ advanced AI and Machine Learning topics:
- Machine Learning, Deep Learning, Neural Networks
- Natural Language Processing (NLP)
- Computer Vision, Convolutional Neural Networks (CNN)
- RNNs, LSTMs, Transfer Learning, Data Science, and more

```
Input:  explain machine learning
Output: Comprehensive ML overview with key aspects

Input:  what is deep learning
Output: DL explanation covering neural networks and applications
```

---

## Quick Start

### Installation (First Time Only)
```bash
cd /Users/macbook/Documents/Python/Chatbot
python3 -m venv chatbot_venv
source chatbot_venv/bin/activate
pip install -r requirements.txt
python3 chatbot.py
```

### Running the Chatbot (Every Session)
```bash
cd /Users/macbook/Documents/Python/Chatbot
source chatbot_venv/bin/activate
python3 chatbot.py
```

---

## Command Reference

| Feature | Example | Output |
|---------|---------|--------|
| **Greeting** | `hello` | `Hello! How can I help you today?` |
| **Identity** | `who are you` | `I am ROMAX, your AI assistant` |
| **Current Time** | `what time is it` | `The current time is 2:30 PM` |
| **Addition** | `5 + 3` | `The result of 5+3 is 8.` |
| **Subtraction** | `10 - 4` | `The result of 10-4 is 6.` |
| **Multiplication** | `7 * 6` | `The result of 7*6 is 42.` |
| **Division** | `20 / 4` | `The result of 20/4 is 5.` |
| **Square Root** | `square root of 16` | `√16 equals 4.0` |
| **Power** | `2 power by 8` | `2 raised to the power of 8 equals 256.` |
| **Python Info** | `what is python` | `Python is an interpreted, object-oriented... programming language` |
| **Java Info** | `tell me about java` | `Java is a flexible language used to develop many software applications` |
| **Matrix Addition** | `matrix addition [[1,2],[3,4]] [[5,6],[7,8]]` | `[[6,8],[10,12]]` |
| **Matrix Multiply** | `matrix multiply [[1,2],[3,4]] [[5,6],[7,8]]` | `[[19,22],[43,50]]` |
| **Matrix Inverse** | `matrix inverse [[4,7],[2,6]]` | Inverse matrix |
| **Determinant** | `determinant [[1,2],[3,4]]` | `-2.000000` |
| **Solve System** | `solve equation [[2,1],[1,3]] [[8],[9]]` | Solution vector |
| **Derivative** | `derivative of x**2 + 3*x` | `2*x + 3` |
| **Integral** | `integral of x**2` | `x**3/3 + C` |
| **AI Topic** | `explain machine learning` | ML explanation |
| **AI Topic** | `what is deep learning` | DL explanation |

---

## Tech Stack

| Component | Library | Purpose |
|-----------|---------|---------|
| Matrix Operations | NumPy | Linear algebra |
| Calculus | SymPy | Symbolic mathematics |
| Scientific Computing | SciPy | Advanced numerical methods |
| AI Explanations | Wikipedia API + Built-in KB | Knowledge base |
| GUI | CustomTkinter | Modern interface |

**Dependencies:** `numpy`, `scipy`, `sympy`, `requests`, `customtkinter`, `Pillow`
