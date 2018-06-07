function go() {
    if(firstname && lastname) {
        let profileLink = document.querySelector('.profile_link_tag');
        profileLink.setAttribute('href', '/music/profile/');
        profileLink.text = firstname + ' ' + lastname;
    }
}

function setActive() {
    if(redirectFrom) {
        let signupTabLink = document.querySelector('#signup-tab-link'),
            signinTabLink = document.querySelector('#signin-tab-link'),
            signupTab = document.querySelector('#signup-tab'),
            signinTab = document.querySelector('#signin-tab');
        if(redirectFrom === "signup") {
            $(signinTabLink).removeClass('is-active');
            $(signinTab).removeClass('is-active');
            $(signupTabLink).addClass('is-active');
            $(signupTab).addClass('is-active');
        } else if(redirectFrom === "login") {
            $(signupTabLink).removeClass('is-active');
            $(signupTab).removeClass('is-active');
            $(signinTabLink).addClass('is-active');
            $(signinTab).addClass('is-active');
        }
    }
}

window.onload = setActive();

// window.onload = go();