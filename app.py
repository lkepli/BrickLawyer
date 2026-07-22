import os
import requests
import streamlit as st


st.set_page_config(
    page_title="BrickLawyer",
    page_icon="⚖️",
    layout="centered",
)

st.title("⚖️ BrickLawyer")
st.subheader("Legal clause classification app")

default_api_url = os.getenv(
    "API_URL",
    "https://bricklawyer-api-499333618614.europe-west1.run.app"
)

with st.sidebar:
    st.header("Settings")
    api_url = st.text_input(
        "API URL",
        value=default_api_url,
        help="Use the local or deployed backend URL.",
    )

clause_text = st.text_area(
    "Paste a contract clause",
    height=220,
    placeholder="Enter a legal contract clause here...",
)

if st.button("Classify clause", type="primary", use_container_width=True):
    if not clause_text.strip():
        st.warning("Please enter a contract clause before classifying.")
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
                    st.warning(
                        "Low confidence prediction. Please review carefully."
                    )
                else:
                    st.info(f"Status: {status}")

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
