import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.use_cases.statement_organizer import StatementOrganizerService

def main():
    st.set_page_config(page_title="Organizador Financeiro", layout="wide")
    
    st.title("📊 Organizador de Extrato Financeiro & Analytics")
    st.write("Faça o upload de um extrato bancário (CSV). O sistema fará uma corrida de performance entre o algoritmo nativo do Python e o nosso motor O(n), seguido de análises visuais.")
    
    uploaded_file = st.file_uploader("Faça o upload do arquivo transactions.csv", type="csv")
    
    if uploaded_file is not None:
        service = StatementOrganizerService()
        buckets, benchmark = service.process_csv_file(uploaded_file)
        
        st.divider()
        st.subheader(" Benchmark de Performance: O(n log n) vs O(n)")
        
        native_str = f"{benchmark['native_ms']:.3f} ms"
        radix_str = f"{benchmark['radix_ms']:.3f} ms"
        
        if benchmark['radix_ms'] < benchmark['native_ms'] and benchmark['radix_ms'] > 0:
            speedup = benchmark['native_ms'] / benchmark['radix_ms']
            delta_str = f"{speedup:.1f}x mais rápido!"
        else:
            delta_str = "Empate técnico (dados insuficientes)"
            
        b_col1, b_col2, b_col3 = st.columns(3)
        b_col1.metric("Timsort Nativo do Python", native_str)
        b_col2.metric("Radix Sort Personalizado", radix_str, delta_str)
        
        df_bench = pd.DataFrame({
            "Algoritmo": ["Timsort (Nativo)", "Radix Sort"],
            "Tempo de Execução (ms)": [benchmark["native_ms"], benchmark["radix_ms"]]
        })
        fig_bench = px.bar(df_bench, x="Algoritmo", y="Tempo de Execução (ms)", 
                           color="Algoritmo", text_auto='.2f', 
                           title="Comparação de Velocidade (Menos é Melhor)")
        b_col3.plotly_chart(fig_bench, use_container_width=True)


        st.divider()
        st.subheader(" Dashboard Analítico Financeiro")
        
        total_micro = sum(tx.amount for tx in buckets["Micro"])
        total_medium = sum(tx.amount for tx in buckets["Medium"])
        total_high = sum(tx.amount for tx in buckets["High"])
        
        d_col1, d_col2 = st.columns(2)
        
        # Gráfico de Pizza: Proporção de Gasto
        df_pizza = pd.DataFrame({
            "Categoria": ["Micro (até R$ 50)", "Médio (R$ 51 a R$ 200)", "Alto (> R$ 200)"],
            "Total Gasto": [total_micro, total_medium, total_high]
        })
        fig_pie = px.pie(df_pizza, values="Total Gasto", names="Categoria", 
                         title="Distribuição de Gastos por Categoria (Bucket Sort)",
                         hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
        d_col1.plotly_chart(fig_pie, use_container_width=True)
        
        d_col2.markdown("### Resumo Consolidado")
        d_col2.dataframe(df_pizza.style.format({"Total Gasto": "R$ {:.2f}"}), use_container_width=True, hide_index=True)


        # --- 📑 SEÇÃO 3: AS TABELAS DOS BALDES ---
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