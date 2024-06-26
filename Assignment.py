
#Assignment: Invoice Data Extraction Using Machine Learning
"""

!pip install pdfplumber

import pdfplumber

!pip install pytesseract

import pytesseract

import os

if not os.path.exists('invoices'):
    os.makedirs('invoices')

import os
import pdfplumber
import pytesseract

invoices_folder = 'invoices'

# Extract text from PDFs using pdfplumber
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
        return text

# Convert PDFs to text using OCR
def convert_pdfs_to_text():
    for file in os.listdir(invoices_folder):
        if file.endswith('.pdf'):
            pdf_file = os.path.join(invoices_folder, file)
            text = extract_text_from_pdf(pdf_file)
            with open(f'{file}.txt', 'w') as f:
                f.write(text)

convert_pdfs_to_text()

"""Data Preprocessing
We'll clean and preprocess the extracted text using pandas and numpy:
"""

import pandas as pd
import numpy as np

# Load the extracted text files
def load_text_files():
    text_files = []
    for file in os.listdir(invoices_folder):
        if file.endswith('.txt'):
            with open(os.path.join(invoices_folder, file), 'r') as f:
                text_files.append(f.read())
    return text_files

# Preprocess the text data
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text

text_files = load_text_files()
preprocessed_text = [preprocess_text(text) for text in text_files]

"""Annotate the Data
We'll annotate the data to identify key information (e.g., sender, receiver, VAT number, amounts) without relying on hardcoded labels. For this example, let's assume we have a CSV file annotations.csv containing the annotated data:
"""

dataset = [
    {"text": "This is an invoice from John to Jane...", "sender": "John", "receiver": "Jane", "vat_number": "123456", "amount": 100.00},
    {"text": "Factuur voor diensten aan Peter...", "sender": "Peter", "receiver": "", "vat_number": "456789", "amount": 200.00},
    # Add more invoices to the dataset
]

invoices_folder = 'invoices'
output_folder = 'output'

def convert_pdfs_to_text():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(invoices_folder):
        if file.endswith('.pdf'):
            pdf_file = os.path.join(invoices_folder, file)
            output_file = os.path.join(output_folder, f'{os.path.splitext(file)[0]}.txt')

            with pdfplumber.open(pdf_file) as pdf:
                text = ''
                for page in pdf.pages:
                    text += page.extract_text()

            with open(output_file, 'w') as f:
                f.write(text)

convert_pdfs_to_text()

"""Model Training
We'll use a pre-trained model and fine-tune it on our annotated dataset. For this example, let's use the transformers library and the bert-base-uncased model:
"""

import torch
from torch.utils.data import Dataset

class InvoiceDataset(Dataset):
    def __init__(self, preprocessed_text, annotations):
        self.preprocessed_text = preprocessed_text
        self.annotations = annotations

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        annotation = self.annotations[index]
        text = self.preprocessed_text[index]
        return text, annotation

# Preprocess the text data
preprocessed_text = [...]  # Populate this list with preprocessed text data

# Create the annotations variable
annotations = [
    {"text": "This is an invoice from John to Jane...", "sender": "John", "receiver": "Jane", "vat_number": "123456", "amount": 100.00},
    {"text": "Factuur voor diensten aan Peter...", "sender": "Peter", "receiver": "", "vat_number": "456789", "amount": 200.00},
    # Add more invoices to the annotations
]

# Create the dataset
dataset = InvoiceDataset(preprocessed_text, annotations)
data_loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)
#dataset = InvoiceDataset(preprocessed_text, annotations)

# Create the data loader
data_loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

import string

import torch
from transformers import BertTokenizer, BertModel

# Load the pre-trained model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Prepare the dataset for training
import pandas as pd

import pandas as pd

# Create a sample dataset
data = {
    "text": [
        "This is an invoice from John to Jane...",
        "Factuur voor diensten aan Peter...",
        "Invoice for services provided to Michael...",
        "Rechnung für Dienstleistungen an Sarah..."
    ],
    "label": [0, 1, 0, 1]  # 0 for English, 1 for non-English
}

df = pd.DataFrame(data)

# Print the sample dataset
print(df)

# Preprocess the text data
preprocessed_text = []
for text in df['text']:
    # Remove punctuation and convert to lowercase
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    preprocessed_text.append(text)

# Create annotations
annotations = df['label'].tolist()

# Create the dataset class
class InvoiceDataset(torch.utils.data.Dataset):
    def __init__(self, text, annotations):
        self.text = text
        self.annotations = annotations

    def __len__(self):
        return len(self.text)

    def __getitem__(self, idx):
        text = self.text[idx]
        annotations = self.annotations[idx]
        encoding = tokenizer.encode_plus(
            text,
            max_length=512,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        labels = torch.tensor(annotations)
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': labels
        }

# Create the dataset and data loader
dataset = InvoiceDataset(preprocessed_text, annotations)
data_loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

# Fine-tune the model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)

for epoch in range(5):
    model.train()
    total_loss = 0
    for batch in data_loader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

"""**Part 2: Model Optimization**

1. Convert to ONNX:
To convert the trained model to ONNX format, you can use the torch.onnx.export function.
"""

pip install torch torchvision

!pip install onnx

import torch
import torchvision

# Define the model
model = torchvision.models.resnet18()

# Convert the model to ONNX format
# Define the model input
x = torch.randn(1, 3, 224, 224)
torch.onnx.export(model,               # model being run
                  x,                         # model input (or a tuple for multiple inputs)
                  "model.onnx",   # where to save the model (can be a file or file-like object)
                  export_params=True,        # store the trained parameter weights inside the model file
                  opset_version=10,          # the ONNX version to export the model to
                  do_constant_folding=True,  # whether to execute constant folding for optimization
                  input_names = ['input'],   # the model's input names
                  output_names = ['output'], # the model's output names
                  dynamic_axes={'input' : {0 : 'batch_size'},    # variable length axes
                                'output' : {0 : 'batch_size'}})

"""2. Optimize the Model:
Once you have the model in ONNX format, you can use tools like ONNX Runtime for optimization. One such optimization technique is quantization, which can reduce the model size and improve performance.
"""

!pip install onnxruntime

import onnxruntime as rt
print(rt.__version__)

import onnxruntime as rt

# Load the model
sess = rt.InferenceSession("model.onnx")

# Quantize the model

"""Part 3: Model Deployment

. Set Up Client Environment:
o Ensure the client machine has the necessary libraries installed.
"""

pip install onnxruntime

"""2. Load and Run the Model:
To load and run the model, you can create a Python script that loads the ONNX model and uses it for inference. Here's an example
"""

import onnxruntime as ort
import numpy as np

# Load the optimized ONNX model
model_path = "model.onnx"
sess = ort.InferenceSession(model_path)

# Get the input and output names
input_name = sess.get_inputs()[0].name
output_name = sess.get_outputs()[0].name

# Prepare the input data
input_data = np.random.rand(1, 3, 224, 224).astype(np.float32)  # assuming input shape is (1, 3, 224, 224)

# Run the model
outputs = sess.run([output_name], {input_name: input_data})

# Get the output
output = outputs[0]

# Print the output
print(output.shape)print(output)



model = joblib.load('optimized_model.joblib')

import joblib

try:
    model = joblib.load('optimized_model.joblib')
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Error: The file 'optimized_model.joblib' does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")

