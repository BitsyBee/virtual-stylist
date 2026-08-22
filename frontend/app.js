const API_BASE = "http://127.0.0.1:8001";

// ================= DOM REFS =================
const $ = id => document.getElementById(id);
const qs = (sel, ctx = document) => ctx.querySelector(sel);
const qsa = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

// ================= THEME TOGGLE =================
function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('aura-theme', next);
    const icon = qs('#themeToggle i');
    if (icon) {
        icon.className = next === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
}

(function initTheme() {
    const saved = localStorage.getItem('aura-theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
    const icon = qs('#themeToggle i');
    if (icon) {
        icon.className = saved === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
})();

document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('themeToggle');
    if (toggle) toggle.addEventListener('click', toggleTheme);
});

// ================= MOBILE MENU =================
function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    if (menu) {
        menu.style.display = menu.style.display === 'flex' ? 'none' : 'flex';
    }
}

function closeMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    if (menu) menu.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('mobileMenuBtn');
    if (btn) btn.addEventListener('click', toggleMobileMenu);
});

// ================= TOAST =================
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        info: 'fa-info-circle'
    };
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<i class="fas ${icons[type] || icons.info}"></i> ${message}`;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(40px)';
        setTimeout(() => toast.remove(), 400);
    }, 4000);
}

// ================= LANDING & NAV =================
function showLanding() {
    const landing = document.getElementById('landingPage');
    const shell = document.getElementById('appShell');
    if (landing) landing.style.display = 'block';
    if (shell) shell.style.display = 'none';
    updateNavState();
    closeMobileMenu();
}

function handleStartStyling() {
    const token = localStorage.getItem('access_token');
    if (token) {
        showAppShell();
    } else {
        openAuthModal('login');
    }
}

async function showAppShell() {
    const landing = document.getElementById('landingPage');
    const modal = document.getElementById('authModal');
    const shell = document.getElementById('appShell');
    if (landing) landing.style.display = 'none';
    if (modal) modal.style.display = 'none';
    if (shell) shell.style.display = 'block';
    updateNavState();
    // Clear profile form before loading (prevents stale data)
    clearProfileForm();
    const profile = await loadProfile();
    renderTrending();
    renderStylistWelcome();
    loadChatHistoryFromBackend();
    renderFavoritesFromBackend();

    // If profile is empty, redirect to profile view
    if (!profile || isProfileEmpty(profile)) {
        showToast('Please complete your style profile to get personalized recommendations.', 'info');
        switchAppView('profile');
    } else {
        switchAppView('stylist');
    }
}

// ================= WELCOME GREETING =================
function getStoredUserName() {
    let name = localStorage.getItem('aura_user_name');
    if (name) return name;

    // Fallback for tokens issued before we started storing the
    // name in localStorage: decode it out of the JWT payload.
    const token = localStorage.getItem('access_token');
    if (!token) return '';
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload.name || '';
    } catch {
        return '';
    }
}

function renderStylistWelcome() {
    const name = getStoredUserName();
    const heading = document.getElementById('stylistWelcome');
    const subtext = document.getElementById('stylistSubtext');
    if (heading) {
        heading.textContent = name ? `Hey, ${name} 👋` : 'Describe your occasion';
    }
    if (subtext) {
        subtext.textContent = "Tell AURA where you're going, climate details, or desired moods.";
    }
}

function isProfileEmpty(profile) {
    if (!profile) return true;
    const fields = ['gender', 'skin_tone', 'body_type', 'style_preference', 'favorite_colors'];
    return fields.every(f => !profile[f] || profile[f].trim() === '');
}

function updateNavState() {
    const token = localStorage.getItem('access_token');
    const publicNav = document.getElementById('publicNav');
    const privateNav = document.getElementById('privateNav');
    const mobilePublic = document.getElementById('mobilePublicNav');
    const mobilePrivate = document.getElementById('mobilePrivateNav');

    if (token) {
        if (publicNav) publicNav.style.display = 'none';
        if (privateNav) privateNav.style.display = 'flex';
        if (mobilePublic) mobilePublic.style.display = 'none';
        if (mobilePrivate) mobilePrivate.style.display = 'flex';
    } else {
        if (publicNav) publicNav.style.display = 'flex';
        if (privateNav) privateNav.style.display = 'none';
        if (mobilePublic) mobilePublic.style.display = 'flex';
        if (mobilePrivate) mobilePrivate.style.display = 'none';
    }
}

function switchAppView(view) {
    const stylist = document.getElementById('stylistSection');
    const profile = document.getElementById('profileSection');
    const favorites = document.getElementById('favoritesSection');

    const tabStylist = document.getElementById('tabStylist');
    const tabProfile = document.getElementById('tabProfile');
    const tabFavorites = document.getElementById('tabFavorites');

    [stylist, profile, favorites].forEach(el => {
        if (el) el.style.display = 'none';
    });
    [tabStylist, tabProfile, tabFavorites].forEach(t => {
        if (t) t.classList.remove('active');
    });

    if (view === 'profile') {
        if (profile) profile.style.display = 'block';
        if (tabProfile) tabProfile.classList.add('active');
    } else if (view === 'favorites') {
        if (favorites) favorites.style.display = 'block';
        if (tabFavorites) tabFavorites.classList.add('active');
        renderFavoritesFromBackend();
    } else {
        if (stylist) stylist.style.display = 'block';
        if (tabStylist) tabStylist.classList.add('active');
        renderStylistWelcome();
    }
    closeMobileMenu();
}

// ================= PROFILE =================
function clearProfileForm() {
    document.getElementById('profileGender').value = '';
    document.getElementById('profileSkinTone').value = '';
    document.getElementById('profileBodyType').value = '';
    document.getElementById('profileStyle').value = '';
    document.getElementById('profileColors').value = '';
}

async function loadProfile() {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    try {
        const res = await fetch(`${API_BASE}/profile/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) return null;
        const p = await res.json();
        if (!p) {
            clearProfileForm();
            return null;
        }
        document.getElementById('profileGender').value = p.gender || '';
        document.getElementById('profileSkinTone').value = p.skin_tone || '';
        document.getElementById('profileBodyType').value = p.body_type || '';
        document.getElementById('profileStyle').value = p.style_preference || '';
        document.getElementById('profileColors').value = p.favorite_colors || '';
        return p;
    } catch (err) {
        console.error(err);
        return null;
    }
}

async function saveProfile() {
    const token = localStorage.getItem('access_token');
    const msg = document.getElementById('profileMessage');

    if (!token) {
        showToast('Please log in first.', 'error');
        return;
    }

    const body = {
        gender: document.getElementById('profileGender').value,
        skin_tone: document.getElementById('profileSkinTone').value,
        body_type: document.getElementById('profileBodyType').value,
        style_preference: document.getElementById('profileStyle').value,
        favorite_colors: document.getElementById('profileColors').value
    };

    // Validate required fields
    if (!body.gender || !body.skin_tone || !body.body_type || !body.style_preference) {
        if (msg) {
            msg.innerText = '⚠️ Please fill in all required fields.';
            msg.style.color = '#E74C3C';
        }
        showToast('Please fill in all required fields.', 'error');
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/profile/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(body)
        });

        const data = await res.json();

        if (res.ok) {
            if (msg) {
                msg.innerText = '✅ Profile saved successfully!';
                msg.style.color = '#27AE60';
            }
            showToast('Profile saved! 🎉', 'success');

            // 🔥 KEY: Re-load profile to confirm it's saved
            const profile = await loadProfile();

            // 🔥 KEY: Check if profile now exists (any field filled)
            if (profile && !isProfileEmpty(profile)) {
                // Switch to stylist view after successful save
                setTimeout(() => {
                    switchAppView('stylist');
                }, 500);
            } else {
                showToast('Profile saved but data seems incomplete. Please check.', 'warning');
            }
        } else {
            const errorMsg = data.detail || data.message || 'Error updating profile.';
            if (msg) {
                msg.innerText = '❌ ' + errorMsg;
                msg.style.color = '#E74C3C';
            }
            showToast(errorMsg, 'error');
        }
    } catch (err) {
        console.error('Save profile error:', err);
        if (msg) {
            msg.innerText = '❌ Connection error. Please try again.';
            msg.style.color = '#E74C3C';
        }
        showToast('Connection error saving profile.', 'error');
    }
}

// ================= AUTH =================
function openAuthModal(mode) {
    const modal = document.getElementById('authModal');
    if (modal) {
        modal.style.display = 'flex';
        toggleAuthMode(mode);
    }
}

function closeAuthModal() {
    const modal = document.getElementById('authModal');
    if (modal) modal.style.display = 'none';
}

function toggleAuthMode(mode) {
    const loginF = document.getElementById('loginForm');
    const signupF = document.getElementById('signupForm');
    if (mode === 'signup') {
        if (loginF) loginF.style.display = 'none';
        if (signupF) signupF.style.display = 'block';
    } else {
        if (loginF) loginF.style.display = 'block';
        if (signupF) signupF.style.display = 'none';
    }
}

async function login() {
    const email = document.getElementById('loginEmail')?.value.trim() || '';
    const password = document.getElementById('loginPassword')?.value || '';
    const errText = document.getElementById('loginResult');
    if (!email || !password) {
        if (errText) errText.innerText = 'Please enter both email and password.';
        return;
    }
    try {
        const res = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        if (!res.ok || !data.access_token) {
            if (errText) errText.innerText = data.detail || data.message || 'Login failed.';
            return;
        }
        localStorage.setItem('access_token', data.access_token);
        if (data.name) localStorage.setItem('aura_user_name', data.name);
        showAppShell();
        showToast('Welcome back! 🎉', 'success');
    } catch (err) {
        if (errText) errText.innerText = 'Connection error to authentication server.';
        showToast('Connection error', 'error');
    }
}

async function signup() {
    const name = document.getElementById('signupName')?.value.trim() || '';
    const email = document.getElementById('signupEmail')?.value.trim() || '';
    const password = document.getElementById('signupPassword')?.value || '';
    const errText = document.getElementById('signupResult');
    if (!name || !email || !password) {
        if (errText) errText.innerText = 'Please complete all fields.';
        return;
    }
    try {
        const res = await fetch(`${API_BASE}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });
        if (!res.ok) {
            const data = await res.json();
            if (errText) errText.innerText = data.detail || 'Registration failed.';
            return;
        }
        document.getElementById('loginEmail').value = email;
        document.getElementById('loginPassword').value = password;
        await login();
        showToast('Account created! Welcome to AURA ✨', 'success');
    } catch (err) {
        if (errText) errText.innerText = 'Failed to create account.';
        showToast('Registration error', 'error');
    }
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('aura_user_name');
    clearProfileForm(); // clear form data
    showLanding();
    showToast('Signed out', 'info');
}

// ================= PREFERENCE PICKER =================
let activePrefs = {};

function setPreference(type, value) {
    activePrefs[type] = value;
    const container = document.getElementById('selectedPrefs');
    if (container) {
        const labels = { formality: 'Formality', season: 'Season' };
        const display = `${labels[type] || type}: ${value}`;
        container.innerHTML = `<span>${display}</span>`;
    }
    document.querySelectorAll('.picker-chip').forEach(chip => {
        const pref = chip.dataset.pref;
        const val = chip.dataset.value;
        chip.classList.toggle('active', pref === type && val === value);
    });
    showToast(`Preference set: ${type} → ${value}`, 'info');
}

// ================= RECOMMENDATION ENGINE =================
function fillPrompt(txt) {
    const box = document.getElementById('userMessage');
    if (box) {
        box.value = txt;
        box.focus();
        box.style.height = 'auto';
        box.style.height = box.scrollHeight + 'px';
    }
}

document.addEventListener('input', (e) => {
    if (e.target.tagName === 'TEXTAREA') {
        e.target.style.height = 'auto';
        e.target.style.height = e.target.scrollHeight + 'px';
    }
});

function escapeHtml(str) {
    const d = document.createElement('div');
    d.textContent = str || '';
    return d.innerHTML;
}

function renderItemCard(item, categoryLabel) {
    const buyUrl = item.product_url && item.product_url !== '#' ? item.product_url : 'https://gflock.lk';
    const brandName = item.brand || 'GFLOCK';
    const fallbackImage = 'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?q=80&w=400';
    const imageSrc = item.image_url
        ? (item.image_url.startsWith('http') ? item.image_url : `${API_BASE}/${item.image_url}`)
        : fallbackImage;
    return `
        <div class="item-card">
            <div class="item-img-wrap">
                <span class="brand-tag">${brandName}</span>
                <img src="${imageSrc}" alt="${escapeHtml(item.name)}" onerror="this.src='${fallbackImage}'">
            </div>
            <div class="item-info">
                <div>
                    <h4>${escapeHtml(item.name)}</h4>
                    <p>${escapeHtml(item.color || '')} · ${escapeHtml(item.style || '')}</p>
                </div>
                <a href="${buyUrl}" target="_blank" rel="noopener noreferrer" class="btn-buy">
                    Shop on ${brandName} <i class="fas fa-arrow-right"></i>
                </a>
            </div>
        </div>
    `;
}

function renderOutfitsHtml(outfits, requestContext = {}) {
    let html = '';
    if (requestContext.occasion || requestContext.style || requestContext.temperature) {
        html += `
            <div class="bubble bubble-stylist">
                <strong>Request understood as:</strong>
                <br><br>
                ${requestContext.occasion ? `Occasion: ${escapeHtml(requestContext.occasion)}<br>` : ''}
                ${requestContext.style ? `Style: ${escapeHtml(requestContext.style)}<br>` : ''}
                ${requestContext.temperature ? `Temperature: ${escapeHtml(requestContext.temperature)}<br>` : ''}
                ${requestContext.season ? `Season: ${escapeHtml(requestContext.season)}<br>` : ''}
            </div>
        `;
    }
    outfits.forEach(outfit => {
        const encodedOutfit = encodeURIComponent(JSON.stringify(outfit));
        html += `
            <div class="outfit-card" data-outfit="${encodedOutfit}">
                <div class="outfit-header">
                    <h3>Outfit Option #${outfit.rank}</h3>
                    <span class="score-badge">Match Score: ${outfit.score}</span>
                    <button class="btn btn-outline" onclick="saveOutfitFromCard(this)" style="padding:4px 10px;font-size:12px;">
                        <i class="fas fa-heart"></i> Save
                    </button>
                </div>
                ${outfit.reasons && outfit.reasons.length ? `
                    <div class="recommendation-reasons">
                        <strong>Why this outfit was recommended</strong>
                        <ul>
                            ${outfit.reasons.slice(0,5).map(r => `<li>${escapeHtml(r)}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                <div class="outfit-items-grid">
                    ${renderItemCard(outfit.top, 'TOP')}
                    ${renderItemCard(outfit.bottom, 'BOTTOM')}
                    ${renderItemCard(outfit.shoes, 'SHOES')}
                </div>
            </div>
        `;
    });
    return html;
}

async function getRecommendation() {
    const message = document.getElementById('userMessage').value.trim();
    const resultDiv = document.getElementById('result');
    const token = localStorage.getItem('access_token');
    if (!message) return;
    if (!token) {
        openAuthModal('login');
        return;
    }

    // Add user message
    const userBubble = document.createElement('div');
    userBubble.className = 'bubble bubble-user';
    userBubble.textContent = message;
    resultDiv.parentNode.insertBefore(userBubble, resultDiv);

    const loadingBubble = document.createElement('div');
    loadingBubble.className = 'bubble bubble-stylist';
    loadingBubble.id = 'loadingBubble';
    loadingBubble.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Understanding your request...`;
    resultDiv.parentNode.insertBefore(loadingBubble, resultDiv);

    document.getElementById('userMessage').value = '';
    document.getElementById('userMessage').style.height = 'auto';

    try {
        const res = await fetch(`${API_BASE}/recommendation/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ user_request: message })
        });
        const data = await res.json();

        if (!res.ok) {
            loadingBubble.outerHTML = `
                <div class="bubble bubble-stylist">
                    ${escapeHtml(data.detail || data.message || 'Unable to generate recommendations.')}
                </div>
            `;
            showToast('Failed to get recommendations', 'error');
            return;
        }
        if (!data.outfits || !Array.isArray(data.outfits) || data.outfits.length === 0) {
            loadingBubble.outerHTML = `
                <div class="bubble bubble-stylist">${escapeHtml(data.message || 'No suitable outfits were found.')}</div>
            `;
            return;
        }

        loadingBubble.remove();
        const resultContainer = document.getElementById('result');
        resultContainer.innerHTML = '';
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = renderOutfitsHtml(data.outfits, data.request_context);
        while (tempDiv.firstChild) {
            resultContainer.appendChild(tempDiv.firstChild);
        }

        // Save chat to backend
        await saveChatToBackend(message, data);

        showToast(`Found ${data.outfits.length} outfit options! ✨`, 'success');

    } catch (error) {
        console.error('Recommendation error:', error);
        loadingBubble.outerHTML = `
            <div class="bubble bubble-stylist">
                Unable to connect to the recommendation service. Please make sure the backend is running.
            </div>
        `;
        showToast('Connection error to recommendation service', 'error');
    }
}

// ================= FAVORITES (Backend API) =================
async function fetchFavorites() {
    const token = localStorage.getItem('access_token');
    if (!token) return [];
    try {
        const res = await fetch(`${API_BASE}/favorites/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) return [];
        return await res.json();
    } catch {
        return [];
    }
}

async function saveFavoriteToBackend(outfitData) {
    const token = localStorage.getItem('access_token');
    if (!token) {
        showToast('Please log in to save outfits.', 'error');
        return false;
    }
    try {
        const res = await fetch(`${API_BASE}/favorites/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ outfit_data: outfitData })
        });
        if (!res.ok) {
            const err = await res.json();
            showToast(err.detail || 'Failed to save.', 'error');
            return false;
        }
        showToast('Outfit saved to favorites! ❤️', 'success');
        return true;
    } catch {
        showToast('Error saving outfit.', 'error');
        return false;
    }
}

async function deleteFavoriteFromBackend(favoriteId) {
    const token = localStorage.getItem('access_token');
    if (!token) return false;
    try {
        const res = await fetch(`${API_BASE}/favorites/${favoriteId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) return false;
        showToast('Removed from favorites', 'info');
        return true;
    } catch {
        return false;
    }
}

async function saveOutfitFromCard(btn) {
    const card = btn.closest('.outfit-card');
    if (!card) {
        showToast('Could not find outfit card.', 'error');
        return;
    }
    const encoded = card.dataset.outfit;
    if (!encoded) {
        showToast('Outfit data not found.', 'error');
        return;
    }
    try {
        const outfit = JSON.parse(decodeURIComponent(encoded));
        const success = await saveFavoriteToBackend(outfit);
        if (success) {
            const favSection = document.getElementById('favoritesSection');
            if (favSection && favSection.style.display !== 'none') {
                renderFavoritesFromBackend();
            }
        }
    } catch (e) {
        console.error('Save outfit error:', e);
        showToast('Error saving outfit. Invalid data.', 'error');
    }
}

async function removeFavoriteFromBackend(favoriteId) {
    const success = await deleteFavoriteFromBackend(favoriteId);
    if (success) {
        renderFavoritesFromBackend();
    }
}

async function renderFavoritesFromBackend() {
    const grid = document.getElementById('favoritesGrid');
    if (!grid) return;
    const favorites = await fetchFavorites();

    if (favorites.length === 0) {
        grid.innerHTML = `
            <div class="favorites-empty">
                <i class="fas fa-heart" style="font-size:48px; color:var(--text-muted);"></i>
                <p>No saved outfits yet. Start saving your favorite looks!</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = favorites.map(fav => {
        const outfit = fav.outfit_data;
        return `
            <div class="favorite-item" data-fav-id="${fav.id}">
                <button class="remove-fav" onclick="removeFavoriteFromBackend(${fav.id})" title="Remove from favorites">
                    <i class="fas fa-trash-alt"></i>
                </button>
                <div class="outfit-header">
                    <h3>Saved Outfit</h3>
                    <span class="score-badge">Score: ${outfit.score}</span>
                </div>
                ${outfit.reasons && outfit.reasons.length ? `
                    <div class="recommendation-reasons" style="margin-bottom:10px;">
                        <ul style="margin:0;padding-left:17px;">
                            ${outfit.reasons.slice(0,3).map(r => `<li>${escapeHtml(r)}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                <div class="outfit-items-grid">
                    ${renderItemCard(outfit.top, 'TOP')}
                    ${renderItemCard(outfit.bottom, 'BOTTOM')}
                    ${renderItemCard(outfit.shoes, 'SHOES')}
                </div>
            </div>
        `;
    }).join('');
}

// ================= CHAT HISTORY (Backend API) =================
async function fetchChatHistory() {
    const token = localStorage.getItem('access_token');
    if (!token) return [];
    try {
        const res = await fetch(`${API_BASE}/chat/history?limit=50`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) return [];
        return await res.json();
    } catch {
        return [];
    }
}

async function saveChatToBackend(userMessage, responseData) {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    try {
        await fetch(`${API_BASE}/chat/history`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ user_message: userMessage, response_data: responseData })
        });
    } catch (e) {
        console.warn('Failed to save chat history:', e);
    }
}

async function loadChatHistoryFromBackend() {
    const chatLog = document.getElementById('chatLog');
    if (!chatLog) return;
    const history = await fetchChatHistory();
    if (history.length === 0) {
        chatLog.innerHTML = `
            <div class="bubble bubble-stylist">
                <i class="fas fa-robot"></i> Welcome back. Let me know what event or outfit mood you are preparing for today.
            </div>
            <div id="result"></div>
        `;
        return;
    }
    let html = `
        <div class="bubble bubble-stylist">
            <i class="fas fa-robot"></i> Welcome back. Let me know what event or outfit mood you are preparing for today.
        </div>
    `;
    const reversed = [...history].reverse();
    for (const entry of reversed) {
        html += `<div class="bubble bubble-user">${escapeHtml(entry.user_message)}</div>`;
        const data = entry.response_data;
        if (data.outfits && data.outfits.length) {
            html += renderOutfitsHtml(data.outfits, data.request_context || {});
        } else {
            html += `<div class="bubble bubble-stylist">${escapeHtml(data.message || 'No outfits found.')}</div>`;
        }
    }
    html += `<div id="result"></div>`;
    chatLog.innerHTML = html;
    chatLog.scrollTop = chatLog.scrollHeight;
}

// ================= VOICE INPUT =================
let recognition = null;
let isListening = false;

function startVoiceInput() {
    const micBtn = document.querySelector('.mic-btn');
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        showToast('Voice input not supported in this browser.', 'error');
        return;
    }
    if (isListening) {
        if (recognition) recognition.stop();
        isListening = false;
        if (micBtn) micBtn.classList.remove('listening');
        return;
    }
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = function() {
        isListening = true;
        if (micBtn) micBtn.classList.add('listening');
        showToast('Listening... Speak now', 'info');
    };
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        const box = document.getElementById('userMessage');
        if (box) {
            box.value = transcript;
            box.style.height = 'auto';
            box.style.height = box.scrollHeight + 'px';
            box.focus();
        }
        showToast('Voice input captured!', 'success');
    };
    recognition.onerror = function(event) {
        console.error('Speech recognition error', event.error);
        showToast('Voice input error: ' + event.error, 'error');
        if (micBtn) micBtn.classList.remove('listening');
        isListening = false;
    };
    recognition.onend = function() {
        isListening = false;
        if (micBtn) micBtn.classList.remove('listening');
    };
    recognition.start();
}

// ================= TRENDING =================
function renderTrending() {
    const grid = document.getElementById('trendingGrid');
    if (!grid) return;
    const trends = [
        { name: 'Oversized Blazer', image: 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?q=80&w=300', tag: 'Business' },
        { name: 'Linen Wide Pants', image: 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?q=80&w=300', tag: 'Summer' },
        { name: 'Leather Midi Skirt', image: 'https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?q=80&w=300', tag: 'Evening' },
        { name: 'Chunky Sneakers', image: 'https://images.unsplash.com/photo-1549298916-b41d501d3772?q=80&w=300', tag: 'Streetwear' }
    ];
    grid.innerHTML = trends.map(t => `
        <div class="trending-item" onclick="fillPrompt('Show me outfits featuring ${t.name}')">
            <img src="${t.image}" alt="${escapeHtml(t.name)}" loading="lazy">
            <div class="info">
                <h4>${escapeHtml(t.name)}</h4>
                <p>${escapeHtml(t.tag)}</p>
            </div>
        </div>
    `).join('');
}

// ================= KEYBOARD SHORTCUTS =================
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        const active = document.activeElement;
        if (active && active.id === 'userMessage') {
            e.preventDefault();
            getRecommendation();
        }
    }
});

// ================= INIT =================
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    if (token) {
        showAppShell();
    } else {
        showLanding();
    }
    renderTrending();
});

// ================= GLOBAL EXPOSURE =================
window.showLanding = showLanding;
window.handleStartStyling = handleStartStyling;
window.showAppShell = showAppShell;
window.switchAppView = switchAppView;
window.openAuthModal = openAuthModal;
window.closeAuthModal = closeAuthModal;
window.toggleAuthMode = toggleAuthMode;
window.login = login;
window.signup = signup;
window.logout = logout;
window.fillPrompt = fillPrompt;
window.getRecommendation = getRecommendation;
window.loadProfile = loadProfile;
window.saveProfile = saveProfile;
window.setPreference = setPreference;
window.renderTrending = renderTrending;
window.renderStylistWelcome = renderStylistWelcome;
window.closeMobileMenu = closeMobileMenu;
window.toggleMobileMenu = toggleMobileMenu;
window.startVoiceInput = startVoiceInput;
window.saveOutfitFromCard = saveOutfitFromCard;
window.removeFavoriteFromBackend = removeFavoriteFromBackend;
window.renderFavoritesFromBackend = renderFavoritesFromBackend;
