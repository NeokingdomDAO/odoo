// using old js syntax outside of Babel
var reportBugBtn = document.getElementById('report-bug-btn');
var submitForm = document.getElementById('report-bug-form');
var recaptchaSiteKey = document.getElementById('recaptcha-site-key').value;

if (reportBugBtn) {
    reportBugBtn.addEventListener('click', function () {
        // Show report bug form
        document.querySelector('.issue-page-container .body').classList.add('d-none');
        document.querySelector('.report-bug-body').classList.add('show');

        // smooth scroll to form (after animation)
        setTimeout(function () {
            // if the user already scrolled, don't scroll again
            if (document.querySelector('.issue-page-container').scrollTop === 0) {
                submitForm.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        }, 450); // .45s is the duration of the animation
    });
}
else {
    console.warn('Failed to bind show issue submit form on click event.');
}

function submitIssue(ev) {
    ev.preventDefault();

    grecaptcha.execute(recaptchaSiteKey, {action: 'submit'}).then(function(token) {
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'recaptcha_token_response';
        input.value = token;

        // Add the token to the form
        submitForm.appendChild(input);

        // Submit the form
        submitForm.submit();
    });
}

if (submitForm) {
    submitForm.addEventListener('submit', submitIssue);
}
else {
    console.warn('Failed to bind on submit event.');
}