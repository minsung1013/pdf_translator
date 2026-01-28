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

uploaded_file = st.file_uploader(
    "📂 PDF 파일 선택",
    type=["pdf"],
    accept_multiple_files=False,
    help="클릭하여 파일을 선택하거나 드래그하세요"
)

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
