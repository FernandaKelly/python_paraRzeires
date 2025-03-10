## Pandas

Antes de tudo precisamos falar sobre o banco de dados. Essa base de dados é advinda do pacote , mas vocẽ pode baixar essa base de dado em vários formatos aqui.






Ao importar a biblioteca *pandas* dessa forma, lembre-se que todas as suas funções serão carregadas. Caso você esteja usando o linux (é o meu caso), pode ser que você se depare com o seguinte erro:

```{markdown}
Error in py_call_impl(callable, call_args$unnamed, call_args$named) : 
  Evaluation error: ModuleNotFoundError: No module named 'pandas'
Run `reticulate::py_last_error()` for details..
Erros durante o embrulho: Evaluation error: ModuleNotFoundError: No module named 'pandas'
Run `reticulate::py_last_error()` for details..
Error: no more error handlers available (recursive errors?); invoking 'abort' restart
```

Para resolvê-lo, você deve ir ao terminal e seguir com o seguinte comando,


pip install pandas


Agora vamos importar a biblioteca de interesse.


#Importação da biblioteca
import pandas


*Se você não conseguiu instalar, volte no ponto de preparação.*

### Brincadeirinhas

Vamos ler uma base de dados através da biblioteca pandas, que diferente do R, todas as opções de leitura de dados se encontram nessa mesma biblioteca.

```{python}
df = pandas.read_csv("dados/imdb.csv")
type(df)
```

```{python}
df
```

Essa leitura de banco de dados é mais fácil que você vai ver (rs), mas é bem possível que você se depare com alguns erros de encoding, de separadores ou decimais. A função reade_csv do pandas possui parâmetros para especificar cada um desses problemas com o intuito de solucioná-los. Veja a documentação da função.

Como defaut o python joga 'fora" todos os NA's quando usamos essa função:

```{python}
df.describe()
```

Para saber o nome e tipo de classe das variáveis,

```{python}
df.info()
```
E assim conseguimos aplicar qualquer função de interesse na base de dados:

```{python}
df.sum()
df.receita.sum()
```

É importante dizer que há um **help** assim como há no RStudio.
Obs.: O python que me desculpe, mas esse help é bem ruim.

```{python}
help(pandas.read_csv)
```

### Principais verbos

Vamos fazer um/dois exemplos de cada um desses verbos.

####   Ordenar linhas

Para ordenar linhas podemos utilizar **sort_index()** ou **sort_values()**. 
 
```{python}
df2 = df.sort_values(['id_filme', 'ano'])
```

É muito falado que na linguagem python o índice se inicia no **0** e, por isso, ao solicitar a ordenação pelo índice a primeira linha será a 0. E , caso seja de interesse, podemos ordenar de forma decrescente, visto que o defautl é na ordem crescente. Para isso basta utilizar dentro da função *sort_index* o parâmetro *ascending = False*. 

```{python}
df3 = df.sort_index(ascending = False)
```

E você pode pensar, mas o **sort_values** também não faz isso? FAZ SIM"

```{python}
df4 = df.sort_values(['id_filme', 'ano'], ascending = False)
```

####   Selecionar linhas/colunas

É possível selecionar linhar e colunas das seguintes formas:

  - Utilizando colchetes:

Na minha opinião é ruim, visto que a gente precisa saber o nome da variável bem certinho. 

```{python}
df["ano"]
```

E como você pode ver, a variável ano está como **float64**, o que implica ter esse **.0** ao final. Vamos trocar isso rapidinho? Claro! Vamos selecionar a variável com o colchetes.

```{python}
df["ano"].fillna(0).astype(int)
```

Não quer tratar os NA's agora? Então vamos utilizar somente **astype('Int64')**.

```{python}
df["ano"].astype('Int64')
```

Mas, nesse momento nós estamos estudando o pandas, então vamos utilizar o pandar também para fazer essa transformação. Isso pode ser útil para reduzir o uso de memória ao escolher o tipo inteiro mais eficiente.

```{python}
pandas.to_numeric(df["ano"], downcast="integer")
```

Fer, que parâmetro é esse aí? **Downcast**?

Esse parâmetro economiza memória ao escolher automaticamente int8, int16 ou int32, em vez de um int64 desnecessário, o que ocorre quando usamos a função astype. Ele também evita valores inesperados ao converter corretamente os números sem arredondamentos. Mas, é importante ressaltar que: **Se quiser garantir que NaN sejam preservados, use df["ano"].astype('Int64'), pois pd.to_numeric() converte NaN para float64.**


  - Utilizando a função .loc
  
Esse método é estilo o que usamos no R. Veja que estamos usando o **:** como indexador das linhas.
  
```{python}
df.loc[:, ['ano']]
```
  
  - Utilizando a função .iloc

Essa função é A M-E-L-H-O-R para os Rzeires (na minha opinião), pois utilizamos as posições das variáveis. Veja só:

```{python}
df.iloc[:, 2]
```

A ideia é selecionar mais colunas? Podemos fazer por posição das variáveis do dataframe:

```{python}
df.iloc[:, 1:4]
```

E como selecionar as linhas? Acredito que agora tenha ficado mais fácil.

```{python}
df.iloc[1:10, 1:4]
```

Outra forma de selecionar colunas é em forma de atributo. Se vê muito em tutoriais essa forma de seleção de colunas.

```{python}
df.ano[1:10]
```

####   Criar colunas

Criar colunas do zeroeu acho um pouco mais dificil no dia a dia de uma analista/cientista de dados, a não ser que esteja criando KPI's, mas o que fazemos MUITO é criar variáveis a partir de variáveis já existente na base de dados.

Nessa etapa eu fui aprender com o [Programação Dinâmica](https://www.youtube.com/watch?v=S4hPzAKxClo).

Vamos lá?

Antes de tudo que aplicar algo que faça essas variáveis float se tornarem int, mas todas de uma vez só para não perder tempo. Eu achei incrível a forma que o python atua com essa necessidade e acabei aprendendo duas novas funçlões, a **select_dtypes**, **apply** e a partir dela o parâmetro **errors = "coerce"** que transforma a notação científica em um número normal. Essa transformação foi necessária devido a algumas variáveis estarem em notação cientifica.

Como tratativa de float -inf ou inf, vamos alterá-las por NA:

```{python}
df.replace([float("inf"), float("-inf")], pandas.NA, inplace=True) 
```

Uma das formas de encontrar as variáveis da classe float na base de dados é utilizando a função **select_dtypes**, sendo assim:

```{python}
 print(df.select_dtypes(include="float").columns)
 for col in df.select_dtypes(include="float").columns:
     print(f"\nColuna: {col}")
     print(df[col].unique())  # Verifica valores únicos
```

As variáveis flot são:

- ano
- orcamento
- receita
- receita_eua
- nota_imdb
- num_criticas_publico
- num_criticas_critica

Coloquei elas em um vetor para facilitar:

```{python}
colunas_float = ["ano", "orcamento", "receita", "receita_eua", "nota_imdb", "num_criticas_publico", "num_criticas_critica"]
```

Seguindo a transformação:

```{python}

df[df.select_dtypes(include="float").columns] = df.select_dtypes(include="float").apply(pandas.to_numeric, errors = "coerce").round(0).astype("Int64")

# OU PODEMOS TRABALHAR DA SENGUINTE FOR: #
#df[colunas_float] = df[colunas_float].apply(pandas.to_numeric, errors = "coerce").round(0).astype("Int64")

                                             
# UMA FORMA MAIS INTERESSANTE DE FAZER O MESMO CÓDIGO ACIMA COM A IDEIA DE ESCADA #
# df[df.select_dtypes(include="float").columns] = (
#   df.select_dtypes(include="float")
#   .apply(pandas.to_numeric, errors = "coerce")
#   .round(0)
#   .astype('Int64')
#   )

```

E você estar se perguntando: Fer, porquê você usou o **.astype** após aplicar o **pandas.to_mumeric** e o **.round** antes do **.astype**:?

Eu gosto de dizer que a programação orientada a objeto é uma escadinha e para ir subindo/descendo precisamos passar por etapas para não cair. A função **astype("Int64")** possui alguns requisitos para conseguir converter float ou o que desejar para inteiro, logo se houver:  

- Valores decimais reais (12.34, 56.78)
- Strings ocultas ("unknown", "N/A") misturadas na coluna
- Valores infinitos (inf, -inf) não removidos corretamente

Vai dar E-R-R-O, pois estes casos não conseguem ser convestido e, por isso, precisamos dessas tratativas. Já o pandas.to_numeric(errors="coerce") converte valores para número e transforma erros em NaN.

Observando a base de dados após a manipulação:

```{python}
df.dtypes
df.info()
```

E essa **data_lancamento**?

```{python}

type(df["data_lancamento"])

```

Veja que no describe essa variável se encontra como objetc e classe **pandas.core.series.Series**. Precisamos que ela seja considerada como date/data (Poxa! Se data no R já dava trabalho, espero que o python nos ajude de uma forma melhor em relação a isso.).

Com o pandas podemos utilizar a função bem intuitiva que é **to_datetime** para converter essa variável. Mas, veja que dá um errinho aí...

```{python}
#df['data_lancamento'] = pandas.to_datetime(df['data_lancamento'])
```


```{markdown}
Error in py_call_impl(callable, call_args$unnamed, call_args$named) : 
  Evaluation error: NameError: name 'pandas' is not defined
Run `reticulate::py_last_error()` for details..
Erros durante o embrulho: Evaluation error: NameError: name 'pandas' is not defined
Run `reticulate::py_last_error()` for details..
Error: no more error handlers available (recursive errors?); invoking 'abort' restart
```

Ele reclama do formato da nossa data que é "%Y-%m-%d" e nos dá que algumas observações que não estão nesse formato. E sim, nós temos casos em que temos **somente** o ano e não a data por inteiro.

O que vamos fazer?

Podemos resolver isso identificando e substituindo as linhas que contêm apenas o ano por NaN, visto que, no primeiro momento, é o que faz sentido. A brincadeira com datas sempre fica séria e vejo que aqui teremos que trabalhar com strings e regex para identificar esse padrão do ano (YYYY) e, como estamnos no python, procurei uma library para isso e me indicaram um de re.

- *A biblioteca re do Python é uma biblioteca padrão que permite trabalhar com expressões regulares. Com ela, é possível procurar padrões de texto, como todas as palavras que começam com "a" ou todas as frases que terminam com "!".* 


```{python}
import re
```

Sendo assim, vamos alterar aquelas observações com apenas 4 digitos para valores ausentes utilizando as blibliotecas **re** e **pandas**:

```{python}

data_lancamentoN2 = "data_lancamento"
mascara_anos = df[data_lancamentoN2].astype(str).str.match(r"^\d{4}$")

# Substituir os anos isolados por NaN
df.loc[mascara_anos, data_lancamentoN2] = pandas.NA

# Agora, converter para datetime e extrair apenas a data
df[data_lancamentoN2] = pandas.to_datetime(df[data_lancamentoN2], errors="coerce").dt.date

```

Obs.: usamos o parâmetro **errors="coerce"** em funções como pd.to_numeric() ou pd.to_datetime() pois estes substituem os valores inválidos por NaN (Not a Number) ou NaT (Not a Time), em vez de gerar um erro.

Será que deu certo?

```{python}
# Verificar o resultado
print(df[data_lancamentoN2].head())
```

Se fosse no R, provavelmente eu iria utilizar a função **case_when** ou o nosso querido **ifelse**, mas aqui no python temos outra opção: utilizar a função **where** da biblioteca numpy (vamos estudar ela no próximo post).

```{python}
import numpy
```

```{python}
data_lancamentoN3 = "data_lancamento"
df[data_lancamentoN3] = numpy.where(mascara_anos, pandas.NA, df[data_lancamentoN3])
df[data_lancamentoN3]  = data_lancamentoN3
print(df[data_lancamentoN3].head())
```

Acredito que já deu pra entender que a lógica de criação de variáveis é bem parecida com a do R e isso já é mais do que meio caminho andado no universo de ETL.

####   Sumarizar

Uma parte BEMMM importante é a sumarização dos nossos dados. 

Como assim Fê?

Tentar trazer medidas de posição já é um ótimo início, mas muitas vezes queremos agrupar a base de dados por alguma variável e assim somar algum valor, fazer a média para entender algum comportamento ou simplesmente contar o número de observações.

No R nós temos o dplyr e suas funções que são incríveis, no python... Já é um pouco diferente. Conhecendo a nossa base de dados, vamos selecionar algumas de interesse:

- genero
- ano
- duracao
- nota_imdb
- receita
- orcamento

Com essas variáveis vamos conseguir trabalhar algumas funções importantes.

```{python}
variaveis_summ = ["generos", "ano", "duracao", "nota_imdb", "receita", "orcamento"]
df_summ = df.filter(variaveis_summ)
df_summ.info()
```

A gente pode ver que a variável **duracao** está em minutos, mas nós queremos trabalhar com elas em hora e para isso precisamos aplicar alguma transformação. No R, usaríamos o mutate, mas aqui vamos usar  a função **assing**.

- *A função .assign() do Pandas é usada para adicionar novas colunas ao DataFrame de forma funcional, ou seja, sem modificar o DataFrame original, a menos que você o reatribua.*

Utilizando essa função:

```{python}

df.assign(
  duracao_h = df.duracao/60
).filter(["duracao_h"])

#df["duracao_h"]

```


Eu simplesmente A-D-O-R-E-I essa função (rzeire nenhum vai dizer o contrário rs).

Mas vamos lá... A primeira pergunta que eu tenho é: Quantos gêneros nós temos?

```{python}
df["generos"].unique()
```

Parece ser um tantinho bom, mas quantos filmes temos em cada um deles?

```{python}
df["generos"].value_counts()
print(df["generos"].value_counts().head(30))
```

É, já vimos que há muitos gêneros que aparecem apenas uma vez. Vamos ver quantos eles são?

```{python}
df["generos"].value_counts()[df["generos"].value_counts() == 1]
```

Poxa! De 874 gêneros, 288 aparecem somente uma vez, indicando que 33% dos filmes são gêneros pouco produzidos. E aí vem o questionamento: Será que estes gêneros lucram? A parte ruim é que temos muitos valores ausentes, totalizando 73% da amostra com NA, mas para "brincar" vamos continuar com essa ideia.

```{python}
df["receita"].isna().sum()
```

Neste caso, usaríamos a função **mutate** e **case_when** para criar a variável lucro e depois uma dummy com o indicativo de lucro ou não. No python nós seguimos com a função **assign**.

```{python}

df = df.assign(
    lucro = lambda x: x["receita"] - x["orcamento"])
#Tratativa para os valores faltantes para que possamos seguir com a ideia de aprendizagem.
df["lucro"] = df["lucro"].fillna(0).astype(int)

df = df.assign(    
    lucro_cat = lambda x: numpy.select(
        [x.lucro >  1000000, x.lucro > 0, x.lucro.isnull()],
        ["Mais de milhão", "Pouco", "Sem info"],
        "Não lucrou"
    )
  )


#     ).filter(["receita", "orcamento", "lucro"])

```

Outra função que também pode ajudar com essa mesma ideia de **ifelse** é a função **where**:

```{python}
df.assign(
        lucro_cat = lambda x: numpy.where(
            x.lucro > 1000000,
            'lucro',
            numpy.where(
                x.lucro > 0,
                'pouco lucro',
                numpy.where(
                  x.lucro.isnull(),
                  'sem info',
                'neutro'
    )))
)

#df = df["lucro"].fillna(0)
```

Queria dizer que "apanhei" com os erros que tive para conseguir construir essa nova variável. Infelizmente, a saída de erros do python não são esclarecedoras como o R é, mas consegui entender que algumas funções não conseguem trabalhar com NA's e essas funções não possuem parâmetros para atribuir o que fazer nesses casos.

Mas e aí, temos muitos lucros?

Conseguimos contar o n de cada categoria com a função **value_counts**:

```{python}
df.lucro_cat.value_counts()
```

Poderíamos "brincar" com essa base de dados e ter insights bem legal somente com descritivas de sumarização de dados, mas este não é o meu intuito nesse momento.

No R usamos o **summarize** junto ao **group_by** para conseguir medidas por agrupamentos de interesse e é bem fácil entender a dinâmica da utilização dessas duas funções que são MUITO utilizadas em nosso dia a dia como analistas. 

Bora pensar em fazer isso com o python?

Observando todo o contexto que construímos até aqui, acredito que seria interessante observar em qual gênero está concentrado (ou não) os maiores lucros, receita e orçamento.  Para isso, vamos utilizar a função **groupby** e a **agg**.

- **A função .agg() no Python é usada para agregar valores de colunas em um DataFrame ou Series, aplicando funções estatísticas ou personalizadas. Ela é muito útil no pandas quando queremos resumir ou transformar dados de diferentes maneiras.**

- **O .groupby() segue três etapas principais:**

  - **Divisão – Os dados são separados em grupos com base em uma coluna.**
  - **Aplicação – Aplicamos uma função estatística ou personalizada sobre cada grupo.**
  - **Combinação – O resultado é reunido em um novo DataFrame ou Series.**

Vamos lá?

Primeiro vamos entender como funciona o **.groupby()** e para isso vou criar uma base de dados com o agrupamento:

```{python}
df_by = df.groupby("generos").count()

#df.info()
```

Veja que a lógica é idêntica a do group_by + summarise do R. Na saída acima temos a quantidade de filmes por gênero.

Vamos fazer o lucro por gênero?

```{python}
df.groupby("generos")["lucro"].sum()
```

Viu que é mais parecido com o R do que a gente imagina? Mas agora eu quero olhar somente para o ano de 2020.

```{python}
df[df["ano"] == 2020].groupby("generos")["lucro"].sum()
```

Você conseguiu ver que até o momento usamos duas formas (ou funções) para filtrar a base de dados? 

Usamos o sinal de **==** e a função **.filter**. Cada uma foi utilizada em um contexto diferente. 


O do filter foi  esse:

```{markdown}
(df = df.assign(
    lucro = lambda x: x["receita"] - x["orcamento"])).filter(["receita", "orcamento", "lucro"])
#     ).filter(["receita", "orcamento", "lucro"])
```

E o do **==** foi:

```{markdown}
df[df["ano"] == 2020].groupby("generos")["lucro"].sum()
```


Eles são usados para propósitos diferentes no Pandas, e cada um tem sua aplicação específica. A função **.filter()** não é usada para filtrar linhas! Ela serve para selecionar **colunas** ou **índices** com base em critérios. Já o **==** filtra **linhas** com base em valores.

E Fê, e aquela função **.agg** lá que você tinha comentado?

É verdade, vamos falar sobre ela. Como estávamos falando da função **.groupby**, com o .agg() podemos aplicar múltiplas funções ao mesmo tempo. Isso é incrível e vem de encontro com a ideia do **summarise** do R.

Vamos de exemplo:

Nós somamos os lucros, que não deixa de ser uma medida ruim, mas vamos analisar a média, moda e desvio padrão por gênero e para aqueles que possuem um lucro diferente de 0. 

```{python}
lucro_metricas = df[df["lucro"] != 0] .groupby("generos").agg(
                   total_lucro=('lucro', 'sum'),
                   avg_lucro=('lucro', 'mean'),
                   num_count=('id_filme', 'count')
)
```

É incrível, né?

Por enquanto, foi assim que iniciei os meus estudos do python. Para alguns já é um ótimo conhecimento, mas ainda falta a parte de pivotagem e um bom aprofundamento na biblioteca **numpy**. 

Vou falar sobre pivotagem no **step_2**. Esse será o próximo post.



```{python}
# customer_metrics = df1.groupby('customer_id').agg(
#                    total_spent=('amount', 'sum'),
#                    avg_purchase_value=('amount', 'mean'),
#                    num_purchases=('purchase_id', 'count'),
#                    most_frequent_category=('category', lambda x: x.mode()[0] if not x.mode().empty else None)
# ).reset_index()
# 
# df1['month'] = df1['purchase_date'].dt.to_period('M')
# 
# monthly_trends = df1.groupby('month').agg(
#                  total_sales=('amount', 'sum'),
#                  avg_purchase_value=('amount', 'mean')
# ).reset_index()
```

