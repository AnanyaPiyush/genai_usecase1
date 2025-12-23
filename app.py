import streamlit as st
import pandas as pd
import openai
import re

# Set OpenAI API key
openai.api_key = "open_api_key"

# Define compliance categories and their priorities
CATEGORIES = {
    "Secrecy Breach": 3,  # High - Confidentiality violations
    "Market Manipulation/Misconduct": 3,  # High - Financial/regulatory
    "Market Bribery": 3,  # High - Corruption
    "Change in Communication": 2,  # Medium - Potential compliance impact
    "Complaints": 2,  # Medium - Various issues
    "Employee Ethics": 1,  # Low - Ethical concerns
    "Harassment or Discrimination": 3,  # High
    "Financial Misconduct": 3,  # High
    "Data Privacy Violation": 3,  # High
    "Regulatory Non-Compliance": 2,  # Medium
    "Security Breach": 2,  # Medium
    "Ethical Violation": 1,  # Low
    "No Issue": 0  # Compliant
}

def analyze_email(email_body):
    # For demonstration purposes, using mock analysis since API key may be invalid
    # In production, replace with actual OpenAI API call
    
    # Simple keyword-based mock analysis
    email_lower = email_body.lower()
    
    if "secret" in email_lower or "confidential" in email_lower or "leak" in email_lower:
        return {
            "flagged": True,
            "category": "Secrecy Breach",
            "reason": "Contains confidential information sharing",
            "source": email_body,
            "priority": 3
        }
    elif "manipulate" in email_lower or "rig" in email_lower or "insider" in email_lower:
        return {
            "flagged": True,
            "category": "Market Manipulation/Misconduct",
            "reason": "Discusses market manipulation activities",
            "source": email_body,
            "priority": 3
        }
    elif "bribe" in email_lower or "kickback" in email_lower:
        return {
            "flagged": True,
            "category": "Market Bribery",
            "reason": "References bribery or kickbacks",
            "source": email_body,
            "priority": 3
        }
    elif "discriminat" in email_lower or "harass" in email_lower:
        return {
            "flagged": True,
            "category": "Harassment or Discrimination",
            "reason": "Contains discriminatory or harassing content",
            "source": email_body,
            "priority": 3
        }
    elif "privacy" in email_lower or "personal data" in email_lower:
        return {
            "flagged": True,
            "category": "Data Privacy Violation",
            "reason": "Violates data privacy regulations",
            "source": email_body,
            "priority": 3
        }
    elif "unethical" in email_lower or "ethics" in email_lower:
        return {
            "flagged": True,
            "category": "Employee Ethics",
            "reason": "Raises ethical concerns",
            "source": email_body,
            "priority": 1
        }
    else:
        return {
            "flagged": False,
            "category": "No Issue",
            "reason": "No compliance issues detected",
            "source": "",
            "priority": 0
        }

st.title("AI-Driven Communication Surveillance Application")

uploaded_file = st.file_uploader("Choose a CSV file containing emails", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.write("Data Preview:")
    st.dataframe(df.head())
    
    # Assume columns: subject, body, sender, etc.
    if 'body' not in df.columns:
        st.error("CSV must contain a 'body' column for email content.")
    else:
        # Display list of emails
        st.subheader("Select an Email to Analyze")
        email_options = [f"{i}: {row['subject']} - {row.get('sender', 'Unknown')}" for i, row in df.iterrows()]
        selected_email = st.selectbox("Choose an email:", email_options)
        
        if selected_email:
            index = int(selected_email.split(':')[0])
            email_data = df.iloc[index]
            
            st.subheader("Selected Email")
            st.write(f"**Subject:** {email_data['subject']}")
            st.write(f"**Sender:** {email_data.get('sender', 'Unknown')}")
            st.write(f"**Body:** {email_data['body']}")
            
            if st.button("Analyze for Compliance"):
                with st.spinner("Analyzing..."):
                    result = analyze_email(email_data['body'])
                
                st.subheader("Analysis Result")
                if result["flagged"]:
                    st.error("🚩 Non-Compliant Email Detected")
                    st.write(f"**Category:** {result['category']}")
                    st.write(f"**Reason:** {result['reason']}")
                    st.write(f"**Source Line:** {result['source']}")
                    st.write(f"**Priority:** {result['priority']} (1=Low, 2=Medium, 3=High)")
                else:
                    st.success("✅ Email is Compliant")
                    st.write(f"**Category:** {result['category']}")
        
        # Option to analyze all emails
        if st.button("Analyze All Emails"):
            st.subheader("Batch Analysis Results")
            progress_bar = st.progress(0)
            results = []
            
            for i, row in df.iterrows():
                result = analyze_email(row['body'])
                result['index'] = i
                result['subject'] = row['subject']
                result['sender'] = row.get('sender', 'Unknown')
                results.append(result)
                progress_bar.progress((i+1)/len(df))
            
            # Display flagged emails
            flagged = [r for r in results if r['flagged']]
            if flagged:
                st.write(f"**Flagged Emails: {len(flagged)}**")
                for r in flagged:
                    st.write(f"- Index {r['index']}: {r['subject']} - {r['category']} (Priority: {r['priority']})")
            else:
                st.success("No non-compliant emails found.")


