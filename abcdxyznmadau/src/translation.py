from transformers import MarianMTModel, MarianTokenizer

# Mô hình chuyên biệt cho EN->VI
model_name = "Helsinki-NLP/opus-mt-en-vi"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate_en_to_vi(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    translated = model.generate(**inputs, max_length=512, num_beams=4)
    return tokenizer.decode(translated[0], skip_special_tokens=True)