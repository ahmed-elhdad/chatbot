from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
import openai
from src.models import ChunkResult
from src.config import get_settings
app_settings=get_settings()
# إعداد مقطع النصوص
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=app_settings.FILE_DEFAULT_CHUNK_SIZE,        # حجم مناسب جداً لخدمة العملاء
    chunk_overlap=150,
    separators=["\n\n", "\n", " ", ""]
)


async def process_text_input(text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """تقطيع النصوص المباشرة إلى Chunks"""
    chunks = text_splitter.split_text(text)
    return [
        {
            "type": "text",
            "content": chunk,
            "metadata": metadata or {}
        }
        for chunk in chunks
    ]

async def process_image_input(image_path_or_url: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    إرسال الصورة لـ GPT-4o لوصفها بدقة، وتجهيز الوصف لعمل الـ Embedding
    """
    # ملاحظة: يجب أن تكون الصورة مرفوعة على سيرفرك أو ممررة كـ Base64
    response = openai.chat.completions.create(
        model="gpt-4o-mini", # خيار سريع وممتاز للرؤية ووصف الصور
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "صف هذه الصورة بالتفصيل لغرض استخدامها في خدمة العملاء والدعم الفني. اذكر المنتجات، الألوان، أو المشاكل الموضحة فيها إن وجدت."},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_path_or_url}, # أو مسار محلي إذا كنت تستخدم مكتبة معالجة محليه
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    
    image_description = response.choices[0].message.content
    
    # دمج مسار الصورة في الميتا داتا حتى نتمكن من عرض الصورة للمستخدم في الشات لاحقاً
    extended_metadata = metadata or {}
    extended_metadata["image_source"] = image_path_or_url
    
    return {
        "type": "image",
        "content": image_description, # سيتم عمل embedding لهذا الوصف
        "metadata": extended_metadata
    }
# process_image_input(image_path_or_url='/data/uploads/files/٢٠٢٦٠٣٢٢_٠٦٥٨٣١.jpg')