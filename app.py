
import streamlit as st
import pandas as pd
from collections import Counter
import base64

# Custom CSS for background and styling
def set_background():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(to right, #e0f7fa, #ffffff);
            color: #333333;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .stButton > button {{
            background-color: #00796b;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
        }}
        .css-1d391kg {{
            background-color: #ffffff88 !important;
            border-radius: 10px;
            padding: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply background styling
set_background()

# Title and description
st.title("🧬 Codon Usage Table Generator")
st.markdown("""
Upload your DNA sequences and get a professional, publication-ready codon usage table showing codon counts and relative frequencies (%).

**Supported formats:** Plain DNA sequence or FASTA file.
""")

# Function to parse FASTA or plain text
def parse_sequences(input_text):
    sequences = []
    current_seq = ""
    for line in input_text.strip().splitlines():
        line = line.strip()
        if line.startswith(">"):
            if current_seq:
                sequences.append(current_seq)
                current_seq = ""
        else:
            current_seq += line
    if current_seq:
        sequences.append(current_seq)
    return sequences

# Function to get codon list
def get_codons(sequence):
    sequence = sequence.upper().replace("\n", "").replace(" ", "")
    codons = [sequence[i:i+3] for i in range(0, len(sequence), 3) if len(sequence[i:i+3]) == 3]
    return codons

# Codon Usage Calculator
def calculate_codon_usage(sequences):
    codon_counter = Counter()
    total_codons = 0
    for seq in sequences:
        codons = get_codons(seq)
        codon_counter.update(codons)
        total_codons += len(codons)
    
    data = []
    for codon in sorted(codon_counter.keys()):
        count = codon_counter[codon]
        frequency = (count / total_codons) * 100 if total_codons else 0
        data.append({"Codon": codon, "Count": count, "Frequency (%)": round(frequency, 2)})
    
    df = pd.DataFrame(data)
    return df

# File upload
uploaded_file = st.file_uploader("📂 Upload a DNA Sequence File (.txt or .fasta)", type=["txt", "fasta"])

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    sequences = parse_sequences(content)
    
    if sequences:
        st.success(f"✅ {len(sequences)} sequence(s) detected. Calculating Codon Usage...")

        result_df = calculate_codon_usage(sequences)
        st.dataframe(result_df, use_container_width=True)

        # CSV Download option
        csv = result_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="codon_usage.csv">📥 Download Codon Usage Table as CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.error("❌ No valid DNA sequences found. Please check your input file.")

st.markdown("""
---

**Created by piyush panchal, FYBI, MGM's College of CS & IT, Nanded**
""")
