import pandas as pd

results = {
    "Metric": ["Accuracy", "False Acceptance Rate (FAR)", "False Rejection Rate (FRR)"],
    "Value": [96.3, 3.5, 4.2] 
}

results_df = pd.DataFrame(results)
results_df.to_csv("results/model_evaluation.csv", index=False)
print("Synthetic model evaluation results saved to 'results/model_evaluation.csv'!")