# Organizador de Extratos Financeiros 

Uma aplicação web desenvolvida em Python e Streamlit projetada para organizar e categorizar grandes volumes de transações financeiras (extratos bancários em CSV) utilizando algoritmos de ordenação não-comparativos.

O grande diferencial deste projeto é a otimização da complexidade de tempo: substituindo os motores de ordenação tradicionais nativos do Python ($O(n \log n)$) por uma combinação arquitetural de **Radix Sort** e **Bucket Sort**, atingindo um tempo de execução estritamente linear de **$O(n)$**.

## Dados Acadêmicos

* **Aluna:** Dara Maria Barbosa de Sousa
* **Matrícula:** 202046040


---

## 1. O Problema: O Gargalo da Ordenação Tradicional

No setor financeiro (bancos, adquirentes e fintechs), o processo de reconciliação de pagamentos exige o cruzamento de milhões de transações diárias. Antes de cruzar os dados, os extratos precisam ser perfeitamente ordenados cronologicamente e separados por faixas de valores.

A maioria dos sistemas utiliza algoritmos de ordenação baseados em comparação, como o Quick Sort, Merge Sort ou o Timsort (padrão em Python e Java). O limite matemático absoluto desses algoritmos no caso médio e pior caso é **$O(n \log n)$**. À medida que o volume de dados escala para milhões de linhas, o custo computacional de CPU se torna um gargalo insustentável para operações em tempo real.

## 2. A Solução: Abordagem Não-Comparativa

Como os dados financeiros possuem características anatômicas estritas (datas seguem um calendário previsível e moedas possuem casas decimais fixas), não precisamos comparar os elementos uns contra os outros.

Este software resolve o gargalo de performance processando os dados através de algoritmos de distribuição. A solução é orquestrada em duas fases sequenciais e complementares, reduzindo a complexidade de tempo do motor de ordenação para **$O(n)$**.

---

## 3. Escolha e Aplicação dos Algoritmos

### Fase 1: Ordenação Cronológica com Radix Sort

O arquivo bruto de transações possui as datas misturadas. O primeiro passo é ordená-las da transação mais antiga para a mais recente.

* **Como foi aplicado:** As datas no formato `YYYY-MM-DD` foram convertidas para números inteiros (ex: `2025-01-15` torna-se `20250115`). O Radix Sort avalia esses inteiros dígito a dígito (da direita para a esquerda - método LSD).
* **Motor Interno:** Para ordenar cada dígito (de 0 a 9), foi implementado o **Counting Sort**.
* **Estabilidade Obrigatória:** A estabilidade temporal é mantida rigorosamente. Se uma transação do "Uber" apareceu antes de uma do "iFood" no mesmo dia no arquivo original, ela continuará antes na saída.
* **Complexidade de Tempo:** $O(d \cdot n)$, onde $d$ é a quantidade de dígitos (no nosso caso, uma constante exata de 8 dígitos para a data). Como $d$ é constante, a complexidade simplifica-se para **$O(n)$**.
* **Complexidade de Espaço:** $O(n + k)$, onde $k$ é a base numérica (10), exigindo memória auxiliar para não mutar a lista original.

### Fase 2: Categorização de Valores com Bucket Sort

Com a lista agora perfeitamente ordenada por datas, o usuário precisa visualizar seus gastos separados por perfil financeiro.

* **Como foi aplicado:** As transações são injetadas em uma função de *Scatter-Gather*, onde são direcionadas a 3 "baldes" (Buckets) distintos com base no valor nominal (`amount`):
1. **Micro:** $0.00 a $50.00
2. **Medium:** $50.01 a $200.00
3. **High:** Acima de $200.00


* **A Magia da Orquestração:** Em um Bucket Sort clássico, os elementos caem desordenados no balde, exigindo um *Insertion Sort* ($O(n^2)$ no pior caso) interno. No entanto, como injetamos a lista **já pré-ordenada cronologicamente pelo Radix Sort**, a inserção sequencial nas listas de cada balde elimina a necessidade de ordenação interna. O custo do Bucket Sort cai para uma única iteração de leitura.
* **Complexidade de Tempo:** **$O(n)$** para distribuição.

---

## 4. Arquitetura do Projeto 

O projeto foi construído separando fortemente as regras de negócio da interface web, seguindo princípios arquiteturais limpos:

* `/src/domain/`: Contém a entidade `Transaction` puramente em Python.
* `/src/use_cases/`: Contém a lógica pesada (Os algoritmos puros `radix_sort.py` e `bucket_sort.py`, além do orquestrador).
* `/src/ui/`: Contém a camada de apresentação web (Streamlit).
* `/src/utils/`: Ferramentas auxiliares, como o gerador automático de massa de dados fictícios.
* `/tests/`: Testes unitários orientados a comportamento (TDD) para validar a eficácia matemática dos algoritmos.

---

## 5. Como Executar a Aplicação Localmente

Siga o passo a passo abaixo para rodar a aplicação no seu ambiente Windows.

### Pré-requisitos

* **Python 3.10+** instalado no sistema.
* Terminal de Comando (PowerShell, CMD ou Git Bash).

### Passo 1: Configuração do Ambiente Virtual

Clone o repositório, abra o terminal na pasta raiz e instale as dependências isoladas:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

```

### Passo 2: Gerar os Dados Fictícios

O repositório não sobe arquivos CSV para economizar banda. Para gerar um arquivo de 1.000 transações embaralhadas para testar a aplicação, rode:

```powershell
python src\utils\mock_generator.py

```

*(Isso criará o arquivo `transactions.csv` dentro da pasta `data/`).*

### Passo 3: Iniciar a Interface Gráfica

Para rodar a aplicação web interativa:

```powershell
streamlit run src\ui\app.py

```

Seu navegador abrirá automaticamente a interface (geralmente na porta `http://localhost:8501`). Arraste o arquivo `data/transactions.csv` recém-gerado para o campo de upload para ver o Radix Sort e Bucket Sort operando em conjunto instantaneamente.

---

## 6. Como Executar os Testes Unitários

O projeto utiliza o **Pytest** para atestar a estabilidade e integridade dos algoritmos baseados em TDD. Para validar se os métodos não sofreram regressão de código, no terminal com o `venv` ativado, basta executar:

```powershell
pytest -v

```

Você deverá ver todos os casos de teste relatados em verde indicando sucesso (`PASSED`).
