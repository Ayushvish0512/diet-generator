import torch
from transformers import AutoProcessor, AutoModelForImageTextToText
from PIL import Image
import requests
import json
from app.models.meal import MealPlan

class LocalMedGemma:
    def __init__(self, model_id="google/medgemma-4b-it"):
        print(f"Loading {model_id} locally. This may take a few minutes...")
        # Device management: Use CUDA (GPU) if available, otherwise CPU
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.bfloat16 if self.device == "cuda" else torch.float32
        
        self.model = AutoModelForImageTextToText.from_pretrained(
            model_id,
            torch_dtype=self.dtype,
            device_map="auto" if self.device == "cuda" else None,
        )
        self.processor = AutoProcessor.from_pretrained(model_id)
        print(f"Model loaded successfully on {self.device}!")

    def generate_json(self, prompt: str) -> dict:
        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": "You are an expert nutritionist and dietitian. Always return ONLY valid JSON."}]
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ]
        
        inputs = self.processor.apply_chat_template(
            messages, add_generation_prompt=True, tokenize=True,
            return_dict=True, return_tensors="pt"
        ).to(self.model.device, dtype=self.dtype)

        input_len = inputs["input_ids"].shape[-1]

        with torch.inference_mode():
            generation = self.model.generate(
                **inputs, 
                max_new_tokens=500, 
                do_sample=True, 
                temperature=0.2
            )
            generation = generation[0][input_len:]

        decoded = self.processor.decode(generation, skip_special_tokens=True)
        
        # Extract JSON from potential conversational text
        try:
            # Simple extraction in case it adds prose
            json_start = decoded.find('{')
            json_end = decoded.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = decoded[json_start:json_end]
                return json.loads(json_str)
            return {"error": "No JSON found", "raw": decoded}
        except Exception as e:
            print(f"JSON Parsing Error: {e}")
            return {"error": str(e), "raw": decoded}

# Singleton instance to avoid reloading model on every request
_local_model = None

def get_local_model():
    global _local_model
    if _local_model is None:
        _local_model = LocalMedGemma()
    return _local_model
