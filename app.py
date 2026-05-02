import uuid
import streamlit as st
from openai import AuthenticationError, BadRequestError, OpenAIError
from src.workflow import build_graph

st.set_page_config(
    page_title="OpsPilot AI",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 OpsPilot AI")
st.caption("Agentic CloudOps Incident Diagnosis Copilot using LangGraph")

with st.sidebar:
    st.header("Workflow")
    st.markdown(
        """
        1. Router  
        2. Specialized Diagnostics  
        3. Root Cause Analysis  
        4. Fix Generator  
        5. Evaluator  
        6. Final Report  
        """
    )

incident_text = st.text_area(
    "Paste ECS, Docker, CloudWatch, or deployment logs:",
    height=260,
    placeholder="Example: ECS Fargate task is running but Streamlit app is not loading. Logs show connection refused on port 8501..."
)

if st.button("Diagnose Incident", type="primary"):
    if not incident_text.strip():
        st.warning("Please paste an incident or logs first.")
    else:
        graph = build_graph()

        initial_state = {
            "Incident_text": incident_text,
            "user_question": None,
            "messages": [],
            "memory": {},
            "plan": None,
            "log_summary": None,
            "root_cause": None,
            "fix": None,
            "final_report": None,
            "retrieved_docs": None,
            "evidence": None,
            "eval_score": None,
            "eval_notes": None,
            "hallucination_risk": None,
            "trace_id": str(uuid.uuid4()),
            "node_history": [],
            "errors": [],
            "needs_human_review": False,
            "approved_action": None,
            "incident_type": None,
            "routing_reason": None,
            "eval_status": None,
            "eval_feedback": None,
            "retry_count": 0,
        }

        try:
            with st.spinner("Running LangGraph incident workflow..."):
                result = graph.invoke(initial_state)
        except AuthenticationError:
            st.error(
                "OpenAI authentication failed. Update OPENAI_API_KEY in your .env file with a valid key, "
                "then rebuild and rerun the Docker container."
            )
            st.stop()
        except BadRequestError as exc:
            message = str(exc)
            if "invalid model" in message.lower():
                st.error(
                    "OpenAI rejected the configured model ID. Update OPENAI_MODEL in your .env file "
                    "to a valid model such as gpt-4o-mini, then restart the Docker container."
                )
            else:
                st.error(f"OpenAI API request was invalid: {exc}")
            st.stop()
        except OpenAIError as exc:
            st.error(f"OpenAI API request failed: {exc}")
            st.stop()
        except RuntimeError as exc:
            st.error(str(exc))
            st.stop()

        st.success("Diagnosis complete")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Incident Type", result.get("incident_type", "unknown"))

        with col2:
            st.metric("Evaluation", result.get("eval_status", "not evaluated"))

        with col3:
            st.metric("Retries", result.get("retry_count", 0))

        st.divider()

        st.subheader("Final Incident Report")
        st.markdown(result.get("final_report") or "No final report generated.")

        with st.expander("Diagnostic Plan"):
            st.markdown(result.get("plan") or "No plan generated.")

        with st.expander("Log / Diagnostic Summary"):
            st.markdown(result.get("log_summary") or "No log summary generated.")

        with st.expander("Root Cause Analysis"):
            st.markdown(result.get("root_cause") or "No root cause generated.")

        with st.expander("Fix Recommendation"):
            st.markdown(result.get("fix") or "No fix generated.")

        with st.expander("Evaluator Feedback"):
            st.markdown(result.get("eval_feedback") or "No evaluator feedback.")

        with st.expander("Execution Trace"):
            st.write(result.get("node_history"))
            st.code(result.get("trace_id"))
