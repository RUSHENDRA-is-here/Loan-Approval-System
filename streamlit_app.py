"""
Streamlit UI for Loan Approval System
"""

import streamlit as st
from src.models import LoanApplication, EmploymentType
from src.orchestration import LoanOrchestrator
from datetime import datetime

st.set_page_config(
    page_title="Loan Approval System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏦 AI-Powered Loan Approval System")
st.markdown(
    "Multi-Agent system using Claude Sonnet for intelligent loan decisions"
)

# Initialize orchestrator
@st.cache_resource
def get_orchestrator():
    return LoanOrchestrator()

orchestrator = get_orchestrator()

# Application state storage
if "applications" not in st.session_state:
    st.session_state.applications = {}

# Sidebar for navigation
page = st.sidebar.radio(
    "Navigation",
    ["Submit Application", "View Decisions", "Demo Scenarios"],
)

# Page 1: Submit Application
if page == "Submit Application":
    st.header("Submit Loan Application")

    col1, col2 = st.columns(2)

    with col1:
        applicant_id = st.text_input(
            "Applicant ID",
            value=f"APP{datetime.now().strftime('%Y%m%d%H%M%S')[-6:]}",
        )
        age = st.number_input("Age", min_value=18, max_value=100, value=35)
        income = st.number_input(
            "Annual Income ($)", min_value=10000, max_value=500000, value=80000
        )
        employment_type = st.selectbox(
            "Employment Type",
            [EmploymentType.EMPLOYED, EmploymentType.SELF_EMPLOYED,
             EmploymentType.RETIRED, EmploymentType.UNEMPLOYED],
        )

    with col2:
        credit_score = st.number_input(
            "Credit Score", min_value=300, max_value=850, value=720
        )
        loan_amount = st.number_input(
            "Loan Amount ($)", min_value=10000, max_value=1000000, value=250000
        )
        tenure_months = st.number_input(
            "Loan Tenure (months)", min_value=12, max_value=360, value=60
        )
        employment_years = st.number_input(
            "Years of Employment", min_value=0.0, max_value=50.0, value=5.5
        )

    col3, col4 = st.columns(2)

    with col3:
        existing_liabilities = st.number_input(
            "Existing Liabilities ($)", min_value=0, max_value=500000, value=30000
        )
        location = st.text_input("Location", value="New York")

    # Submit button
    if st.button("🚀 Submit Application", type="primary", use_container_width=True):
        with st.spinner("Processing application..."):
            try:
                # Create application
                application = LoanApplication(
                    applicant_id=applicant_id,
                    age=age,
                    income=income,
                    employment_type=employment_type,
                    credit_score=credit_score,
                    loan_amount=loan_amount,
                    tenure_months=tenure_months,
                    existing_liabilities=existing_liabilities,
                    location=location,
                    employment_years=employment_years,
                )

                # Process through orchestrator
                decision = orchestrator.process_application(application)

                # Store in session
                st.session_state.applications[applicant_id] = decision

                # Display results
                st.success("Application processed successfully!")

                # Decision card
                col_decision, col_score, col_confidence = st.columns(3)

                with col_decision:
                    if decision.classification.value == "APPROVED":
                        st.success(f"**Decision: {decision.classification.value}** ✅")
                    elif decision.classification.value == "REJECTED":
                        st.error(f"**Decision: {decision.classification.value}** ❌")
                    else:
                        st.warning(f"**Decision: {decision.classification.value}** ⚠️")

                with col_score:
                    st.metric("Risk Score", f"{decision.risk_score}/100")

                with col_confidence:
                    st.metric("Confidence", f"{decision.confidence:.1%}")

                # Reasoning
                st.info(f"**Reasoning:** {decision.reasoning}")

                # Key factors
                st.subheader("Key Decision Factors")
                if decision.factors:
                    for factor in decision.factors:
                        st.write(f"• {factor}")

                # Case ID
                st.caption(f"Case ID: {decision.case_id}")

            except Exception as e:
                st.error(f"Error processing application: {str(e)}")

# Page 2: View Decisions
elif page == "View Decisions":
    st.header("Application Decisions History")

    if st.session_state.applications:
        for app_id, decision in st.session_state.applications.items():
            with st.expander(f"{app_id} - {decision.classification.value}"):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Decision", decision.classification.value)
                with col2:
                    st.metric("Risk Score", decision.risk_score)
                with col3:
                    st.metric("Confidence", f"{decision.confidence:.1%}")

                st.write(f"**Reasoning:** {decision.reasoning}")

                if decision.factors:
                    st.write("**Factors:**")
                    for factor in decision.factors:
                        st.write(f"• {factor}")

                st.caption(f"Case ID: {decision.case_id}")
    else:
        st.info("No applications processed yet. Submit one to see results.")

# Page 3: Demo Scenarios
elif page == "Demo Scenarios":
    st.header("Demo Scenarios")

    scenarios = {
        "Excellent Applicant (APPROVED)": {
            "age": 45,
            "income": 150000,
            "employment_type": EmploymentType.EMPLOYED,
            "credit_score": 800,
            "loan_amount": 100000,
            "tenure_months": 60,
            "existing_liabilities": 10000,
            "location": "San Francisco",
            "employment_years": 10.0,
        },
        "Good Applicant (APPROVED)": {
            "age": 40,
            "income": 80000,
            "employment_type": EmploymentType.EMPLOYED,
            "credit_score": 720,
            "loan_amount": 100000,
            "tenure_months": 72,
            "existing_liabilities": 15000,
            "location": "New York",
            "employment_years": 5.0,
        },
        "Marginal Applicant (MANUAL_REVIEW)": {
            "age": 35,
            "income": 60000,
            "employment_type": EmploymentType.EMPLOYED,
            "credit_score": 680,
            "loan_amount": 50000,
            "tenure_months": 60,
            "existing_liabilities": 15000,
            "location": "Austin",
            "employment_years": 3.0,
        },
        "Poor Applicant (REJECTED)": {
            "age": 24,
            "income": 28000,
            "employment_type": EmploymentType.SELF_EMPLOYED,
            "credit_score": 580,
            "loan_amount": 150000,
            "tenure_months": 120,
            "existing_liabilities": 40000,
            "location": "Chicago",
            "employment_years": 0.5,
        },
    }

    selected_scenario = st.selectbox("Choose a scenario", list(scenarios.keys()))

    if st.button("Run Demo Scenario", type="primary", use_container_width=True):
        with st.spinner("Processing demo application..."):
            try:
                scenario_data = scenarios[selected_scenario]
                app_id = f"DEMO_{selected_scenario.replace(' ', '_')}"

                application = LoanApplication(
                    applicant_id=app_id,
                    **scenario_data,
                )

                decision = orchestrator.process_application(application)
                st.session_state.applications[app_id] = decision

                # Display results
                st.success("Demo completed!")

                col_decision, col_score, col_confidence = st.columns(3)

                with col_decision:
                    if decision.classification.value == "APPROVED":
                        st.success(f"**Decision: {decision.classification.value}** ✅")
                    elif decision.classification.value == "REJECTED":
                        st.error(f"**Decision: {decision.classification.value}** ❌")
                    else:
                        st.warning(f"**Decision: {decision.classification.value}** ⚠️")

                with col_score:
                    st.metric("Risk Score", f"{decision.risk_score}/100")

                with col_confidence:
                    st.metric("Confidence", f"{decision.confidence:.1%}")

                st.info(f"**Reasoning:** {decision.reasoning}")

                st.subheader("Key Factors")
                if decision.factors:
                    for factor in decision.factors:
                        st.write(f"• {factor}")

            except Exception as e:
                st.error(f"Error running demo: {str(e)}")

# Footer
st.divider()
st.markdown(
    """
    ---
    **Loan Approval System** | Multi-Agent Agentic AI | Powered by Claude Sonnet 4.6
    """
)
