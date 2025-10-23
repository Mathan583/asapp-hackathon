from sentence_transformers import SentenceTransformer
from transformers import pipeline

class AirlineModel:
    def __init__(self):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.generator = pipeline("text-generation", model="gpt2")

    def get_embedding(self, text):
        return self.embedder.encode([text])[0]

    def generate_response(self, prompt):
        response = self.generator(
            prompt, 
            max_new_tokens=30, 
            temperature=0.3,
            do_sample=True,
            pad_token_id=self.generator.tokenizer.eos_token_id
        )[0]['generated_text']
        
        # Extract only the bot's response, not the full prompt
        if "Bot:" in response:
            bot_response = response.split("Bot:")[-1].strip()
            # Clean up any extra text after the response
            if "\n" in bot_response:
                bot_response = bot_response.split("\n")[0].strip()
            if "User:" in bot_response:
                bot_response = bot_response.split("User:")[0].strip()
            return bot_response
        else:
            # Fallback: return the last part of the response
            return response.split("\n")[-1].strip()
