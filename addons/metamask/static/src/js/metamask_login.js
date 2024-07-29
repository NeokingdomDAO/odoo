odoo.define('metamask.metamask_login', function (require) {
    "use strict";

    const ajax = require('web.ajax');

    async function connectMetaMask() {
        if (typeof window.ethereum !== 'undefined') {
            try {
                let accounts = await ethereum.request({ method: 'eth_requestAccounts' });
                let account = accounts[0];

                // Request the user to sign a message
                let message = "Please sign this message to authenticate with Odoo.";
                let signature = await ethereum.request({ method: 'personal_sign', params: [message, account] });

                // Send the address and the signature to the backend
                ajax.jsonRpc('/metamask/login', 'call', { 'wallet_address': account, 'signature': signature, 'message': message }).then(function (result) {
                    if (result.success) {
                        window.location.href = '/web';
                    } else {
                        alert(result.message);
                    }
                });
            } catch (error) {
                console.error('User denied account access or denied message signing', error);
            }
        } else {
            console.log('MetaMask is not installed');
            alert('Please install MetaMask to use this feature.');
        }
    }

    document.getElementById('metamask-login-button').addEventListener('click', connectMetaMask);
});