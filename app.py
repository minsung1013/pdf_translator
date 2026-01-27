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

st.title("PDF 번역기")
st.write("영어 PDF를 한국어로 번역합니다")

uploaded_file = st.file_uploader("PDF 파일을 드래그하세요", type="pdf")

if uploaded_file:
    if st.button("번역 시작"):
        with st.spinner("번역 중..."):
            mono, dual = translate_stream(
                stream=uploaded_file.read(),
                lang_in="en",
                lang_out="ko",
                service="google",
                thread=4,
                model=model
            )

        st.success("번역 완료!")

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "번역본 다운로드",
                mono,
                file_name="translated.pdf",
                mime="application/pdf"
            )
        with col2:
            st.download_button(
                "원문+번역 비교본",
                dual,
                file_name="bilingual.pdf",
                mime="application/pdf"
            )
