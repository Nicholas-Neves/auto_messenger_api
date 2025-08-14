# README — Auto Messenger com Supabase + Z-API (Python)

## Descrição

Script em Python que lê até 3 contatos do banco de dados **Supabase** e envia uma mensagem personalizada via **Z-API** no WhatsApp.

---

## Como usar

1. **Clonar este repositório**

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Abrir no PyCharm**

   * Vá em **File → Open** e selecione a pasta do projeto.

3. **Configurar variáveis de ambiente**

   * Copie o arquivo `.env.template` para `.env`.
   * Preencha com suas chaves e URLs do Supabase e da Z-API.

4. **Instalar dependências**

   * No PyCharm, abra o terminal integrado (**Alt+F12**) e rode:

     ```bash
     pip install -r requirements.txt
     ```

5. **Executar o script**

   * Clique com o botão direito no arquivo `main.py` → **Run 'main'**.

6. **O que o script faz**

   * Lê contatos do Supabase.
   * Envia para até 3 números a mensagem:

     > "Olá {{nome\_contato}}, tudo bem com você?"
   * Utiliza a API da Z-API para disparar no WhatsApp.

---

## Observações importantes

* O arquivo `.env` **não** deve ser commitado.
* Telefones devem estar no formato internacional, apenas com dígitos (ex.: `5511999999999`).
* Se usar chave `anon` no Supabase, garanta que a tabela tenha permissões de leitura configuradas.

---
