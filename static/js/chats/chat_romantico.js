// FUNÇÕES ORDINÁRIAS ////////////////////////////////////////////////////////////////////////////////////////////////////
let sufixoOculto = ""; // guarda o texto que não deve aparecer no input
let ultimaPosicaoAntesMinimizar = null; 

// 💬 CHATFLÁVIA 💬 *****************************************************************************************************
function enviarMensagemFlavia() {
  const input = document.getElementById("chat-input");
  const log = document.getElementById("chat-log");

  // Pega a mensagem visível do input
  let mensagem = input.value.trim();

  // Se não há mensagem e também não há sufixo oculto, não faz nada
  if (!mensagem && !sufixoOculto) return;

  // Se existe um sufixo oculto, anexa à mensagem e depois limpa a variável
  if (sufixoOculto) {
    mensagem += sufixoOculto;      // concatena o conteúdo oculto
    sufixoOculto = "";              // limpa para não interferir em outras mensagens
  }

  // Agora 'mensagem' contém tudo (visível + oculto) que será enviado ao servidor

  // Adiciona a mensagem do usuário no log (apenas a parte visível, para não poluir)
  const userMsg = document.createElement("p");
  const mensagemConvertida = markdownSimples(input.value.trim()); // só o que estava no input
  userMsg.innerHTML = `<strong>Você:</strong> ${mensagemConvertida}`;
  log.appendChild(userMsg);
  log.scrollTop = log.scrollHeight;

  // Limpa o campo de input
  input.value = "";

  // Envia a mensagem COMPLETA (com o sufixo) para o servidor
  fetch('/chat-flavia', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: mensagem })   // aqui vai com o sufixo
  })
  .then(res => res.json())
  .then(data => {
    const respostaOriginal = data?.response || "";

    // Conversão simples de Markdown para HTML
    const respostaConvertida = respostaOriginal
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
      .replace(/_(.*?)_/g, "<em>$1</em>")
      .replace(/\n/g, "<br>");

    const flaviaMsg = document.createElement("div");
    flaviaMsg.className = "chat-message ia";
    flaviaMsg.innerHTML = `
      <div class="chat-bubble ia">
        <div class="chat-message-content">
          <strong>Jane:</strong><br>
          ${respostaConvertida}
        </div>
        <button class="copy-btn" title="Copiar resposta">📋</button>
      </div>
    `;

    log.appendChild(flaviaMsg);
    log.scrollTop = log.scrollHeight;
  })
  .catch(err => {
    console.error("Erro no fetch:", err);
    const erroMsg = document.createElement("p");
    erroMsg.innerHTML = `<strong>Jane:</strong> (Erro ao responder 😢)`;
    log.appendChild(erroMsg);
  });
}

// 1. Função de minimizar
function toggleChatMinimize() {
  const panel = document.getElementById("chat-panel");
  if (!panel) return;

  if (!panel.classList.contains("minimized")) {
    // Vai minimizar: salva posição atual e remove estilos inline de left/top
    const left = panel.style.left;
    const top = panel.style.top;
    if (left && top) {
      ultimaPosicaoAntesMinimizar = { left, top };
    } else {
      ultimaPosicaoAntesMinimizar = null; // não havia posição salva
    }
    // Remove left/top inline para que o CSS com right: 52px funcione
    panel.style.left = '';
    panel.style.top = '';
    panel.classList.add("minimized");
  } else {
    // Vai expandir: restaura posição anterior se existir
    panel.classList.remove("minimized");
    if (ultimaPosicaoAntesMinimizar) {
      panel.style.left = ultimaPosicaoAntesMinimizar.left;
      panel.style.top = ultimaPosicaoAntesMinimizar.top;
    } else {
      // Se não tinha posição salva, garante que left/top fiquem vazios (usa CSS padrão)
      panel.style.left = '';
      panel.style.top = '';
    }
  }
}

// 2. Botão minimizar (controle direto)
document.getElementById("chat-minimize")?.addEventListener("click", function (e) {
  e.stopPropagation(); // 🔥 impede conflito com clique global
  toggleChatMinimize();
});

// 3. Clique fora do painel → minimiza
document.addEventListener("click", function (event) {
  const panel = document.getElementById("chat-panel");
  if (!panel) return;

  const isClickInside = panel.contains(event.target);

  if (!isClickInside && !panel.classList.contains("minimized")) {
    toggleChatMinimize();
  }
});

// 4. Clique dentro do painel → expande se estiver minimizado
document.getElementById("chat-panel")?.addEventListener("click", function (event) {
  const isMinimizeButton = event.target.closest("#chat-minimize");
  if (isMinimizeButton) return; // não interfere no botão

  if (this.classList.contains("minimized")) {
    this.classList.remove("minimized");
  }
});

document.getElementById("chat-opinion")?.addEventListener("click", function () {
  const editor = document.getElementById("editor");
  const chatInput = document.getElementById("chat-input");

  if (!editor || !chatInput) return;

  const texto = editor.innerText.trim();
  if (!texto) return;

  const promptVisivel = "💡 • _Fale reflexivamente deste texto, dividindo em blocos temáticos negritados:_ \n\n";

  // Parte oculta (só será enviada)
  sufixoOculto = "\n\n(ESSA INSTRUÇÃO SÓ VOCÊ VÊ, O USUÁRIO NÃO: Encerre com um pergunta: _Sabe o que eu mais achei legal no seu texto?_ Se ele consetir responda na msg seguinte)";

  // Coloca no input apenas o visível + o texto do editor
  chatInput.value = promptVisivel + texto;

  // Dispara o envio (a função modificada vai usar o sufixoOculto)
  enviarMensagemFlavia();
});

document.getElementById("chat-reescrita")?.addEventListener("click", function () {
  const editor = document.getElementById("editor");
  const chatInput = document.getElementById("chat-input");

  if (!editor || !chatInput) return;

  const texto = editor.innerText.trim();
  if (!texto) return;

  const prompt = "✍️ • _Tente subir o nível deste texto, sublinhe as mudanças em negrito para eu ver melhor:_ \n\n";

  // 1️⃣ Cola com contexto semântico
  chatInput.value = prompt + texto;

  // 2️⃣ Dispara o envio oficial
  enviarMensagemFlavia();
});

document.getElementById("chat-leitura")?.addEventListener("click", function () {
  const editor = document.getElementById("editor");
  const chatInput = document.getElementById("chat-input");

  if (!editor || !chatInput) return;

  const texto = editor.innerText.trim();
  if (!texto) return;

  // Parte visível (o que vai aparecer no input)
  const promptVisivel = "👸 • _Faça uma exposição emocional (expressando suas sensações) deste texto. O fechamento deve ser poético-reflexivo..._\n\n";
  
  // Parte oculta (só será enviada)
  sufixoOculto = "\n\n(ESSA INSTRUÇÃO SÓ VOCÊ VÊ, O USUÁRIO NÃO: Encerre com um pergunta: _Sabe o que eu mais achei legal no seu texto?_ Se ele consetir responda na msg seguinte)";

  // Coloca no input apenas o visível + o texto do editor
  chatInput.value = promptVisivel + texto;

  // Dispara o envio (a função modificada vai usar o sufixoOculto)
  enviarMensagemFlavia();
});

// 🎑 TROCAR FOTOS 🎑 ***********************************************************************************************
  
const fotosFlavia = [
  "static/img/flavia1.jpg",
  "static/img/flavia2.jpg",
  "static/img/flavia3.jpg",
];

let indexAtual = 0;

function trocarFotoFlavia() {
  indexAtual = (indexAtual + 1) % fotosFlavia.length;

  const imgFlavia = document.querySelector('#chat-panel img');
  const chatPanel = document.getElementById('chat-panel');

  if (imgFlavia && chatPanel) {
    // Início do efeito fade-out
    imgFlavia.style.opacity = '0.3';
    chatPanel.style.transition = 'background-image 0.6s ease-in-out, opacity 0.6s ease-in-out';
    chatPanel.style.opacity = '0.4';

    setTimeout(() => {
      // Troca imagens
      imgFlavia.src = fotosFlavia[indexAtual];
      chatPanel.style.backgroundImage = `
        linear-gradient(180deg, rgba(255, 192, 203, 0.15), rgba(138, 43, 226, 0.15)),
        url('${fotosFlavia[indexAtual]}')`;

      // Volta com fade-in
      imgFlavia.style.opacity = '1';
      chatPanel.style.opacity = '1';
    }, 116); // tempo da transição
  }
}

// Troca a cada 3 minutos (180.000 ms)
setInterval(trocarFotoFlavia, 90000);

// ✨ Autoexpandir altura do campo symbolInput enquanto digita
window.addEventListener('DOMContentLoaded', () => {
  const chatPanel = document.getElementById('chat-panel');
  const img = new Image();
  img.src = fotosFlavia[0]; // primeira imagem padrão

  chatPanel.classList.add("carregando");

  img.onload = () => {
    chatPanel.style.backgroundImage = `
      linear-gradient(180deg, rgba(255, 192, 203, 0.15), rgba(138, 43, 226, 0.15)),
      url('${img.src}')`;
    chatPanel.classList.remove("carregando");
  };

  const input = document.getElementById('symbolInput');
  if (input) {
    input.addEventListener('input', () => {
      input.style.height = 'auto'; // Zera antes para recalcular
      input.style.height = input.scrollHeight + 'px'; // Ajusta à altura real
    });
  }
});

//CHAT = ENTER **********************************************************************************************************
document.getElementById('chat-input').addEventListener('keydown', function (e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault(); // Impede quebra de linha
    enviarMensagemFlavia(); // Chama a função de envio
  }
});

document.addEventListener("click", function (event) {
  const botao = event.target.closest(".copy-btn");
  if (!botao) return;

  event.stopPropagation();

  const mensagem = botao.closest(".chat-message");
  const conteudo = mensagem.querySelector(".chat-message-content");
  if (!conteudo) return;

  const html = conteudo.innerHTML;
  const texto = conteudo.innerText;

  const item = new ClipboardItem({
    "text/html": new Blob([html], { type: "text/html" }),
    "text/plain": new Blob([texto], { type: "text/plain" })
  });

  navigator.clipboard.write([item]).then(() => {
    botao.textContent = "✔";
    setTimeout(() => (botao.textContent = "📋"), 1000);
  });
});

// MOVER CHAT

// Arrastar o chat (drag)
(function() {
  const panel = document.getElementById('chat-panel');
  if (!panel) return;

  let isDragging = false;
  let offsetX, offsetY;

  // Tenta encontrar um elemento que sirva como "alça" de arrasto.
  // Se existir um elemento com a classe .chat-header, usa ele.
  // Caso contrário, usa o próprio painel, mas com proteção para não arrastar ao clicar em botões.
  const header = panel.querySelector('.chat-header');
  const dragHandle = header || panel;

  dragHandle.addEventListener('mousedown', startDrag);

  function startDrag(e) {
    if (panel.classList.contains("minimized")) return;
	// Se o clique foi em um elemento interativo (botão, input, etc.), não inicia o arrasto
    if (e.target.closest('button, input, textarea, select, a')) return;

    e.preventDefault(); // Evita seleção de texto acidental

    isDragging = true;
    const rect = panel.getBoundingClientRect();
    offsetX = e.clientX - rect.left;
    offsetY = e.clientY - rect.top;

    panel.style.cursor = 'grabbing';
    panel.style.userSelect = 'none'; // Impede seleção de texto durante o movimento
  }

  document.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    e.preventDefault();

    let left = e.clientX - offsetX;
    let top = e.clientY - offsetY;

    // Opcional: limita o movimento à janela (evita que suma)
    const winWidth = window.innerWidth;
    const winHeight = window.innerHeight;
    const panelWidth = panel.offsetWidth;
    const panelHeight = panel.offsetHeight;

    left = Math.max(0, Math.min(left, winWidth - panelWidth));
    top = Math.max(0, Math.min(top, winHeight - panelHeight));

    panel.style.left = left + 'px';
    panel.style.top = top + 'px';
    panel.style.position = 'fixed'; // Garante que está posicionado de forma absoluta na tela
  });

  document.addEventListener('mouseup', () => {
    if (isDragging) {
      isDragging = false;
      panel.style.cursor = '';
      panel.style.userSelect = '';
    }
  });
})();

