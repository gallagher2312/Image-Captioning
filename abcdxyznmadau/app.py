import gradio as gr
from PIL import Image
import os
import glob
from src.captioning import generate_caption
from src.translation import translate_en_to_vi

# Custom CSS for beautiful interface
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.gradio-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.main-container {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    margin: 15px;
}

#title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(45deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 5px;
}

#subtitle {
    text-align: center;
    font-size: 1rem;
    color: #666;
    margin-bottom: 20px;
    font-weight: 300;
}

.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #667eea;
    margin-bottom: 10px;
    text-align: center;
}

.gallery-container {
    background: linear-gradient(135deg, #f8f9ff 0%, #e8f0ff 100%);
    border-radius: 12px;
    padding: 15px;
    margin: 15px 0;
    border: 2px solid #e1e8ff;
}

.gallery-title {
    font-size: 1rem;
    font-weight: 600;
    color: #667eea;
    margin-bottom: 10px;
    text-align: center;
}

.image-container {
    border: 3px dashed #ddd;
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    background: linear-gradient(45deg, #f8f9ff, #f0f2ff);
    transition: all 0.3s ease;
}

.image-container:hover {
    border-color: #667eea;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
}

.caption-box {
    background: linear-gradient(135deg, #f8f9ff 0%, #e8f0ff 100%);
    border: 2px solid #e1e8ff;
    border-radius: 10px;
    padding: 15px;
    margin: 8px 0;
    min-height: 80px;
    font-size: 1rem;
    line-height: 1.5;
    transition: all 0.3s ease;
}

.caption-box:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.generate-btn {
    background: linear-gradient(45deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 12px 30px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 6px 15px rgba(102, 126, 234, 0.3) !important;
    margin: 15px auto !important;
    display: block !important;
    width: 180px !important;
}

.generate-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4) !important;
}

.translate-btn {
    background: linear-gradient(45deg, #56ab2f, #a8e6cf) !important;
    color: white !important;
    border: none !important;
    border-radius: 15px !important;
    padding: 8px 20px !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(86, 171, 47, 0.3) !important;
    margin: 8px auto !important;
    display: block !important;
    width: 120px !important;
}

.translate-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 15px rgba(86, 171, 47, 0.4) !important;
}

.result-container {
    background: linear-gradient(135deg, #fff8f0 0%, #ffe8d6 100%);
    border-radius: 12px;
    padding: 15px;
    margin: 8px 0;
    border: 2px solid #ffd6b8;
    transition: all 0.3s ease;
}

.result-container:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(255, 214, 184, 0.3);
}

.language-tag {
    display: inline-block;
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    padding: 6px 12px;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 8px;
}

.caption-text {
    font-size: 1rem;
    line-height: 1.5;
    color: #333;
    font-weight: 400;
}

/* Sample gallery styles */
.sample-gallery {
    display: flex;
    overflow-x: auto;
    gap: 10px;
    padding: 10px 0;
    scroll-behavior: smooth;
}

.sample-gallery::-webkit-scrollbar {
    height: 6px;
}

.sample-gallery::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
}

.sample-gallery::-webkit-scrollbar-thumb {
    background: #667eea;
    border-radius: 3px;
}

.sample-gallery::-webkit-scrollbar-thumb:hover {
    background: #5a6fd8;
}

.sample-image {
    flex: 0 0 auto;
    width: 80px;
    height: 80px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    object-fit: cover;
}

.sample-image:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
}

.footer {
    text-align: center;
    margin-top: 20px;
    padding: 15px;
    background: linear-gradient(90deg, #f8f9ff, #e8f0ff);
    border-radius: 10px;
}

.footer p {
    color: #666;
    font-size: 0.85rem;
    margin: 0;
}

/* Responsive design */
@media (max-width: 768px) {
    #title {
        font-size: 1.8rem;
    }
    
    .main-container {
        padding: 15px;
        margin: 10px;
    }
    
    .generate-btn, .translate-btn {
        width: 100% !important;
    }
    
    .sample-image {
        width: 60px;
        height: 60px;
    }
}
"""

# Function to load sample images
def load_sample_images():
    """Load sample images from test_images folder"""
    image_folder = "test_images"
    
    # Check if folder exists
    if not os.path.exists(image_folder):
        return []
    
    # Get all image files
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.webp']
    image_files = []
    
    for extension in image_extensions:
        image_files.extend(glob.glob(os.path.join(image_folder, extension)))
        image_files.extend(glob.glob(os.path.join(image_folder, extension.upper())))
    
    # Return first 12 images
    return sorted(image_files)[:10]

def select_sample_image(evt: gr.SelectData):
    """Handle sample image selection"""
    sample_images = load_sample_images()
    if evt.index < len(sample_images):
        image_path = sample_images[evt.index]
        return Image.open(image_path)
    return None

with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    
    with gr.Column(elem_classes="main-container"):
        # Header
        gr.HTML("""
        <div id="title">🎨 AI Image Captioning</div>
        <div id="subtitle">Upload an image and get beautiful captions in English and Vietnamese</div>
        """)
        
        # Main content area
        with gr.Row():
            # Left column - Image upload
            with gr.Column(scale=1):
                gr.HTML('<div class="section-title">📸 Upload Your Image</div>')
                image_input = gr.Image(
                    type="pil", 
                    label="", 
                    elem_classes="image-container",
                    height=300
                )
                
                process_btn = gr.Button(
                    "✨ Generate Caption", 
                    elem_classes="generate-btn",
                    variant="primary"
                )
                
                # Sample images gallery
                with gr.Column(elem_classes="gallery-container"):
                    gr.HTML('<div class="gallery-title">🖼️ Sample Images</div>')
                    
                    # Load sample images
                    sample_images = load_sample_images()
                    
                    if sample_images:
                        sample_gallery = gr.Gallery(
                            value=sample_images,
                            label="",
                            show_label=False,
                            elem_id="sample-gallery",
                            columns=6,
                            rows=2,
                            object_fit="cover",
                            height=120,
                            allow_preview=False
                        )
                        
                        # Connect gallery selection to image input
                        sample_gallery.select(
                            fn=select_sample_image,
                            outputs=image_input
                        )
                    else:
                        gr.HTML('<p style="text-align: center; color: #999;">No sample images found in test_images folder</p>')
            
            # Right column - Results
            with gr.Column(scale=1):
                gr.HTML('<div class="section-title">📝 Caption Results</div>')
                
                # English caption
                with gr.Row(elem_classes="result-container"):
                    gr.HTML('<div class="language-tag">🇺🇸 English</div>')
                    image_output_1 = gr.Textbox(
                        label="",
                        placeholder="English caption will appear here...",
                        elem_classes="caption-text",
                        lines=2,
                        interactive=False
                    )
                
                # Translate button
                translate_btn = gr.Button(
                    "🔄 Translate", 
                    elem_classes="translate-btn",
                    variant="secondary"
                )
                
                # Vietnamese caption
                with gr.Row(elem_classes="result-container"):
                    gr.HTML('<div class="language-tag">🇻🇳 Tiếng Việt</div>')
                    image_output_2 = gr.Textbox(
                        label="",
                        placeholder="Vietnamese caption will appear here...",
                        elem_classes="caption-text",
                        lines=2,
                        interactive=False
                    )
        
        # Footer
        gr.HTML("""
        <div class="footer">
            <p>🚀 Powered by AI • Built with ❤️ • Support multiple languages</p>
        </div>
        """)
    
    # Event handlers
    process_btn.click(
        fn=generate_caption,
        inputs=image_input,
        outputs=image_output_1
    )
    
    translate_btn.click(
        fn=translate_en_to_vi,
        inputs=image_output_1,
        outputs=image_output_2
    )

# Launch with custom configuration
if __name__ == "__main__":
    demo.launch(
        share=True
    )