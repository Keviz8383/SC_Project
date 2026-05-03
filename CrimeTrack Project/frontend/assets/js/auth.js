/**
 * CrimeTrack - Auth Logic
 */

async function handleAuth(event, mode) {
    event.preventDefault();
    const btn = event.submitter;
    const originalHTML = btn.innerHTML;

    btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Authenticating...';
    btn.disabled = true;
    utils.showLoader();

    try {
        let payload = {};
        let endpoint = '';

        if (mode === 'register') {
            const name = document.getElementById('reg-name').value;
            const email = document.getElementById('reg-email').value;
            const password = document.getElementById('reg-password').value;
            const confirm = document.getElementById('reg-confirm').value;
            const role = document.getElementById('reg-role').value;

            if (password !== confirm) {
                utils.showMessage('Passwords do not match!', 'error');
                return;
            }

            payload = { name, email, password, role };
            endpoint = '/auth/register';
        } else {
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;

            payload = { email, password };
            endpoint = '/auth/login';
        }

        const data = await utils.apiFetch(endpoint, {
            method: 'POST',
            body: JSON.stringify(payload)
        });

        utils.showMessage(mode === 'register' ? 'Account Created Successfully!' : 'Identity Verified. Welcome.', 'success');
            
        if (mode === 'login') {
            utils.saveUser(data.user);
            utils.saveToken(data.session.access_token);

            setTimeout(() => {
                window.location.href = data.user.role === 'admin' ? 'admin.html' : 'citizen.html';
            }, 1000);
        } else {
            setTimeout(() => toggleAuth('login'), 2000);
        }
    } catch (err) {
        utils.showMessage(err.message, 'error');
    } finally {
        btn.innerHTML = originalHTML;
        btn.disabled = false;
        utils.hideLoader();
    }
}
