const form = document.getElementById('form-tarefa');
const lista = document.getElementById('lista-tarefas');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const titulo = document.getElementById('nova-tarefa').value.trim();
    if (!titulo) return;

    await fetch('/api/tarefas', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({titulo})
    });

    document.getElementById('nova-tarefa').value = '';
    carregarTarefas();
});

async function carregarTarefas() {
    const resposta = await fetch('/api/tarefas');
    if (resposta.status === 401) {
        alert('Você precisa fazer login.');
        window.location.href = '/login';
        return;
    }
    const tarefas = await resposta.json();
    lista.innerHTML = '';

    tarefas.forEach(tarefa => {
        const li = document.createElement('li');
        li.textContent = tarefa.titulo;

        const btnEditar = document.createElement('button');
        btnEditar.textContent = 'Editar';
        btnEditar.classList.add('edit-btn');
        btnEditar.onclick = async () => {
            const novoTitulo = prompt('Editar tarefa:', tarefa.titulo);
            if (novoTitulo && novoTitulo.trim()) {
                await fetch(`/api/tarefas/${tarefa.id}`, {
                    method: 'PUT',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({titulo: novoTitulo.trim()})
                });
                carregarTarefas();
            }
        };

        const btnApagar = document.createElement('button');
        btnApagar.textContent = 'Apagar';
        btnApagar.classList.add('delete-btn');
        btnApagar.onclick = async () => {
            if (confirm('Tem certeza que quer apagar esta tarefa?')) {
                await fetch(`/api/tarefas/${tarefa.id}`, {
                    method: 'DELETE'
                });
                carregarTarefas();
            }
        };

        li.appendChild(btnEditar);
        li.appendChild(btnApagar);
        lista.appendChild(li);
    });
}

carregarTarefas();
