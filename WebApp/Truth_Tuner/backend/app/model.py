import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from preprocess import preprocess_text

import os
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../bigbird-roberta_best_model"))

tokenizer = AutoTokenizer.from_pretrained(model_path)

# Load trained model (assume saved checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

id2label = {
    0: "Left-Leaning",
    1: "Center",
    2: "Right-Leaning"
}

def predict_bias(title: str, content: str) -> str:
    processed_title = preprocess_text(title)
    processed_content = preprocess_text(content)

    inputs = tokenizer(
        processed_title,
        processed_content,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=4096
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        pred = torch.argmax(logits, dim=1).item()
        return id2label[pred]
