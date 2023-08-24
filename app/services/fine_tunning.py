from transformers import OpenAIGPTTokenizer, OpenAIGPTLMHeadModel
from ..utils import extract_text_from_pdf, extract_text
from torch.optim import Adam
from torch.nn.utils.rnn import pad_sequence

import random
import torch

def fine_tunning(input_text):
    # loading pre-trained model and tokenizer
    model = OpenAIGPTLMHeadModel.from_pretrained("openai-gpt")
    tokenizer = OpenAIGPTTokenizer.from_pretrained("openai-gpt")

    model.train() # set the model for training mode
    tokenized_text = tokenizer.tokenize(input_text)
    if not tokenized_text:
        raise ValueError("Input text could not be tokenized, please check the input.")
    input_ids = tokenizer.convert_tokens_to_ids(tokenized_text)

    # split the inputs_ids into chunks of 512
    input_chunks = [input_ids[i:i + 512] for i in range(0, len(input_ids), 512)]

    # hyperparameters
    epochs = 3
    learning_rate = 1e-4
    optimizer = Adam(model.parameters(), lr=learning_rate)
    for epoch in range(epochs):
        for input_ids in input_chunks:
            optimizer.zero_grad()
            input_data = pad_sequence([torch.tensor(input_ids)], batch_first=True)
            outputs = model(input_data, labels=input_data)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
        user_id = random.randint(1, 10000)
        # saving 
        model_dir = f"user_models/{user_id}"
        model.save_pretrained(model_dir)
        tokenizer.save_pretrained(model_dir)

        # Loading
        model = OpenAIGPTLMHeadModel.from_pretrained(model_dir)
        tokenizer = OpenAIGPTTokenizer.from_pretrained(model_dir)
        model.eval() # set model to evaluation mode

