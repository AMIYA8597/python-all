#!/usr/bin/env python3
"""
Mathematics for ML/AI/Data Science - Complete Demo
=================================================

This script demonstrates all the mathematics modules and provides
usage examples for beginners learning ML/AI/Data Science mathematics.

Run this script to see all components in action!

Author: Mathematics Tutorial System
Date: 2024
"""

import sys
import traceback
from pathlib import Path

def print_header(title, emoji="📚"):
    """Print a formatted header"""
    print("\n" + "="*80)
    print(f"{emoji} {title}")
    print("="*80)

def print_section(title, emoji="🔹"):
    """Print a section header"""
    print(f"\n{emoji} {title}")
    print("-" * 50)

def safe_import_and_run(module_name, demo_function, description):
    """Safely import module and run demonstration"""
    try:
        print(f"\n🔄 Loading {module_name}...")
        
        if module_name == "mathematics_for_ml_ai_datascience":
            from mathematics_for_ml_ai_datascience import comprehensive_demo
            demo_function = comprehensive_demo
        elif module_name == "interactive_math_tutorial":
            from interactive_math_tutorial import create_student_tutorial
            demo_function = lambda: demonstrate_interactive_tutorial()
        
        print(f"✅ Successfully loaded {module_name}")
        print(f"📝 Running demonstration: {description}")
        
        if demo_function:
            demo_function()
            
        return True
        
    except ImportError as e:
        print(f"❌ Could not import {module_name}: {e}")
        print(f"💡 Make sure all required packages are installed:")
        print("   pip install numpy scipy matplotlib")
        return False
    except Exception as e:
        print(f"❌ Error running {module_name} demo: {e}")
        print(f"🔍 Full traceback:")
        traceback.print_exc()
        return False

def demonstrate_interactive_tutorial():
    """Demonstrate the interactive tutorial system"""
    from interactive_math_tutorial import create_student_tutorial
    
    print("\n" + "="*60)
    print("🎓 INTERACTIVE MATHEMATICS TUTORIAL DEMO")
    print("="*60)
    
    print("\n📋 Creating a sample student tutorial...")
    
    # Create tutorial for demo user
    tutorial = create_student_tutorial("DemoUser")
    
    print("\n📊 Showing dashboard...")
    tutorial.show_dashboard()
    
    print("\n📚 Listing available topics...")
    tutorial.list_topics()
    
    print("\n❓ Showing help...")
    tutorial.show_help()
    
    print("\n💡 Interactive Tutorial Features:")
    print("   ✅ Personalized progress tracking")
    print("   ✅ Step-by-step guided lessons")
    print("   ✅ Interactive exercises with feedback")
    print("   ✅ Achievement system and streaks")
    print("   ✅ Adaptive difficulty progression")
    
    print("\n🚀 To use the interactive tutorial:")
    print("   1. Run: tutorial = create_student_tutorial('YourName')")
    print("   2. Start learning: tutorial.start_tutorial()")
    print("   3. Track progress: tutorial.show_dashboard()")

def demonstrate_key_concepts():
    """Demonstrate key mathematical concepts with simple examples"""
    print_header("Key Mathematical Concepts Demo", "🧮")
    
    try:
        import numpy as np
        
        print_section("Linear Algebra Basics")
        
        # Vectors
        a = np.array([1, 2, 3])
        b = np.array([4, 5, 6])
        
        print(f"Vector a: {a}")
        print(f"Vector b: {b}")
        print(f"Dot product: {np.dot(a, b)}")
        print(f"Magnitude of a: {np.linalg.norm(a):.3f}")
        
        # Matrices
        A = np.array([[1, 2], [3, 4]])
        B = np.array([[5, 6], [7, 8]])
        
        print(f"\nMatrix A:\n{A}")
        print(f"Matrix B:\n{B}")
        print(f"Matrix multiplication A @ B:\n{A @ B}")
        
        print_section("Probability & Statistics")
        
        # Random data
        np.random.seed(42)
        data = np.random.normal(50, 10, 100)
        
        print(f"Sample data (first 10): {data[:10]}")
        print(f"Mean: {np.mean(data):.2f}")
        print(f"Standard deviation: {np.std(data):.2f}")
        print(f"Min: {np.min(data):.2f}, Max: {np.max(data):.2f}")
        
        # Correlation
        x = np.random.normal(0, 1, 50)
        y = 2*x + np.random.normal(0, 0.5, 50)
        correlation = np.corrcoef(x, y)[0, 1]
        print(f"Correlation between x and y: {correlation:.3f}")
        
        print_section("Basic Calculus")
        
        # Numerical derivative approximation
        def f(x):
            return x**2
        
        x_point = 3
        h = 1e-7
        derivative_approx = (f(x_point + h) - f(x_point - h)) / (2 * h)
        print(f"f(x) = x²")
        print(f"f'(3) ≈ {derivative_approx:.6f} (should be 6.0)")
        
        print_section("Information Theory")
        
        # Entropy calculation
        def entropy(probabilities):
            p = np.array(probabilities)
            p = p[p > 0]  # Remove zeros
            return -np.sum(p * np.log2(p))
        
        fair_coin = [0.5, 0.5]
        biased_coin = [0.9, 0.1]
        
        print(f"Fair coin entropy: {entropy(fair_coin):.3f} bits")
        print(f"Biased coin entropy: {entropy(biased_coin):.3f} bits")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in demonstration: {e}")
        return False

def show_learning_path():
    """Show the recommended learning path"""
    print_header("Recommended Learning Path", "🗺️")
    
    learning_path = {
        "Beginner Level (Start Here!)": [
            ("Linear Algebra Fundamentals", "3-4 weeks", "Vectors, matrices, basic operations"),
            ("Probability Theory Basics", "2-3 weeks", "Basic probability, Bayes' theorem")
        ],
        "Intermediate Level": [
            ("Statistics for Data Science", "4-5 weeks", "Descriptive stats, correlation, hypothesis testing"),
            ("Calculus for Optimization", "4-6 weeks", "Derivatives, gradients, optimization methods")
        ],
        "Advanced Level": [
            ("Information Theory", "2-3 weeks", "Entropy, mutual information, KL divergence")
        ]
    }
    
    for level, topics in learning_path.items():
        print(f"\n📚 {level}")
        for i, (topic, duration, description) in enumerate(topics, 1):
            print(f"   {i}. {topic} ({duration})")
            print(f"      📋 {description}")
    
    print("\n⏰ Total Estimated Time: 15-21 weeks for comprehensive mastery")
    
    print("\n💡 Study Tips:")
    print("   🎯 Follow the path sequentially - each level builds on previous knowledge")
    print("   📅 Set aside 1-2 hours per day for consistent progress")
    print("   💻 Practice with code examples alongside theory")
    print("   🤝 Join study groups or online communities")
    print("   📝 Take notes and create your own reference materials")

def show_file_overview():
    """Show overview of created files"""
    print_header("Created Files Overview", "📁")
    
    files_info = [
        {
            "name": "mathematics_for_ml_ai_datascience.py",
            "description": "Complete mathematical implementations and tutorials",
            "size": "~1700 lines",
            "features": [
                "Linear Algebra (vectors, matrices, eigenvalues, SVD)",
                "Probability Theory (distributions, Bayes' theorem, CLT)",
                "Statistics (descriptive, correlation, hypothesis testing)",
                "Calculus (derivatives, gradients, optimization)",
                "Information Theory (entropy, mutual information, KL divergence)",
                "Comprehensive demonstrations and examples"
            ]
        },
        {
            "name": "interactive_math_tutorial.py", 
            "description": "Interactive learning system with progress tracking",
            "size": "~860 lines",
            "features": [
                "Personalized learning dashboard",
                "Step-by-step guided tutorials",
                "Interactive exercises with immediate feedback",
                "Progress tracking and achievement system",
                "Adaptive difficulty progression",
                "Self-paced learning experience"
            ]
        },
        {
            "name": "Mathematics_Reference_Guide.md",
            "description": "Comprehensive markdown reference with theory and formulas",
            "size": "~1270 lines", 
            "features": [
                "Complete mathematical theory explanations",
                "LaTeX formatted formulas and equations",
                "Practical ML/AI applications and examples",
                "Learning paths and study strategies",
                "Quick reference tables and cheat sheets",
                "Extensive study resources and recommendations"
            ]
        }
    ]
    
    for file_info in files_info:
        print(f"\n📄 {file_info['name']}")
        print(f"   📝 {file_info['description']}")
        print(f"   📊 Size: {file_info['size']}")
        print(f"   ✨ Features:")
        for feature in file_info['features']:
            print(f"      • {feature}")
    
    print(f"\n🎯 How to Get Started:")
    print(f"   1. Read the Mathematics_Reference_Guide.md for theory")
    print(f"   2. Run mathematics_for_ml_ai_datascience.py for implementations") 
    print(f"   3. Use interactive_math_tutorial.py for guided learning")
    print(f"   4. Practice regularly and connect concepts to real ML projects")

def main():
    """Main demonstration function"""
    print_header("Mathematics for Machine Learning, AI, and Data Science", "🎓")
    print("Complete Tutorial System - Beginner-Friendly Implementation")
    print("\nWelcome to your comprehensive mathematics learning system!")
    print("This demonstration will show you all the available components.")
    
    # Show file overview
    show_file_overview()
    
    # Show learning path
    show_learning_path()
    
    # Demonstrate key concepts
    print("\n" + "="*80)
    print("🚀 RUNNING DEMONSTRATIONS")
    print("="*80)
    
    # Quick concepts demo
    concepts_success = demonstrate_key_concepts()
    
    # Try to run comprehensive mathematics demo
    print_section("Full Mathematics Tutorial")
    math_success = safe_import_and_run(
        "mathematics_for_ml_ai_datascience",
        None,
        "Complete mathematics concepts with implementations"
    )
    
    # Try to run interactive tutorial demo  
    print_section("Interactive Tutorial System")
    tutorial_success = safe_import_and_run(
        "interactive_math_tutorial", 
        None,
        "Personalized learning system with progress tracking"
    )
    
    # Summary
    print_header("Demo Summary", "📋")
    
    success_count = sum([concepts_success, math_success, tutorial_success])
    
    print(f"✅ Successfully demonstrated: {success_count}/3 components")
    
    if concepts_success:
        print("   ✓ Key mathematical concepts")
    if math_success:
        print("   ✓ Comprehensive mathematics tutorial")
    if tutorial_success:
        print("   ✓ Interactive tutorial system")
    
    print(f"\n🎯 Next Steps:")
    print(f"   1. Explore the Mathematics_Reference_Guide.md for detailed theory")
    print(f"   2. Run individual modules to dive deeper into specific topics")
    print(f"   3. Use the interactive tutorial for structured learning")
    print(f"   4. Practice implementing concepts in your own ML projects")
    
    print(f"\n💡 Tips for Success:")
    print(f"   • Start with linear algebra and probability theory")
    print(f"   • Practice regularly - mathematics requires consistent effort") 
    print(f"   • Connect every concept to practical ML applications")
    print(f"   • Don't rush - understanding is more important than speed")
    print(f"   • Join communities and discussion groups for support")
    
    print(f"\n🚀 Happy learning! You now have a complete mathematics toolkit")
    print(f"   for mastering ML, AI, and Data Science fundamentals!")
    
    return success_count == 3

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n🎉 Demo completed successfully!")
            sys.exit(0)
        else:
            print(f"\n⚠️  Demo completed with some issues. Check the output above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n\n👋 Demo interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)
