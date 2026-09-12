# THE COGNITIVE LEARNING SYSTEM

This repository is not a reference manual. It is a **cognitive learning machine** designed to move knowledge from your screen into your long-term memory, and from your memory into your fingertips.

## The Problem with Tutorials
Most tutorials fail because they optimize for *reading fluency*. You read the code, it makes sense, and you feel like you learned it. But when you close the screen and try to build a system from scratch, you realize you only recognized the code; you didn't learn it.

## The 4 Pillars of This Repository

### 1. Active Recall (The "Close the Screen" Rule)
Every file in this repository contains an **Active Recall** section. 
**The Rule:** You are not allowed to say you understand a file until you can answer the Active Recall questions out loud, with the screen closed, using accurate technical vocabulary.

### 2. Spaced Repetition & Interleaving
Do not read this repository top-to-bottom once.
- **Day 0:** Read the file, understand the Intuition and Trace.
- **Day 1:** Attempt the Active Recall questions.
- **Day 3:** Attempt to write the "Educational From-Scratch Implementation" entirely from memory.
- **Day 7:** Find the "Deliberately Buggy Implementation" and debug it without looking at the answers.
- **Day 14:** Connect the concept to a real-world Project.

### 3. Error-Driven Learning
Professional engineering is 80% debugging. 
Every major concept here includes a **Deliberately Buggy Implementation**. You will learn to recognize what failure looks like. You will learn the difference between an `IndexError`, a `TypeError`, and a silent logical failure (e.g., an infinite loop in Binary Search).

### 4. The Engineering Progression
For every concept, you will follow this mental progression:
1. **Intuition:** What is the physical/real-world analogy?
2. **Formalism:** What is the mathematical or computational definition?
3. **From-Scratch:** How do I build it if libraries didn't exist? (To understand the engine).
4. **Library:** How do I build it in production? (To use the car).
5. **Trade-offs:** When should I explicitly *avoid* using this?

## How to Proceed
1. Open the `MASTER-ROADMAP.md` to see the global progression.
2. Enter the current Phase folder.
3. Open the `.py` or `.md` files.
4. Read the A-X documentation header.
5. Study the code traces.
6. Execute the `run_tests()` block locally.
7. Close the file and test your Active Recall.

*You do not know AI until you can build it. You cannot build it until you remember it.*
