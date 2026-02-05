// FUNÇÕES ORDINÁRIAS ////////////////////////////////////////////////////////////////////////////////////////////////////

// 💬 CHATFLÁVIA 💬 *****************************************************************************************************
function enviarMensagemFlavia() {
  const input = document.getElementById("chat-input");
  const log = document.getElementById("chat-log");
  const mensagem = input.value.trim();
  if (!mensagem) return;

  // Adiciona mensagem do usuário
  const userMsg = document.createElement("p");
  const mensagemConvertida = markdownSimples(mensagem);
  userMsg.innerHTML = `<strong>Você:</strong> ${mensagemConvertida}`;

  log.appendChild(userMsg);
  log.scrollTop = log.scrollHeight;

  // Limpa o campo
  input.value = "";

  // Envia mensagem
  fetch('/chat-flavia', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: mensagem })
  })
  .then(res => res.json())
  .then(data => {
    const respostaOriginal = data?.response || ""; // 🔒 proteção contra undefined

    // Conversão simples de Markdown para HTML
    const respostaConvertida = respostaOriginal
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // **negrito**
      .replace(/\*(.*?)\*/g, "<em>$1</em>")             // *itálico*
      .replace(/_(.*?)_/g, "<em>$1</em>")               // _itálico_
      .replace(/\n/g, "<br>");                          // quebra de linha

    const flaviaMsg = document.createElement("div");
flaviaMsg.className = "chat-message ia";

flaviaMsg.innerHTML = `
  <div class="chat-bubble ia">
    <div class="chat-message-content">
      <strong>Jane:</strong><br>
      ${respostaConvertida}
    </div>
    <button class="copy-btn" title="Copiar resposta">📑</button>
  </div>
`;

log.appendChild(flaviaMsg);
log.scrollTop = log.scrollHeight;

  })
  .catch(err => {
    console.error("Erro no fetch:", err); // 👀 log no console para depurar
    const erroMsg = document.createElement("p");
    erroMsg.innerHTML = `<strong>Jane:</strong> (Erro ao responder 😢)`;
    log.appendChild(erroMsg);
  });
}

// 1. Função de minimizar
function toggleChatMinimize() {
  const panel = document.getElementById("chat-panel");
  if (!panel) return;
  panel.classList.toggle("minimized");
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

  const prompt = "💡 • _Fale reflexivamente deste texto, dividindo em blocos temáticos negritados:_ \n\n";

  // 1️⃣ Cola com contexto semântico
  chatInput.value = prompt + texto;

  // 2️⃣ Dispara o envio oficial
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

//CHAT = ENTER *********************************************************************************************************
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
    setTimeout(() => (botao.textContent = "📑"), 1000);
  });
});



