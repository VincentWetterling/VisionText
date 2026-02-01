from transformers import BlipProcessor, BlipForConditionalGeneration
import os


class BLIPVision:
    def __init__(self):
        # prefer local repo-style folder if available (set BLIP_LOCAL_DIR or place under ./models/Salesforce/...)
        candidates = []
        env_dir = os.environ.get('BLIP_LOCAL_DIR')
        if env_dir:
            candidates.append(env_dir)

        repo_local = os.path.join(os.getcwd(), 'models', 'Salesforce', 'blip-image-captioning-base')
        candidates.append(repo_local)

        hf_home = os.environ.get('HF_HOME', os.path.expanduser('~/.cache/huggingface'))
        hf_cached = os.path.join(hf_home, 'transformers', 'models--Salesforce--blip-image-captioning-base')
        candidates.append(hf_cached)

        found_local = None
        for p in candidates:
            try:
                if p and os.path.exists(p):
                    found_local = p
                    break
            except Exception:
                continue

        if found_local:
            self.processor = BlipProcessor.from_pretrained(found_local, local_files_only=True)
            self.model = BlipForConditionalGeneration.from_pretrained(found_local, local_files_only=True)
        else:
            self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    def run(self, image):
        inputs = self.processor(image, return_tensors="pt")
        out = self.model.generate(**inputs)
        return self.processor.decode(out[0], skip_special_tokens=True)
