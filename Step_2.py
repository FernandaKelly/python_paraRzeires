## Pandas

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

```{markdown}
pip install pandas
```

Agora vamos importar a biblioteca de interesse.

```{python}
#Importação da biblioteca
import pandas
```

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

E como você pode ver, a variável ano está como **float64**, o que implica ter esse **.0** ao final. Vamos trocar isso rapidinho? Clato! Vamos selecionar a variável com o colchetes.

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




####   Pivotagem

















