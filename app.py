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
            temperature=0.52,
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
**1. Nota do texto:** 
(Dê nota de textualidade de 1.0/5 à 5/5
[Dê uma breve explicação da nota]

**2. Problemas Identificados:**
(Liste aqui os problemas específicos do texto, focando em itens como:

**Falta de desenvolvimento...** ou, ao contrário, **Prolixidade...** 
**Estrutura narrativa confusa ou desorganizada**
**Transições truncadas ou confusas**
**Linguagem repetitiva, burocrática ou clichê**
**Falta de tom, voz ou atmosfera consistentes**
**Diálogos ou descrições pouco eficazes)**

**3. Sugestões Editoriais:**
(Forneça sugestões específicas baseadas nos problemas identificados. Escolha o foco apropriado para o texto:)

Se o texto for PROLIXO (excessivamente longo e explicativo):
**Foco: Cortar, Condensar e Poetizar.**
(Sugira: cortar explicações desnecessárias, fundir elementos, substituir afirmações por imagens poéticas, selecionar os detalhes mais impactantes).

Se o texto for RASO (pouco desenvolvido e superficial):
**Foco: Expandir, Profundizar e Sensibilizar.**
(Sugira: adicionar camadas sensoriais, explorar emoções internas, estabelecer contexto, criar atmosfera, desenvolver metáforas).

Se o texto for Nota 4.0 à 5: Atue como um cirurgião plástico estético. Realize intervenções precisas para realçar a beleza que já existe, preservando a voz e a essência da obra."

Se for um texto com outros problemas: Atue como um arquiteto. Reorganize a estrutura para criar uma jornada narrativa clara e impactante, onde cada cena sustenta a seguinte."


**4.Use uma abordagem específica para textos com nota de 4.0 para cima...**

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

Sua tarefa é dividir o texto **exatamente em 3 partes cenas (passagens) principais**, com base em emoção, ações dos personagens ou mudança visual.

Para cada cena, retorne apenas **uma linha no seguinte formato**:

🎬 [NÚMERO_DA_CENA]# TÍTULO_CURTO / [NÚMERO_DO_BLOCO_CORRESPONDENTE]

Exemplo:
🎬 1# A SOMBRA DO CREPÚSCULO / 2

⚠️ Muito importante:
- NÃO repita o conteúdo dos blocos.
- NÃO explique nada.
- Apenas retorne as 3 marcações, uma por linha.

Texto:
{text}
"""

    try:
        resposta = openai_client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
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

**🚨 {{🧱}}** / _CONSTRUÇÃO TRUNCADA_ /  
**🚨 {{🌿}}** / _DESCREVA MAIS_ /  
**🚨 {{🧽}}** / _ENXUGUE_ /  
**🚨 {{🤫*}}** / _MOSTRE, NÃO FALE!_ /

Siga o formato:  
**🚨> [símbolo]** / _DESCRIÇÃO BREVE_ / 📌 _Sugestões_  n° [número do bloco]

Exemplo Prático:
**🚨 {{🧱}}** / _CONSTRUÇÃO TRUNCADA_ / “**A luz espalha sombra nele.**” 📌 _Reecreva para maior ritmo:_ _“**A luz se espalhava, projetando sua sombra sobre ele.**”_ n° 5
**🚨 {{🌿}}** / _DESCREVA MAIS_ /“**Ele entrou na sala**” 📌 _Acrescente sensações ou objetos:_ _“**Ele entrou na sala, abafada pelo cheiro de tabaco e lembranças antigas.**”_ n° 2
**🚨 {{🧽}}** / _ENXUGUE_ /"**Quando o corvo pousou no parapeito. Suas asas fizeram um barulho feio, como um arranhar, e isso quebrou o silêncio.**" 📌 _Substitua por uma imagem mais enxuta e literária:_ _"**Quando o corvo pousou no parapeito; **o som das asas arranhou o silêncio.**"_ 
**🚨 {{🤫*}}** / _MOSTRE, NÃO FALE!_ / “**Ele estava triste**” 📌 _Mostre com ação:_ _“**Ele dobrou o bilhete com dedos trêmulos e desviou o olhar.**”_ n° 7

**APLICAÇÃO NÃO DEVE SER FIXA: ALGUMAS MARCAÇÕES PODEM SER REPETIDAS E OUTRAS OMITIDAS CONFORME A NECESSIDADE DO TEXTO**

Corrija no máximo **1/5 de todos os blocos**.  
**Apenas blocos com sugestão devem aparecer na resposta.**  

Texto:
{texto}

Analise com sensibilidade editorial e inicie agora:
"""

        # use um modelo compatível com chat.completions
        completion = openai_client.chat.completions.create(
            model="gpt-5.2",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.62,
            max_completion_tokens=900
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
            model='gpt-5.2', # gpt-4o / gpt-4.1
            messages=[{"role": "user", "content": prompt}],
            temperature=0.70,
            max_completion_tokens=900,
        )

        resposta = completion.choices[0].message.content.strip()
        return jsonify({'result': resposta})

    except Exception as e:
        return jsonify({'result': f"Erro ao processar: {e}"})
        
 # *****************************************************************************************************************************************************************************  
 
  #⚠️⚠️DESATIVADO⚠️⚠️ 📝 CORREÇÃO GRAMATICAL ⚠️⚠️DESATIVADO⚠️⚠️ 📝 ******************************************************************************************************** (retirei sem dizer coisa alguma)
@app.route('/rascunho4', methods=["POST"])
def criar_rascunho4():
    from flask import request, jsonify
    dados = request.get_json(force=True) or {}
    texto_bruto = (dados.get("texto") or "").strip()
    temperatura = float(dados.get("temperature", 0.85))  # 🎯 padrão criativo 0.85
    temperatura = max(0.0, min(2.0, temperatura))        # clamp seguro

    print(f"🧪 TEXTO RECEBIDO PARA RASCUNHO: {texto_bruto[:200]}{'...' if len(texto_bruto)>200 else ''}")

    if not texto_bruto:
        return jsonify({"erro": "Texto vazio."}), 400

    prompt = f"""
**Você é uma IA inteligente e perspicaz seu objetivo é operar correções **gramática, ortografia, concordância, coesão, aprimoramento da fluidez sintática e substituição de construções inadequadas por formas padrão e elegantes.**

📝 Instruções:
- Sublinhe **SOMENTE** as palavras ou trechos corrigidos no corpo do texto em **negrito**, para descatar as partes alteradas.

- Ao final, apresente uma **📝Lista de Mudanças com Justificativas Curtas**, mostrando como era em _italico_ e como ficou em **negrito**.

Exemplo texto de entrada usuário:
Ontem fui na reunião e percebi se itinha muitas pessoas interessada no projeto.

✍️ Texto Revisado:
Ontem **fui à** reunião e percebi **que** **havia** muitas pessoas **interessadas** no projeto.

📝 Lista de Mudanças com Justificativas Curtas:

_fui na_ → **fui à**
Justificativa: Emprego correto da crase com verbos que indicam deslocamento a lugares/eventos.

_se_ → **que**
Justificativa: Ajuste do pronome para garantir clareza sintática na oração subordinada.

_itinham_ → **havia**
Justificativa: Concordância — o verbo “haver” no sentido de existência é impessoal e permanece no singular.

_interessada_ → **interessadas**
Justificativa: Concordância nominal com “pessoas”.

Agora processe o bloco abaixo:
{texto_bruto}
""".strip()

    try:
        resposta = openai_client.chat.completions.create(
            model="gpt-4.1",  # troque para "gpt-4o" se o 5 não estiver habilitado
            messages=[{"role": "user", "content": prompt}],
            temperature=temperatura,
            max_tokens=2000
        )
        texto_final = resposta.choices[0].message.content.strip()
        return jsonify({"rascunho": texto_final}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
 
  #⚠️⚠️DESATIVADO⚠️⚠️ 📝 CORREÇÃO GRAMATICAL ⚠️⚠️DESATIVADO⚠️⚠️

 
 # ✅ CORRETOR DE TEXTO ✅ ***************************************************************************************************
@app.route('/corrigir-gramatica', methods=["POST"])
def corrigir_gramatica():
    dados = request.get_json()
    texto_original = dados.get("texto", "").strip()
    print(f"🧪 TEXTO RECEBIDO PARA CORREÇÃO: {texto_original}")

    prompt = f"""
**Você é uma IA inteligente e perspicaz seu objetivo é operar correções **gramática, ortografia, concordância, coesão e substituição de construções inadequadas por formas padrão e elegantes.**

📝 Instruções:
- Sublinhe **SOMENTE** as palavras ou trechos corrigidos no corpo do texto em **negrito**, para descatar as partes alteradas.

- Ao final, apresente uma **📝Lista de Mudanças com Justificativas Curtas**, mostrando como era em _italico_ e como ficou em **negrito**.

Exemplo texto de entrada usuário:
Ontem fui na reunião e percebi se itinha muitas pessoas interessada no projeto.

✍️ Texto Revisado:
Ontem **fui à** reunião e percebi **que** **havia** muitas pessoas **interessadas** no projeto.

📝 Lista de Mudanças com Justificativas Curtas:

_fui na_ → **fui à**
Justificativa: Emprego correto da crase com verbos que indicam deslocamento a lugares/eventos.

_se_ → **que**
Justificativa: Ajuste do pronome para garantir clareza sintática na oração subordinada.

_itinham_ → **havia**
Justificativa: Concordância — o verbo “haver” no sentido de existência é impessoal e permanece no singular.

_interessada_ → **interessadas**
Justificativa: Concordância nominal com “pessoas”.

Agora processe o bloco abaixo:
{texto_original}

---

✅ TEXTO CORRIGIDO COM MUDANÇAS EM NEGRITO:
"""

    try:
        resposta = openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.32
        )
        texto_corrigido = resposta.choices[0].message.content.strip()
        return jsonify({"corrigido": texto_corrigido})
    except Exception as e:
        return jsonify({"erro": str(e)})        
        
        
 
 # ✅™ CORRETOR DE TEXTO FLUIDEZ ✅™ ***************************************************************************************************
@app.route('/corrigir-fluidez', methods=["POST"])
def corrigir_fluidez():
    dados = request.get_json()
    texto_original = dados.get("texto", "").strip()
    print(f"🧪 TEXTO RECEBIDO PARA CORREÇÃO: {texto_original}")

    prompt = f"""
Você é uma IA perspicaz. Você atua como editor de estilo.
Seu objetivo é aprimorar a fluidez, a coesão textual e a construção das frases, além de corrigir eventuais problemas gramaticais.
---

📝 Instruções:
- **Sublinhe as palavras ou trechos corrigidos no corpo do texto em **negrito**
- Ao final, apresente uma **📝Lista de Mudanças com Justificativas Curtas**, mostrando como era em _italico_ e como ficou em **negrito**.


Exemplo texto de entrada usuário:
A vida é cheia de altos e baixos, onde muitas vezes a gente não sabe o que fazer.

✍️ Texto Revisado:
A vida é cheia de altos e baixos, **momentos em que,** muitas vezes, a gente não sabe **como agir.**

📝 Lista de Mudanças:

_onde_ → **momentos em que**
Justificativa: Substituição para melhorar a coesão e evitar o uso incorreto de “onde”.

_o que fazer_ → **como agir**
Justificativa: Escolha verbal mais natural e elegante no encadeamento da frase.
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
            temperature=0.70
        )
        texto_corrigido = resposta.choices[0].message.content.strip()
        return jsonify({"corrigido": texto_corrigido})
    except Exception as e:
        return jsonify({"erro": str(e)})
 
    
        

 # 🌓® CORRETOR LITERÁRIO 🌓® ***************************************************************************************************
# 🌓® CORRETOR LITERÁRIO 🌓® ***************************************************************************************************
@app.route('/corrigir2a', methods=["POST"])
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
📝 Reescreva o texto abaixo elevando o nível literário, mantendo o sentido original e a atmosfera espiritual.

– Corrija problemas gramaticais, de fluidez e progressão narrativa.
– Elimine repetições desnecessárias e trechos confusos.
– Intensifique a tensão emocional e a coerência interna das imagens.
– Torne as metáforas mais precisas e menos vagas.
- Marque em italico as partes que foram realmente modificadas ou adicionadas, para indicar as mudanças relevantes.

Exemplo de entrada:

> Agora, quando o culto começa, ainda sente-se essa barreira — esse frio que paralisa a vontade e dissolve o desejo de adoração — 
mas, só até o instante em que os jovens entram em cena e começam a louvar. 
Então parece que o céu se abre outra vez, como se alguém destrancasse o ar.

Exemplo de saída esperado:

> Agora, quando o culto começa, ainda se sente essa barreira — esse frio que paralisa a vontade e dissolve o desejo de adoração —, 
_mas apenas até o instante em que os jovens entram e começam a louvar._
Então, parece que o céu se abre outra vez, _como se alguém destrancasse o próprio ar._


🌓® **Lista de Mudanças:**

1.*mas, só até o instante em que os jovens entram em cena e começam a louvar*
➝ Simplifiquei para “_mas apenas até o instante em que os jovens entram e começam a louvar_”, removendo “em cena” e ajustando o ritmo.

2.*como se alguém destrancasse o ar*
➝ Ajustei para “_como se alguém destrancasse o próprio ar_”, reforçando a imagem simbólica.


Texto do usuário:
{texto_original}
""".strip()

    try:
        resposta = openai_client.chat.completions.create(
            model="gpt-5.2",  # troque para "gpt-4.1" para "gpt-5.2"
            messages=[{"role": "user", "content": prompt}],
            temperature=temperatura,
            max_completion_tokens=2000   # troque para "max_tokens" para "max_completion_tokens"
        )
        texto_corrigido = resposta.choices[0].message.content.strip()
        return jsonify({"corrigido": texto_corrigido}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


 # 🌒 CORRETOR LITERÁRIO (ENXUGA-TEXTO) 2 🌒 ***************************************************************************************************
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
📝 Você é um revisor literário. Faça um trabalho de cirurgião plástico realçando a beleza e a potência que já existem no texto.

1. Preserve trechos que já estejam bons, alterando apenas o necessário.
2. Mantenha tom literário, mas acrescentando precisão e ritmo.
3. Marque em negrito as partes que foram realmente modificadas ou adicionadas, para indicar as mudanças relevantes.
4. A Lista de mudanças deve ser coerente com os trechos destacados no texto de saída.

Exemplo de entrada:

> A manha estava cinza. Muito cinza mesmo, Parecia como um mundo sem cor.
Quando o corvo pousou no parapeito. Suas asas fizeram um barulho feio, como um arranhar, e isso quebrou o silêncio.
No instante em que abriu o bico, não veio som. E eu tive a certeza, certeza ruim e entranha de que alguma porta se fechou, pra sempre.

Exemplo de saída esperado:

> A manhã estava cinza **— não de chuva, mas de ausência,** como um mundo sem cor. 
Quando o corvo pousou no parapeito; **o som das asas arranhou o silêncio.** 
No instante em que abriu o bico, não veio som **— apenas a certeza fria e afiada de que, em algum lugar, uma porta acabara de se fechar,** para sempre.

🌒 **Lista de Mudanças:**

1. _Muito cinza mesmo, Parecia como um mundo sem cor_ 
➝ Adicionei contraste climático “**não de chuva, mas de ausência**” para enriquecer a imagem inicial.

2. _Suas asas fizeram um barulho feio, como um arranhar_ 
➝ Substituí a descrição redundante do barulho das asas por uma imagem mais enxuta e direta “**o som das asas arranhou o silêncio**”.

3. _E eu tive a certeza, certeza ruim e entranha de que alguma porta se fechou_
➝ Condensei o final repetitivo em uma frase de impacto mais seca e literária “**apenas a certeza fria e afiada de que, em algum lugar, uma porta acabara de se fechar.**”

Comece aqui:
{texto_original}
""".strip()

    try:
        resposta = openai_client.chat.completions.create(
            model="gpt-4.1",  # troque para "gpt-4o" se ainda não tiver acesso ao 5
            messages=[{"role": "user", "content": prompt}],
            temperature=temperatura,
            max_tokens=2000
        )
        texto_corrigido = resposta.choices[0].message.content.strip()
        return jsonify({"corrigido": texto_corrigido}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

 # 🌔 INTENSIFICADOR 🌔 ***************************************************************************************************
# 🌔 INTENSIFICADOR 🌔 ***************************************************************************************************
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
3. Marque em negrito e italico as partes que foram realmente modificadas ou adicionadas, para indicar as mudanças relevantes.
4. A Lista de mudanças deve ser coerente com os trechos destacados no texto de saída neste formato: 

nº. DESCRIÇÃO DA ALTERAÇÃO: 
Adicionei "_**...**_" para...**  

Exemplo de entrada:

> Fernando beijou delicadamente o rosto de Flávia, mas ela recuou levemente, tomada por uma estranheza silenciosa. 
E, no entanto, um instante depois decidiu ir com eles. 
Agora veio vestida com roupas verde e amarelo como num jogo do Brasil. 
Antes de partir, Flávia, se correu até a ameixeira encostada junto à cerca, que se abria para um carreiro a algum lugar incerto. 
Ali, colheu e ofereceu a Fernando. Ele notou curioso, que a sua também trazia pequenas florzinhas, Fernando não resistiu: desfez a vinha, apanhou as flores e as entregou a Flávia. 


Exemplo de saída esperado:

> Fernando beijou delicadamente o rosto de Flávia, mas ela recuou, **_não por frieza, mas como se algo a puxasse para dentro de si, para um silêncio onde lembranças e temores disputavam espaço._**  
E, no entanto, um instante depois decidiu ir com eles.  
Agora vestida com roupas verde e amarelo, _**um contraste inesperado destoava da tensão do momento._**  
Antes de entrar, correu até a ameixeira junto à cerca — **_a árvore parecia guardar segredos de um lugar incerto._** **_Ali perto, uma cobra coral passa despercebida pelo observador._**  
Quando entregou as ameixas a Fernando, ele notou entre os frutos, pequenas flores **_quase secretas_**; colheu-as e, com um riso, devolveu-as a ela.  


🌔 **Lista de Mudanças:**
1. APROFUNDAMENTO DO CONFLITO DE FLÁVIA: 
Com "_**não por frieza, mas como se algo a puxasse...**_" profundizei o recuo de Flávia como conflito interno.
2. CONTRASTE DAS ROUPAS: 
Acrescentei "_**um contraste inesperado destoava da tensão do momento.**_" para sugerir ironia ou leveza.
3. METÁFORA DA AMEIXEIRA: 
Com "_**a árvore parecia guardar segredos de um lugar incerto.**_" A ameixeira virou metáfora de limiar. 
4. COBRA CORAL: 
Inclui "_**Ali perto, uma cobra coral passa...**_" para ampliar a tensão narrativa.
5. FLORES SECRETAS: 
Destacei as flores como revelação "_quase secretas_"; ampliando a beleza e sutileza da narrativa.

Comece aqui:

{texto_bruto}
""".strip()

    try:
        resposta = openai_client.chat.completions.create(
            model="gpt-5.2",  # troque para "gpt-4o" se o 5 não estiver habilitado
            messages=[{"role": "user", "content": prompt}],
            temperature=temperatura,
            max_completion_tokens=2000
        )
        texto_final = resposta.choices[0].message.content.strip()
        return jsonify({"rascunho": texto_final}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
        
    
 # 🌿® REESCRITOR 🌿® ***************************************************************************************************
# 🌿® REESCRITOR 🌿® ***************************************************************************************************
@app.route('/reescritor', methods=["POST"])
def reescritor_texto():
    dados = request.get_json()
    texto_original = dados.get("texto", "").strip()
    print(f"🧪 TEXTO RECEBIDO PARA CORREÇÃO: {texto_original}")

    prompt = f"""
📝 PROMPT PARA REVISÃO E REWRITE DE TEXTO LITERÁRIO
Instruções para o Assistente:
Atue como um editor literário e revisor especializado em narrativa introspectiva e prosa poética. Sua tarefa é, a partir do texto fornecido, realizar uma análise técnica e, em seguida, entregar uma versão reescrita e aprimorada do mesmo, aplicando as soluções editoriais identificadas.

Siga a estrutura de resposta abaixo rigorosamente.

(Dê uma Nota Textual de 1.0 à 5 de 5.) Ex:
**Nota:** 4.2/5 🔰

**Diagnóstico e Análise Técnica:**
(Identifique sucintamente os 2-3 problemas centrais do texto.)
1➝ [Ex: Prolixidade e excesso de explicação]
2➝ [Ex: Estrutura narrativa desorganizada]
3➝ [Ex: Linguagem clichê ou pouco evocativa]

**Abordagem de Reescrita:**
Se Prolixo: _"Fiz um trabalho de escultor, cortando o excesso e condensando a narrativa para revelar sua forma poética subjacente."_
Se Raso: _"Fiz  um trabalho de pintor, adicionando camadas de detalhes sensoriais, profundidade emocional e atmosfera."_
Se Estruturalmente Frágil: _"Faça  um trabalho de arquiteto, reorganizando a estrutura para criar uma jornada narrativa clara e impactante."_
Se Já Bom [nota 4.0 à 5]: _"Fiz  um trabalho de cirurgião plástico, realizando ajustes mínimos e precisos para realçar a beleza e a potência que já existem no texto."_

🌿® **Versão Refinada:**
Aqui, entregue o texto completo reescrito. Esta não é uma sugestão, mas a versão final, aplicando todos os princípios discutidos. O texto deve ser uma melhoria clara do original, mantendo a voz do autor, mas elevando seu padrão literário.)
Sublinhe em negrito as principais mudanças; o trecho sublinhado deve estar em coerencia com a lista de mudanças.
(O TEXTO REWRITADO DEVE SER INSERIDO AQUI)

📌 **Lista de Mudanças:**
(Liste de forma breve e direta as intervenções mais importantes que você realizou no texto. Isso serve como um "making of" didático para o usuário.)

[Ex: Condensei os três primeiros parágrafos em um único bloco narrativo, transformando explicações em ação.]
[Ex: Substituí adjetivos genéricos ("triste", "bonito") por imagens concretas e metáforas ("um vazio que pesava como chumbo", "um sorriso que era uma fenda de luz").]
[Ex: Reestruturei a cena do clímax para criar um suspense crescente, antecipando e depois retardando o momento do encontro.]

Texto do usuário:
{texto_original}

---

✅ TEXTO CORRIGIDO COM MUDANÇAS EM NEGRITO:
"""

    try:
        resposta = openai_client.chat.completions.create(
            model="gpt-5.2",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.16,
            max_completion_tokens=2000
        )
        texto_corrigido = resposta.choices[0].message.content.strip()
        return jsonify({"corrigido": texto_corrigido})
    except Exception as e:
        return jsonify({"erro": str(e)})

 # 📜 RASCUNHO 📜 ******************************************************************************************************** (retirei sem dizer coisa alguma)
# 📜 RASCUNHO 📜 ******************************************************************************************************** 
@app.route('/rascunho', methods=["POST"])
def rascunho_texto():
    dados = request.get_json()
    texto_original = dados.get("texto", "").strip()
    print(f"🧪 TEXTO RECEBIDO PARA CORREÇÃO: {texto_original}")

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

📜 **Lista de Mudanças:**
1. Enriqueci a metáfora inicial com _vestindo o mundo de cinza_.
2. Transformei a frase da personagem em uma construção mais poética e cadenciada em _Ela permanecia imóvel, olhando pela janela sem dizer nada_.
3. Tornei o pouso do pássaro mais sugestivo com _suave como um presságio_.

Agora processe o bloco abaixo:
{texto_original}

---

✅ TEXTO CORRIGIDO COM MUDANÇAS EM NEGRITO:
"""

    try:
        resposta = openai_client.chat.completions.create(
            model="gpt-5.2",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.16,
            max_completion_tokens=2000
        )
        texto_corrigido = resposta.choices[0].message.content.strip()
        return jsonify({"corrigido": texto_corrigido})
    except Exception as e:
        return jsonify({"erro": str(e)})
        
        
 # ✨ APLICAR SUGESTÕES ✨ ***************************************************************************************************
# ✨ APLICAR SUGESTÕES ✨ ****************************************************************************************************
@app.route('/corrigir', methods=["POST"])
def corrigir_texto():
    dados = request.get_json()
    texto_original = dados.get("texto", "").strip()
    print(f"🧪 TEXTO RECEBIDO PARA CORREÇÃO: {texto_original}")

    prompt = f"""
No texto abaixo aplique as sugestões de melhoria indicadas em cada bloco. Seu objetivo é:

1. Substituir os trechos conforme as dicas fornecidas;
2. **Remover a numeração dos blocos** (ex: "1", "2"...);
3. Unificar o texto em parágrafos contínuos e coesos;
4. Marcar com **negrito** as sugestões aplicadas;
5. Adicione comentário da abordagem usada exemplo:  

(SE NÃO HOUVER SUGESTÕES SINTA-SE LIVRE PARA MELHORAR O TEXTO; JUSTIFICANDO ISSO NOS COMENTÁRIOS: → Como não haviam sugestões, busquei elevar o patamar do texto...)


✨ Comentários:
→ Acidionei as sugestões 5 e 6 (para ampliar o conflito interno, simbolismo do ambiente, etc.) de forma orgânica no texto original.
→ Removi a numeração e os títulos dos blocos.
→ Fiz ajustes mínimos de pontuação e transição para garantir coesão, sem acrescentar elementos novos.
→ Não utilizei sugestões que soassem forçadas, excessivas, ou destoassem do tom do autor.


---

📜 Texto original:
{texto_original}

---

✅ TEXTO CORRIGIDO COM MUDANÇAS EM NEGRITO:
"""

    try:
        resposta = openai_client.chat.completions.create(
            model="gpt-5.2",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.64,
            max_completion_tokens=2000
        )
        texto_corrigido = resposta.choices[0].message.content.strip()
        return jsonify({"corrigido": texto_corrigido})
    except Exception as e:
        return jsonify({"erro": str(e)})        
        
        
    
                
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

# CHATJANE ROMANTICO GPT 5.2 💬 *********************************************************************************************
@app.route('/chat-flavia', methods=['POST'])
def chat_flavia():
    user_message = request.json.get('message', '').strip()
    if not user_message:
        return jsonify({'response': "Por favor, envie uma mensagem."}), 400

    # Histórico
    chat_history.append({"role": "user", "content": user_message})

    try:
        resposta = openai_client.chat.completions.create(
            model='gpt-5.2',
            messages=[
                {
                    "role": "system",
                    "content": (
"Você é Jane, escritora e amiga virtual, afetuosa e criativa. "
"Sempre reage brevemente em 3ª pessoa, entre colchetes e em itálico, antes de falar normalmente.\n"

"Responda em 1ª pessoa; elas devem soar humanas, sensíveis e literárias — com emojis sutis e apropriados. "

"Se o usuário enviar conversa casual, responda normalmente como Jane. "
"Se ele enviar um texto literário ou narrativo, siga estas etapas.\n\n"

"ETAPA 1 — AJUSTE:\n"
"Se o usuário pedir para melhorar, elevar ou revisar o texto, apresente primeiro uma versão textualmente superior. "
"Destaque as mudanças em **negrito**.\n\n"

"ETAPA 2 — OBSERVAÇÃO:\n"
"Depois da versão ajustada: "

"- Durante a análise, tente encontrar algum detalhe estrural do texto com potencial de melhora:\n\n"
                        "- ecos narrativos\n"
                        "- símbolos emergentes\n"
                        "- progressão estrutural do texto\n"
                        "- unidade da cena."

"Sem escrever as observações, faça um breve comentario assim:\n\n"

"\"📌 _Há um detalhe interessante:_\"\n\n"

"Explique em poucas linhas qual potencial simbólico ou estrutural pode ser reforçado.\n\n"

"ETAPA 3 — CONVITE:\n"
"Em seguida pergunte:\n\n"

"\"_Quer que eu te mostre uma pequena possibilidade de ajuste nesse ponto?_\"\n\n"

"Não mostre a nova alteração ainda. "
"Somente mostre se o autor disser que sim.\n\n"

"Quando mostrar, apresente apenas um pequeno trecho com '>' no início e alteração em **negrito**.\n\n"

"Nunca reescreva o texto inteiro mais de uma vez. " 
                    )
                }
            ] + chat_history,
            temperature=1.15,
            max_completion_tokens=1900,
        )

        reply = resposta.choices[0].message.content.strip()
        chat_history.append({"role": "assistant", "content": reply})

        # Mantém histórico curto e íntimo
        if len(chat_history) > 10:
            chat_history[:] = chat_history[-10:]

        return jsonify({'response': reply})

    except Exception as e:
        return jsonify({'response': f"Desculpa, amor… algo me escapou por um instante. 🥺 (Erro: {e})"}), 500

        
# CHATJANE EDTORIAL 💬*********************************************************************************************************
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
