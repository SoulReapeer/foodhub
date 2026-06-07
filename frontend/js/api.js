const API_BASE = 'http://localhost:5000/api/v1';

// ── HTTP helpers ──────────────────────────────────────────────
async function apiFetch(path, options = {}) {
  const token = localStorage.getItem('fh_token');
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw { status: res.status, message: data.error || 'Request failed', data };
  return data;
}
const api = {
  get:    (path)         => apiFetch(path),
  post:   (path, body)   => apiFetch(path, { method: 'POST',   body: JSON.stringify(body) }),
  put:    (path, body)   => apiFetch(path, { method: 'PUT',    body: JSON.stringify(body) }),
  delete: (path)         => apiFetch(path, { method: 'DELETE' }),
};

// ── Auth state ────────────────────────────────────────────────
function getUser()    { try { return JSON.parse(localStorage.getItem('fh_user')); } catch { return null; } }
function getToken()   { return localStorage.getItem('fh_token'); }
function isLoggedIn() { return !!getToken(); }
function isAdmin()    { const u = getUser(); return u && u.role === 'admin'; }
function logout()     { localStorage.removeItem('fh_token'); localStorage.removeItem('fh_user'); }

function saveAuth(token, user) {
  localStorage.setItem('fh_token', token);
  localStorage.setItem('fh_user', JSON.stringify(user));
}

function requireAuth() {
  if (!isLoggedIn()) { window.location.href = '../pages/login.html'; return false; }
  return true;
}
function requireAdmin() {
  if (!isLoggedIn() || !isAdmin()) { window.location.href = '../pages/login.html'; return false; }
  return true;
}

// ── Cart ──────────────────────────────────────────────────────
function getCart()       { try { return JSON.parse(localStorage.getItem('fh_cart')) || []; } catch { return []; } }
function saveCart(cart)  { localStorage.setItem('fh_cart', JSON.stringify(cart)); updateCartBadge(); }
function clearCart()     { localStorage.removeItem('fh_cart'); updateCartBadge(); }

function addToCart(item) {
  const cart = getCart();
  const existing = cart.find(c => c.food_id === item.food_id);
  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({ ...item, quantity: 1 });
  }
  saveCart(cart);
  showToast(`${item.name} added to cart 🛒`, 'success');
}

function removeFromCart(food_id) {
  saveCart(getCart().filter(c => c.food_id !== food_id));
}

function updateQty(food_id, qty) {
  const cart = getCart();
  const item = cart.find(c => c.food_id === food_id);
  if (item) {
    item.quantity = qty;
    if (item.quantity <= 0) return removeFromCart(food_id);
  }
  saveCart(cart);
}

function cartTotal() {
  return getCart().reduce((s, c) => s + c.price * c.quantity, 0);
}

function cartCount() {
  return getCart().reduce((s, c) => s + c.quantity, 0);
}

function updateCartBadge() {
  const el = document.getElementById('cart-count');
  if (el) {
    const n = cartCount();
    el.textContent = n;
    el.style.display = n > 0 ? 'flex' : 'none';
  }
}

// ── Toast ─────────────────────────────────────────────────────
function showToast(msg, type = '') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  const t = document.createElement('div');
  t.className = `toast ${type}`;
  t.textContent = msg;
  container.appendChild(t);
  setTimeout(() => {
    t.style.animation = 'fadeOut .3s ease forwards';
    setTimeout(() => t.remove(), 300);
  }, 3000);
}

// ── Navbar renderer ───────────────────────────────────────────
function renderNavbar(rootPrefix = '..') {
  const user = getUser();
  const cartN = cartCount();
  const nav = document.createElement('nav');
  nav.className = 'navbar';
  nav.innerHTML = `
    <a class="navbar__logo" href="${rootPrefix}/index.html">
      <span class="navbar__logo-dot"></span> FoodHub
    </a>
    <div class="navbar__search">
      <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      <input type="text" placeholder="Search restaurants…" id="nav-search-input">
    </div>
    <div class="navbar__actions">
      <button class="navbar__cart-btn" id="nav-cart-btn" onclick="window.location='${rootPrefix}/pages/cart.html'">
        🛒 Cart
        <span class="navbar__cart-count" id="cart-count" style="display:${cartN>0?'flex':'none'}">${cartN}</span>
      </button>
      ${user
        ? `<div style="position:relative">
             <button class="navbar__user-btn" id="nav-user-btn" onclick="toggleUserMenu()">
               👤 ${user.name.split(' ')[0]}
             </button>
             <div id="user-menu" style="display:none;position:absolute;right:0;top:calc(100% + 6px);background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);box-shadow:var(--shadow-md);min-width:160px;overflow:hidden;z-index:200">
               <a href="${rootPrefix}/pages/profile.html" style="display:block;padding:11px 16px;font-size:14px;color:var(--ink-2);transition:background .15s" onmouseover="this.style.background='var(--surface-2)'" onmouseout="this.style.background=''">👤 My Profile</a>
               <a href="${rootPrefix}/pages/orders.html" style="display:block;padding:11px 16px;font-size:14px;color:var(--ink-2);transition:background .15s" onmouseover="this.style.background='var(--surface-2)'" onmouseout="this.style.background=''">📦 My Orders</a>
               ${isAdmin() ? `<a href="${rootPrefix}/pages/admin.html" style="display:block;padding:11px 16px;font-size:14px;color:var(--brand);transition:background .15s" onmouseover="this.style.background='var(--surface-2)'" onmouseout="this.style.background=''">⚙️ Admin Panel</a>` : ''}
               <div style="border-top:1px solid var(--border)"></div>
               <button onclick="doLogout('${rootPrefix}')" style="width:100%;text-align:left;padding:11px 16px;font-size:14px;color:#b91c1c;background:none;border:none;cursor:pointer;transition:background .15s" onmouseover="this.style.background='var(--surface-2)'" onmouseout="this.style.background=''">🚪 Logout</button>
             </div>
           </div>`
        : `<a href="${rootPrefix}/pages/login.html" class="btn btn-primary btn-sm">Sign in</a>`
      }
    </div>`;
  document.body.insertBefore(nav, document.body.firstChild);
  document.body.insertAdjacentHTML('afterbegin', '<div class="nav-page-spacer" style="display:none"></div>');
  // spacer as separate element
  const spacer = document.createElement('div');
  spacer.className = 'nav-page-spacer';
  nav.insertAdjacentElement('afterend', spacer);

  // Search
  const searchInput = nav.querySelector('#nav-search-input');
  if (searchInput) {
    searchInput.addEventListener('keydown', e => {
      if (e.key === 'Enter' && searchInput.value.trim()) {
        window.location = `${rootPrefix}/index.html?q=${encodeURIComponent(searchInput.value.trim())}`;
      }
    });
  }
  // Close menu on outside click
  document.addEventListener('click', e => {
    const menu = document.getElementById('user-menu');
    const btn  = document.getElementById('nav-user-btn');
    if (menu && !menu.contains(e.target) && btn && !btn.contains(e.target)) {
      menu.style.display = 'none';
    }
  });
}

function toggleUserMenu() {
  const menu = document.getElementById('user-menu');
  if (menu) menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
}

function doLogout(rootPrefix) {
  logout(); clearCart();
  window.location = `${rootPrefix}/pages/login.html`;
}

// ── Utility ───────────────────────────────────────────────────
function formatCurrency(n) { return '৳' + Number(n).toFixed(0); }
function formatDate(iso)   { return new Date(iso).toLocaleDateString('en-BD', { day:'numeric', month:'short', year:'numeric', hour:'2-digit', minute:'2-digit' }); }
function starRating(r)     { return '★'.repeat(Math.round(r)) + '☆'.repeat(5 - Math.round(r)); }

function qs(sel, ctx = document)  { return ctx.querySelector(sel); }
function qsa(sel, ctx = document) { return [...ctx.querySelectorAll(sel)]; }

function statusLabel(s) {
  const map = { pending:'Pending', accepted:'Accepted', preparing:'Preparing',
                out_for_delivery:'On the way', delivered:'Delivered', cancelled:'Cancelled' };
  return map[s] || s;
}
