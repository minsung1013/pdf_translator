import os
os.environ["NOTO_FONT_PATH"] = "/tmp/noto.ttf"
os.environ["XDG_CACHE_HOME"] = "/tmp/.cache"
os.environ["HF_HOME"] = "/tmp/.cache/huggingface"

import streamlit as st
from pdf2zh import translate_stream
from pdf2zh.doclayout import OnnxModel

@st.cache_resource
def load_model():
    return OnnxModel.load_available()

model = load_model()

st.title("🐐 흑염소 PDF 번역기")
st.markdown("### 📄 영어 PDF → 한국어 번역")
st.info("💡 수식과 표가 포함된 논문도 번역 가능합니다")

st.markdown("---")

# 모바일 사용자 안내
with st.expander("📱 모바일에서 PDF 파일 찾기"):
    st.markdown("""
    **PDF 파일이 안 보이나요?**

    1. 📂 **다운로드 폴더** 확인
       - 대부분의 PDF는 '다운로드' 또는 'Download' 폴더에 있습니다

    2. 🔍 **파일 관리자 사용**
       - '내 파일' 또는 'Files' 앱에서 PDF 검색
       - 검색창에 ".pdf" 입력

    3. 📧 **이메일/메시지에서 다운로드**
       - PDF를 받은 경우, 먼저 다운로드하세요
       - 다운로드 후 여기서 선택

    4. ☁️ **클라우드 저장소**
       - Google Drive, OneDrive 등에서 먼저 다운로드
    """)

uploaded_file = st.file_uploader(
    "📂 PDF 파일 선택 (클릭하여 파일 찾기)",
    type=["pdf"],
    accept_multiple_files=False,
    help="PDF 파일만 업로드 가능합니다"
)

if not uploaded_file:
    st.warning("⬆️ 위의 '📂 PDF 파일 선택' 버튼을 눌러 PDF 파일을 선택하세요")
    st.caption("💡 파일을 찾을 수 없다면 위의 '📱 모바일에서 PDF 파일 찾기'를 펼쳐보세요")

if uploaded_file:
    st.success(f"✅ 파일 업로드 완료: {uploaded_file.name}")

    if st.button("🚀 번역 시작", use_container_width=True):
        with st.spinner("번역 중..."):
            mono, dual = translate_stream(
                stream=uploaded_file.read(),
                lang_in="en",
                lang_out="ko",
                service="google",
                thread=4,
                model=model
            )

        st.success("✨ 번역 완료!")
        st.balloons()

        st.markdown("### 📥 다운로드")

        st.download_button(
            "📄 번역본만 다운로드",
            mono,
            file_name=f"{uploaded_file.name.replace('.pdf', '')}_번역.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        st.download_button(
            "📚 원문+번역 비교본 다운로드",
            dual,
            file_name=f"{uploaded_file.name.replace('.pdf', '')}_비교.pdf",
            mime="application/pdf",
            use_container_width=True
        )
