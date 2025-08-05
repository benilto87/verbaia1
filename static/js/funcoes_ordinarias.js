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

// INSERIR E REMOVER MARCAÇÕES ❌ *****************************************************************************************************************************

function inserirMarcacaoNoBloco(numero, textoIA) {
  const sentenceGroups = document.querySelectorAll(".sentence-group");

  // Encontrar o grupo correspondente ao número
  const grupo = sentenceGroups[numero - 1];
  if (!grupo) {
    console.warn("❌ Bloco não encontrado:", numero);
    return;
  }

  const textGroup = grupo.querySelector(".text-group");
  if (!textGroup) {
    console.warn("❌ text-group não encontrado no bloco:", numero);
    return;
  }

  // Criar o id único da marcação
  const idMarcacao = `marcacao-${Date.now()}`;

  // Criar o elemento da marcação com botão de fechar
  const span = document.createElement("span");
  span.className = "processed-comment marcacao-com-fechar";
  span.id = idMarcacao;
  span.innerHTML = `
    ${textoIA}
    <button class="marcacao-fechar" onclick="removerMarcacao('${idMarcacao}')">✖</button>
  `;

  // Inserir dentro do .text-group
  textGroup.appendChild(span);
  salvarConteudoAtual();
}

function removerMarcacao(id) {
  const elemento = document.getElementById(id);
  if (elemento) {
    elemento.remove();
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
// NUMBERSENTENCES 1 ***************************************************************************************************
function numberSentences() {
    const editor = document.getElementById("editor");
    
    // 1. Pega o HTML original e o coloca em um contêiner temporário
    const tempDiv = document.createElement("div");
    tempDiv.innerHTML = editor.innerHTML;

    // 2. Remove todos os grupos de numeração e anotações anteriores para limpeza
    tempDiv.querySelectorAll('.sentence-group, .processed-symbol, .processed-comment, .scene-marker').forEach(el => {
        if (el.classList.contains('sentence-group')) {
            const textGroup = el.querySelector('.text-group');
            if (textGroup) {
                el.replaceWith(textGroup);
            }
        } else {
            el.remove();
        }
    });

    // 3. Pega o HTML limpo e substitui reticências por um marcador temporário
    let htmlContent = tempDiv.innerHTML;
    // O regex abaixo encontra '...' em qualquer contexto, incluindo dentro de tags
    const tempEllipsisMarker = '__ELLIPSIS__';
    htmlContent = htmlContent.replace(/\.\.\./g, tempEllipsisMarker);

    let sentences = [];
    let currentSentence = '';
    
    // Agora, o split é feito apenas por tags, ponto final, exclamação, interrogação ou quebra de linha
    const parts = htmlContent.split(/(<[^>]+>|[\.!?]|\n)/g);

    parts.forEach(part => {
        if (!part) return;

        currentSentence += part;
        
        // Finaliza a sentença se encontrar pontuação de fim de frase ou quebra de linha
        if (['.', '!', '?'].includes(part.trim()) || part === '\n') {
            let trimmedSentence = currentSentence.trim();
            if (trimmedSentence) {
                // Adiciona a sentença completa (com tags e pontuação) à lista
                sentences.push(trimmedSentence);
            }
            currentSentence = ''; // Reseta para a próxima sentença
        }
    });

    // Adiciona qualquer conteúdo restante que não tenha pontuação final
    if (currentSentence.trim()) {
        sentences.push(currentSentence.trim());
    }

    // 4. Reconstroi o editor com a nova numeração e formatação
    editor.innerHTML = "";
    sentences.forEach((sentenceHTML, i) => {
        // Restaura as reticências antes de inserir o HTML
        const finalSentenceHTML = sentenceHTML.replace(new RegExp(tempEllipsisMarker, 'g'), '...');

        // Cria o grupo da sentença
        const group = document.createElement("div");
        group.className = "sentence-group";

        // Cria o marcador de número
        const numberSpan = document.createElement("span");
        numberSpan.className = "number-marker";
        numberSpan.innerHTML = `${i + 1}<span class="separador">°</span>`;

        // Cria o contêiner do texto editável com o HTML preservado
        const textSpan = document.createElement("span");
        textSpan.className = "text-group";
        textSpan.setAttribute("contenteditable", "true");
        textSpan.innerHTML = finalSentenceHTML.trim();

        // Adiciona os elementos ao grupo
        group.appendChild(numberSpan);
        group.appendChild(textSpan);
        
        editor.appendChild(group);
    });
}

function numberSentencesBy3() {
    const editor = document.getElementById("editor");
    
    // 1. Pega o HTML original e o coloca em um contêiner temporário
    const tempDiv = document.createElement("div");
    tempDiv.innerHTML = editor.innerHTML;

    // 2. Remove todos os grupos de numeração e anotações anteriores para limpeza
    tempDiv.querySelectorAll('.sentence-group, .processed-symbol, .processed-comment, .scene-marker, .revisao-bloco').forEach(el => {
        if (el.classList.contains('sentence-group')) {
            const textGroup = el.querySelector('.text-group');
            if (textGroup) {
                el.replaceWith(textGroup);
            }
        } else {
            el.remove();
        }
    });

    // 3. Pega o HTML limpo e substitui reticências por um marcador temporário
    let htmlContent = tempDiv.innerHTML;
    const tempEllipsisMarker = '__ELLIPSIS__';
    htmlContent = htmlContent.replace(/\.\.\./g, tempEllipsisMarker);

    let sentences = [];
    let currentSentence = '';
    
    // Agora, o split é feito apenas por tags, ponto final, exclamação, interrogação ou quebra de linha
    const parts = htmlContent.split(/(<[^>]+>|[\.!?]|\n)/g);

    parts.forEach(part => {
        if (!part) return;

        currentSentence += part;
        
        // Finaliza a sentença se encontrar pontuação de fim de frase ou quebra de linha
        if (['.', '!', '?'].includes(part.trim()) || part === '\n') {
            let trimmedSentence = currentSentence.trim();
            if (trimmedSentence) {
                sentences.push(trimmedSentence);
            }
            currentSentence = ''; // Reseta para a próxima sentença
        }
    });

    // Adiciona qualquer conteúdo restante que não tenha pontuação final
    if (currentSentence.trim()) {
        sentences.push(currentSentence.trim());
    }

    // 4. Reconstroi o editor com a nova numeração e formatação em grupos de 3
    editor.innerHTML = "";
    let groupCount = 1;

    for (let i = 0; i < sentences.length; i += 3) {
        const grupoDeSentencasHTML = sentences.slice(i, i + 3).join(" ");
        
        // Restaura as reticências antes de inserir o HTML
        const finalGrupoHTML = grupoDeSentencasHTML.replace(new RegExp(tempEllipsisMarker, 'g'), '...');

        const group = document.createElement("div");
        group.className = "sentence-group";

        const numberSpan = document.createElement("span");
        numberSpan.className = "number-marker";
        numberSpan.innerHTML = `${groupCount++}<span class="separador">°</span>`;

        const textSpan = document.createElement("span");
        textSpan.className = "text-group";
        textSpan.setAttribute("contenteditable", "true");
        textSpan.innerHTML = finalGrupoHTML.trim();

        group.appendChild(numberSpan);
        group.appendChild(textSpan);
        editor.appendChild(group);
    }
}

    // NUMBERSENTENCES 4 ****************************************************************************************************
function numberSentencesBy4() {
    const editor = document.getElementById("editor");
    
    // 1. Pega o HTML original e o coloca em um contêiner temporário
    const tempDiv = document.createElement("div");
    tempDiv.innerHTML = editor.innerHTML;

    // 2. Remove todos os grupos de numeração e anotações anteriores para limpeza
    tempDiv.querySelectorAll('.sentence-group, .processed-symbol, .processed-comment, .scene-marker, .revisao-bloco').forEach(el => {
        if (el.classList.contains('sentence-group')) {
            const textGroup = el.querySelector('.text-group');
            if (textGroup) {
                el.replaceWith(textGroup);
            }
        } else {
            el.remove();
        }
    });

    // 3. Pega o HTML limpo e substitui reticências por um marcador temporário
    let htmlContent = tempDiv.innerHTML;
    const tempEllipsisMarker = '__ELLIPSIS__';
    htmlContent = htmlContent.replace(/\.\.\./g, tempEllipsisMarker);

    let sentences = [];
    let currentSentence = '';
    
    // Agora, o split é feito apenas por tags, ponto final, exclamação, interrogação ou quebra de linha
    const parts = htmlContent.split(/(<[^>]+>|[\.!?]|\n)/g);

    parts.forEach(part => {
        if (!part) return;

        currentSentence += part;
        
        // Finaliza a sentença se encontrar pontuação de fim de frase ou quebra de linha
        if (['.', '!', '?'].includes(part.trim()) || part === '\n') {
            let trimmedSentence = currentSentence.trim();
            if (trimmedSentence) {
                sentences.push(trimmedSentence);
            }
            currentSentence = ''; // Reseta para a próxima sentença
        }
    });

    // Adiciona qualquer conteúdo restante que não tenha pontuação final
    if (currentSentence.trim()) {
        sentences.push(currentSentence.trim());
    }

    // 4. Reconstroi o editor com a nova numeração e formatação em grupos de 4
    editor.innerHTML = "";
    let groupCount = 1;

    for (let i = 0; i < sentences.length; i += 4) {
        const grupoDeSentencasHTML = sentences.slice(i, i + 4).join(" ");
        
        // Restaura as reticências antes de inserir o HTML
        const finalGrupoHTML = grupoDeSentencasHTML.replace(new RegExp(tempEllipsisMarker, 'g'), '...');

        const group = document.createElement("div");
        group.className = "sentence-group";

        const numberSpan = document.createElement("span");
        numberSpan.className = "number-marker";
        numberSpan.innerHTML = `${groupCount++}<span class="separador">°</span>`;

        const textSpan = document.createElement("span");
        textSpan.className = "text-group";
        textSpan.setAttribute("contenteditable", "true");
        textSpan.innerHTML = finalGrupoHTML.trim();

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

// FECHAR E MINIMIZAR TABELA INSPIRAÇÃO 🌺********************************************************************************************

function fecharInspiracao() {
  document.getElementById("inspiracao-lousa").style.display = "none";
}

function minimizarInspiracao() {
  const lousa = document.getElementById("inspiracao-lousa");
  const conteudo = document.getElementById("inspiracao-texto");
  const titulo = lousa.querySelector("strong");

  const estaMinimizado = conteudo.style.display === "none";

  if (estaMinimizado) {
    conteudo.style.display = "block";
    titulo.innerHTML = "🌺 Inspiração da Flávia:";
    lousa.classList.remove("minimizado");
  } else {
    conteudo.style.display = "none";
    titulo.innerHTML = "🌺 (minimizado)";
    lousa.classList.add("minimizado");
  }
}


function permitirArrastarInspiracao() {
  const lousa = document.getElementById("inspiracao-lousa");
  let isDragging = false;
  let offsetX, offsetY;

  function startDrag(e) {
    isDragging = true;
    const rect = lousa.getBoundingClientRect();
    const clientX = e.type === "touchstart" ? e.touches[0].clientX : e.clientX;
    const clientY = e.type === "touchstart" ? e.touches[0].clientY : e.clientY;
    offsetX = clientX - rect.left;
    offsetY = clientY - rect.top;

    document.addEventListener("mousemove", drag);
    document.addEventListener("mouseup", stopDrag);
    document.addEventListener("touchmove", drag, { passive: false });
    document.addEventListener("touchend", stopDrag);
  }

  function drag(e) {
    if (!isDragging) return;

    e.preventDefault();
    const clientX = e.type === "touchmove" ? e.touches[0].clientX : e.clientX;
    const clientY = e.type === "touchmove" ? e.touches[0].clientY : e.clientY;

    lousa.style.left = `${clientX - offsetX}px`;
    lousa.style.top = `${clientY - offsetY}px`;
  }

  function stopDrag() {
    isDragging = false;
    document.removeEventListener("mousemove", drag);
    document.removeEventListener("mouseup", stopDrag);
    document.removeEventListener("touchmove", drag);
    document.removeEventListener("touchend", stopDrag);
  }

  lousa.addEventListener("mousedown", startDrag);
  lousa.addEventListener("touchstart", startDrag);
}

document.addEventListener("DOMContentLoaded", permitirArrastarInspiracao);


// CHAT ALTERNADO **********************************************************************************************************
function trocarModoChat(modo) {
  // Remove estilos e scripts antigos
  const head = document.head;

  // Remove CSS anterior se existir
  const cssAnterior = document.getElementById('chat-css');
  if (cssAnterior) cssAnterior.remove();

  // Remove JS anterior se existir
  const jsAnterior = document.getElementById('chat-js');
  if (jsAnterior) jsAnterior.remove();

  // Cria novo <link> para CSS
  const novoCss = document.createElement('link');
  novoCss.rel = 'stylesheet';
  novoCss.id = 'chat-css';

  // Cria novo <script> para JS
  const novoJs = document.createElement('script');
  novoJs.id = 'chat-js';

  if (modo === 'romantico') {
    novoCss.href = "/static/css/chats/chat_romantico.css";
    novoJs.src  = "/static/js/chats/chat_romantico.js";
  } else if (modo === 'edtorial') {
    novoCss.href = "/static/css/chats/chat_escuro.css";
    novoJs.src  = "/static/js/chats/chat_edtorial.js";
  }

  // Adiciona ao <head>
  head.appendChild(novoCss);
  head.appendChild(novoJs);
}

// BOTÃO ALTERNANCIA TAREFA📌/✍ESCRITOR *********************************************************************************

  let modoTarefaAtivo = false;

  function trocarModo() {
    const botoesModificaveis = document.querySelectorAll('.botao-modificavel');
    const botoesFixos = document.querySelectorAll('.botao-fixo-tarefa');
    const botaoModo = document.querySelector('#botao-modo-geral');

    if (!modoTarefaAtivo) {
      botoesModificaveis.forEach(btn => btn.style.display = 'none');
      botoesFixos.forEach(btn => btn.style.display = 'inline-block');
      botaoModo.innerHTML = 'Modo Escritor ✍';
    } else {
      botoesModificaveis.forEach(btn => btn.style.display = 'inline-block');
      botaoModo.innerHTML = 'Modo Tarefa 📌';
    }

    modoTarefaAtivo = !modoTarefaAtivo;
  }
  
  window.addEventListener("DOMContentLoaded", () => {
  if (!modoTarefaAtivo) {
    trocarModo();
  }
});

document.getElementById("editor").addEventListener("keydown", function (event) {
  // Se tecla for Enter e Shift estiver pressionado, ativa gerarTarefa
  if (event.key === "Enter" && event.shiftKey) {
    event.preventDefault(); // Impede quebra de linha
    gerarTarefa();
  }
});

// CHAT MINIMIZADO VERSÃO MOBILE
window.addEventListener("load", () => {
  const panel = document.getElementById("chat-panel");
  if (window.innerWidth <= 768) {
    panel.classList.add("minimized");
  }
});