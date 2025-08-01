import pandas as pd
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

# Load your CSV
df = pd.read_csv(r'c:\Users\siva\projects\genai_resume_screener\Resource\training_data.csv')

# Prepare training examples
train_examples = []
for _, row in df.iterrows():
    job_desc = str(row['job_description'])
    model_resp = str(row['model_response'])
    label = 1.0  # All positive pairs; for better results, add negative pairs with label=0.0
    train_examples.append(InputExample(texts=[job_desc, model_resp], label=label))

# DataLoader
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=8)

# Load base model
model = SentenceTransformer('BAAI/bge-base-en-v1.5')

# Loss function
train_loss = losses.CosineSimilarityLoss(model)

# Train
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=2,
    warmup_steps=10,
    output_path='output/finetuned-bge-base-en-v1.5'
)

print("Fine-tuning complete! Model saved to output/finetuned-bge-base-en-v1.5")