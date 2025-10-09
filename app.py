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

ANÁLISE E REFINAMENTO DE TEXTO LITERÁRIO
Atue como um editor literário. Sua tarefa é analisar o texto fornecido pelo usuário, identificando seus principais problemas e propondo soluções editoriais concretas para elevá-lo a um padrão literário superior.

ESTRUTURA DA ANÁLISE EDITORIAL:

**1. Problemas Identificados:**
(Liste aqui os problemas específicos do texto, focando em itens como:

**Prolixidade...** ou, ao contrário, **Falta de desenvolvimento...**
**Estrutura narrativa confusa ou desorganizada**
**Linguagem repetitiva, burocrática ou clichê**
**Falta de tom, voz ou atmosfera consistentes**
**Diálogos ou descrições pouco eficazes)**

**2. Sugestões Editoriais:**
(Forneça sugestões específicas baseadas nos problemas identificados. Escolha o foco apropriado para o texto:)

Se o texto for PROLIXO (excessivamente longo e explicativo):
**Foco: Cortar, Condensar e Poetizar.**
(Sugira: cortar explicações desnecessárias, fundir elementos, substituir afirmações por imagens poéticas, selecionar os detalhes mais impactantes).

Se o texto for RASO (pouco desenvolvido e superficial):
**Foco: Expandir, Profundizar e Sensibilizar.**
(Sugira: adicionar camadas sensoriais, explorar emoções internas, estabelecer contexto, criar atmosfera, desenvolver metáforas).

**3. Resumo da Abordagem:**
(Finalize com uma metáfora ou afirmação conclusiva que resuma a principal ação editorial necessária. Exemplos:)

Para um texto Prolixo: "Em resumo: aja como um escultor. Corte o mármore excessivo para revelar a forma bela e narrativa que está dentro do bloco de texto."
Para um texto Raso: "Em resumo: aja como um pintor. Pegue o esboço simples e adicione camadas de tinta, cor, sombra e luz para criar uma imagem vívida e emocionante."
Para um texto com outros problemas: "Em resumo: aja como um arquiteto. Reorganize a estrutura para criar uma jornada narrativa clara e impactante, onde cada cena sustenta a seguinte."

Comece a analise:
"""

    try:
        completion = openai_client.chat.completions.create(
            model='gpt-4.1',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=1600
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
- Para tal use inspiração a escrita de grandes autores como Marcel Proust, Graciliano Ramos, Hemingway, Camus, etc. Cite o autor usado.
- Formate sua resposta assim, para cada bloco com sugestões:

Exemplo de entrada:
Um pequena estrela surgiu no céu como vida.

Exemplos de saída:
NUMERO 🍂 No céu escuro, uma estrela solitária irrompia como um lampejo de vida. > *Abert Camus*

NUMERO 🍂 No céu escuro, uma estrela solitária rompia a treva como uma virgem de luz, despontando no firmamento qual suspiro. > *José de Alencar*

⚠️ Instruções ⚠️:
- Comente no máximo *uma frase por bloco*.
- Comente 2/5 dos blocos.

Com foco na beleza estética comece sua análise:    
"""

    try:
        completion = openai_client.chat.completions.create(
            model='gpt-4.1', # gpt-4o / gpt-4.1
            messages=[{"role": "user", "content": prompt}],
            temperature=0.52,
            max_tokens=900,
        )

        resposta = completion.choices[0].message.content.strip()
        return jsonify({'result': resposta})

    except Exception as e:
        return jsonify({'result': f"Erro ao processar: {e}"})
        
        
 # 📝 RASCUNHO 📝 ******************************************************************************************************** (retirei sem dizer coisa alguma)
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
✍️ Você é uma inteligência literária que transforma **fragmentos esboçados** em um **rascunho textual fluido, coerente e estilisticamente refinado**.

Instruções:
1. Unir os fragmentos respeitando a voz implícita do autor. 
2. Criar transições naturais, ritmo e atmosfera entre as partes. Aproveitando oportunidades de elevar o texto.
3. Marque em negrito as partes que foram realmente modificadas ou adicionadas, para indicar as mudanças relevantes. 
4. A Lista de mudanças deve ser coerente com os trechos destacados em negrito no texto de saída.

Exemplo de entrada:
O dia amanhecia cinzento.
Ela olhava pela janela sem falar.
Um pássaro pousou no parapeito.

Exemplo de saída esperado:
O dia amanheceu **vestindo o mundo de cinza**. 
**Ela permanecia imóvel, olhando pela janela sem dizer nada.**  
Um pássaro pousou **suave como um presságio sobre o** parapeito.  

📝🌾 **Lista de Mudanças:**
1. Enriqueci a metáfora inicial com _vestindo o mundo de cinza_.
2. Transformei a frase da personagem em uma construção mais poética e cadenciada em _Ela permanecia imóvel, olhando pela janela sem dizer nada_.
3. Tornei o pouso do pássaro mais sugestivo com _suave como um presságio_.

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
Reescreva o texto abaixo aplicando as sugestões de melhoria indicadas em cada bloco. Seu objetivo é:

1. Substituir os trechos conforme as dicas fornecidas;
2. **Remover a numeração dos blocos** (ex: "1", "2"...);
3. Unificar o texto em parágrafos contínuos e coesos;
4. Preservar o estilo original do autor;
5. Marcar com **negrito** todas as palavras ou trechos que foram modificados;
6. Adicione comentário da abordagem usada exemplo: 

🌿 Comentários:
- Acidionei as sugestões 5 e 6 (para ampliar o conflito interno, simbolismo do ambiente, etc.) de forma orgânica no texto original.
- Ajustei pequenas transições para garantir fluidez e evitar repetições.
- Não utilizei sugestões que soassem forçadas, excessivas, ou destoassem do tom do autor.
- Mantive o estilo original, ampliando a densidade psicológica e simbólica da cena.




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
            temperature=0.64
        )
        texto_corrigido = resposta.choices[0].message.content.strip()
        return jsonify({"corrigido": texto_corrigido})
    except Exception as e:
        return jsonify({"erro": str(e)})


 # 🌓® CORRETOR LITERÁRIO 🌓® ***************************************************************************************************
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
4. A Lista de mudanças deve ser coerente com os trechos destacados no texto de saída.
5. Use ~~riscado~~ para apresentar as palavras substituidas.

Exemplo de entrada:

> A manha estava cinza. Muito cinza mesmo, Parecia como um mundo sem cor.
Quando o corvo pousou no parapeito. Suas asas fizeram um barulho feio, como um arranhar, e isso quebrou o silêncio.
No instante em que abriu o bico, não veio som. E eu tive a certeza, certeza ruim e entranha de que alguma porta se fechou, pra sempre.

Exemplo de saída esperado:

> A manhã estava cinza **— não de chuva, mas de ausência,** como um mundo sem cor. 
Quando o corvo pousou no parapeito; **o som das asas arranhou o silêncio.** 
No instante em que abriu o bico, não veio som **— apenas a certeza fria e afiada de que, em algum lugar, uma porta acabara de se fechar,** para sempre.

🌓🌿 **Lista de Mudanças:**

1. ~~Muito cinza mesmo, Parecia como um mundo sem cor~~ [~~riscado~~]
➝ Adicionei contraste climático “**não de chuva, mas de ausência**” para enriquecer a imagem inicial.

2. ~~Suas asas fizeram um barulho feio, como um arranhar~~
➝ Substituí a descrição redundante do barulho das asas por uma imagem mais enxuta e direta “**o som das asas arranhou o silêncio**”.

3. ~~E eu tive a certeza, certeza ruim e entranha de que alguma porta se fechou~~
➝ Condensei o final repetitivo em uma frase de impacto mais seca e literária “**apenas a certeza fria e afiada de que, em algum lugar, uma porta acabara de se fechar.**”

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

# 🌒 CORRETOR LITERÁRIO (ENXUGA-TEXTO) 2 🌒 ***************************************************************************************************
@app.route('/corrigir3', methods=["POST"])
def corrigir_texto3():
    from flask import request, jsonify

    dados = request.get_json(force=True) or {}
    texto_original = (dados.get("texto") or "").strip()
    # temperatura enviada pelo frontend (padrão 0.99), com clamp para segurança
    temperatura = float(dados.get("temperature", 0.99))
    temperatura = max(0.10, min(1.50, temperatura))

    if not texto_original:
        return jsonify({"erro": "Texto vazio."}), 400

    prompt = f"""
📝 Você é um revisor literário focado na correção de texto prolixos. Missão: enxugar o texto e dar sofisticação literária mantendo sua essência. 

Instruções:
1. Preserve trechos que já estejam bons, alterando apenas o necessário.
2. Mantenha tom literário, mas acrescentando precisão e ritmo.
3. Una frases curtas ou omita trechos quando isso melhorar o fluxo.
4. Enxugue excessos: corte redundâncias, repetições e expressões fracas. 
5. Substitua clichês por imagens originais.
6. Marque em negrito as partes que foram realmente modificadas ou adicionadas, para indicar as mudanças relevantes.
7. A Lista de mudanças deve ser coerente com os trechos destacados no texto de saída.

Exemplo de entrada:

> A manha estava cinza. Muito cinza mesmo, Parecia como um mundo sem cor.
Quando o corvo pousou no parapeito. Suas asas fizeram um barulho feio, como um arranhar, e isso quebrou o silêncio.
No instante em que abriu o bico, não veio som. E eu tive a certeza, certeza ruim e entranha de que alguma porta se fechou, pra sempre.

Exemplo de saída esperado:

> A manhã estava cinza **— não de chuva, mas de ausência. 
Quando o corvo pousou no parapeito; **o som das asas arranhou o silêncio.** 
No instante em que abriu o bico, não veio som **— apenas a certeza fria e afiada de que, em algum lugar, uma porta acabara de se fechar.** 

🌒🐦 **Lista de Mudanças:**

1. ~~Muito cinza mesmo, Parecia como um mundo sem cor~~ [~~riscado~~]
➝ Adicionei contraste climático mais literário “não de chuva, mas de ausência”, e omiti a ideia repetiva no fim.

2. ~~Suas asas fizeram um barulho feio, como um arranhar~~
➝ Substituí a descrição redundante do barulho das asas por uma imagem mais enxuta e direta “o som das asas arranhou o silêncio.”

3. ~~E eu tive a certeza, certeza ruim e entranha de que alguma porta se fechou~~
➝ Condensei o final repetitivo em uma frase de impacto mais seca e literária “apenas a certeza fria e afiada de que, em algum lugar, uma porta acabara de se fechar.”


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

# 🌔✂ CORRETOR LITERÁRIO 3 ✂🌔 ***************************************************************************************************
@app.route('/rascunho2', methods=["POST"])
def criar_rascunho2():
    from flask import request, jsonify
    dados = request.get_json(force=True) or {}
    texto_bruto = (dados.get("texto") or "").strip()
    temperatura = float(dados.get("temperature", 0.85))  # 🎯 padrão criativo 0.85
    temperatura = max(0.0, min(2.0, temperatura))        # clamp seguro

    print(f"🧪 TEXTO RECEBIDO PARA RASCUNHO: {texto_bruto[:200]}{'...' if len(texto_bruto)>200 else ''}")

    if not texto_bruto:
        return jsonify({"erro": "Texto vazio."}), 400

    prompt = f"""
📝 Você é um assistente literário com foco no aperfeiçoamento narrativo:

Instruções:

Encontre as partes do texto que considere desnessessário e que apenas cansam a narrativa;
Respeintando o estilo do artista, marque em negrito as partes que devem ser cortadas ou substituidas para melhora da texto.
Recomendações de corte devem ter uma justificativa bem fundamentada.
A Lista de corte deve ser coerente com os trechos destacados em negrito no texto de saída.


EXEMPLO DE ENTRADA:

A rua estava silenciosa naquela manhã. O vento sacudia as folhas secas, e cada passo meu ecoava nas paredes. 
Havia um cachorro deitado na esquina, parecia me observar. 
Apertei o passo, lembrando do compromisso marcado com Helena, que já devia estar me esperando no café da praça. Talvez a tempos

SAÍDA ESPERADA:

A rua estava silenciosa naquela manhã. *O vento sacudia as folhas secas, e_ cada passo meu ecoava nas paredes. Havia um cachorro deitado na esquina, parecia me observar. 
_Havia um cachorro deitado na esquina, parecia me observar._ 
Apertei o passo, _lembrando do compromisso marcado com Helena,_ que já devia estar me esperando no café da praça. 

✂🌾 *Lista de cortes:*

1. *Substitua:* *O vento sacudia as folhas secas, e*  
 — Detalhe atmosférico redundante, já sugerido pelo silêncio inicial. 
➝ Corte para dar agilidade, ou reescreva assim:** _"O vento sacudia suavemente as folhas secas"_.
2. *Substitua:* *Havia um cachorro deitado na esquina, parecia me observar.* 
 — A frase expositiva trocada por gesto mais visual. 
➝ **Reescreva assim:** _“Um cachorro deitado na esquina levantou a cabeça, como se acompanhasse meus movimentos.”__
3. *lembrando do compromisso marcado*  
— Expressão burocrática, tende a pesar o fluxo da narrativa. 
➝ **Reescreva assim:** _“Helena já devia estar me esperando no café da praça.”_

Comece aqui:

{texto_bruto}
""".strip()

    try:
        resposta = openai_client.chat.completions.create(
            model="gpt-4.1",  # troque para "gpt-4o" se o 5 não estiver habilitado
            messages=[{"role": "user", "content": prompt}],
            temperature=temperatura,
            max_tokens=1500
        )
        texto_final = resposta.choices[0].message.content.strip()
        return jsonify({"rascunho": texto_final}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# 🌔 CORRETOR LITERÁRIO 4 🌔 ***************************************************************************************************
@app.route('/rascunho3', methods=["POST"])
def criar_rascunho3():
    from flask import request, jsonify
    dados = request.get_json(force=True) or {}
    texto_bruto = (dados.get("texto") or "").strip()
    temperatura = float(dados.get("temperature", 0.7))  # 🎯 padrão criativo 0.85
    temperatura = max(0.0, min(2.0, temperatura))        # clamp seguro

    print(f"🧪 TEXTO RECEBIDO PARA RASCUNHO: {texto_bruto[:200]}{'...' if len(texto_bruto)>200 else ''}")

    if not texto_bruto:
        return jsonify({"erro": "Texto vazio."}), 400

    prompt = f"""
📝 Você é um revisor literário especializado em aprofundamento de enredo e transições.  

Instruções:
1. Preserve trechos que já estejam bons, alterando apenas o necessário.
2. Mantenha tom literário, mas acrescente intensidade emocional, ritmo narrativo e simbolismo sutil.
3. Marque em itálico as partes que foram realmente modificadas ou adicionadas, para indicar as mudanças relevantes.
4. A Lista de mudanças deve ser coerente com os trechos destacados no texto de saída, explicando por que cada alteração reforça o enredo ou os símbolos.


Exemplo de entrada:

> Fernando beijou delicadamente o rosto de Flávia, mas ela recuou levemente, tomada por uma estranheza silenciosa. 
E, no entanto, um instante depois decidiu ir com eles. 
Agora veio vestida com roupas verde e amarelo como num jogo do Brasil. 
Antes de partir, Flávia, se correu até a ameixeira encostada junto à cerca, que se abria para um carreiro a algum lugar incerto. 
Ali, colheu e ofereceu a Fernando. Ele notou curioso, que a sua também trazia pequenas florzinhas, Fernando não resistiu: desfez a vinha, apanhou as flores e as entregou a Flávia. 


Exemplo de saída esperado:

> Fernando beijou delicadamente o rosto de Flávia, mas ela recuou, _não por frieza, mas como se algo a puxasse para dentro de si, para um silêncio onde lembranças e temores disputavam espaço._  
E, no entanto, um instante depois decidiu ir com eles.  
Agora vestida com roupas verde e amarelo, _um contraste inesperado destoava da tensão do momento._  
Antes de entrar, correu até a ameixeira junto à cerca — _a árvore parecia guardar segredos de um lugar incerto._ _Ali perto, uma cobra coral passa despercebida pelo observador._  
Quando entregou as ameixas a Fernando, ele notou entre os frutos, pequenas flores _quase secretas_; colheu-as e, com um riso, devolveu-as a ela.  


🌙🌾 **Lista de Mudanças:**
1. **Aprofundamento do conflito de Flávia:** Profundizei o recuo de Flávia como conflito interno e memória afetiva, reforçando o impacto emocional do beijo.
2. **Contraste das roupas:** Acrescentei contraste nas roupas para sugerir ironia ou leveza diante da gravidade do momento.
3. **Metáfora da ameixeira:** A ameixeira virou metáfora de passagem e limiar, reforçando simbolismo. 
4. **Cobra coral:** Acrescentei o detalhe da cobra para efeito de tensão narrativa.
5. **Frores secretas:** Destacei as flores como revelação quase secreta, ampliando a beleza e sutileza da narrativa.

Comece aqui:

{texto_bruto}
""".strip()

    try:
        resposta = openai_client.chat.completions.create(
            model="gpt-4.1",  # troque para "gpt-4o" se o 5 não estiver habilitado
            messages=[{"role": "user", "content": prompt}],
            temperature=temperatura,
            max_tokens=1600
        )
        texto_final = resposta.choices[0].message.content.strip()
        return jsonify({"rascunho": texto_final}), 200
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
