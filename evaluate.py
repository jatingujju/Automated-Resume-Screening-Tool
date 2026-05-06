import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score


def precision_at_k(df, k=5):
    df_sorted = df.sort_values(by="score", ascending=False).head(k)
    return df_sorted["label"].sum() / max(1, k)


def evaluate(file_path):
    df = pd.read_csv(file_path)

    # normalize score if it is 0–100
    if df["score"].max() > 1:
        df["score"] = df["score"] / 100.0

    y_true = df["label"]
    y_scores = df["score"]

    roc = roc_auc_score(y_true, y_scores)
    pr = average_precision_score(y_true, y_scores)

    print("\n📊 Evaluation Results")
    print(f"ROC AUC: {roc:.3f}")
    print(f"PR AUC : {pr:.3f}")

    for k in [1, 3, 5]:
        print(f"Precision@{k}: {precision_at_k(df, k):.3f}")


if __name__ == "__main__":
    evaluate("data/labeled_pairs.csv")