import logging
import os

logging.basicConfig(level=logging.INFO)


def try_dl(name, func, *args, **kwargs):
    try:
        logging.info(f"Downloading {name}...")
        func(*args, **kwargs)
        logging.info(f"{name} downloaded")
    except Exception as e:
        logging.warning(f"Failed to download {name}: {e}")


def main():
    # pick a cache dir (prefer environment variable, else use image-stable path)
    cache_dir = os.environ.get('HF_CACHE_DIR') or os.environ.get('HF_HOME') or '/app/models/huggingface'
    # ensure transformer-specific cache path
    transformers_cache = os.path.join(cache_dir, 'transformers')
    os.makedirs(transformers_cache, exist_ok=True)

    # preload BLIP (captioning)
    try:
        from transformers import BlipProcessor, BlipForConditionalGeneration
        # prefer snapshot_download to create a repo-style folder under /app/models
        try:
            from huggingface_hub import snapshot_download
            target_dir = os.path.join('/app/models', 'Salesforce', 'blip-image-captioning-base')
            os.makedirs(target_dir, exist_ok=True)
            logging.info(f"Snapshot downloading Salesforce/blip-image-captioning-base to {target_dir}...")
            repo_path = snapshot_download("Salesforce/blip-image-captioning-base", cache_dir=cache_dir)
            # copy repo files into target_dir so transformers can load from a repo-style folder
            import shutil
            shutil.copytree(repo_path, target_dir, dirs_exist_ok=True)
            logging.info("Salesforce/blip-image-captioning-base snapshot saved")
        except Exception:
            # fallback to cached from_pretrained behavior
            try_dl("Salesforce/blip-image-captioning-base", BlipProcessor.from_pretrained, "Salesforce/blip-image-captioning-base", cache_dir=cache_dir)
            try_dl("Salesforce/blip-image-captioning-base-model", BlipForConditionalGeneration.from_pretrained, "Salesforce/blip-image-captioning-base", cache_dir=cache_dir)
    except Exception as e:
        logging.warning(f"transformers not available or BLIP preload failed: {e}")


    # preload EasyOCR internal models by creating a Reader
    try:
        import easyocr
        try_dl("easyocr-reader", easyocr.Reader, ['en'])
    except Exception as e:
        logging.warning(f"easyocr not available or preload failed: {e}")



if __name__ == '__main__':
    main()
