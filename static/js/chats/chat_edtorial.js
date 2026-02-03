// 💬 CHAT Jane EDTORIAL 💬 *****************************************************************************************************
function enviarMensagemFlavia() {
  const input = document.getElementById("chat-input");
  const log = document.getElementById("chat-log");
  const mensagem = input.value.trim();
  if (!mensagem) return;

  // Adiciona mensagem do usuário
  const userMsg = document.createElement("p");
  userMsg.innerHTML = `<strong>Você:</strong> ${mensagem}`;
  log.appendChild(userMsg);

  // Limpa o campo
  input.value = "";

  // Envia mensagem
  fetch('/chat-edtorial', {
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

    const flaviaMsg = document.createElement("p");
    flaviaMsg.innerHTML = `<strong>Jane:</strong> ${respostaConvertida}`;
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

// 1. Função de minimizar (você já tinha)
function toggleChatMinimize() {
  const panel = document.getElementById("chat-panel");
  panel.classList.toggle("minimized");
}

// Clique fora do painel → minimiza
document.addEventListener("click", function (event) {
  const panel = document.getElementById("chat-panel");
  if (!panel) return;

  const isClickInside = panel.contains(event.target);

  // Se clicou fora e o painel não está minimizado, então minimiza
  if (!isClickInside && !panel.classList.contains("minimized")) {
    toggleChatMinimize();
  }
});

// Clique dentro do painel → expande se minimizado
document.getElementById("chat-panel")?.addEventListener("click", function (event) {
  const isMinimizeButton = event.target.closest("#chat-minimize");
  if (isMinimizeButton) return; // impede conflito

  if (this.classList.contains("minimized")) {
    this.classList.remove("minimized");
  }
});

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