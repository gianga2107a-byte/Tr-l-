Python 3.14.0 (tags/v3.14.0:ebf955d, Oct  7 2025, 10:15:03) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
"""
TRỢ LÝ AI PHÁP LUẬT HỖ TRỢ CÔNG AN XÃ
Chạy bằng: uvicorn law_ai_assistant:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

# =========================
# 1️⃣ CẤU HÌNH API KEY
# =========================
# Cách 1 (khuyến nghị):
# export OPENAI_API_KEY="your_api_key_here"
#
# Cách 2 (đơn giản để test):
... # os.environ["OPENAI_API_KEY"] = "your_api_key_here"
... 
... client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
... 
... # =========================
... # 2️⃣ PROMPT "BỘ NÃO"
... # =========================
... SYSTEM_PROMPT = """
... Bạn là trợ lý AI pháp luật chuyên hỗ trợ Công an xã Việt Nam.
... 
... MỤC TIÊU:
... - Trả lời các câu hỏi pháp luật phục vụ công tác của Công an xã.
... - Nội dung trả lời phải chính xác, đúng quy định pháp luật hiện hành.
... - Ưu tiên giải thích ngắn gọn, rõ ràng, dễ áp dụng trong thực tế.
... 
... PHẠM VI HỖ TRỢ:
... - Luật Xử lý vi phạm hành chính
... - Bộ luật Hình sự (ở mức độ tham khảo, không kết luận vụ việc)
... - Luật Cư trú
... - Luật Giao thông đường bộ
... - Thẩm quyền, nhiệm vụ của Công an xã
... 
... NGUYÊN TẮC BẮT BUỘC:
... - KHÔNG kết luận có tội hay không có tội.
... - KHÔNG đưa ra chỉ đạo nghiệp vụ mang tính mệnh lệnh.
... - KHÔNG hướng dẫn lách luật hoặc né tránh trách nhiệm pháp lý.
... - KHÔNG thay thế quyết định của người có thẩm quyền.
... 
... CÁCH TRẢ LỜI:
... - Giọng điệu nghiêm túc, chuẩn mực, lịch sự.
... - Có thể thân thiện, gần gũi nhưng không suồng sã.
... - Ưu tiên gạch đầu dòng, trình bày rõ ràng.
... - Khi cần, nêu căn cứ pháp luật (không bịa điều luật).
... 
... KHI CÂU HỎI VƯỢT THẨM QUYỀN HOẶC CHƯA ĐỦ DỮ LIỆU:
... - Phải nói rõ giới hạn hỗ trợ.
... - Đề xuất tham khảo cấp trên hoặc văn bản pháp luật liên quan.
... """
... 
... # =========================
# 3️⃣ KHỞI TẠO FASTAPI
# =========================
app = FastAPI(
    title="Trợ lý AI Pháp luật Công an xã",
    description="Hỗ trợ tra cứu và giải thích pháp luật phục vụ Công an xã",
    version="1.0"
)

# =========================
# 4️⃣ MODEL REQUEST / RESPONSE
# =========================
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

# =========================
# 5️⃣ API CHÍNH
# =========================
@app.post("/ask", response_model=AnswerResponse)
def ask_law_ai(data: QuestionRequest):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": data.question}
        ]
    )

    answer = response.choices[0].message.content
    return {"answer": answer}


# =========================
# 6️⃣ API TEST NHANH
# =========================
@app.get("/")
def root():
    return {
        "message": "Trợ lý AI Pháp luật Công an xã đang hoạt động",
        "usage": "POST /ask với JSON { 'question': '...' }"
    }
