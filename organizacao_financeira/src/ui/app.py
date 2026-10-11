import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.use_cases.statement_organizer import StatementOrganizerService

def main():
    st.set_page_config(page_title="Organizador Financeiro", layout="wide")
    
    st.title("📊 Organizador de Extrato Financeiro")
    st.write("Faça o upload de um extrato bancário bruto (CSV) para ordenar e categorizar automaticamente as transações em complexidade de tempo O(n) usando Radix e Bucket Sort.")
    
    # 1. Componente de Upload
    uploaded_file = st.file_uploader("Faça o upload do arquivo transactions.csv", type="csv")
    
    if uploaded_file is not None:
        st.success("Arquivo carregado com sucesso! Processando ...")
        
        service = StatementOrganizerService()
        buckets = service.process_csv_file(uploaded_file)
        
        st.divider()
        st.subheader("Transações Categorizadas e Ordenadas Cronologicamente")
        
        col1, col2, col3 = st.columns(3)
        
        def to_dataframe(tx_list):
            return pd.DataFrame([{
                "Data": tx.date.strftime("%d/%m/%Y"), 
                "Descrição": tx.description,
                "Valor (R$)": f"{tx.amount:.2f}".replace(".", ",") 
            } for tx in tx_list])
            
        with col1:
            st.markdown(r"### 🥉 Micro (R\$ 0 - R\$ 50)")
            st.metric("Total de Transações", len(buckets["Micro"]))
            if buckets["Micro"]:
                st.dataframe(to_dataframe(buckets["Micro"]), use_container_width=True, hide_index=True)
                
        with col2:
            st.markdown(r"### 🥈 Médio (R\$ 51 - R\$ 200)")
            st.metric("Total de Transações", len(buckets["Medium"]))
            if buckets["Medium"]:
                st.dataframe(to_dataframe(buckets["Medium"]), use_container_width=True, hide_index=True)
                
        with col3:
            st.markdown(r"### 🥇 Alto (> R\$ 200)")
            st.metric("Total de Transações", len(buckets["High"]))
            if buckets["High"]:
                st.dataframe(to_dataframe(buckets["High"]), use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()