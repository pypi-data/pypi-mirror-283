# privhealth-lib
PrivHealth Libs


Esta é a biblioteca de módulos do PrivHealth

## Instalação

```bash
pip install privhealth-lib

```


## Manutenção

### Bibliotecas necessárias

```bash
pip install setuptools, wheel, twine

```

### Comandos para gerar arquivos wheel(já estão gerados)

```bash
python setup.py sdist bdist_wheel

```


### Testar localmente

```bash
pip install dist/privhealth_lib-0.1-py3-none-any.whl

```

### Verificar se está instalado localmente 

```bash
pip list

```

### Enviar pro PyPI

```bash
twine upload dist/*

```
