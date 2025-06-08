# Techniques Used

- **Model**: _BigBird-RoBERTa-base_ (transformer model suited for long documents)
- **Training**: Fine-tuned on labeled data with class-weighted loss
- **Evaluation**: Custom F-beta scores (β = 1, 1.5, 1.8, 2.0) to reflect recall importance
