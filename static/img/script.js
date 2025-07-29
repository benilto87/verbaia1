document.addEventListener('DOMContentLoaded', (event) => {
    const chat = document.getElementById('chat');
    const form = document.getElementById('form');
    const input = document.getElementById('input');

    function addMessage(text, sender) {
        const msg = document.createElement('div');
        msg.classList.add('msg', sender);
        msg.textContent = text;
        chat.appendChild(msg);
        chat.scrollTop = chat.scrollHeight; // Rola para o final do chat
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Impede o recarregamento da página
        const userMessage = input.value.trim(); // Pega a mensagem do usuário e remove espaços em branco

        if (userMessage === '') { // Não envia mensagem vazia
            return;
        }

        addMessage(userMessage, 'user'); // Adiciona a mensagem do usuário ao chat
        input.value = ''; // Limpa o campo de input

        try {
            // Faz a requisição POST para o seu backend Flask
            const response = await fetch('http://localhost:5000/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage })
            });

            if (!response.ok) { // Verifica se a resposta foi bem-sucedida (código 200)
                const errorData = await response.json();
                throw new Error(errorData.reply || `Erro na resposta do servidor: ${response.status}`);
            }

            const data = await response.json();
            addMessage(data.reply, 'bot'); // Adiciona a resposta da IA ao chat
        } catch (error) {
            console.error('Erro ao enviar mensagem para a IA:', error);
            addMessage("Desculpa, amor... tive um probleminha e não consigo responder agora 🥺", 'bot');
        }
    });
});