# readdbc
Um pacote python para ler dados no formato DBC (DBF comprimido) usado pelo DATASUS.  


# Uso
O código abaixo descompactará o arquivo `COLEBR15.dbc` e salvará o conteúdo em `COLEBR15.dbf`.
```
import readdbc

readdbc.dbc2dbf('COLEBR15.dbc', 'COLEBR15.dbf')
```


# Inspiração
[read.dbc](https://github.com/danicat/read.dbc)  
An R package for reading data in the DBC (compressed DBF) format used by DATASUS.
