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
    type=None,
    accept_multiple_files=False,
    help="PDF 파일을 업로드하세요"
)

if uploaded_file:
    # PDF 파일 검증
    if not uploaded_file.name.lower().endswith('.pdf'):
        st.error("❌ PDF 파일만 업로드 가능합니다. 다른 파일을 선택해주세요.")
        st.stop()

    # 파일 크기 확인
    file_size_mb = uploaded_file.size / (1024 * 1024)

    st.success(f"✅ 파일 업로드 완료: {uploaded_file.name} ({file_size_mb:.1f}MB)")

    # 큰 파일 경고
    if file_size_mb > 100:
        st.warning(f"⚠️ 파일 크기가 {file_size_mb:.1f}MB로 큽니다. 번역에 시간이 오래 걸릴 수 있습니다.")

    if st.button("🚀 번역 시작", use_container_width=True):
        try:
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
        except Exception as e:
            st.error(f"❌ 오류가 발생했습니다: {str(e)}")
            st.info("PDF 파일이 손상되었거나 올바른 형식이 아닐 수 있습니다.")
