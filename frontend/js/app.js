const API_URL = "http://localhost:8000/api";

const WHATSAPP_NUMBER = "557186903947"; 

let menuData = {};
let cart = {
    size: null,
    flavors: [], // IDs dos sabores
    beverages: [] // {id, qty, price, name}
};

async function init() {
    const res = await fetch(`${API_URL}/menu`);
    menuData = await res.json();
    renderSizes();
    renderBeverages();
}

// --- RENDERIZAÇÃO ---

function renderSizes() {
    const container = document.getElementById('sizes-list');
    container.innerHTML = menuData.sizes.map(s => `
        <div class="size-card" onclick="selectSize(${s.id})" id="size-${s.id}">
            <div>
                <strong>${s.name}</strong><br>
                <small>Até ${s.max_flavors} sabores</small>
            </div>
            <div class="price-tag">R$ ${s.price.toFixed(2)}</div>
        </div>
    `).join('');
}

function renderFlavors() {
    const container = document.getElementById('flavors-list');
    let html = '';
    
    // Categorias
    for (const [category, flavors] of Object.entries(menuData.flavors)) {
        html += `<h4 style="margin:10px 0; color:#666">${category}</h4>`;
        html += flavors.map(f => {
            const isSelected = cart.flavors.includes(f.id);
            return `
            <div class="flavor-item" onclick="toggleFlavor(${f.id})">
                <div class="flavor-info">
                    <strong>${f.name}</strong>
                    <small>${f.description || ''}</small>
                </div>
                <button class="btn-add ${isSelected ? 'active' : ''}">
                    ${isSelected ? '✔' : '+'}
                </button>
            </div>
            `;
        }).join('');
    }
    container.innerHTML = html;
}

function renderBeverages() {
    const container = document.getElementById('beverages-list');
    container.innerHTML = menuData.beverages.map(b => `
        <div class="flavor-item">
            <div>
                <strong>${b.name}</strong>
                <small>R$ ${b.price.toFixed(2)}</small>
            </div>
            <div class="counter">
                <button class="btn-add" onclick="updateBev(${b.id}, -1)">-</button>
                <span id="bev-qty-${b.id}">0</span>
                <button class="btn-add" onclick="updateBev(${b.id}, 1)">+</button>
            </div>
        </div>
    `).join('');
}

// --- LÓGICA DE PEDIDO ---

function selectSize(id) {
    cart.size = menuData.sizes.find(s => s.id === id);
    cart.flavors = []; // Reseta sabores ao trocar tamanho
    
    // UI Update
    document.querySelectorAll('.size-card').forEach(el => el.classList.remove('selected'));
    document.getElementById(`size-${id}`).classList.add('selected');
    
    document.getElementById('flavors-section').style.display = 'block';
    document.querySelector('.ai-btn').style.display = 'block';
    
    renderFlavors();
    updateTotal();
}

function toggleFlavor(id) {
    if (!cart.size) return;
    
    const index = cart.flavors.indexOf(id);
    if (index > -1) {
        cart.flavors.splice(index, 1);
    } else {
        if (cart.flavors.length >= cart.size.max_flavors) {
            alert(`O tamanho ${cart.size.name} permite apenas ${cart.size.max_flavors} sabores.`);
            return;
        }
        cart.flavors.push(id);
    }
    renderFlavors(); // Re-render para mostrar checkmarks
    updateTotal();
}

function updateBev(id, change) {
    let bevItem = cart.beverages.find(b => b.id === id);
    const bevData = menuData.beverages.find(b => b.id === id);

    if (!bevItem) {
        bevItem = { id: id, qty: 0, price: bevData.price, name: bevData.name };
        cart.beverages.push(bevItem);
    }

    bevItem.qty += change;
    if (bevItem.qty < 0) bevItem.qty = 0;

    document.getElementById(`bev-qty-${id}`).innerText = bevItem.qty;
    updateTotal();
}

async function askAI() {
    if (!cart.size) return;
    const btn = document.querySelector('.ai-btn');
    btn.innerText = "Pensando...";
    
    try {
        const res = await fetch(`${API_URL}/suggest/${cart.size.id}`);
        const suggestions = await res.json();
        
        if (suggestions.length > 0) {
            const sug = suggestions[0]; // Pega a primeira
            if(confirm(`Sugestão da Chef:\n${sug.title}\n\nAceitar esta combinação?`)) {
                cart.flavors = sug.ids;
                renderFlavors();
                updateTotal();
            }
        }
    } catch (e) {
        alert("A Chef está ocupada. Tente escolher manualmente.");
    } finally {
        btn.innerText = "✨ Sugestão da Chef (IA)";
    }
}

function updateTotal() {
    let total = 0;
    
    // Preço da Pizza (fixo pelo tamanho)
    if (cart.size) {
        total += cart.size.price;
        document.getElementById('flavor-counter').innerText = 
            `(${cart.flavors.length}/${cart.size.max_flavors})`;
    }
    
    // Bebidas
    cart.beverages.forEach(b => total += (b.qty * b.price));
    
    document.getElementById('total-display').innerText = total.toFixed(2).replace('.', ',');
}

function toggleChangeInput() {
    const method = document.getElementById('payment-method').value;
    const box = document.getElementById('change-box');
    box.style.display = (method === 'dinheiro') ? 'block' : 'none';
}

function sendOrder() {
    if (!cart.size) return alert("Escolha um tamanho de pizza!");
    if (cart.flavors.length === 0) return alert("Escolha pelo menos 1 sabor!");
    
    // Validação dos novos campos obrigatórios
    const name = document.getElementById('client-name').value;
    const street = document.getElementById('addr-street').value;
    const number = document.getElementById('addr-number').value;
    const district = document.getElementById('addr-district').value;
    const payment = document.getElementById('payment-method').value;

    if (!name || !street || !number || !district || !payment) {
        return alert("Por favor, preencha todos os campos obrigatórios (Nome, Endereço e Pagamento).");
    }

    // Lógica do Troco
    let paymentInfo = payment.toUpperCase();
    if (payment === 'dinheiro') {
        const change = document.getElementById('change-value').value;
        if (change) paymentInfo += ` (Troco para R$ ${change})`;
        else paymentInfo += ` (Sem troco)`;
    }

    // Montar texto dos sabores
    const flavorNames = cart.flavors.map(id => {
        for(let cat in menuData.flavors) {
            const found = menuData.flavors[cat].find(f => f.id === id);
            if(found) return found.name;
        }
    });

    // Montar Bebidas
    const bevLines = cart.beverages
        .filter(b => b.qty > 0)
        .map(b => `${b.qty}x ${b.name} (R$ ${b.price.toFixed(2)})`);

    const obs = document.getElementById('client-obs').value;
    const ref = document.getElementById('addr-ref').value;
    const total = document.getElementById('total-display').innerText;

    // --- MENSAGEM DO WHATSAPP (Clean Version) ---
    // Usamos poucos emojis e quebras de linha claras
    let msg = `*PEDIDO BIBI PIZZA* \n`;
    msg += `------------------------------\n`;
    
    msg += `*CLIENTE:* ${name}\n`;
    msg += `*LOCAL:* ${street}, ${number} - ${district}\n`;
    if (ref) msg += `(Ref: ${ref})\n`;
    msg += `------------------------------\n`;
    
    msg += `*PIZZA:* ${cart.size.name}\n`;
    msg += `*SABORES:*\nEAR: ${flavorNames.join(' + ')}\n`; // "EAR" é um jeito simples de listar, ou use seta
    
    if (bevLines.length > 0) {
        msg += `\n*BEBIDAS:*\n${bevLines.join('\n')}\n`;
    }
    
    if (obs) msg += `\n*OBS:* ${obs}\n`;
    
    msg += `------------------------------\n`;
    msg += `*PAGAMENTO:* ${paymentInfo}\n`;
    msg += `*TOTAL:* R$ ${total}\n`;

    // Enviar
    window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(msg)}`, '_blank');
}

init();