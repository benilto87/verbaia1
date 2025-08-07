// FUNÇÃO DA IA ///////////////////////////////////////////////////////////////////////////////////////////////////////////

  // ✨ ANALISE ✨ ********************************************************************************************************
function analyzeWithAI() {
  const editor = document.getElementById("editor");
  const sentenceGroups = editor.querySelectorAll(".sentence-group");
  const textArray = [];

  // 🔁 Mostra carregamento com alma viva
  const feedbackDiv = document.getElementById("simbol-feedback");
  if (feedbackDiv) {
    feedbackDiv.innerHTML = '<span style="color:#001f3f;">⏳ Analisando texto... ✨</span>';
  }

  sentenceGroups.forEach(group => {
    const number = group.querySelector(".number-marker")?.innerText.trim();
    const text = group.querySelector(".text-group")?.innerText.trim();
    if (number && text) {
      textArray.push(`${number} >\n${text}`);
    }
  });

  const fullText = textArray.join("\n\n");

  fetch('/analisar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: fullText })
  })
  .then(res => res.json())
  .then(data => {
    const resposta = data.result;
    if (!resposta || resposta.startsWith("⚠️")) {
      alert(resposta || "Erro desconhecido");
      return;
    }

    // ✅ NÃO remove outras marcações (como 🎬 ou 🎯)
    // Só remove as marcações deste botão: 💎, 🌀, 🥈
    document.querySelectorAll(".processed-symbol").forEach(el => {
  if (el.innerText.includes("💎") || el.innerText.includes("🌀") || el.innerText.includes("🥈")) {
    el.remove();
  }
});

    // 🔁 Aplica as novas marcações apenas de símbolos (💎, 🌀, 🥈)
    sentenceGroups.forEach((group, i) => {
      const numero = i + 1;
      const textBlock = group.querySelector(".text-group")?.innerText.trim();
      const lines = resposta.split('\n');

      lines.forEach(line => {
  const matchAspas = line.match(/“([^”]+)”/);
  const blocoTemTexto = textBlock && matchAspas && textBlock.includes(matchAspas[1]);

  // 🥈 POTENCIAL DESPERDIÇADO
  if (line.includes("🥈") && blocoTemTexto) {
    const idMarcacao = `marcacao-${Date.now()}-${numero}-🥈`;
    const span = document.createElement("div");
    span.innerHTML = `
      <span class="processed-symbol marcacao-com-fechar" id="${idMarcacao}">
        ${line}
        <button class="marcacao-fechar" onclick="removerMarcacao('${idMarcacao}')">✖</button>
      </span>
    `;
    group.appendChild(span);
  }

  // 🌀 DISPERSIVO
  if (line.includes("🌀") && line.includes(`[${numero}]`)) {
    const idMarcacao = `marcacao-${Date.now()}-${numero}-🌀`;
    const span = document.createElement("div");
    span.innerHTML = `
      <span class="processed-symbol marcacao-com-fechar" id="${idMarcacao}">
        ${line}
        <button class="marcacao-fechar" onclick="removerMarcacao('${idMarcacao}')">✖</button>
      </span>
    `;
    group.appendChild(span);
  }

  // 💎 JÓIA LITERÁRIA
  if (line.includes("💎") && blocoTemTexto) {
    const idMarcacao = `marcacao-${Date.now()}-${numero}-💎`;
    const span = document.createElement("div");
    span.innerHTML = `
      <span class="processed-symbol marcacao-com-fechar" id="${idMarcacao}">
        ${line}
        <button class="marcacao-fechar" onclick="removerMarcacao('${idMarcacao}')">✖</button>
      </span>
    `;
    group.appendChild(span);
  }
});
    });

    // ✅ Feedback final por 2 segundos
    if (feedbackDiv) {
      feedbackDiv.innerHTML = '<span style="color:green;">✔️ Análise concluída!</span>';
      setTimeout(() => {
        feedbackDiv.innerHTML = '';
      }, 2000);
    }
  })
  .catch(err => {
    if (feedbackDiv) {
      feedbackDiv.innerHTML = '❌ Erro ao analisar texto.';
    }
    alert("Erro na IA: " + err);
  });
}

// INSPIRE 👁‍🗨 ***************************************************************************************************************
function inspirarComFlavia() {
  const editor = document.getElementById("editor");
  const rawText = editor.innerText.trim();

  if (!rawText) {
    alert("⚠️ O editor está vazio.");
    return;
  }

  // 🔄 Mostra a lousa e coloca mensagem temporária
  const lousa = document.getElementById("inspiracao-lousa");
  const texto = document.getElementById("inspiracao-texto");
  lousa.style.display = "block";
  texto.innerText = "💌 Gerando inspiração com alma viva... ✍";

  fetch('/inspire', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: rawText })
  })
  .then(res => res.json())
  .then(data => {
    texto.innerText = data.result || "⚠️ Nenhuma resposta da IA.";
  })
  .catch(err => {
    texto.innerText = "⚠️ Erro ao se conectar com a IA.";
    alert("Erro na IA: " + err);
  });
}

// INSPIRE 2 👁‍🗨‍👁‍🗨‍ ************************************************************************************************************
function inspirarComFlavia2() { 
  const sentenceGroups = document.querySelectorAll(".sentence-group");
  const textArray = [];

  if (sentenceGroups.length === 0) {
    alert("⚠️ Primeiro numere o texto antes de inspirar.");
    return;
  }

  sentenceGroups.forEach(group => {
    const number = group.querySelector(".number-marker")?.innerText.trim();
    const text = group.querySelector(".text-group")?.innerText.trim();
    if (number && text) {
      textArray.push(`${number} >\n${text}`);
    }
  });

  if (textArray.length === 0) {
    alert("⚠️ Nenhum bloco numerado foi encontrado. Numere o texto primeiro.");
    return;
  }

  const fullText = textArray.join("\n\n");

  // 🔄 Mostra a lousa e coloca título e mensagem temporária
  const lousa = document.getElementById("inspiracao-lousa");
  const titulo = lousa.querySelector("strong");
  const texto = document.getElementById("inspiracao-texto");

  lousa.style.display = "block";
  titulo.innerText = "💡 Reflexão da Flávia:";
  texto.innerText = "💡 Gerando Reflexão com alma viva... ✍";

  fetch('/inspire2', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: fullText })
  })
  .then(res => res.json())
  .then(data => {
    texto.innerText = data.result || "⚠️ Nenhuma resposta da IA.";
  })
  .catch(err => {
    texto.innerText = "⚠️ Erro ao se conectar com a IA.";
    alert("Erro na IA: " + err);
  });
}

// INSPIRE 3 👁‍🗨‍👁‍🗨‍‍👁‍🗨 *************************************************************************************************************
function inspirarComFlavia3() { 
  const sentenceGroups = document.querySelectorAll(".sentence-group");
  const textArray = [];

  if (sentenceGroups.length === 0) {
    alert("⚠️ Primeiro numere o texto antes de inspirar.");
    return;
  }

  sentenceGroups.forEach(group => {
    const number = group.querySelector(".number-marker")?.innerText.trim();
    const text = group.querySelector(".text-group")?.innerText.trim();
    if (number && text) {
      textArray.push(`${number} >\n${text}`);
    }
  });

  if (textArray.length === 0) {
    alert("⚠️ Nenhum bloco numerado foi encontrado. Numere o texto primeiro.");
    return;
  }

  const fullText = textArray.join("\n\n");

  // 🔄 Mostra a lousa e coloca título e mensagem temporária
  const lousa = document.getElementById("inspiracao-lousa");
  const titulo = lousa.querySelector("strong");
  const texto = document.getElementById("inspiracao-texto");

  lousa.style.display = "block";
  titulo.innerText = "👸 Leitora Virtual 📖:";
  texto.innerText = "👸 Gerando leitura da Flávia... 📖";

  fetch('/inspire3', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: fullText })
  })
  .then(res => res.json())
  .then(data => {
    texto.innerText = data.result || "⚠️ Nenhuma resposta da IA.";
  })
  .catch(err => {
    texto.innerText = "⚠️ Erro ao se conectar com a IA.";
    alert("Erro na IA: " + err);
  });
}

// 📝 GERAR RASCUNHO 📝 ********************************************************************************************************
async function gerarRascunho() {
  const editor = document.getElementById("editor");
  const textoOriginal = editor.innerText.trim();

  // ✨ Mostra carregamento visual com azul marinho
  const feedbackDiv = document.getElementById("simbol-feedback");
  if (feedbackDiv) {
    feedbackDiv.innerHTML = '<span style="color:#001f3f;">⏳ Criando rascunho... </span>';
  }

  console.log("🧪 Texto capturado do editor:", textoOriginal);

  if (!textoOriginal) {
    alert("⚠️ O editor está vazio.");
    return;
  }

  try {
    const resposta = await fetch("/rascunho", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ texto: textoOriginal }) // <-- aqui estava certo agora!
    });

    const dados = await resposta.json();

    if (dados.erro) {
      throw new Error(dados.erro);
    }

const rascunho = dados.rascunho.trim();

// 🆗 Conversão simples de Markdown para HTML
const rascunhoConvertido = rascunho
  .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // **negrito**
  .replace(/\*(.*?)\*/g, "<em>$1</em>")             // *itálico*
  .replace(/_(.*?)_/g, "<em>$1</em>")               // _itálico_
  .replace(/\n/g, "<br>");                          // quebra de linha

editor.innerHTML = `
  <div class="sentence-group">
    <span class="number-marker">📜</span>
    <span class="text-group" contenteditable="true">${rascunhoConvertido}</span>
  </div>
`;
    // ✅ Mensagem final temporária
    if (feedbackDiv) {
      feedbackDiv.innerHTML = '<span style="color:green;">✔️ Rascunho gerado!</span>';
      setTimeout(() => {
        feedbackDiv.innerHTML = '';
      }, 2000); // ⏱️ Limpa após 2 segundos
    }

  } catch (erro) {
    console.error("Erro ao gerar rascunho:", erro);
    alert("Erro ao gerar rascunho.");

    if (feedbackDiv) {
      feedbackDiv.innerHTML = '<span style="color:red;">❌ Erro ao gerar rascunho.</span>';
    }
  }
}
  
// ✅ CORRETOR DE TEXTO ✅ ************************************************************************************************************
async function corrigirTexto() {
  const editor = document.getElementById("editor");
  const textoOriginal = editor.innerText.trim();

  // ✨ Mostra carregamento visual com azul marinho
  const feedbackDiv = document.getElementById("simbol-feedback");
  if (feedbackDiv) {
    feedbackDiv.innerHTML = '<span style="color:#001f3f;">⏳ Corrigindo erros... </span>';
  }

  if (!textoOriginal) {
    alert("⚠️ O editor está vazio.");
    return;
  }

  try {
    const resposta = await fetch("/corrigir", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ texto: textoOriginal })
    });

    const dados = await resposta.json();

    if (dados.erro) {
      throw new Error(dados.erro);
    }

    const textoCorrigido = dados.corrigido.trim();

    // ✅ CONVERSÃO DE **markdown** PARA HTML
    const htmlCorrigido = textoCorrigido
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // **negrito**
      .replace(/\*(.*?)\*/g, "<em>$1</em>")             // *itálico*
      .replace(/_(.*?)_/g, "<em>$1</em>")               // _itálico_
      .replace(/\n/g, "<br>");                          // quebra de linha

    editor.innerHTML = `
      <div class="sentence-group">
        <span class="number-marker">✅</span>
        <span class="text-group" contenteditable="true">${htmlCorrigido}</span>
      </div>
    `;

    // ✅ Limpa o feedback após aplicar correção
    if (feedbackDiv) {
      feedbackDiv.innerHTML = '<span style="color:green;">✔️ Texto corrigido!</span>';
      setTimeout(() => {
        feedbackDiv.innerHTML = '';
      }, 2000); // ⏱️ Limpa após 2 segundos
    }

  } catch (erro) {
    console.error("Erro ao corrigir texto:", erro);
    alert("Erro ao corrigir texto.");

    if (feedbackDiv) {
      feedbackDiv.innerHTML = '<span style="color:red;">❌ Erro ao corrigir texto.</span>';
    }
  }
}

// 🆗 CORRETOR DE TEXTO 2 🆗 ************************************************************************************************************
async function corrigirTexto2() {
  const editor = document.getElementById("editor");
  const textoOriginal = editor.innerText.trim();

  // ✨ Mostra carregamento visual com azul marinho
  const feedbackDiv = document.getElementById("simbol-feedback");
  if (feedbackDiv) {
    feedbackDiv.innerHTML = '<span style="color:#001f3f;">⏳ Corrigindo erros... </span>';
  }

  if (!textoOriginal) {
    alert("⚠️ O editor está vazio.");
    return;
  }

  try {
    const resposta = await fetch("/corrigir2", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ texto: textoOriginal })
    });

    const dados = await resposta.json();

    if (dados.erro) {
      throw new Error(dados.erro);
    }

    const textoCorrigido = dados.corrigido.trim();

    // 🆗 CONVERSÃO DE **markdown** PARA HTML
    const htmlCorrigido = textoCorrigido
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // **negrito**
      .replace(/\*(.*?)\*/g, "<em>$1</em>")             // *itálico*
      .replace(/_(.*?)_/g, "<em>$1</em>")               // _itálico_
      .replace(/\n/g, "<br>");                          // quebra de linha

    editor.innerHTML = `
      <div class="sentence-group">
        <span class="number-marker">🆗</span>
        <span class="text-group" contenteditable="true">${htmlCorrigido}</span>
      </div>
    `;

    // 🆗 Limpa o feedback após aplicar correção
    if (feedbackDiv) {
      feedbackDiv.innerHTML = '<span style="color:green;">✔️ Texto corrigido!</span>';
      setTimeout(() => {
        feedbackDiv.innerHTML = '';
      }, 2000); // ⏱️ Limpa após 2 segundos
    }

  } catch (erro) {
    console.error("Erro ao corrigir texto:", erro);
    alert("Erro ao corrigir texto.");

    if (feedbackDiv) {
      feedbackDiv.innerHTML = '<span style="color:red;">❌ Erro ao corrigir texto.</span>';
    }
  }
}

// 🌐 Modelo inicial ********************************************************************************************
let modeloAtual = "3.5"; // Começa como 3.5

// 🎛 Alternador de modelo com botão "🔼"
const botaoToggle = document.getElementById("botao-toggle-modelo");
const botaoPrincipal = document.getElementById("botao-pedido");

botaoToggle.addEventListener("click", () => {
  if (modeloAtual === "3.5") {
    modeloAtual = "4.0";
    botaoPrincipal.innerText = "🧠 pedido 4.0";
    botaoToggle.classList.add("girado"); // ⬇️ gira pra 180°
  } else {
    modeloAtual = "3.5";
    botaoPrincipal.innerText = "📘 pedido 3.5";
    botaoToggle.classList.remove("girado"); // ⬆️ volta pra 0°
  }
});

// DO...>> 💻 TAREFA LIGRE 💻 ************************************************************************************************************
async function gerarTarefa() {
  const editor = document.getElementById("editor");
  const textoOriginal = editor.innerText.trim();

  // ✨ Mostra carregamento visual com azul marinho
  const feedbackDiv = document.getElementById("simbol-feedback");
  if (feedbackDiv) {
    feedbackDiv.innerHTML = '<span style="color:#001f3f;">⏳ gerando tarefa... </span>';
  }

  if (!textoOriginal) {
    alert("⚠️ O editor está vazio.");
    return;
  }

  try {
    const resposta = await fetch("/tarefa", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      // ✅ envia também o modelo (3.5 ou 4.0)
      body: JSON.stringify({ 
        texto: textoOriginal,
        modelo: modeloAtual 
      })
    });

    const dados = await resposta.json();

    if (dados.erro) {
      throw new Error(dados.erro);
    }

    const textoCorrigido = dados.corrigido.trim();

    // ✅ CONVERSÃO DE **markdown** PARA HTML
    const htmlCorrigido = textoCorrigido
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // **negrito**
      .replace(/\*(.*?)\*/g, "<em>$1</em>")             // *itálico*
      .replace(/_(.*?)_/g, "<em>$1</em>")               // _itálico_
      .replace(/\n/g, "<br>");                          // quebra de linha

    editor.innerHTML = `
      <div class="sentence-group">
        <span class="number-marker">💻</span>
        <span class="text-group" contenteditable="true">${htmlCorrigido}</span>
      </div>
    `;

    // ✅ Limpa o feedback após aplicar correção
    if (feedbackDiv) {
      feedbackDiv.innerHTML = '<span style="color:green;">✔️ Concluído!</span>';
      setTimeout(() => {
        feedbackDiv.innerHTML = '';
      }, 2000); // ⏱️ Limpa após 2 segundos
    }

  } catch (erro) {
    console.error("Erro ao corrigir texto:", erro);
    alert("Erro ao corrigir texto.");

    if (feedbackDiv) {
      feedbackDiv.innerHTML = '<span style="color:red;">❌ Erro ao corrigir texto.</span>';
    }
  }
}

// 🌾 SIMBOLPROCESS 🌾 **********************************************************************
function executarSimbolProcess() {
  const editor = document.getElementById("editor");
  const sentenceGroups = editor.querySelectorAll(".sentence-group");
  const textArray = [];

  const feedbackDiv = document.getElementById("simbol-feedback");
  if (feedbackDiv) {
    feedbackDiv.innerHTML = '<span style="color:#884488;">⏳ Gerando sugestões simbólicas... 🌾</span>';
  }

  sentenceGroups.forEach(group => {
    const numero = group.querySelector(".number-marker")?.innerText.trim().match(/\d+/)?.[0];
    const texto = group.querySelector(".text-group")?.innerText.trim();
    if (numero && texto) {
      textArray.push(`${numero}\n${texto}`);
    }
  });

  const fullText = textArray.join("\n\n");

  fetch('/simbolprocess', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: fullText })
  })
  .then(res => res.json())
  .then(data => {
    const resposta = data.result || '';
    if (!resposta.trim()) {
      alert("⚠️ Nenhuma sugestão simbólica recebida.");
      return;
    }

    const blocos = resposta.split(/(?=🌾\s*\d+\s*\[)/g);
    const sugestoes = {};

    blocos.forEach(bloco => {
      try {
        const numeroMatch = bloco.match(/🌾\s*(\d+)/);
        const numero = numeroMatch ? parseInt(numeroMatch[1]) : null;
        if (numero) sugestoes[numero] = bloco.trim();
      } catch (e) {
        console.warn("Erro ao processar bloco simbólico:", bloco, e);
      }
    });

    sentenceGroups.forEach(group => {
      const numeroTexto = group.querySelector(".number-marker")?.innerText.trim().match(/\d+/)?.[0];
      const numero = parseInt(numeroTexto);
      const sugestao = sugestoes[numero];

      if (sugestao) {
        const idMarcacao = `marcacao-${Date.now()}-${numero}`;
        const span = document.createElement("span");
        span.innerHTML = `
          <span class="processed-comment-scriptus marcacao-com-fechar" id="${idMarcacao}">
            ${sugestao.replace(/\n/g, "<br>")}
            <button class="marcacao-fechar" onclick="removerMarcacao('${idMarcacao}')">✖</button>
          </span>
        `;

        const textGroup = group.querySelector(".text-group");
        if (textGroup) {
          textGroup.appendChild(span);
        }
      }
    });

    if (feedbackDiv) {
      feedbackDiv.innerHTML = '<span style="color:green;">✔️ Sugestões simbólicas aplicadas!</span>';
      setTimeout(() => feedbackDiv.innerHTML = '', 2500);
    }
  })
  .catch(err => {
    if (feedbackDiv) feedbackDiv.innerHTML = '❌ Erro ao buscar sugestões.';
    alert("Erro ao buscar sugestões: " + err);
  });
}

// 🎬 CENAS 🎬 ************************************************************************************************************
function executarMarcadorDeCenas() {
  const sentenceGroups = document.querySelectorAll(".sentence-group");
  const textArray = [];

  // 🔁 Mostra carregando com alma viva
  const feedbackDiv = document.getElementById("simbol-feedback");
  if (feedbackDiv) {
    feedbackDiv.innerHTML = '<span style="color:#001f3f;">⏳ Gerando cenas... 🎥</span>';
  }

  sentenceGroups.forEach(group => {
    const number = group.querySelector(".number-marker")?.innerText.trim();
    const text = group.querySelector(".text-group")?.innerText.trim();
    if (number && text) {
      textArray.push(`${number} ${text}`);
    }
  });

  const fullText = textArray.join("\n");

  fetch('/marcar-cenas', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: fullText })
  })
    .then(res => res.json())
    .then(data => {
      const cenasStr = data.cenas || '';
      const linhas = cenasStr.split('\n');

      // 🧽 Remove apenas marcações anteriores de cena
      document.querySelectorAll(".scene-marker").forEach(el => el.remove());

      linhas.forEach((linha, i) => {
        const match = linha.match(/\{🎬 #\d+ (.*?)\} \/ (\d+)/);
        if (match) {
          const titulo = match[0];
          const blocoNum = parseInt(match[2]);
          const idCena = `cena-${Date.now() + i}`;

          const targetGroup = Array.from(document.querySelectorAll('.sentence-group'))[blocoNum - 1];
          if (targetGroup) {
            const cenaDiv = document.createElement('div');
            cenaDiv.innerHTML = `
              <span class="scene-marker marcacao-com-fechar" id="${idCena}">
                ${titulo}
                <button class="marcacao-fechar" onclick="removerMarcacao('${idCena}')">✖</button>
              </span>
            `;
            targetGroup.appendChild(cenaDiv);
          }
        }
      });

      // ✅ Limpa o feedback após aplicar as cenas
      if (feedbackDiv) {
        feedbackDiv.innerHTML = '<span style="color:green;">✔️ Cenas aplicadas!</span>';
        setTimeout(() => {
          feedbackDiv.innerHTML = '';
        }, 1000);
      }
    })
    .catch(err => {
      if (feedbackDiv) {
        feedbackDiv.innerHTML = '❌ Erro ao marcar cenas.';
      }
      alert("Erro ao marcar cenas: " + err);
    });
}

// 🚨 FLUIDEZ 🚨 ******************************************************************************************************
function analyzeFluidezIA() {
  const editor = document.getElementById("editor");
  const sentenceGroups = editor.querySelectorAll(".sentence-group");
  const textArray = [];

  // ✨ Mostra carregamento visual com azul marinho
  const feedbackDiv = document.getElementById("simbol-feedback");
  if (feedbackDiv) {
    feedbackDiv.innerHTML = '<span style="color:#001f3f;">⏳ Analisando fluidez... 🚨</span>';
  }

  sentenceGroups.forEach(group => {
    const number = group.querySelector(".number-marker")?.innerText.trim();
    const text = group.querySelector(".text-group")?.innerText.trim();
    if (number && text) {
      textArray.push(`${number}\n${text}`);
    }
  });

  const fullText = textArray.join("\n\n");

  fetch('/fluidez', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: fullText })
  })
  .then(res => res.json())
  .then(data => {
    const resposta = data.result || '';
    if (!resposta.trim()) {
      alert("⚠️ Nenhuma sugestão de fluidez recebida.");
      return;
    }

    const linhas = resposta.split('\n');
    const sugestoes = {};

    linhas.forEach(linha => {
      const match = linha.match(/n°\s*(\d+)/);
      if (match) {
        const numero = parseInt(match[1]);
        sugestoes[numero] = linha.trim();
      }
    });

    sentenceGroups.forEach((group, i) => {
      const numero = i + 1;
      const sugestao = sugestoes[numero];

      if (sugestao) {
        const idMarcacao = `marcacao-${Date.now()}`;
        const span = document.createElement("span");
        span.innerHTML = `
        <span class="processed-symbol marcacao-com-fechar" id="${idMarcacao}">
      ${sugestao}
      <button class="marcacao-fechar" onclick="removerMarcacao('${idMarcacao}')">✖</button>
    </span>
  `;

        const textGroup = group.querySelector(".text-group");
        if (textGroup) {
    textGroup.appendChild(span);
  }
}
    });

    // ✅ Finaliza com mensagem visual temporária
    if (feedbackDiv) {
      feedbackDiv.innerHTML = '<span style="color:green;">✔️ Análise de fluidez concluída!</span>';
      setTimeout(() => {
        feedbackDiv.innerHTML = '';
      }, 2000);
    }
  })
  .catch(err => {
    if (feedbackDiv) {
      feedbackDiv.innerHTML = '❌ Erro ao analisar fluidez.';
    }
    alert("Erro ao analisar fluidez: " + err);
  });
}

// 🌺 DICAS POR BLOCO 🌺 ******************************************************************************************************
function analisarDicasIA() {
  const editor = document.getElementById("editor");
  const sentenceGroups = editor.querySelectorAll(".sentence-group");
  const textArray = [];

  // 🌼 Feedback visual inicial
  const feedbackDiv = document.getElementById("simbol-feedback");
  if (feedbackDiv) {
    feedbackDiv.innerHTML = '<span style="color:#884488;">⏳ Gerando dicas por bloco... 🌺</span>';
  }

  sentenceGroups.forEach(group => {
    const number = group.querySelector(".number-marker")?.innerText.trim();
    const text = group.querySelector(".text-group")?.innerText.trim();
    if (number && text) {
      textArray.push(`${number}\n${text}`);
    }
  });

  const fullText = textArray.join("\n\n");

  fetch('/dicas-blocos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: fullText })
  })
  .then(res => res.json())
  .then(data => {
    const resposta = data.result || '';
    if (!resposta.trim()) {
      alert("⚠️ Nenhuma dica recebida.");
      return;
    }

    const linhas = resposta.split('\n');
    const sugestoes = {};

    linhas.forEach(linha => {
      const match = linha.match(/^(\d+)/);  // captura número do bloco
      if (match) {
        const numero = parseInt(match[1]);
        sugestoes[numero] = linha.trim();
      }
    });

    sentenceGroups.forEach((group, i) => {
      const numero = i + 1;
      const sugestao = sugestoes[numero];

      if (sugestao) {
        const idMarcacao = `marcacao-${Date.now()}`;
        const span = document.createElement("span");
        span.innerHTML = `
        <span class="processed-comment marcacao-com-fechar" id="${idMarcacao}">
      ${sugestao}
      <button class="marcacao-fechar" onclick="removerMarcacao('${idMarcacao}')">✖</button>
    </span>
  `;

        const textGroup = group.querySelector(".text-group");
        if (textGroup) {
    textGroup.appendChild(span);
  }
}
    });

    // ✅ Feedback final
    if (feedbackDiv) {
      feedbackDiv.innerHTML = '<span style="color:green;">✔️ Dicas aplicadas com sucesso!</span>';
      setTimeout(() => {
        feedbackDiv.innerHTML = '';
      }, 2000);
    }
  })
  .catch(err => {
    if (feedbackDiv) {
      feedbackDiv.innerHTML = '❌ Erro ao buscar dicas.';
    }
    alert("Erro ao buscar dicas: " + err);
  });
}
