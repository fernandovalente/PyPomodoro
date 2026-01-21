# PyPomodoro

## Gerar executaveis (Windows e macOS)

### 1) Preparar o ambiente

- Crie e ative um ambiente virtual (opcional, recomendado).
- Instale as dependencias do projeto:

```
pip install -r requirements.txt
```

- Instale o PyInstaller:

```
pip install pyinstaller
```

### 2) Gerar o pacote

Use o arquivo de spec ja configurado:

```
pyinstaller pypomodoro.spec
```

### 3) Onde ficam os arquivos gerados

- Windows: `dist/PyPomodoro/PyPomodoro.exe`
- macOS: `dist/PyPomodoro.app`

### Observacoes importantes

- Gere o executavel em cada sistema operacional. Nao e possivel gerar um `.app` no Windows ou um `.exe` no macOS.
- Caso falte alguma dependencia, instale com `pip` e execute novamente.
