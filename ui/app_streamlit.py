"""Streamlit UI for json-to-essay."""

import json
import uuid
from pathlib import Path

import streamlit as st
from pydantic import ValidationError

from json_to_essay.compliance.policy import Policy
from json_to_essay.pipeline.run import run_pipeline
from json_to_essay.schemas.spec import EssaySpec
from json_to_essay.settings import get_settings
from json_to_essay.util.files import write_json, write_text

st.set_page_config(page_title="JSON to Essay", page_icon="📝", layout="wide")

settings = get_settings()
policy = Policy(settings.policy_path)


def main() -> None:
    """Main Streamlit app."""
    st.title("📝 JSON to Essay Generator")
    st.markdown("Generate essays from JSON specs with compliance checking")

    # Input section
    st.header("Input Specification")
    input_method = st.radio("Input method", ["Paste JSON", "Upload JSON file"])

    spec_text = ""
    if input_method == "Paste JSON":
        spec_text = st.text_area("JSON Spec", height=300, placeholder='{"language": "en", ...}')
    else:
        uploaded_file = st.file_uploader("Upload JSON file", type=["json"])
        if uploaded_file:
            spec_text = uploaded_file.read().decode("utf-8")

    # Generate button
    if st.button("Generate Essay", type="primary"):
        if not spec_text:
            st.error("Please provide a JSON spec")
            return

        try:
            # Parse spec
            spec_data = json.loads(spec_text)
            spec = EssaySpec(**spec_data)

            # Create output directory
            run_id = str(uuid.uuid4())[:8]
            output_dir = settings.output_base_dir / "ui" / run_id
            output_dir.mkdir(parents=True, exist_ok=True)

            # Save input spec
            write_json(output_dir / "input_spec.json", spec_data)

            # Run pipeline
            with st.spinner("Generating essay and running compliance checks..."):
                report, meta = run_pipeline(spec, Path("input"), output_dir, policy=policy)

            # Display results
            st.success(f"Generation complete! Run ID: {run_id}")

            # Essay display
            st.header("Generated Essay")
            essay_path = output_dir / "essay.md"
            if essay_path.exists():
                essay_content = essay_path.read_text(encoding="utf-8")
                st.markdown(essay_content)

            # Compliance report
            st.header("Compliance Report")
            col1, col2 = st.columns(2)

            with col1:
                status_color = {
                    "pass": "🟢",
                    "warn": "🟡",
                    "block": "🔴",
                }
                status_emoji = status_color.get(report.status, "⚪")
                st.metric("Status", f"{status_emoji} {report.status.upper()}")

            with col2:
                st.metric("Issues Found", len(report.reasons))

            # Show reasons
            if report.reasons:
                st.subheader("Issues")
                for reason in report.reasons:
                    severity_color = {
                        "error": "🔴",
                        "warn": "🟡",
                        "info": "🔵",
                    }
                    emoji = severity_color.get(reason.severity, "⚪")
                    st.write(f"{emoji} **{reason.code}** ({reason.severity})")
                    st.write(f"   {reason.message}")
                    if reason.evidence:
                        st.code(reason.evidence, language=None)

            # Show checks
            st.subheader("Check Results")
            check_data = {
                "Check": list(report.checks.keys()),
                "Passed": [check.passed for check in report.checks.values()],
            }
            st.dataframe(check_data, use_container_width=True)

            # Show full report JSON
            with st.expander("View Full Compliance Report JSON"):
                st.json(report.model_dump())

            # Show actions taken
            if report.actions_taken:
                st.subheader("Actions Taken")
                for action in report.actions_taken:
                    st.write(f"- {action}")

            # Download links
            st.header("Download Artifacts")
            st.info(f"Artifacts saved to: `{output_dir}`")

            if st.button("Download Essay (Markdown)"):
                st.download_button(
                    label="Download",
                    data=essay_content,
                    file_name="essay.md",
                    mime="text/markdown",
                )

            if st.button("Download Compliance Report (JSON)"):
                st.download_button(
                    label="Download",
                    data=json.dumps(report.model_dump(), indent=2),
                    file_name="compliance_report.json",
                    mime="application/json",
                )

        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON: {e}")
        except ValidationError as e:
            st.error(f"Invalid spec: {e}")
        except Exception as e:
            st.exception(f"Error: {e}")


if __name__ == "__main__":
    main()

