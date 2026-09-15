import streamlit as st
import json
import traceback
from graph import review_graph
from utils.db import init_db, save_review, get_all_reviews
from agents.chat_agent import generate_chat_response

# Initialize Database
init_db()

st.set_page_config(page_title="AI Code Review Bot", page_icon="🤖", layout="wide")

if "active_review" not in st.session_state:
    st.session_state.active_review = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ================= SIDEBAR =================
with st.sidebar:
    st.header("🤖 Code Review Bot")
    if st.button("➕ New Review", type="primary", use_container_width=True):
        st.session_state.active_review = None
        st.session_state.chat_history = []
        st.rerun()
        
    st.divider()
    st.markdown("### 📚 History")
    
    for item in get_all_reviews():
        btn_label = f"{item['language']} ({item['score']}/100)\n{item['timestamp']}"
        if st.button(btn_label, key=f"hist_{item['id']}", use_container_width=True):
            st.session_state.active_review = json.loads(item['state_json'])
            st.session_state.chat_history = []
            st.rerun()

# ================= MAIN AREA =================
if st.session_state.active_review is None:
    st.title("New Code Review")
    language = st.selectbox("Select Language:", ["Python", "JavaScript", "Java", "C++", "HTML/CSS"])
    code_input = st.text_area("Paste your source code here:", height=300)

    if st.button("🔍 Review Code", type="primary"):
        if not code_input.strip():
            st.warning("Please paste some code.")
        else:
            with st.spinner("Analyzing code..."):
                try:
                    initial_state = {
                        "code": code_input, "language": language, "error": "",
                        "bugs": [], "security_issues": [], "quality_issues": [], "performance_issues": [],
                        "combined_issues": [], "improved_code": "", "final_review": {}
                    }
                    
                    final_state = review_graph.invoke(initial_state)
                    
                    if final_state.get("error"):
                        st.error(final_state["error"])
                    else:
                        save_review(final_state)
                        st.session_state.active_review = final_state
                        st.session_state.chat_history = []
                        st.rerun()
                        
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                        st.error("⏳ Google API Rate Limit Reached! Because this app uses 6 AI agents per review, you hit the free tier speed limit. Please wait 1 minute and try again.")
                    else:
                        st.error(f"❌ Application Error: {error_msg}")
                
                # 🔴 NO TRY/EXCEPT HERE. IF IT FAILS, THE SCREEN WILL TURN GREY AND SHOW THE REAL PYTHON ERROR 🔴
                final_state = review_graph.invoke(initial_state)
                
                if final_state.get("error"):
                    st.error(final_state["error"])
                else:
                    save_review(final_state)
                    st.session_state.active_review = final_state
                    st.session_state.chat_history = []
                    st.rerun()
else:
    review = st.session_state.active_review
    final_data = review.get("final_review", {})
    
    st.title(f"Review Results: {review['language']}")
    col1, col2 = st.columns(2)
    col1.metric("Overall Score", f"{final_data.get('overall_score', 0)}/100")
    col2.metric("Risk Level", final_data.get('risk_level', 'Unknown'))
    
    st.markdown("### 📝 Summary")
    st.write(final_data.get('summary', ''))
    
    tab1, tab2 = st.tabs(["🚨 Issues", "✨ Improved Code"])
    
    with tab1:
        for issue in review.get("combined_issues", []):
            with st.expander(f"[{issue['severity']}] {issue['category']}: {issue['title']} (Line: {issue['line']})"):
                st.markdown(f"**Problem:** {issue['explanation']}\n\n**Fix:** {issue['recommendation']}")

    with tab2:
        st.code(review["improved_code"], language=review["language"].lower())

    st.divider()
    st.markdown("### 💬 Chat about this review")
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_message := st.chat_input("Ask a follow-up question..."):
        st.session_state.chat_history.append({"role": "user", "content": user_message})
        with st.chat_message("user"):
            st.markdown(user_message)
            
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response_text = generate_chat_response(
                        st.session_state.active_review,
                        st.session_state.chat_history[:-1],
                        user_message
                    )
                    st.markdown(response_text)
                    st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    st.error("Chat Error:")
                    st.code(traceback.format_exc(), language="python")