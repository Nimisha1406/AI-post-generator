document.addEventListener("DOMContentLoaded", async function () {

    const dashboard =
        document.getElementById("dashboard-link");

    const logout =
        document.getElementById("logout-link");

    const login =
        document.getElementById("login-link");

    const signup =
        document.getElementById("signup-link");


    let loggedIn = false;


    try {

        let response = await fetch("/auth/me", {
            credentials: "include"
        });


        loggedIn = response.ok;


    } catch (error) {

        loggedIn = false;

    }



    if (loggedIn) {

        if (dashboard)
            dashboard.style.display = "block";

        if (logout)
            logout.style.display = "block";

        if (login)
            login.style.display = "none";

        if (signup)
            signup.style.display = "none";

    }

    else {

        if (dashboard)
            dashboard.style.display = "none";

        if (logout)
            logout.style.display = "none";

        if (login)
            login.style.display = "block";

        if (signup)
            signup.style.display = "block";

    }



    document.body.style.visibility = "visible";


    const navbar =
        document.getElementById("main-navbar");


    if (navbar) {

        navbar.style.visibility = "visible";

    }

});