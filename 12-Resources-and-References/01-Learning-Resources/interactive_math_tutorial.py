"""
Interactive Mathematics Tutorial for ML/AI/Data Science
======================================================

An interactive tutorial system that guides beginners through essential mathematical concepts
with step-by-step explanations, hands-on exercises, and progress tracking.

Features:
- Step-by-step guided tutorials
- Interactive exercises with immediate feedback
- Progress tracking and achievement system
- Personalized learning paths
- Visual explanations with code examples
- Self-paced learning with difficulty adaptation

Author: Interactive Mathematics Learning System
Date: 2024
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import os

class InteractiveMathTutorial:
    """
    Main interactive tutorial system for mathematics education
    """
    
    def __init__(self, student_name: str = "Student"):
        self.student_name = student_name
        self.progress_file = f"math_progress_{student_name.lower().replace(' ', '_')}.json"
        self.current_session = {
            'start_time': datetime.now(),
            'topics_covered': [],
            'exercises_completed': 0,
            'correct_answers': 0
        }
        
        # Load or create progress
        self.progress = self.load_progress()
        
        # Tutorial structure
        self.tutorial_structure = {
            'linear_algebra': {
                'name': 'Linear Algebra Fundamentals',
                'difficulty': 1,
                'prerequisites': [],
                'lessons': ['vectors', 'matrices', 'eigenvalues', 'svd'],
                'estimated_time': '45-60 minutes'
            },
            'probability': {
                'name': 'Probability Theory',
                'difficulty': 1,
                'prerequisites': [],
                'lessons': ['basic_probability', 'conditional_probability', 'distributions'],
                'estimated_time': '40-50 minutes'
            },
            'statistics': {
                'name': 'Statistics for Data Science',
                'difficulty': 2,
                'prerequisites': ['probability'],
                'lessons': ['descriptive_stats', 'correlation', 'hypothesis_testing'],
                'estimated_time': '50-70 minutes'
            },
            'calculus': {
                'name': 'Calculus for Optimization',
                'difficulty': 2,
                'prerequisites': ['linear_algebra'],
                'lessons': ['derivatives', 'gradients', 'optimization'],
                'estimated_time': '60-80 minutes'
            },
            'information_theory': {
                'name': 'Information Theory',
                'difficulty': 3,
                'prerequisites': ['probability', 'statistics'],
                'lessons': ['entropy', 'mutual_information', 'kl_divergence'],
                'estimated_time': '40-60 minutes'
            }
        }
        
        print(f"🎓 Welcome {self.student_name} to Interactive Mathematics Tutorial!")
        print("   Your personalized learning companion for ML/AI/Data Science math")
    
    def load_progress(self) -> Dict:
        """Load student progress from file"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default progress structure
        return {
            'student_name': self.student_name,
            'total_study_time': 0,
            'topics_mastered': [],
            'current_level': 'Beginner',
            'achievements': [],
            'lesson_scores': {},
            'last_session': None,
            'streak_days': 0
        }
    
    def save_progress(self):
        """Save student progress to file"""
        try:
            with open(self.progress_file, 'w') as f:
                json.dump(self.progress, f, indent=2, default=str)
            print(f"💾 Progress saved successfully!")
        except Exception as e:
            print(f"⚠️  Could not save progress: {e}")
    
    def show_dashboard(self):
        """Display student progress dashboard"""
        print("\n" + "="*60)
        print(f"📊 {self.student_name}'s Learning Dashboard")
        print("="*60)
        
        # Progress overview
        total_topics = len(self.tutorial_structure)
        mastered_topics = len(self.progress['topics_mastered'])
        completion_rate = (mastered_topics / total_topics) * 100
        
        print(f"🎯 Overall Progress: {completion_rate:.1f}% ({mastered_topics}/{total_topics} topics)")
        print(f"⏱️  Total Study Time: {self.progress['total_study_time']:.1f} minutes")
        print(f"🎓 Current Level: {self.progress['current_level']}")
        print(f"🔥 Study Streak: {self.progress['streak_days']} days")
        
        # Progress bar
        progress_bar = "█" * int(completion_rate // 5) + "░" * (20 - int(completion_rate // 5))
        print(f"📈 Progress: [{progress_bar}] {completion_rate:.1f}%")
        
        # Achievements
        if self.progress['achievements']:
            print(f"\n🏆 Recent Achievements:")
            for achievement in self.progress['achievements'][-3:]:
                print(f"   • {achievement}")
        
        # Recommended next topics
        recommended = self.get_recommended_topics()
        if recommended:
            print(f"\n💡 Recommended Next Topics:")
            for topic in recommended[:3]:
                info = self.tutorial_structure[topic]
                print(f"   📚 {info['name']} (Level {info['difficulty']}) - {info['estimated_time']}")
        
        print()
    
    def get_recommended_topics(self) -> List[str]:
        """Get recommended topics based on progress and prerequisites"""
        available_topics = []
        
        for topic_id, topic_info in self.tutorial_structure.items():
            # Skip if already mastered
            if topic_id in self.progress['topics_mastered']:
                continue
            
            # Check prerequisites
            prereqs_met = all(prereq in self.progress['topics_mastered'] 
                            for prereq in topic_info['prerequisites'])
            
            if prereqs_met:
                available_topics.append(topic_id)
        
        # Sort by difficulty
        available_topics.sort(key=lambda x: self.tutorial_structure[x]['difficulty'])
        return available_topics
    
    def start_tutorial(self, topic_id: str = None):
        """Start an interactive tutorial session"""
        if not topic_id:
            recommended = self.get_recommended_topics()
            if not recommended:
                print("🎉 Congratulations! You've mastered all available topics!")
                return
            topic_id = recommended[0]
        
        if topic_id not in self.tutorial_structure:
            print(f"❌ Topic '{topic_id}' not found!")
            return
        
        topic_info = self.tutorial_structure[topic_id]
        
        print(f"\n🚀 Starting Tutorial: {topic_info['name']}")
        print(f"📊 Difficulty Level: {topic_info['difficulty']}")
        print(f"⏱️  Estimated Time: {topic_info['estimated_time']}")
        
        if topic_info['prerequisites']:
            prereqs = [self.tutorial_structure[p]['name'] for p in topic_info['prerequisites']]
            print(f"📋 Prerequisites: {', '.join(prereqs)}")
        
        print("\n" + "="*60)
        
        # Start the specific tutorial
        tutorial_method = getattr(self, f"tutorial_{topic_id}", None)
        if tutorial_method:
            session_start = time.time()
            tutorial_method()
            session_time = (time.time() - session_start) / 60
            
            # Update progress
            self.update_progress(topic_id, session_time)
        else:
            print(f"⚠️  Tutorial for '{topic_id}' not implemented yet!")
    
    def update_progress(self, topic_id: str, session_time: float):
        """Update student progress after completing a tutorial"""
        self.progress['total_study_time'] += session_time
        
        if topic_id not in self.progress['topics_mastered']:
            self.progress['topics_mastered'].append(topic_id)
            topic_name = self.tutorial_structure[topic_id]['name']
            achievement = f"Mastered {topic_name} - {datetime.now().strftime('%Y-%m-%d')}"
            self.progress['achievements'].append(achievement)
        
        # Update level
        mastered_count = len(self.progress['topics_mastered'])
        if mastered_count >= 5:
            self.progress['current_level'] = 'Expert'
        elif mastered_count >= 3:
            self.progress['current_level'] = 'Advanced'
        elif mastered_count >= 1:
            self.progress['current_level'] = 'Intermediate'
        
        self.progress['last_session'] = datetime.now().isoformat()
        self.save_progress()
    
    def tutorial_linear_algebra(self):
        """Interactive Linear Algebra Tutorial"""
        print("📐 LINEAR ALGEBRA FUNDAMENTALS")
        print("="*40)
        
        # Lesson 1: Vectors
        self.lesson_title("Lesson 1: Understanding Vectors")
        
        print("🔢 What is a vector?")
        print("   A vector is a list of numbers that represents:")
        print("   • Direction and magnitude in space")
        print("   • Features in machine learning")
        print("   • Data points in multi-dimensional space")
        
        # Interactive example
        print("\n💻 Let's create your first vector!")
        vector_a = np.array([3, 4])
        print(f"   vector_a = {vector_a}")
        print(f"   This represents a point or direction in 2D space")
        
        # Visualization would go here in a full implementation
        print(f"   📏 Length (magnitude): {np.linalg.norm(vector_a):.2f}")
        
        # Interactive exercise
        if self.ask_continue("Ready for your first exercise?"):
            score = self.exercise_vector_basics()
            if score >= 0.8:
                print("🎉 Excellent! You understand vectors!")
            else:
                print("💡 Good try! Let's review vector concepts again.")
        
        # Lesson 2: Vector Operations
        self.lesson_title("Lesson 2: Vector Operations")
        
        print("➕ Vector Addition:")
        print("   When we add vectors, we add corresponding elements")
        
        a = np.array([1, 2])
        b = np.array([3, 4])
        result = a + b
        
        print(f"   [{a[0]}, {a[1]}] + [{b[0]}, {b[1]}] = [{result[0]}, {result[1]}]")
        print("   🎯 ML Application: Combining feature vectors")
        
        print("\n• Dot Product:")
        dot_result = np.dot(a, b)
        print(f"   {a} · {b} = {a[0]}×{b[0]} + {a[1]}×{b[1]} = {dot_result}")
        print("   🎯 ML Application: Similarity between vectors")
        
        # Exercise
        if self.ask_continue("Ready for vector operations exercise?"):
            score = self.exercise_vector_operations()
            if score >= 0.8:
                print("🌟 Outstanding! You've mastered vector operations!")
        
        # Lesson 3: Matrices
        self.lesson_title("Lesson 3: Matrices - The Foundation of ML")
        
        print("📊 What is a matrix?")
        print("   A matrix is a 2D array of numbers")
        print("   • Represents transformations in space")
        print("   • Stores datasets (rows = samples, columns = features)")
        print("   • Neural network weights")
        
        # Interactive matrix example
        print("\n💻 Creating a matrix:")
        matrix_A = np.array([[1, 2, 3],
                            [4, 5, 6]])
        print("Matrix A:")
        print(matrix_A)
        print(f"Shape: {matrix_A.shape} (2 rows, 3 columns)")
        print("🎯 ML Application: 2 data samples, 3 features each")
        
        # Matrix multiplication
        print("\n🔄 Matrix Multiplication:")
        B = np.array([[1, 0],
                     [0, 1],
                     [2, 3]])
        C = np.dot(matrix_A, B)
        print("A × B =")
        print(C)
        print("🎯 ML Application: Neural network forward pass")
        
        # Exercise
        if self.ask_continue("Ready to practice matrix operations?"):
            score = self.exercise_matrices()
            if score >= 0.7:
                print("🏆 Fantastic! Matrices are no longer mysterious!")
        
        print("\n🎓 Linear Algebra Tutorial Complete!")
        print("Key ML Applications you've learned:")
        print("• Vectors: Feature representation, embeddings")
        print("• Dot products: Similarity, attention mechanisms")
        print("• Matrices: Data storage, neural network weights")
        print("• Matrix multiplication: Forward propagation")
    
    def tutorial_probability(self):
        """Interactive Probability Theory Tutorial"""
        print("🎲 PROBABILITY THEORY")
        print("="*40)
        
        # Lesson 1: Basic Probability
        self.lesson_title("Lesson 1: What is Probability?")
        
        print("🎯 Probability measures uncertainty:")
        print("   • P(event) = Number of favorable outcomes / Total outcomes")
        print("   • Probability ranges from 0 (impossible) to 1 (certain)")
        print("   • Essential for AI decision making under uncertainty")
        
        # Interactive coin flip simulation
        print("\n🪙 Coin Flip Simulation:")
        np.random.seed(42)
        flips = 100
        heads = np.sum(np.random.choice(['H', 'T'], flips) == 'H')
        prob_heads = heads / flips
        
        print(f"   Flipped coin {flips} times")
        print(f"   Got {heads} heads")
        print(f"   P(Heads) ≈ {prob_heads:.3f}")
        print(f"   Theoretical P(Heads) = 0.500")
        
        # Exercise
        if self.ask_continue("Let's test your understanding!"):
            score = self.exercise_basic_probability()
            if score >= 0.8:
                print("🎉 You grasp the basics of probability!")
        
        # Lesson 2: Conditional Probability
        self.lesson_title("Lesson 2: Conditional Probability & Bayes' Theorem")
        
        print("🧠 Conditional Probability:")
        print("   P(A|B) = Probability of A given B has occurred")
        print("   Foundation of machine learning and AI reasoning")
        
        # Medical diagnosis example
        print("\n🏥 Medical Diagnosis Example:")
        print("   Disease prevalence: 1%")
        print("   Test accuracy: 95% (detects disease when present)")
        print("   False positive rate: 2% (positive when no disease)")
        
        print("\n❓ Question: If test is positive, what's P(Disease)?")
        print("   Intuition might say 95%, but let's calculate...")
        
        # Bayes' calculation
        p_disease = 0.01
        p_positive_given_disease = 0.95
        p_positive_given_no_disease = 0.02
        
        p_positive = (p_positive_given_disease * p_disease + 
                     p_positive_given_no_disease * (1 - p_disease))
        
        p_disease_given_positive = (p_positive_given_disease * p_disease) / p_positive
        
        print(f"\n🧮 Using Bayes' Theorem:")
        print(f"   P(Disease|Positive) = {p_disease_given_positive:.3f}")
        print(f"   Only {p_disease_given_positive:.1%} chance of having disease!")
        print("   🎯 ML Application: Naive Bayes classifier")
        
        # Exercise
        if self.ask_continue("Ready for a Bayes' theorem challenge?"):
            score = self.exercise_bayes_theorem()
            if score >= 0.7:
                print("🌟 You understand conditional probability!")
        
        print("\n🎓 Probability Tutorial Complete!")
        print("Key concepts mastered:")
        print("• Basic probability and uncertainty quantification")
        print("• Conditional probability for reasoning")
        print("• Bayes' theorem for machine learning")
    
    def tutorial_statistics(self):
        """Interactive Statistics Tutorial"""
        print("📊 STATISTICS FOR DATA SCIENCE")
        print("="*40)
        
        # Lesson 1: Descriptive Statistics
        self.lesson_title("Lesson 1: Describing Data")
        
        print("📈 Descriptive statistics summarize data:")
        print("   • Central tendency: mean, median, mode")
        print("   • Spread: variance, standard deviation")
        print("   • Shape: skewness, outliers")
        
        # Generate sample data
        np.random.seed(42)
        data = np.concatenate([
            np.random.normal(50, 10, 80),  # Main group
            np.random.normal(80, 5, 20)    # Smaller group
        ])
        
        print(f"\n💻 Analyzing sample dataset (n={len(data)}):")
        mean_val = np.mean(data)
        median_val = np.median(data)
        std_val = np.std(data)
        
        print(f"   Mean: {mean_val:.2f}")
        print(f"   Median: {median_val:.2f}")
        print(f"   Standard Deviation: {std_val:.2f}")
        
        # Interpretation
        if abs(mean_val - median_val) < 2:
            print("   📊 Data appears roughly symmetric")
        else:
            print("   📊 Data appears skewed")
        
        print("   🎯 ML Application: Feature preprocessing, outlier detection")
        
        # Exercise
        if self.ask_continue("Let's practice with descriptive statistics!"):
            score = self.exercise_descriptive_stats()
            if score >= 0.8:
                print("📊 Excellent statistical intuition!")
        
        print("\n🎓 Statistics Tutorial Complete!")
    
    def lesson_title(self, title: str):
        """Display lesson title with formatting"""
        print(f"\n{'-'*50}")
        print(f"📚 {title}")
        print(f"{'-'*50}")
    
    def ask_continue(self, question: str) -> bool:
        """Ask user if they want to continue with interactive content"""
        response = input(f"\n{question} (y/n): ").lower().strip()
        return response in ['y', 'yes', '']
    
    def exercise_vector_basics(self) -> float:
        """Interactive exercise on vector basics"""
        print("\n🏋️ Exercise: Vector Basics")
        print("="*30)
        
        score = 0
        total_questions = 3
        
        # Question 1: Vector magnitude
        print("Q1: What is the magnitude of vector [3, 4]?")
        print("   a) 5.0")
        print("   b) 7.0") 
        print("   c) 12.0")
        print("   d) 3.5")
        
        answer = input("Your answer (a/b/c/d): ").lower().strip()
        if answer == 'a':
            print("✅ Correct! √(3² + 4²) = √25 = 5.0")
            score += 1
        else:
            print("❌ Incorrect. The magnitude is √(3² + 4²) = 5.0")
        
        # Question 2: Vector addition
        print("\nQ2: What is [1, 2] + [3, 4]?")
        print("   a) [3, 6]")
        print("   b) [4, 6]")
        print("   c) [1, 8]")
        print("   d) [4, 8]")
        
        answer = input("Your answer (a/b/c/d): ").lower().strip()
        if answer == 'b':
            print("✅ Correct! [1+3, 2+4] = [4, 6]")
            score += 1
        else:
            print("❌ Incorrect. Add corresponding elements: [1+3, 2+4] = [4, 6]")
        
        # Question 3: Dot product
        print("\nQ3: What is the dot product of [2, 3] and [1, 4]?")
        print("   a) 10")
        print("   b) 12")
        print("   c) 14")
        print("   d) 16")
        
        answer = input("Your answer (a/b/c/d): ").lower().strip()
        if answer == 'c':
            print("✅ Correct! 2×1 + 3×4 = 2 + 12 = 14")
            score += 1
        else:
            print("❌ Incorrect. Dot product: 2×1 + 3×4 = 14")
        
        final_score = score / total_questions
        print(f"\n📊 Score: {score}/{total_questions} ({final_score:.1%})")
        
        return final_score
    
    def exercise_vector_operations(self) -> float:
        """Exercise on vector operations"""
        print("\n🏋️ Exercise: Vector Operations")
        print("="*35)
        
        # Generate random vectors for exercise
        np.random.seed(int(time.time()) % 100)
        v1 = np.random.randint(1, 6, 2)
        v2 = np.random.randint(1, 6, 2)
        
        score = 0
        total_questions = 2
        
        # Question 1: Vector addition
        print(f"Q1: Calculate {v1} + {v2}")
        correct_sum = v1 + v2
        
        try:
            user_x = int(input("Enter first component: "))
            user_y = int(input("Enter second component: "))
            user_answer = np.array([user_x, user_y])
            
            if np.array_equal(user_answer, correct_sum):
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Incorrect. Answer: {correct_sum}")
        except:
            print(f"❌ Invalid input. Answer: {correct_sum}")
        
        # Question 2: Dot product
        print(f"\nQ2: Calculate the dot product of {v1} and {v2}")
        correct_dot = np.dot(v1, v2)
        
        try:
            user_dot = int(input("Enter dot product: "))
            if user_dot == correct_dot:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Incorrect. Answer: {correct_dot}")
        except:
            print(f"❌ Invalid input. Answer: {correct_dot}")
        
        final_score = score / total_questions
        print(f"\n📊 Score: {score}/{total_questions} ({final_score:.1%})")
        
        return final_score
    
    def exercise_matrices(self) -> float:
        """Exercise on matrix operations"""
        print("\n🏋️ Exercise: Matrix Operations")
        print("="*32)
        
        score = 0
        total_questions = 2
        
        # Question 1: Matrix dimensions
        print("Q1: If matrix A is 3×4 and matrix B is 4×2, what is the dimension of A×B?")
        print("   a) 3×2")
        print("   b) 4×4")
        print("   c) 3×4")
        print("   d) Cannot multiply")
        
        answer = input("Your answer (a/b/c/d): ").lower().strip()
        if answer == 'a':
            print("✅ Correct! (3×4) × (4×2) = 3×2")
            score += 1
        else:
            print("❌ Incorrect. Matrix multiplication: (m×n) × (n×p) = (m×p)")
        
        # Question 2: Identity matrix
        print("\nQ2: What happens when you multiply any matrix by the identity matrix?")
        print("   a) The matrix becomes zero")
        print("   b) The matrix stays the same")
        print("   c) The matrix is transposed")
        print("   d) The matrix is inverted")
        
        answer = input("Your answer (a/b/c/d): ").lower().strip()
        if answer == 'b':
            print("✅ Correct! Identity matrix is like multiplying by 1")
            score += 1
        else:
            print("❌ Incorrect. A × I = A (identity property)")
        
        final_score = score / total_questions
        print(f"\n📊 Score: {score}/{total_questions} ({final_score:.1%})")
        
        return final_score
    
    def exercise_basic_probability(self) -> float:
        """Exercise on basic probability"""
        print("\n🏋️ Exercise: Basic Probability")
        print("="*32)
        
        score = 0
        total_questions = 3
        
        # Question 1
        print("Q1: A bag has 3 red balls and 7 blue balls. What's P(red)?")
        print("   a) 0.3")
        print("   b) 0.7")
        print("   c) 3.0")
        print("   d) 0.1")
        
        answer = input("Your answer (a/b/c/d): ").lower().strip()
        if answer == 'a':
            print("✅ Correct! P(red) = 3/(3+7) = 3/10 = 0.3")
            score += 1
        else:
            print("❌ Incorrect. P(red) = favorable/total = 3/10 = 0.3")
        
        # Question 2
        print("\nQ2: If P(A) = 0.4 and P(B) = 0.6, what's the maximum possible P(A and B)?")
        print("   a) 1.0")
        print("   b) 0.6")
        print("   c) 0.4")
        print("   d) 0.24")
        
        answer = input("Your answer (a/b/c/d): ").lower().strip()
        if answer == 'c':
            print("✅ Correct! P(A and B) ≤ min(P(A), P(B)) = 0.4")
            score += 1
        else:
            print("❌ Incorrect. Maximum overlap is limited by smaller probability")
        
        # Question 3
        print("\nQ3: All probabilities must sum to what value?")
        
        try:
            user_answer = float(input("Enter value: "))
            if abs(user_answer - 1.0) < 0.01:
                print("✅ Correct! All probabilities sum to 1")
                score += 1
            else:
                print("❌ Incorrect. All probabilities must sum to 1")
        except:
            print("❌ Invalid input. Answer: 1")
        
        final_score = score / total_questions
        print(f"\n📊 Score: {score}/{total_questions} ({final_score:.1%})")
        
        return final_score
    
    def exercise_bayes_theorem(self) -> float:
        """Exercise on Bayes' theorem"""
        print("\n🏋️ Exercise: Bayes' Theorem")
        print("="*30)
        
        print("🏥 Medical Test Scenario:")
        print("   • Disease prevalence: 2%")
        print("   • Test sensitivity: 90% (detects disease when present)")
        print("   • Test specificity: 95% (negative when no disease)")
        print("\n❓ If someone tests positive, what's P(Disease|Positive)?")
        
        # Calculate correct answer
        p_disease = 0.02
        p_pos_given_disease = 0.90
        p_pos_given_no_disease = 0.05
        
        p_positive = (p_pos_given_disease * p_disease + 
                     p_pos_given_no_disease * (1 - p_disease))
        
        correct_answer = (p_pos_given_disease * p_disease) / p_positive
        
        try:
            user_answer = float(input("Enter probability (0.0 to 1.0): "))
            
            if abs(user_answer - correct_answer) < 0.05:
                print(f"✅ Excellent! Close to {correct_answer:.3f}")
                return 1.0
            elif abs(user_answer - correct_answer) < 0.1:
                print(f"🟡 Good attempt! Actual answer: {correct_answer:.3f}")
                return 0.7
            else:
                print(f"❌ Not quite. Using Bayes': {correct_answer:.3f}")
                return 0.3
        except:
            print(f"❌ Invalid input. Answer: {correct_answer:.3f}")
            return 0.0
    
    def exercise_descriptive_stats(self) -> float:
        """Exercise on descriptive statistics"""
        print("\n🏋️ Exercise: Descriptive Statistics")
        print("="*38)
        
        # Generate data for exercise
        data = [2, 4, 4, 6, 8, 10, 12]
        print(f"Dataset: {data}")
        
        score = 0
        total_questions = 3
        
        # Question 1: Mean
        print("Q1: What is the mean?")
        correct_mean = np.mean(data)
        
        try:
            user_mean = float(input("Enter mean: "))
            if abs(user_mean - correct_mean) < 0.1:
                print(f"✅ Correct! Mean = {correct_mean}")
                score += 1
            else:
                print(f"❌ Incorrect. Mean = {correct_mean}")
        except:
            print(f"❌ Invalid input. Mean = {correct_mean}")
        
        # Question 2: Median
        print("\nQ2: What is the median?")
        correct_median = np.median(data)
        
        try:
            user_median = float(input("Enter median: "))
            if abs(user_median - correct_median) < 0.1:
                print(f"✅ Correct! Median = {correct_median}")
                score += 1
            else:
                print(f"❌ Incorrect. Median = {correct_median}")
        except:
            print(f"❌ Invalid input. Median = {correct_median}")
        
        # Question 3: Which is larger?
        print("\nQ3: Is the mean or median larger?")
        print("   a) Mean")
        print("   b) Median")
        print("   c) They are equal")
        
        answer = input("Your answer (a/b/c): ").lower().strip()
        if correct_mean > correct_median and answer == 'a':
            print("✅ Correct! Mean is larger")
            score += 1
        elif correct_median > correct_mean and answer == 'b':
            print("✅ Correct! Median is larger")
            score += 1
        elif abs(correct_mean - correct_median) < 0.1 and answer == 'c':
            print("✅ Correct! They are equal")
            score += 1
        else:
            comparison = "equal" if abs(correct_mean - correct_median) < 0.1 else ("mean" if correct_mean > correct_median else "median")
            print(f"❌ Incorrect. The {comparison} is larger")
        
        final_score = score / total_questions
        print(f"\n📊 Score: {score}/{total_questions} ({final_score:.1%})")
        
        return final_score
    
    def show_help(self):
        """Show help and available commands"""
        print("\n" + "="*60)
        print("📖 INTERACTIVE MATH TUTORIAL HELP")
        print("="*60)
        
        print("🎯 Available Commands:")
        print("   tutorial.show_dashboard()        - View your progress")
        print("   tutorial.start_tutorial()        - Start recommended tutorial")
        print("   tutorial.start_tutorial('topic') - Start specific topic")
        print("   tutorial.show_help()             - Show this help")
        print("   tutorial.list_topics()           - List all available topics")
        
        print("\n📚 Available Topics:")
        for topic_id, info in self.tutorial_structure.items():
            status = "✅ Mastered" if topic_id in self.progress['topics_mastered'] else "📖 Available"
            print(f"   {topic_id:18} - {info['name']} ({status})")
        
        print("\n💡 Study Tips:")
        print("   • Start with recommended topics based on prerequisites")
        print("   • Complete exercises for better retention")
        print("   • Review concepts you find challenging")
        print("   • Practice regularly to build your streak")
        
        print(f"\n🎓 Your Progress: {len(self.progress['topics_mastered'])}/{len(self.tutorial_structure)} topics mastered")
    
    def list_topics(self):
        """List all available topics with details"""
        print("\n" + "="*60)
        print("📚 AVAILABLE MATHEMATICS TOPICS")
        print("="*60)
        
        for topic_id, info in self.tutorial_structure.items():
            status = "✅ Mastered" if topic_id in self.progress['topics_mastered'] else "📖 Available"
            prereq_status = "✅" if all(p in self.progress['topics_mastered'] for p in info['prerequisites']) else "⏳"
            
            print(f"\n🔸 {info['name']}")
            print(f"   ID: {topic_id}")
            print(f"   Status: {status}")
            print(f"   Prerequisites: {prereq_status}")
            print(f"   Difficulty: {'⭐' * info['difficulty']}")
            print(f"   Duration: {info['estimated_time']}")
            
            if info['prerequisites']:
                prereq_names = [self.tutorial_structure[p]['name'] for p in info['prerequisites']]
                print(f"   Required: {', '.join(prereq_names)}")


def create_student_tutorial(name: str = None) -> InteractiveMathTutorial:
    """
    Factory function to create a personalized tutorial instance
    """
    if not name:
        name = input("👤 Enter your name: ").strip()
        if not name:
            name = "Student"
    
    print(f"\n🌟 Creating personalized tutorial for {name}...")
    tutorial = InteractiveMathTutorial(name)
    
    print(f"\n🚀 Tutorial ready! Here's how to get started:")
    print(f"   tutorial.show_dashboard()  # See your progress")
    print(f"   tutorial.start_tutorial()  # Start learning!")
    print(f"   tutorial.show_help()       # Get help anytime")
    
    return tutorial


if __name__ == "__main__":
    print("🎓 Interactive Mathematics Tutorial for ML/AI/Data Science")
    print("=========================================================")
    print()
    
    # Create tutorial instance
    print("Welcome to your personalized mathematics learning experience!")
    tutorial = create_student_tutorial()
    
    # Show initial dashboard
    tutorial.show_dashboard()
    
    # Show help
    print(f"\nType 'tutorial.show_help()' for available commands")
    print(f"Ready to start your mathematical journey? Try 'tutorial.start_tutorial()'")
    
    # Example usage demonstration
    print("\n" + "="*60)
    print("📋 QUICK START GUIDE")
    print("="*60)
    print("The tutorial object is ready to use. Try these commands:")
    print()
    print("# Start your first lesson")
    print("tutorial.start_tutorial()")
    print()
    print("# View your learning progress") 
    print("tutorial.show_dashboard()")
    print()
    print("# Get help anytime")
    print("tutorial.show_help()")
    print()
    print("# List all available topics")
    print("tutorial.list_topics()")
    print()
    print("Happy learning! 🚀")
