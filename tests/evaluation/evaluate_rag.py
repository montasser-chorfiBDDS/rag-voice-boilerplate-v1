"""
RAG Evaluation Script using Ragas

This script evaluates the performance of the RAG engine using a test dataset.
It measures metrics like context precision, context recall, faithfulness, and answer relevancy.
"""

import os
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
import json

# Sample ground truth dataset (in a real scenario, load this from a CSV or JSON file)
data_samples = {
    "question": [
        "What is the main feature of the RAG Voice Boilerplate?",
        "How do I install the dependencies?",
    ],
    "answer": [
        "The main feature is a production-ready RAG application with voice processing capabilities, including Speech-to-text and text-to-speech.",
        "You can install the dependencies by running 'pip install -r requirements.txt'.",
    ],
    "contexts": [
        ["A production-ready Python boilerplate for building RAG (Retrieval Augmented Generation) applications with voice processing capabilities.", "- **🎤 Voice Processing Pipeline** - Speech-to-text and text-to-speech"],
        ["3. Install dependencies:\n```bash\npip install -r requirements.txt\n```"],
    ],
    "ground_truth": [
        "It is a Python boilerplate for building RAG applications that includes voice processing features like Speech-to-text and text-to-speech.",
        "Run 'pip install -r requirements.txt' to install the dependencies.",
    ]
}

def run_evaluation():
    print("Preparing evaluation dataset...")
    dataset = Dataset.from_dict(data_samples)

    print("Running Ragas evaluation...")
    # NOTE: You need OPENAI_API_KEY set in your environment for the default LLM used by Ragas evaluators
    if "OPENAI_API_KEY" not in os.environ:
        print("WARNING: OPENAI_API_KEY not found in environment. Evaluation might fail if using default OpenAI models.")

    metrics = [
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ]

    try:
        result = evaluate(
            dataset,
            metrics=metrics,
        )

        print("\n=== Evaluation Results ===")
        print(result)

        # Save results to a file
        output_file = "evaluation_results.json"
        
        # result is a dictionary-like object in ragas
        result_dict = {metric.name: result[metric.name] for metric in metrics if metric.name in result}
        
        with open(output_file, "w") as f:
            json.dump(result_dict, f, indent=4)
        print(f"\nResults saved to {output_file}")
        
    except Exception as e:
        print(f"Evaluation failed: {e}")

if __name__ == "__main__":
    run_evaluation()
