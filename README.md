# Image-Captioning

📌 Mục tiêu dự án
Ứng dụng kết hợp dịch Anh–Việt và mô tả ảnh tự động bằng các mô hình pretrained từ thư viện 🤗 Transformers.

✅ Lý do chọn mô hình
Helsinki-NLP/opus-mt-en-vi:

Là mô hình dịch ngôn ngữ chuyên biệt cho cặp ngôn ngữ English → Vietnamese.

Được huấn luyện trên tập dữ liệu song ngữ chất lượng cao từ OPUS.

Dễ triển khai, không yêu cầu fine-tuning, hiệu quả cao cho các đoạn văn ngắn đến trung bình.

microsoft/git-base:

Là mô hình Vision-to-Text dạng GIT (Generative Image-to-Text).

Có khả năng mô tả nội dung ảnh tự động, áp dụng tốt trong các hệ thống hỗ trợ người khiếm thị, tìm kiếm ảnh,...

Cách chạy ứng dụng
Cài đặt thư viện:

bash
Sao chép
Chỉnh sửa
pip install -r requirements.txt
Chạy ứng dụng chính:

bash
Sao chép
Chỉnh sửa
python app.py
Ví dụ sử dụng (trong app.py):

Dịch văn bản:

python
Sao chép
Chỉnh sửa
translate_en_to_vi("How are you today?")
Mô tả ảnh:

python
Sao chép
Chỉnh sửa
from PIL import Image
image = Image.open("your_image.jpg")
generate_caption(image)
🛠 Đề xuất cải thiện khi triển khai production
Vấn đề	Hướng cải thiện
Hiệu năng chậm	- Sử dụng mô hình nhẹ hơn (opus-mt-tiny-en-vi nếu chấp nhận độ chính xác thấp hơn).
- Dùng torch.compile() (PyTorch 2.x) để tăng tốc.
Tốn RAM / GPU	- Dùng mô hình dạng quantized (qua bitsandbytes, optimum).
- Load mô hình một lần, tránh reload mỗi request (dùng FastAPI + cache).
Dịch vụ dịch nâng cao	- Tích hợp Google Translate API (trả phí) nếu yêu cầu chất lượng cao hơn.
Triển khai web	- Tạo REST API với FastAPI hoặc Flask.
- Có thể đóng gói thành container Docker để triển khai cloud (AWS, GCP, Azure).
