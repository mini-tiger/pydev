from transformers import BertTokenizer
import os
os.environ["http_proxy"]="http://127.0.0.1:1081"
os.environ["https_proxy"]="http://127.0.0.1:1081"
tokenizer = BertTokenizer.from_pretrained("bert-base-cased")

# Transformer's tokenizer - input_ids
sequence = "A Titan RTX has 24GB of VRAM"
print("Original sequence: ", sequence)
tokenized_sequence = tokenizer.tokenize(sequence)
print("Tokenized sequence: ", tokenized_sequence)
encodings = tokenizer(sequence)
encoded_sequence = encodings['input_ids']
print("Encoded sequence: ", encoded_sequence)
decoded_encodings = tokenizer.decode(encoded_sequence)
print("Decoded sequence: ", decoded_encodings)