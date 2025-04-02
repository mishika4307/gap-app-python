import streamlit as st
import pandas as pd

def calculate_rrp_inc_gst(cost, company):
    if company == "GAP & SOS":
        if cost < 100:
            return round(cost * 1.735, 2)
        elif 101 <= cost <= 149:
            return round(cost * 1.6, 2)
        else:
            return round(cost * 1.5, 2)
    else:
        if cost < 100:
            return round(cost * 1.65, 2)
        elif 101 <= cost <= 149:
            return round(cost * 1.6, 2)
        else:
            return round(cost * 1.5, 2)

def calculate_rrp_ex_gst(rrp_inc_gst):
    return round(rrp_inc_gst / 1.1, 2)

def calculate_trade_ex(cost, company):
    return round(cost * 1.22, 2) if cost < 100 else round(cost * 1.2, 2)

def calculate_club_ex(cost, company):
    return round(cost * 1.2, 2) if cost < 100 else round(cost * 1.18, 2)

def calculate_distributor(cost):
    return round(cost * 1.05, 2)

def calculate_wholesale_ex_gst(cost):
    return round(cost * 1.12, 2)

def process_file(uploaded_file, company):
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()  # Remove extra spaces from column names
    
    if 'Cost' not in df.columns:
        st.error("Error: Column 'Cost' not found in uploaded file.")
        return None
    
    df['RRP Inc GST'] = df['Cost'].apply(lambda x: calculate_rrp_inc_gst(x, company))
    df['RRP Ex GST'] = df['RRP Inc GST'].apply(calculate_rrp_ex_gst)
    df['Trade Ex'] = df['Cost'].apply(lambda x: calculate_trade_ex(x, company))
    df['Club Ex'] = df['Cost'].apply(lambda x: calculate_club_ex(x, company))
    df['Distributor'] = df['Cost'].apply(calculate_distributor)
    
    if company == "GAP & SOS":
        df['Wholesale Ex GST'] = df['Cost'].apply(calculate_wholesale_ex_gst)
    
    return df

def main():
    st.title("Fisher & Paykel Pricing Calculator for GAP Cin7 & ASW Portal")
    
    company = st.radio("Select Company:", ["GAP & SOS", "ASW"])
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    
    if uploaded_file:
        df_result = process_file(uploaded_file, company)
        if df_result is not None:
            st.write("### Processed Data:")
            st.dataframe(df_result)
            
            output_file = "processed_pricing.xlsx"
            df_result.to_excel(output_file, index=False)
            
            with open(output_file, "rb") as file:
                st.download_button(
                    label="Download Processed Pricing File",
                    data=file,
                    file_name=output_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
if __name__ == "__main__":
    main()
