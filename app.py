import os
from pathlib import Path

import requests
import streamlit as st


LOGO_PATH = Path(__file__).resolve().parent / "assets" / "brick_logo.svg"

st.set_page_config(
    page_title="BrickLawyer",
    page_icon=str(LOGO_PATH),
    layout="centered",
)

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    .bl-eyebrow {
        font-family: ui-monospace, monospace;
        font-size: 0.85rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #8a8478;
        margin-top: -0.5rem;
        margin-bottom: 1rem;
    }
    div.stButton > button {
        border-radius: 14px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:0.25rem;">
        <div style="display:grid; grid-template-columns:1fr 1fr; grid-template-rows:1fr 1fr; gap:4px; width:32px; height:32px; background:#d81f26; border-radius:8px; padding:5px;">
            <span style="background:#fff; border-radius:50%;"></span>
            <span style="background:#fff; border-radius:50%;"></span>
            <span style="background:#fff; border-radius:50%;"></span>
            <span style="background:#fff; border-radius:50%;"></span>
        </div>
        <span style="font-size:2.25rem; font-weight:800; line-height:1;">BrickLawyer</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="bl-eyebrow">Legal clause classification app</div>', unsafe_allow_html=True)

api_url = os.getenv(
    "API_URL",
    "https://bricklawyer-api-499333618614.europe-west1.run.app"
)

clause_text = st.text_area(
    "Paste a contract clause",
    height=220,
    placeholder="Enter a legal contract clause here...",
)

if st.button("Classify clause", type="primary", use_container_width=True):
    stripped_clause = clause_text.strip()

    if not stripped_clause:
        st.markdown(
            '<p style="color:#d81f26; font-weight:700;">'
            "Please enter a legal text before classifying.</p>",
            unsafe_allow_html=True,
        )
    elif len(stripped_clause) < 20 or len(stripped_clause.split()) < 3:
        st.markdown(
            '<p style="color:#d81f26; font-weight:700;">'
            "Please enter a real/valid legal text before classifying.</p>",
            unsafe_allow_html=True,
        )
    else:
        try:
            with st.spinner("Classifying clause..."):
                response = requests.post(
                    f"{api_url.rstrip('/')}/predict",
                    json={"text": clause_text.strip()},
                    timeout=15,
                )

            response.raise_for_status()
            result = response.json()

            required_fields = {"predicted_label", "probability", "status"}

            if not required_fields.issubset(result):
                st.error(
                    "The API response does not contain the expected fields."
                )
            else:
                predicted_label = result["predicted_label"]
                confidence = float(result["probability"])
                status = result["status"]

                st.divider()
                st.subheader("Prediction")

                st.success(f"Predicted label: **{predicted_label}**")
                st.metric("Confidence", f"{confidence:.0%}")

                if status == "low_confidence":
                    st.markdown(
                        """
                        <div style="display:inline-flex; align-items:center; gap:8px;
                            font-family:ui-monospace, monospace; font-size:0.95rem;
                            color:#a8402f; background:#fbe9e5; padding:8px 16px;
                            border-radius:100px; margin-top:0.5rem;">
                            <span style="width:8px; height:8px; border-radius:50%;
                                background:#a8402f; display:inline-block;"></span>
                            Low confidence prediction. Please review carefully.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                        <div style="display:inline-flex; align-items:center; gap:8px;
                            font-family:ui-monospace, monospace; font-size:0.95rem;
                            color:#2f7a45; background:#e4f3e8; padding:8px 16px;
                            border-radius:100px; margin-top:0.5rem;">
                            <span style="width:8px; height:8px; border-radius:50%;
                                background:#2f7a45; display:inline-block;"></span>
                            Status: {status}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        except requests.exceptions.ConnectionError:
            st.error(
                "The API could not be reached. Check that the backend is running "
                "and that the API URL is correct."
            )
        except requests.exceptions.Timeout:
            st.error("The API request timed out. Please try again.")
        except requests.exceptions.HTTPError as error:
            st.error(f"The API returned an error: {error}")
        except ValueError:
            st.error("The API returned an invalid response.")
        except requests.exceptions.RequestException as error:
            st.error(f"Something went wrong while contacting the API: {error}")
