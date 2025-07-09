from transformers import AutoProcessor, AutoModelForCausalLM
import torch

# Load GIT model
caption_processor = AutoProcessor.from_pretrained("microsoft/git-base")
caption_model = AutoModelForCausalLM.from_pretrained("microsoft/git-base")
caption_model.eval()

def generate_caption(image):
    inputs = caption_processor(images=image, return_tensors="pt")
    with torch.inference_mode():
        generated_ids = caption_model.generate(pixel_values=inputs["pixel_values"], max_length=50)
        caption = caption_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return caption