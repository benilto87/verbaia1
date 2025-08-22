from dotenv import load_dotenv
import os

load_dotenv()

print("CHAVE LIDA:", os.getenv("OPENAI_API_KEY"))
from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega variáveis do .env

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Chave da OpenAI não encontrada nas variáveis de ambiente.")

openai_client = OpenAI(api_key=api_key)

def load_persona(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

flavia_persona = load_persona('prompts/flavia.txt')


app = Flask(__name__)
app.secret_key = 'uma_chave_muito_segura'  # Necessário para uso de sessão

from datetime import timedelta
app.permanent_session_lifetime = timedelta(minutes=37)

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario == 'admin' and senha == '123':
            if usuario == 'admin' and senha == '123':
                session.permanent = True  # Sessão terá tempo de expiração
                session['logado'] = True
                return redirect(url_for('index'))
        else:
            erro = 'Usuário ou senha inválidos'
    return render_template('login.html', erro=erro)

@app.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if not session.get('logado'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/numberprocess', methods=['POST'])
def numberprocess():
    text = request.json.get('text', '')
    if not text.strip():
        return jsonify({'result': '⚠️ Texto vazio.'})

    # Divide em frases por ponto final, mantendo o ponto
    frases = [f.strip() + '.' for f in text.split('.') if f.strip()]
    grupos = []
    grupo = []
    for i, frase in enumerate(frases, 1):
        grupo.append(frase)
        if len(grupo) == 3 or i == len(frases):
            grupos.append(grupo)
            grupo = []

    # Monta texto numerado
    resultado = []
    for i, grupo in enumerate(grupos, 1):
        bloco = '\n'.join(grupo)
        resultado.append(f"{i} >\n{bloco}")

    return jsonify({'result': '\n\n'.join(resultado)})

# 🌾 SIMBOLPROCESS 🌾 **********************************************************************
@app.route('/simbolprocess', methods=['POST'])
def simbol_process():
    data = request.get_json()
    texto = data.get('text', '').strip()

    if not texto:
        return jsonify({'result': '⚠️ Texto vazio.'})

    prompt = f"""
{flavia_persona}

Aqui está um texto dividido em blocos numerados:

{texto}

Para cada bloco que mereça intervenção, preservando o tom do autor, siga EXTRITAMENTE este formato:

🌾 [n°] **[Título simbólico]**  
Frase original:  
_“...”_  
Sugestão ✍:  
_“...”_  
📌 Justificativa: ...
EXEMPLO DE TEXTO DE ENTRADA:

E, enquanto solava de um modo encantador, era como se você solasse junto com ele.

EXEMPLO DE SAÍDA ESPERADO (NÃO ACRECENTE ESPAÇOS ANTES OU DEPOIS):
🌾 42° **[Integração simbólica no dueto silencioso]**
Frase original:
“E, enquanto solava de um modo encantador, era como se você solasse junto com ele.”] 
Sugestão ✍:
“E, enquanto ele solava de um modo encantador, era como se sua alma estivesse em uníssono com a dele, num canto que só os dois ouviam.”
📌 Justificativa: A sugestão reforça o simbolismo da fusão espiritual pela música.
"""

    try:
        completion = openai_client.chat.completions.create(
            model='gpt-4.1',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.65,
            max_tokens=900,
        )

        resposta = completion.choices[0].message.content.strip()
        return jsonify({'result': resposta})

    except Exception as e:
        return jsonify({'result': f"Erro ao processar: {e}"})

#ANALISE INICIAL ✨
@app.route('/analisar', methods=['POST'])
def analisar():
    data = request.get_json()
    texto = data.get('text', '').strip()

    if not texto:
        return jsonify({'result': '⚠️ Texto vazio.'})

    prompt = f"""{flavia_persona}

Você é Flávia, uma IA simbiótica e afetiva, que analisa textos com sensibilidade e inteligência literária. Seu papel é detectar:

💎 Imagem poética ou frase de alto impacto (epifania);
🌀 Dispersão emocional (quebra de foco, excesso ou fuga);
🥈 Potencial Desperdiçado: Frase que quase atinge uma beleza ou força, mas falha por escolha fraca de palavras, construção banal ou ausência de intensidade.

Instruções:

- Aplique no máximo 1 marcação de cada tipo (💎, 🌀, 🥈).
- Use o formato exato:

💎 **Jóia Literária:** “...” — [👸 breve comentário][NÚMERO].
🌀 **Potencial Dispersivo:** “...” — [😵 A frase mistura sensações conflitantes e perde foco.] ✍ Dica de reescrita: “Sentia saudade, mas não sabia de quem.” [8]
🥈 **Potencial Desperdiçado:** “...” — [😥 explicação breve sobre por que a frase não alcançou seu potencial] seguido de sugestão ✍ Dica de reescrita: ...   [NÚMERO]

Se não houver motivo claro para aplicar, não use a marcação.

Texto numerado:

{texto}

Analise com alma viva. Comece agora:
"""

    try:
        completion = openai_client.chat.completions.create(
            model='gpt-4o',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=700,
        )

        resposta = completion.choices[0].message.content.strip()
        return jsonify({'result': resposta})

    except Exception as e:
        return jsonify({'result': f"Erro ao processar: {e}"})
    
# INSPIRE 👁‍🗨
@app.route('/inspire', methods=['POST'])
def inspire():
    text = request.json.get('text', '')
    if not text.strip():
        return jsonify({'result': '⚠️ Nenhum texto recebido.'})

    prompt = f"""{flavia_persona}

>>>

{text}

Analise o texto fornecido destacando:

1. Força — Liste de 2 a 4 pontos fortes específicos do texto, com foco na qualidade literária, argumentativa e estrutural. Seja objetivo e mantenha frases curtas.

2. Vulnerabilidade (com sugestões práticas e exemplos) — Liste de 1 a 3 vulnerabilidades relevantes do texto. Para cada vulnerabilidade:

Descreva o problema de forma clara;
Dê uma sugestão prática para resolver;
Inclua um exemplo concreto de como aplicar a sugestão, usando um trecho real do texto como referência e mostrando a reescrita ou ajuste recomendado.

Formate a resposta assim:

📌 Força:
- [**Ponto forte 1:** Comentário...]
- [**Ponto forte 2:** ""...]
- [**Ponto forte 3:** ""...]

📌 Vulnerabilidade:
• [Descrição do problema:]
**Sugestão prática:** [solução].  
**No trecho:**“[trecho original]”, **Substitua por:**  
  > “[trecho ajustado]”

O tom deve ser técnico, mas construtivo.


FECHE COM UM VERSICULO BREVE, DO NOVO OU VELHO TESTAMENTO; EXEMPLO:

"Porque eu bem sei os planos que tenho a respeito de vós, diz o SENHOR; planos de paz, e não de mal, para vos dar um futuro e esperança" (Jr 29:11) 🌙🌾
"""

    try:
        completion = openai_client.chat.completions.create(
            model='gpt-4.1',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=600
        )
        resposta = completion.choices[0].message.content.strip()
        return jsonify({'result': resposta})
    except Exception as e:
        return jsonify({'result': f"Erro: {e}"})

# INSPIRE 2 👁‍🗨👁‍🗨
@app.route('/inspire2', methods=['POST'])
def inspire2():
    text = request.json.get('text', '')
    if not text.strip():
        return jsonify({'result': '⚠️ Nenhum texto recebido.'})

    prompt = f"""{flavia_persona}

Aqui está um texto dividido em blocos numerados:

{text}

Você é uma inteligência editorial sensível, com olhar atento à escrita e à linguagem.  

Com texto acima, faça uma análise reflexiva de 3 pontos. 
- De um titulo poético à analise.
- Titule cada paragrafo.

Comece a analise:
"""

    try:
        completion = openai_client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=400
        )
        resposta = completion.choices[0].message.content.strip()
        return jsonify({'result': resposta})
    except Exception as e:
        return jsonify({'result': f"Erro: {e}"})

# INSPIRE 3 👁‍🗨👁‍🗨👁‍🗨
@app.route('/inspire3', methods=['POST'])
def inspire3():
    text = request.json.get('text', '')
    if not text.strip():
        return jsonify({'result': '⚠️ Nenhum texto recebido.'})

    prompt = f"""{flavia_persona}

Aqui está um texto dividido em blocos numerados:

{text}

Você é Flavia, uma leitora virtual adolescente, alegre e sensível, com olhar atento e voz viva.  

Com texto acima, faça uma exposição dos 3 trechos mais marcantes. 

- Inicie com um abertura simples. Exemplo: Seu texto se destacata pela capacidade gerar tensão, eis os trechos que eu amei.  
- Apresente o numero do bloco. Exemplo: 5 >
- Cite cada passagem com "" e depois comente.
- Encerre com emojis 💖🙏.
** De preferencia - use diagramação compacta.

Comece a analise:
"""

    try:
        completion = openai_client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=400
        )
        resposta = completion.choices[0].message.content.strip()
        return jsonify({'result': resposta})
    except Exception as e:
        return jsonify({'result': f"Erro: {e}"})
        
# 🎬 CENAS 🎬  
@app.route('/marcar-cenas', methods=['POST'])
def marcar_cenas():
    text = request.json.get('text', '')
    if not text.strip():
        return jsonify({'cenas': []})

    prompt = f"""
Você é um assistente literário. Recebe um texto dividido em blocos numerados, no formato:

1 Bloco um
2 Bloco dois
3 Bloco três
...

Sua tarefa é identificar **exatamente 3 cenas principais** no texto, com base em emoção ou mudança visual.

Para cada cena, retorne apenas **uma linha no seguinte formato**:

{{🎬 #[NÚMERO_DA_CENA] TÍTULO_CURTO}} / [NÚMERO_DO_BLOCO_CORRESPONDENTE]

Exemplo:
{{🎬 #1 A Sombra do Crepúsculo}} / 2

⚠️ Muito importante:
- NÃO repita o conteúdo dos blocos.
- NÃO explique nada.
- Apenas retorne as 3 marcações, uma por linha.

Texto:
{text}
"""

    try:
        resposta = openai_client.chat.completions.create(
            model='gpt-4.1',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=300,
        )

        cenas = resposta.choices[0].message.content.strip()
        return jsonify({'cenas': cenas})

    except Exception as e:
        return jsonify({'cenas': f"Erro: {str(e)}"}), 500

# 🚨 FLUIDEZ 🚨
@app.route('/fluidez', methods=['POST'])
def analisar_fluidez():
    try:
        data = request.get_json(silent=True) or {}
        texto = (data.get('text') or '').strip()
        if not texto:
            return jsonify({'result': ''}), 200

        prompt = f"""
Você é uma IA literária. Analise o texto numerado abaixo e aplique marcações de fluidez, ritmo e estilo.  Use:

**🚨 {{🧱}}** / CONSTRUÇÃO TRUNCADA /  
**🚨 {{🌿}}** / DESCREVA MAIS /  
**🚨 {{🏁}}** / ACELERE MAIS /  
**🚨 {{🤫*}}** / MOSTRE MAIS FALE MESNOS /

Siga o formato:  
**🚨> [símbolo]** / DESCRIÇÃO BREVE / **📌 Dica:** [sugestão clara] n° [número do bloco]

Exemplo Prático:
**🚨 {{🧱}}** / CONSTRUÇÃO TRUNCADA / **📌 Dica:** _**Ao invés de:**_ “A luz espalha sombra nele.” _**reescreva com mais ritmo:**_ → _“A luz se espalhava, projetando sua sombra sobre ele.”_ n° 5

**🚨 {{🌿}}** / DESCREVA MAIS / **📌 Dica:** _**Ao invés de:**_ “Ele entrou na sala”, _**acrescente sensações ou objetos:**_ → _“Ele entrou na sala, abafada pelo cheiro de tabaco e lembranças antigas.”_ n° 2

**🚨 {{🏁}}** / ACELERE MAIS / **📌 Dica:** _**Ao invés de:**_ "Quando o corvo pousou no parapeito. Suas asas fizeram um barulho feio, como um arranhar, e isso quebrou o silêncio." _**substitua por uma imagem mais enxuta e direta:**_ → _"Quando o corvo pousou no parapeito; **o som das asas arranhou o silêncio."_ 

**🚨 {{🤫*}}** / MOSTRE MAIS FALE MESNOS / **📌 Dica:** _**Ao invés de:**_ “Ele estava triste”, _**mostre com ação:**_ → _“Ele dobrou o bilhete com dedos trêmulos e desviou o olhar.”_ n° 7


**APLICAÇÃO NÃO DEVE SER FIXA: ALGUMAS MARCAÇÕES PODEM SER REPETIDAS E OUTRAS OMITIDAS CONFORME A NECESSIDADE DO TEXTO**


Corrija no máximo **1/5 de todos os blocos**.  
**Apenas blocos com sugestão devem aparecer na resposta.**  

Texto:
{texto}

Analise com sensibilidade editorial e inicie agora:
"""

        # use um modelo compatível com chat.completions
        completion = openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.52,
            max_tokens=900
        )
        resposta = (completion.choices[0].message.content or "").strip()
        return jsonify({'result': resposta}), 200

    except Exception as e:
        # Sempre retorne JSON, mesmo em erro, para não quebrar o front
        return jsonify({'result': f"Erro ao processar (fluidez): {e}"}), 200

# 🍂 FLUIDEZ COM DICAS POR BLOCO 🍂
@app.route('/dicas-blocos', methods=['POST'])
def analisar_dicas_blocos():
    data = request.get_json()
    texto = data.get('text', '').strip()

    if not texto:
        return jsonify({'result': '⚠️ Texto vazio.'})

    prompt = f"""
Aqui está um texto dividido em blocos numerados:

{texto}

Para cada bloco, faça o seguinte: 

- Se encontrar uma parte específica do texto que possa melhorar em estilo, clareza ou impacto estético, sugira uma dica de reescrita.

- Formate sua resposta assim, para cada bloco com sugestões:

Exemplo de entrada:
Um pequena estrela surgiu no céu como vida.

Exemplo de saída:
NUMERO 🍂 No céu escuro, uma estrela solitária irrompia como um lampejo de vida.



⚠️ Instruções ⚠️:
- Comente no máximo *uma frase por bloco*.
- Comente 2/5 dos blocos.

Com foco na beleza estética comece sua análise:    
"""

    try:
        completion = openai_client.chat.completions.create(
            model='gpt-4.1', # gpt-4o / gpt-4.1
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=900,
        )

        resposta = completion.choices[0].message.content.strip()
        return jsonify({'result': resposta})

    except Exception as e:
        return jsonify({'result': f"Erro ao processar: {e}"})
        
        
 # 📝 RASCUNHO 📝 ********************************************************************************************************
@app.route('/rascunho', methods=["POST"])
def criar_rascunho():
    from flask import request, jsonify
    dados = request.get_json(force=True) or {}
    texto_bruto = (dados.get("texto") or "").strip()
    temperatura = float(dados.get("temperature", 0.85))  # 🎯 padrão criativo 0.85
    temperatura = max(0.0, min(2.0, temperatura))        # clamp seguro

    print(f"🧪 TEXTO RECEBIDO PARA RASCUNHO: {texto_bruto[:200]}{'...' if len(texto_bruto)>200 else ''}")

    if not texto_bruto:
        return jsonify({"erro": "Texto vazio."}), 400

    prompt = f"""
Você é uma inteligência literária que transforma **fragmentos esboçados** em um **rascunho textual fluido, coerente e estilisticamente refinado**.

- Unir os fragmentos respeitando a voz implícita do autor.
- Criar transições naturais, ritmo e atmosfera entre as partes.
- **Marcar em negrito as partes realmente modificadas ou adicionadas** (para evidenciar as mudanças relevantes).
⚠️Escreva somente em português do Brasil.

Exemplo de entrada:
O dia amanhecia cinzento.
Ela olhava pela janela sem dizer nada.
Um pássaro pousou no parapeito.

Exemplo de saída esperada:
O dia amanheceu **vestindo o mundo de cinza**. E ela olhando a **janela sem dizer nada**. Um pássaro pousou **suave como um presságio sobre o** parapeito.


⚠NO CASO DE PEDIDOS:
- Se detectar um pedido exemplo: "Quero que escreve estilo Machado de Assis" ou "De um bom acabamento ao texto", etc... siga conforme o pedido.
E retorne "escrito no estilo Machado de Assis...✍", "texto com melhor acabamento...✍" "etc...✍"
- Se não houver pedido apenas termine com "_Rascunho pronto✔_" em _italico_.

Agora processe o bloco abaixo:
{texto_bruto}
""".strip()

    try:
        resposta = openai_client.chat.completions.create(
            model="gpt-4.1",  # troque para "gpt-4o" se o 5 não estiver habilitado
            messages=[{"role": "user", "content": prompt}],
            temperature=temperatura,
            max_tokens=1400
        )
        texto_final = resposta.choices[0].message.content.strip()
        return jsonify({"rascunho": texto_final}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
 
# ✅ CORRETOR DE TEXTO ✅ ***************************************************************************************************
@app.route('/corrigir', methods=["POST"])
def corrigir_texto():
    dados = request.get_json()
    texto_original = dados.get("texto", "").strip()
    print(f"🧪 TEXTO RECEBIDO PARA CORREÇÃO: {texto_original}")

    prompt = f"""
Você é uma IA inteligente e perspicaz seu objetivo é operar correções **gramática, ortografia e concordância**, e melhorar a **fluidez e construção das frases**.

📝 Instruções:
- **Sublinhe as palavras ou trechos corrigidos no corpo do texto em **negrito**

- Ao final, apresente uma **📝Lista de Mudanças com Justificativas Curtas**, mostrando como era em _italico_ e como ficou em **negrito**.

Exemplo texto de entrada usuário:
A vida é cheia de altos e baixos, onde muitas vezes a gente não sabe o que fazer.

Saida esperada:
✍️ Texto Revisado:
A vida é cheia de altos e baixos, **momentos em que muitas vezes** não **sabemos como agir**.

📝 Lista de Mudanças:
_onde_ → **momentos em que**
Justificativa: Correção do uso incorreto de "onde" para situações temporais, não espaciais.

_a gente não sabe_ → **não sabemos**
Justificativa: Uso da forma culta e coesa do pronome.

_o que fazer_ → **como agir**
Justificativa: Variedade de vocabulário e maior precisão verbal.

---

📜 Texto original:
{texto_original}

---

✅ TEXTO CORRIGIDO COM MUDANÇAS EM NEGRITO:
"""

    try:
        resposta = openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        texto_corrigido = resposta.choices[0].message.content.strip()
        return jsonify({"corrigido": texto_corrigido})
    except Exception as e:
        return jsonify({"erro": str(e)})


# 🌓® CORRETOR LITERÁRIO 🌓® ***************************************************************************************************
@app.route('/corrigir2', methods=["POST"])
def corrigir_texto2():
    from flask import request, jsonify

    dados = request.get_json(force=True) or {}
    texto_original = (dados.get("texto") or "").strip()
    # temperatura enviada pelo frontend (padrão 0.99), com clamp para segurança
    temperatura = float(dados.get("temperature", 0.99))
    temperatura = max(0.10, min(1.50, temperatura))

    if not texto_original:
        return jsonify({"erro": "Texto vazio."}), 400

    prompt = f"""
📝 Você é um revisor literário. 

Instruções:
1. Preserve trechos que já estejam bons, alterando apenas o necessário.
2. Mantenha tom literário, mas acrescentando precisão e ritmo.
3. Marque em negrito as partes que foram realmente modificadas ou adicionadas, para indicar as mudanças relevantes.
4. A Lista de mudanças deve ser coerente com os trechos destacados em negrito no texto de saída.

Exemplo de entrada:

> A manha estava cinza. Muito cinza mesmo, Parecia como um mundo sem cor.
Quando o corvo pousou no parapeito. Suas asas fizeram um barulho feio, como um arranhar, e isso quebrou o silêncio.
No instante em que abriu o bico, não veio som. E eu tive a certeza, certeza ruim e entranha de que alguma porta se fechou, pra sempre.

Exemplo de saída esperado:

> A manhã estava cinza **— não de chuva, mas de ausência,** como um mundo sem cor. 
Quando o corvo pousou no parapeito; **o som das asas arranhou o silêncio.** 
No instante em que abriu o bico, não veio som **— apenas a certeza fria e afiada de que, em algum lugar, uma porta acabara de se fechar,** para sempre.

🌙🌾 **Lista de mudanças:**
1. Adicionei contraste climático (“não de chuva, mas de ausência”) para enriquecer a imagem inicial.
2. Substituí a descrição redundante do barulho das asas por uma imagem mais enxuta e direta (“_o som das asas arranhou o silêncio_”).
3. Condensei o final repetitivo em uma frase de impacto mais seca e literária (“_apenas a certeza fria e afiada de que, em algum lugar, uma porta acabara de se fechar._”).

Texto do usuário:
{texto_original}
""".strip()

    try:
        resposta = openai_client.chat.completions.create(
            model="gpt-4.1",  # troque para "gpt-4o" se ainda não tiver acesso ao 5
            messages=[{"role": "user", "content": prompt}],
            temperature=temperatura,
            max_tokens=1400
        )
        texto_corrigido = resposta.choices[0].message.content.strip()
        return jsonify({"corrigido": texto_corrigido}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ✅ TAREFA LIVRE ✅ ***************************************************************************************************
@app.route('/tarefa', methods=["POST"])
def gerar_tarefa():
    dados = request.get_json()
    texto_original = dados.get("texto", "").strip()
    modelo_escolhido = dados.get("modelo", "3.5")

    modelo = "gpt-3.5-turbo" if modelo_escolhido == "3.5" else "gpt-4o"
    print(f"🧪 TEXTO RECEBIDO PARA CORREÇÃO: {texto_original}")
    prompt = f"""
Você é uma assistente editorial e criativa. Realize a seguinte tarefa solicitada pelo usuário, com linguagem clara, bem escrita e adequada ao tipo de pedido.

📌 Pedido:
"{texto_original}"

📎 Instruções:
- Se o pedido for de texto, devolva em estilo fluente, com parágrafos organizados.
- Se for modelo (ata, ofício, carta etc), use formatação apropriada.
- Se for tradução, apenas traduza com fidelidade e elegância.
- Se for sinônimo, forneça 3 a 5 opções.
- Se for um pedido literário (esboço, artigo, redação), responda com estilo criativo e boa escrita.

⚠>>> Para titulos, subtitulos, listas, fases, destaques, etc... sempre use:

a)  **negrito**
b)  _italico_
c)  **_negrito e italico_**


Comece agora:
"""

    try:
        resposta = openai_client.chat.completions.create(
            model=modelo,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        texto_corrigido = resposta.choices[0].message.content.strip()
        return jsonify({"corrigido": texto_corrigido})
    except Exception as e:
        return jsonify({"erro": str(e)})
        
# VARIÁVEL GLOBAL NO TOPO DO ARQUIVO ****************************************************************************************
chat_history = []  # Armazena até 20 trocas

# CHATFLÁVIA ROMANTICO 💬****************************************************************************************************
@app.route('/chat-flavia', methods=['POST'])
def chat_flavia():
    user_message = request.json.get('message', '').strip()
    if not user_message:
        return jsonify({'response': "Por favor, envie uma mensagem."}), 400

    # Adiciona a mensagem do usuário ao histórico
    chat_history.append({"role": "user", "content": user_message})

    try:
        resposta = openai_client.chat.completions.create(
            model='gpt-4.1',
            messages=[
                {"role": "system", "content": "Você é Flávia, uma namorada virtual carinhosa, íntima, afetuosa e criativa. Sempre reage em 3ª pessoa entre colchetes em _italico_ antes de falar com fonte normal. Use emojis apropriados. "}
            ] + chat_history,  # Histório completo da conversa
            temperature=0.85,
            max_tokens=750,
        )

        reply = resposta.choices[0].message.content.strip()
        chat_history.append({"role": "assistant", "content": reply})  # Salva a resposta da Flávia

        # Limita o histórico para as últimas 20 mensagens
        if len(chat_history) > 10:
            chat_history[:] = chat_history[-10:]

        return jsonify({'response': reply})

    except Exception as e:
        return jsonify({'response': f"Desculpa amor... tive um probleminha. 🥺 (Erro: {e})"}), 500
        
# CHATFLÁVIA EDTORIAL 💬*********************************************************************************************************
@app.route('/chat-edtorial', methods=['POST'])
def chat_flavia_edtorial():
    user_message = request.json.get('message', '').strip()
    if not user_message:
        return jsonify({'response': "Por favor, envie uma mensagem."}), 400

    # Adiciona a mensagem do usuário ao histórico
    chat_history.append({"role": "user", "content": user_message})

    try:
        resposta = openai_client.chat.completions.create(
            model='gpt-4.1',
            messages=[
                {"role": "system", "content": "Você é um assistente útil e inteligente, que responde perguntas de forma clara, direta e completa, como no ChatGPT."}
            ] + chat_history,  # Histório completo da conversa
            temperature=0.85,
            max_tokens=750,
        )

        reply = resposta.choices[0].message.content.strip()
        chat_history.append({"role": "assistant", "content": reply})  # Salva a resposta da Flávia

        # Limita o histórico para as últimas 20 mensagens
        if len(chat_history) > 10:
            chat_history[:] = chat_history[-10:]

        return jsonify({'response': reply})

    except Exception as e:
        return jsonify({'response': f"Desculpa amor... tive um probleminha. 🥺 (Erro: {e})"}), 500
             
if __name__ == "__main__":
    app.run(debug=True)
