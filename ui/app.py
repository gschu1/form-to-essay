"""Streamlit UI for json-to-essay with form-based input."""

import io
import json
import zipfile
from pathlib import Path

import streamlit as st

from json_to_essay.schemas.spec import EssaySpec
from json_to_essay.settings import get_settings
from json_to_essay.ui.pipeline_helper import run_pipeline_from_spec_dict
from json_to_essay.ui.spec_builder import FormState, build_spec_from_form

st.set_page_config(page_title="JSON to Essay", page_icon="📝", layout="wide")

settings = get_settings()


def get_provider_status() -> dict:
    """Get current provider status (without exposing API key)."""
    try:
        provider_type = settings.get_provider_type()
        model = settings.openai_model if provider_type == "openai" else "mock"
        return {
            "provider": provider_type,
            "model": model,
            "has_api_key": bool(settings.openai_api_key) if provider_type == "openai" else None,
        }
    except ValueError as e:
        return {
            "provider": "error",
            "error": str(e),
        }


def create_zip_from_dir(dir_path: Path) -> bytes:
    """Create a ZIP file from a directory."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in dir_path.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(dir_path)
                zip_file.write(file_path, arcname)
    zip_buffer.seek(0)
    return zip_buffer.read()


def main() -> None:
    """Main Streamlit app."""
    st.title("📝 JSON to Essay Generator")
    st.markdown("Generate essays from JSON specs with compliance checking")

    # Show provider status
    provider_status = get_provider_status()
    with st.expander("Provider Status", expanded=False):
        if provider_status.get("error"):
            st.error(f"⚠️ {provider_status['error']}")
        else:
            st.info(
                f"**Provider:** {provider_status['provider']} | "
                f"**Model:** {provider_status['model']}"
            )
            if provider_status["provider"] == "openai" and not provider_status.get("has_api_key"):
                st.warning(
                    "⚠️ OPENAI_API_KEY not set. Set it in your .env file to use OpenAI provider."
                )

    # Form section
    st.header("Essay Specification")

    with st.form("essay_form"):
        # Basic fields
        topic = st.text_area(
            "Topic *",
            placeholder="Enter the essay topic...",
            help="The main subject or theme of the essay",
            height=100,
        )

        col1, col2 = st.columns(2)

        with col1:
            purpose = st.selectbox(
                "Purpose",
                ["inform", "persuade", "analyze", "explain"],
                help="The purpose of the essay",
            )
            audience = st.selectbox(
                "Audience",
                ["general", "expert", "student", "executive"],
                help="Target audience for the essay",
            )

        with col2:
            length = st.selectbox(
                "Length",
                ["short", "medium", "long"],
                help="Approximate reading time",
            )
            tone = st.selectbox(
                "Tone",
                ["neutral", "argumentative", "playful", "formal"],
                help="Writing tone and style",
            )

        # Constraints
        st.subheader("Constraints")
        col3, col4 = st.columns(2)

        with col3:
            avoid_cliches = st.checkbox("Avoid cliches")
            use_concrete_examples = st.checkbox("Use concrete examples")

        with col4:
            steelman_opposition = st.checkbox("Steelman opposing arguments")
            include_citations = st.checkbox("Include citations (if available)")

        # Advanced options
        with st.expander("Advanced Options"):
            extra_notes = st.text_area(
                "Additional Notes",
                placeholder="Comma-separated list of topics or phrases to include...",
                help="Optional: additional topics or phrases to include in the essay",
            )

        # Show JSON toggle
        show_json = st.checkbox("Show JSON spec before generating", value=False)

        submitted = st.form_submit_button("Generate Essay", type="primary")

    if submitted:
        if not topic.strip():
            st.error("⚠️ Please enter a topic")
            return

        # Build form state
        form_state = FormState(
            topic=topic.strip(),
            purpose=purpose,
            audience=audience,
            length=length,
            tone=tone,
            avoid_cliches=avoid_cliches,
            use_concrete_examples=use_concrete_examples,
            steelman_opposition=steelman_opposition,
            extra_notes=extra_notes.strip() if extra_notes else None,
            include_citations=include_citations,
        )

        # Build spec dict
        try:
            spec_dict = build_spec_from_form(form_state)
            spec = EssaySpec(**spec_dict)

            # Show JSON if requested
            if show_json:
                st.subheader("Generated Spec JSON")
                st.json(spec_dict)

            # Create output directory with unique ID
            import uuid
            run_id = str(uuid.uuid4())[:8]
            output_dir = settings.output_base_dir / "ui_runs" / run_id
            output_dir.mkdir(parents=True, exist_ok=True)

            # Run pipeline
            with st.spinner("Generating essay and running compliance checks..."):
                try:
                    report, meta = run_pipeline_from_spec_dict(spec_dict, output_dir)
                except Exception as e:
                    st.error(f"❌ Error generating essay: {str(e)}")
                    st.exception(e)
                    return

            # Success message
            st.success(f"✅ Generation complete! Run ID: {meta.run_id[:8]}")

            # Check for truncation warning
            if meta.finish_reason == "length":
                st.warning(
                    "⚠️ **Output may be truncated** (finish_reason=length). "
                    "Consider increasing the Length setting or setting `OPENAI_MAX_OUTPUT_TOKENS` in your .env file."
                )

            # Display run info
            st.info(f"📁 Artifacts saved to: `{output_dir}`")

            # Show usage stats if available
            if meta.usage:
                with st.expander("Token Usage"):
                    st.json(meta.usage)

            # Display essay
            st.header("Generated Essay")
            essay_path = output_dir / "essay.md"
            if essay_path.exists():
                essay_content = essay_path.read_text(encoding="utf-8")
                st.markdown(essay_content)
            else:
                st.warning("Essay file not found")

            # Compliance report
            st.header("Compliance Report")
            
            # Policy info expander
            with st.expander("Policy / Checks Info"):
                from json_to_essay.compliance.policy import Policy
                policy = Policy(settings.policy_path)
                banned_words = policy.get_banned_words()
                st.write("**Banned/Flagged Words:**")
                if banned_words:
                    st.write(", ".join(banned_words))
                else:
                    st.write("None configured")
                st.write(
                    "**Note:** This is a heuristic flag list. Words may appear in legitimate contexts. "
                    "Warnings are informational unless configured to block."
                )

            col_status1, col_status2 = st.columns(2)

            with col_status1:
                status_display = {
                    "pass": "🟢 PASS",
                    "warn": "🟡 WARN",
                    "block": "🔴 BLOCK",
                }
                st.metric("Status", status_display.get(report.status, report.status.upper()))

            with col_status2:
                st.metric("Issues Found", len(report.reasons))

            # Show issues if any
            if report.reasons:
                st.subheader("Issues")
                for reason in report.reasons:
                    severity_icon = {
                        "error": "🔴",
                        "warn": "🟡",
                        "info": "🔵",
                    }
                    icon = severity_icon.get(reason.severity, "⚪")
                    st.write(f"{icon} **{reason.code}** ({reason.severity})")
                    st.write(f"   {reason.message}")
                    if reason.evidence:
                        st.code(reason.evidence, language=None)

            # Check results
            with st.expander("Check Results"):
                check_data = {
                    "Check": list(report.checks.keys()),
                    "Passed": [check.passed for check in report.checks.values()],
                }
                st.dataframe(check_data, use_container_width=True)

            # Full compliance report JSON
            with st.expander("Full Compliance Report JSON"):
                st.json(report.model_dump())

            # Meta information
            with st.expander("Run Metadata"):
                st.json(meta.model_dump())

            # Download section
            st.header("Download")
            col_dl1, col_dl2 = st.columns(2)

            with col_dl1:
                if essay_path.exists():
                    st.download_button(
                        label="📄 Download Essay (Markdown)",
                        data=essay_content,
                        file_name="essay.md",
                        mime="text/markdown",
                    )

            with col_dl2:
                st.download_button(
                    label="📊 Download Compliance Report (JSON)",
                    data=json.dumps(report.model_dump(), indent=2),
                    file_name="compliance_report.json",
                    mime="application/json",
                )

            # Download full run bundle
            st.download_button(
                label="📦 Download Run Bundle (ZIP)",
                data=create_zip_from_dir(output_dir),
                file_name=f"run_{meta.run_id[:8]}.zip",
                mime="application/zip",
            )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.exception(e)


if __name__ == "__main__":
    main()

