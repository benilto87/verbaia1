// FUNÇÕES ORDINÁRIAS ////////////////////////////////////////////////////////////////////////////////////////////////////

// ABAS NA LOUSA 📋 *************************************************************************************************
 
let lousas = {};
let lousaAtual = null;
let proximaLousaId = 1;

function criarNovaAba() {
  const novaId = `lousa-${proximaLousaId++}`;
  lousas[novaId] = document.getElementById("editor").innerHTML || ""; // mantém texto se houver
  lousaAtual = novaId;

  atualizarAbas();
  carregarConteudoAtual();
}

function atualizarAbas() {
  const abasContainer = document.getElementById("abas-container");
  abasContainer.innerHTML = "";

  for (const id in lousas) {
    const botao = document.createElement("button");
    botao.className = "tab-button" + (id === lousaAtual ? " active" : "");

    if (id === lousaAtual) {
      // Coloca o nome + X dentro do botão
      botao.innerHTML = `${id} <span class="fechar-x">×</span>`;
      botao.querySelector(".fechar-x").onclick = (e) => {
        e.stopPropagation(); // evita ativar a aba
        deletarAba(id);
      };
    } else {
      botao.textContent = id;
    }

    botao.onclick = () => {
      salvarConteudoAtual();
      lousaAtual = id;
      carregarConteudoAtual();
      atualizarAbas();
    };

    abasContainer.appendChild(botao);
  }

  const botaoNova = document.createElement("button");
  botaoNova.className = "tab-button";
  botaoNova.innerHTML = "➕";
  botaoNova.onclick = criarNovaAba;
  abasContainer.appendChild(botaoNova);
}

// ❌ DELETAR ABAS NA LOUSA 📋 ********************************************************

function deletarAba(id) {
  if (confirm(`Tem certeza que deseja fechar ${id}?`)) {
    delete lousas[id];

    // Se deletar a aba atual, vai para outra
    const idsRestantes = Object.keys(lousas);
    lousaAtual = idsRestantes.length > 0 ? idsRestantes[0] : null;

    carregarConteudoAtual();
    atualizarAbas();
  }
}

function salvarConteudoAtual() {
  if (lousaAtual) {
    const editor = document.getElementById("editor");
    lousas[lousaAtual] = editor.innerHTML;
  }
}

function carregarConteudoAtual() {
  const editor = document.getElementById("editor");
  if (lousaAtual && lousas[lousaAtual] !== undefined) {
    editor.innerHTML = lousas[lousaAtual];
  } else {
    editor.innerHTML = "";
  }
}

// NEGRITO E ITALICO N&I E ALINHAMENTOS 📍************************************************************************************************

function aplicarNegrito() {
  document.execCommand('bold');
}

function aplicarItalico() {
  document.execCommand('italic');
}

document.addEventListener('keydown', function (e) {
  if (e.ctrlKey && e.key === 'b') {
    e.preventDefault();
    aplicarNegrito();
  }
  if (e.ctrlKey && e.key === 'i') {
    e.preventDefault();
    aplicarItalico();
  }
});

function centralizarTexto() {
  document.execCommand('justifyCenter');
}

function alinharEsquerda() {
  document.execCommand('justifyLeft');
}

function alinharDireita() {
  document.execCommand('justifyRight');
}

function justificarTexto() {
  document.execCommand('justifyFull');
}

// ALTERNA CAIXA "aA" *********************************************************************************************************
function alternarCaixa() {
  const selection = window.getSelection();
  if (!selection.rangeCount) return;

  const range = selection.getRangeAt(0);

  const startOffset = range.startOffset;
  const endOffset = range.endOffset;
  const container = range.startContainer;

  if (container.nodeType !== 3) return; // Garante que seja texto puro

  const text = container.textContent;
  const selectedText = text.slice(startOffset, endOffset);

  if (!selectedText.trim()) return;

  const isUpperCase = selectedText === selectedText.toUpperCase();
  const newText = isUpperCase ? selectedText.toLowerCase() : selectedText.toUpperCase();

  // Substitui mantendo o restante do conteúdo intacto
  const updatedText = text.slice(0, startOffset) + newText + text.slice(endOffset);
  container.textContent = updatedText;

  // Reaplica a seleção
  const newRange = document.createRange();
  newRange.setStart(container, startOffset);
  newRange.setEnd(container, startOffset + newText.length);

  selection.removeAllRanges();
  selection.addRange(newRange);
}

// ALTERNA TAMANHO DA FONTE "A+" *********************************************************************************************************
function aumentarFonte() {
  const selection = window.getSelection();
  if (!selection.rangeCount) return;

  const range = selection.getRangeAt(0);
  const selectedText = range.toString();
  if (!selectedText.trim()) return;

  const span = document.createElement("span");
  span.style.fontSize = "1.4em";
  span.style.lineHeight = "1.4em"; // Reduz impacto visual
  span.textContent = selectedText;

  range.deleteContents();
  range.insertNode(span);

  // Mantém seleção
  const novaSelecao = document.createRange();
  novaSelecao.selectNodeContents(span);
  selection.removeAllRanges();
  selection.addRange(novaSelecao);
}

// DIMINUIR TAMANHO DA FONTE "A-" ***************************************************************************************************
function diminuirFonte()  {
  const selection = window.getSelection();
  if (!selection.rangeCount) return;

  const range = selection.getRangeAt(0);
  const container = range.startContainer;

  let span = container.nodeType === 3 ? container.parentNode : container; // 3 = Text Node

  // Verifica se é um <span> com estilo de fonte aplicado
  if (span.tagName === "SPAN" && span.style.fontSize) {
    const texto = span.textContent;
    const textNode = document.createTextNode(texto);
    span.replaceWith(textNode);

    // Restaura a seleção
    const novaSelecao = document.createRange();
    novaSelecao.selectNodeContents(textNode);
    selection.removeAllRanges();
    selection.addRange(novaSelecao);
  } else {
    console.log("⚠️ Nenhum span com fonte detectado.");
  }
}

/* 🔍  BOTÃO BUSCA 🔍  ******************************** 🔍  BOTÃO BUSCA 🔍 ************************************************ */

function abrirBusca() {
  document.getElementById("busca-local").style.display = "block";
  document.getElementById("inputBusca").focus();
}

function fecharBusca() {
  document.getElementById("busca-local").style.display = "none";
  limparDestaques();
}

function destacarBusca() {
  const termo = document.getElementById("inputBusca").value;
  const editor = document.getElementById("editor");

  limparDestaques();

  if (termo.length >= 1) {
    const regex = new RegExp(`(${termo})`, "gi");
    editor.innerHTML = editor.innerHTML.replace(regex, `<mark>$1</mark>`);
  }
}

function limparDestaques() {
  const editor = document.getElementById("editor");
  editor.innerHTML = editor.innerHTML.replace(/<mark>(.*?)<\/mark>/gi, "$1");
}

// 🔍 Atalhos de teclado
document.addEventListener("keydown", function (e) {
  // Ctrl + L → abrir busca
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "l") {
    e.preventDefault(); // evita conflito com o navegador
    abrirBusca();
  }

  // Esc → fechar busca
  if (e.key === "Escape") {
    fecharBusca();
  }
});

// 🔍 ***************************************************************************************************************

// ✅ Carrega a primeira aba automaticamente ao abrir
document.addEventListener("DOMContentLoaded", () => {
  criarNovaAba(); // cria e carrega lousa-1
});
 
// SALVAR 💾 *****************************************************************************************************
function saveText() {
  salvarConteudoAtual(); // garante que a aba ativa seja salva

  localStorage.setItem('todasAsLousas', JSON.stringify(lousas));
  localStorage.setItem('lousaAtual', lousaAtual);

  const btn = document.getElementById('saveButton');
  btn.textContent = 'Salvo!';
  setTimeout(() => btn.textContent = '💾', 2000);
}

setInterval(() => {
  saveText();
}, 90000); // 90.000 milissegundos = 1min30s

// CARREGAR 📁 *****************************************************************************************************
function loadText() {
  const salvas = localStorage.getItem('todasAsLousas');
  const atual = localStorage.getItem('lousaAtual');

  if (salvas) {
    lousas = JSON.parse(salvas);
    lousaAtual = atual;

    carregarConteudoAtual();
    atualizarAbas();
    alert('Todas as lousas foram carregadas com sucesso!');
  } else {
    alert('Nenhuma lousa salva encontrada.');
  }
}

// CARREGAR E SALVAR COMO: 📋 *****************************************************************************************************

function saveAsFile() {
    salvarConteudoAtual(); // garante que a lousa atual seja salva
    const data = {
        lousas: lousas,
        lousaAtual: lousaAtual
    };

    const fileName = prompt("Digite o nome do arquivo (sem extensão):", "projeto");
    if (fileName) {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json;charset=utf-8' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `${fileName}.txt`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// CARREGAR ARQUIVO DE LOUSAS
function loadFromFile(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                const data = JSON.parse(e.target.result);
                if (data.lousas && typeof data.lousas === "object") {
                    lousas = data.lousas;
                    lousaAtual = data.lousaAtual || Object.keys(lousas)[0];
                    carregarConteudoAtual();
                    atualizarAbas();
                    alert('Projeto carregado com sucesso!');
                } else {
                    throw new Error("Formato inválido.");
                }
            } catch (err) {
                alert('Erro ao carregar o arquivo: ' + err.message);
            }
        };
        reader.readAsText(file);
    }
    event.target.value = ''; // permite recarregar o mesmo arquivo
}

 // ADIANTAR E VOLTAR 📋 *****************************************************************************************************
 // ADIANTAR E VOLTAR 📋 *****************************************************************************************************
let undoStack = [];
let redoStack = [];
let ultimoSalvo = "";
let tempoEspera;
const editor = document.getElementById('editor');

// Estado inicial
window.addEventListener('load', () => {
  ultimoSalvo = editor.innerHTML;
  undoStack.push(ultimoSalvo);
});

// Salva após pausa ou caractere-chave
editor.addEventListener('input', () => {
  clearTimeout(tempoEspera);
  const atual = editor.innerHTML;

  // Se digitar ponto, enter ou travessão, salva imediatamente
  if (atual.endsWith('.') || atual.endsWith('!') || atual.endsWith('?') || atual.includes('<div>') || atual.includes('—')) {
    salvarEstado(atual);
  } else {
    // Senão, aguarda 1.5 segundos antes de salvar
    tempoEspera = setTimeout(() => salvarEstado(atual), 700);
  }
});

function salvarEstado(conteudo) {
  if (conteudo !== ultimoSalvo) {
    undoStack.push(conteudo);
    if (undoStack.length > 50) undoStack.shift();  // Limita a 50
    redoStack = [];
    ultimoSalvo = conteudo;
  }
}

function undo() {
  if (undoStack.length > 1) {
    const atual = undoStack.pop();
    redoStack.push(atual);
    const anterior = undoStack[undoStack.length - 1];
    editor.innerHTML = anterior;
    ultimoSalvo = anterior;
  }
}

function redo() {
  if (redoStack.length > 0) {
    const estado = redoStack.pop();
    undoStack.push(estado);
    editor.innerHTML = estado;
    ultimoSalvo = estado;
  }
}


// COPIAR TEXTO 📋 *****************************************************************************************************
// COPIAR TEXTO 📋 *****************************************************************************************************
function copyText() {
  const editor = document.getElementById("editor");
  const textGroups = editor.querySelectorAll(".text-group");

  let htmlContent = "";

  if (textGroups.length > 0) {
    htmlContent = Array.from(textGroups)
      .map(group => {
        const wrapper = document.createElement("div");
        wrapper.innerHTML = group.innerHTML;
        wrapper.style.fontSize = "12pt";
        wrapper.style.fontFamily = "Arial, sans-serif";
        wrapper.style.textAlign = group.style.textAlign || "left";
        wrapper.style.marginBottom = "1em";
        return wrapper.outerHTML;
      })
      .join("");
  } else {
    // Fallback: editor inteiro mesmo sem text-group
    const wrapper = document.createElement("div");
    wrapper.innerHTML = editor.innerHTML;
    wrapper.style.fontSize = "12pt";
    wrapper.style.fontFamily = "Arial, sans-serif";
    wrapper.style.marginBottom = "1em";
    htmlContent = wrapper.outerHTML;
  }

  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = htmlContent;
  tempDiv.style.position = "absolute";
  tempDiv.style.left = "-9999px";
  document.body.appendChild(tempDiv);

  const range = document.createRange();
  range.selectNodeContents(tempDiv);
  const selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(range);

  try {
    document.execCommand("copy");
    const btn = document.getElementById("copyButton");
    if (btn) {
      btn.textContent = "📋 Copiado!";
      setTimeout(() => (btn.textContent = "📋"), 1000);
    }
  } catch (err) {
    alert("❌ Erro ao copiar.");
  }

  document.body.removeChild(tempDiv);
  selection.removeAllRanges();
}



    // NUMBERSENTENCES 1 ***************************************************************************************************
function numberSentences() {
  const editor = document.getElementById("editor");
  const rawHTML = editor.innerHTML;

  // Cria um contêiner temporário para processar o HTML
  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = rawHTML;

  const nodes = Array.from(tempDiv.childNodes);
  let frases = [];
  let buffer = "";

  nodes.forEach(node => {
    const content = node.outerHTML || node.textContent;

    // Divide mantendo a pontuação final
    const partes = content.split(/([.!?]+)(\s+|$)/);
    for (let i = 0; i < partes.length; i += 3) {
      const frase = (partes[i] || "") + (partes[i + 1] || "");
      if (frase.trim()) frases.push(frase.trim());
    }
  });

  editor.innerHTML = "";
  frases.forEach((frase, i) => {
    const group = document.createElement("div");
    group.className = "sentence-group";

    const numberSpan = document.createElement("span");
    numberSpan.className = "number-marker";
    numberSpan.textContent = i + 1;

    const textSpan = document.createElement("span");
    textSpan.className = "text-group";
    textSpan.setAttribute("contenteditable", "true");
    textSpan.innerHTML = frase;

    group.appendChild(numberSpan);
    group.appendChild(textSpan);
    editor.appendChild(group);
  });
}


function numberSentencesBy3() {
  const editor = document.getElementById("editor");
  const rawHTML = editor.innerHTML;

  // Cria um contêiner temporário para manipular os elementos
  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = rawHTML;

  const nodes = Array.from(tempDiv.childNodes);
  let frases = [];
  let buffer = "";

  nodes.forEach(node => {
    if (node.nodeType === 3 || node.nodeType === 1) {
      const content = node.outerHTML || node.textContent;

      // Divide mantendo pontuação
      const partes = content.split(/([.!?]+)(\s+|$)/);
      for (let i = 0; i < partes.length; i += 3) {
        const frase = (partes[i] || "") + (partes[i + 1] || "");
        if (frase.trim()) frases.push(frase.trim());
      }
    }
  });

  editor.innerHTML = "";
  let groupCount = 1;

  for (let i = 0; i < frases.length; i += 3) {
    const grupo = frases.slice(i, i + 3).join(" ");

    const group = document.createElement("div");
    group.className = "sentence-group";

    const numberSpan = document.createElement("span");
    numberSpan.className = "number-marker";
    numberSpan.textContent = groupCount++;

    const textSpan = document.createElement("span");
    textSpan.className = "text-group";
    textSpan.setAttribute("contenteditable", "true");
    textSpan.innerHTML = grupo;

    group.appendChild(numberSpan);
    group.appendChild(textSpan);
    editor.appendChild(group);
  }
}

    // NUMBERSENTENCES 4 ****************************************************************************************************
function numberSentencesBy4() {
  const editor = document.getElementById("editor");
  const rawHTML = editor.innerHTML;

  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = rawHTML;

  const nodes = Array.from(tempDiv.childNodes);
  let frases = [];

  nodes.forEach(node => {
    if (node.nodeType === 1 || node.nodeType === 3) {
      const content = node.outerHTML || node.textContent;

      const partes = content.split(/([.!?]+)(\s+|$)/); // divide mantendo pontuação
      for (let i = 0; i < partes.length; i += 3) {
        const frase = (partes[i] || "") + (partes[i + 1] || "");
        if (frase.trim()) frases.push(frase.trim());
      }
    }
  });

  editor.innerHTML = "";
  let groupCount = 1;

  for (let i = 0; i < frases.length; i += 4) {
    const grupo = frases.slice(i, i + 4).join(" ");

    const group = document.createElement("div");
    group.className = "sentence-group";

    const numberSpan = document.createElement("span");
    numberSpan.className = "number-marker";
    numberSpan.textContent = groupCount++;

    const textSpan = document.createElement("span");
    textSpan.className = "text-group";
    textSpan.setAttribute("contenteditable", "true");
    textSpan.innerHTML = grupo;

    group.appendChild(numberSpan);
    group.appendChild(textSpan);
    editor.appendChild(group);
  }
}

  // REMOVENUMBER 🧺 *******************************************************************************************************
function removeNumbering() {

  const editor = document.getElementById("editor");
  const groups = editor.querySelectorAll(".sentence-group");

  const cleanText = Array.from(groups).map(group => {
    const text = group.querySelector(".text-group")?.innerText.trim();
    return text || '';
  }).join(' '); // Junta frases com espaço

  // 🔄 Limpa o conteúdo do editor e coloca o texto diretamente
  editor.innerHTML = cleanText;

  // 🖱️ Posiciona o cursor ao final do conteúdo do editor
  const range = document.createRange();
  const sel = window.getSelection();
  range.selectNodeContents(editor);
  range.collapse(false); // Fim do texto
  sel.removeAllRanges();
  sel.addRange(range);

  // ⚠️ Garante que o editor permaneça editável
  editor.setAttribute('contenteditable', 'true');
}

// 🧹 LIMPAR SÍMBOLOS *****************************************************************************************************
function cleanSymbols() {
    const editor = document.getElementById('editor');
    const symbols = editor.querySelectorAll('.processed-symbol');
    symbols.forEach(symbol => symbol.remove());
    const comments = editor.querySelectorAll('.processed-comment');
    comments.forEach(comment => comment.remove());
    document.getElementById('output').textContent = "Símbolos e comentários removidos ✅";
    addToHistory(captureState());
}

// 🧽 REMOVEDOR *****************************************************************************************************

function removerFormatacaoSelecao() {
  const selection = window.getSelection();
  if (!selection.rangeCount || selection.isCollapsed) return;

  const range = selection.getRangeAt(0);

  // Cria uma div temporária para capturar o conteúdo da seleção
  const divTemp = document.createElement("div");
  divTemp.appendChild(range.cloneContents());

  // Extrai apenas o texto puro da seleção
  const textoLimpo = divTemp.textContent || divTemp.innerText;

  // Substitui o conteúdo original pela versão sem formatação
  range.deleteContents();
  range.insertNode(document.createTextNode(textoLimpo));

  // Remove a seleção ativa
  selection.removeAllRanges();

  // Atualiza histórico (se tiver essa função no sistema)
  if (typeof addToHistory === "function") {
    addToHistory(captureState());
  }
}

// FECHAR TABELA INSPIRAÇÃO ********************************************************************************************

function fecharInspiracao() {
  document.getElementById("inspiracao-lousa").style.display = "none";
}

// CHAT ALTERNADO 💬💬 ************************************************************************************************
function trocarModoChat(modo) {
  const head = document.head;

  // Remove CSS e JS anteriores se existirem
  const cssAnterior = document.getElementById('chat-css');
  if (cssAnterior) cssAnterior.remove();

  const jsAnterior = document.getElementById('chat-js');
  if (jsAnterior) jsAnterior.remove();

  // Cria novo CSS e JS
  const novoCss = document.createElement('link');
  novoCss.rel = 'stylesheet';
  novoCss.id = 'chat-css';

  const novoJs = document.createElement('script');
  novoJs.id = 'chat-js';

  if (modo === 'romantico') {
    novoCss.href = "/static/css/chats/chat_romantico.css";
    novoJs.src  = "/static/js/chats/chat_romantico.js";

    // 🌸 Aplica imagem inicial de fundo direto no painel
    const chatPanel = document.getElementById("chat-panel");
    if (chatPanel) {
      chatPanel.style.backgroundImage = `
        linear-gradient(180deg, rgba(255, 192, 203, 0.15), rgba(138, 43, 226, 0.15)),
        url('/static/img/flavia.jpg')`;
      chatPanel.style.opacity = '1';
    }

  } else if (modo === 'edtorial') {
    novoCss.href = "/static/css/chats/chat_escuro.css";
    novoJs.src  = "/static/js/chats/chat_edtorial.js";
  }

  // Aplica no <head>
  head.appendChild(novoCss);
  head.appendChild(novoJs);
}

function atualizarVisualizacao() {
  const botoesModificaveis = document.querySelectorAll('.botao-modificavel');
  const botoesFixos = document.querySelectorAll('.botao-fixo-tarefa');
  const modoPC = document.querySelectorAll('.modo-pc');
  const modoCelular = document.querySelectorAll('.modo-celular');
  const botaoCelular = document.getElementById("botaoToggleModoCelular");
  const botaoModo = document.getElementById("botao-modo-geral");

  // Visualização geral
  if (modoCelularAtivo) {
    modoPC.forEach(el => el.style.display = 'none');
    modoCelular.forEach(el => el.style.display = 'flex');
    botaoCelular.innerText = "💻";
  } else {
    modoPC.forEach(el => el.style.display = '');
    modoCelular.forEach(el => el.style.display = 'none');
    botaoCelular.innerText = "📲";
  }

  // Botões internos (só aplicados se NÃO estiver no modo celular)
  if (!modoCelularAtivo) {
    if (modoTarefaAtivo) {
      botoesModificaveis.forEach(btn => btn.style.display = 'none');
      botoesFixos.forEach(btn => btn.style.display = 'inline-block');
      botaoModo.innerHTML = 'Modo Escritor ✍';
    } else {
      botoesModificaveis.forEach(btn => btn.style.display = 'inline-block');
      botoesFixos.forEach(btn => btn.style.display = 'inline-block');
      botaoModo.innerHTML = 'Modo Tarefa 📌';
    }
  }
}



// BOTÃO ALTERNANCIA TAREFA📌/✍ESCRITOR *********************************************************************************

let modoTarefaAtivo = false;

function trocarModo() {
  const botoesModificaveis = document.querySelectorAll('.botao-modificavel');
  const botoesFixos = document.querySelectorAll('.botao-fixo-tarefa');
  const botaoModo = document.querySelector('#botao-modo-geral');

  // 👉 Se estiver no modo celular, não altera visualização
  if (modoCelularAtivo) {
    modoTarefaAtivo = !modoTarefaAtivo; // apenas alterna lógica interna
    botaoModo.innerHTML = modoTarefaAtivo ? 'Modo Escritor ✍' : 'Modo Tarefa 📌';
    return;
  }

  if (!modoTarefaAtivo) {
    // Entrar no modo tarefa
    botoesModificaveis.forEach(btn => btn.style.display = 'none');
    botoesFixos.forEach(btn => btn.style.display = 'inline-block');
    botaoModo.innerHTML = 'Modo Escritor ✍';
  } else {
    // Voltar ao modo completo
    botoesModificaveis.forEach(btn => btn.style.display = 'inline-block');
    botaoModo.innerHTML = 'Modo Tarefa 📌';
  }

  modoTarefaAtivo = !modoTarefaAtivo;
}

// MODO CELULAR *****************************************************************************************************************

let modoCelularAtivo = false;

function alternarModoCelular() {
  const modoPC = document.querySelectorAll('.modo-pc');
  const modoCelular = document.querySelectorAll('.modo-celular');
  const botao = document.getElementById("botaoToggleModoCelular");

  if (!modoCelularAtivo) {
    modoPC.forEach(el => el.style.display = 'none');
    modoCelular.forEach(el => el.style.display = 'flex');
    botao.innerText = "💻";
    modoCelularAtivo = true;
  } else {
    modoPC.forEach(el => {
      el.style.display = ''; // Restaurar
      el.querySelectorAll('.toolbar-button').forEach(btn => btn.style.display = 'inline-block');
    });
    modoCelular.forEach(el => el.style.display = 'none');
    botao.innerText = "📲";
    modoCelularAtivo = false;
  }
}

function ajustarClassesModoCelular(forcarComo = "modificavel") {
  const botoesCelular = document.querySelectorAll('.modo-celular .toolbar-button');

  botoesCelular.forEach(botao => {
    botao.classList.remove("botao-fixo-tarefa", "botao-modificavel");

    if (forcarComo === "fixo") {
      botao.classList.add("botao-fixo-tarefa");
    } else {
      botao.classList.add("botao-modificavel");
    }
  });
}

document.getElementById("editor").addEventListener("keydown", function (event) {
  // Se tecla for Enter e Shift estiver pressionado, ativa gerarTarefa
  if (event.key === "Enter" && event.shiftKey) {
    event.preventDefault(); // Impede quebra de linha
    gerarTarefa();
  }
});

