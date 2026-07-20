let messageTimeout;

function showMessage(text, type) {
    const message = document.getElementById("message");

    if (!message) return;

    message.innerHTML = `
        <div class="alert alert-${type}">
            ${text}
        </div>
    `;

    // Clear any previous timer
    clearTimeout(messageTimeout);

    // Hide the message after 3 seconds
    messageTimeout = setTimeout(() => {
        message.innerHTML = "";
    }, 3000);
}




async function signup() {

    let username =
        document.getElementById("username").value.trim();

    let email =
        document.getElementById("email").value.trim();

    let password =
        document.getElementById("password").value;



    if (!username || !email || !password) {


        showMessage(
            "All fields are required",
            "danger"
        );

        return;

    }


    let response = await fetch(
        "/auth/signup",
        {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },


            body: JSON.stringify({

                username: username,

                email: email,

                password: password

            })

        }
    );



    let data = await response.json();




    if (response.ok) {

        // Save email for OTP page

        localStorage.setItem(
            "signup_email",
            email
        );



        showMessage(
            "OTP sent to your email",
            "success"
        );



        setTimeout(
            function () {

                window.location = "/verify-otp";

            },
            1500
        );



    }


    else {

        showMessage(
            data.error || "Signup failed",
            "danger"
        );

    }

}




async function verifyOTP() {


    let email = localStorage.getItem(
        "signup_email"
    );


    let otp =
        document.getElementById("otp").value;



    if (!email) {

        showMessage(
            "Signup email not found. Please signup again.",
            "danger"
        );

        return;

    }



    if (!otp) {

        showMessage(
            "Please enter OTP",
            "danger"
        );

        return;

    }



    let response = await fetch(
        "/auth/verify-otp",
        {

            method: "POST",

            credentials:"include",

            headers: {

                "Content-Type": "application/json"

            },


            body: JSON.stringify({

                email: email,

                otp: otp

            })

        }
    );



    let data = await response.json();


    if (response.ok) {

        localStorage.removeItem(
            "signup_email"
        );


        showMessage(
            "Signed in successfully",
            "success"
        );


        setTimeout(
            function () {

                window.location = "/dashboard";

            },
            1500
        );

    }

    else {

        showMessage(
            data.error || "OTP verification failed",
            "danger"
        );

    }

}






async function login() {

    let response = await fetch(
        "/auth/login",
        {

            method: "POST",

            credentials: "include",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({

                email:
                    document.getElementById(
                        "login_email"
                    ).value,

                password:
                    document.getElementById(
                        "login_password"
                    ).value

            })

        }
    );

    let data =
        await response.json();

    if (response.ok) {

        showMessage(
            "Login successful",
            "success"
        );

        setTimeout(function () {

            window.location =
                "/dashboard";

        }, 1000);


    }

    else {

        showMessage(
            data.error || "Login failed",
            "danger"
        );

    }

}




async function forgotPassword() {


    let response =
        await fetch(
            "/auth/forgot-password",
            {

                method: "POST",

                credentials:"include",

                headers: {
                    "Content-Type":
                        "application/json"
                },


                body: JSON.stringify({

                    email:
                        document.getElementById(
                            "forgot_email"
                        ).value

                })

            }
        );


    let data =
        await response.json();

    if (response.ok) {

        showMessage(
            "Password reset OTP sent to your email",
            "success"
        );


        localStorage.setItem(
            "reset_email",
            document.getElementById(
                "forgot_email"
            ).value
        );


        setTimeout(function () {

            window.location =
                "/reset-password";

        }, 1500);

    }

    else {

        showMessage(
            data.error,
            "danger"
        );

    }

}





async function resetPassword() {

    let email =
        localStorage.getItem(
            "reset_email"
        );


    let response =
        await fetch(
            "/auth/reset-password",
            {

                method: "POST",

                credentials:"include",

                headers: {
                    "Content-Type":
                        "application/json"
                },


                body: JSON.stringify({

                    email: email,


                    otp:
                        document.getElementById(
                            "reset_otp"
                        ).value,


                    new_password:
                        document.getElementById(
                            "new_password"
                        ).value

                })

            }
        );


    let data =
        await response.json();


    if (response.ok) {


        showMessage(
            "Password updated successfully",
            "success"
        );


        localStorage.removeItem(
            "reset_email"
        );


        setTimeout(function () {

            window.location =
                "/login";

        }, 1500);

    }

    else {

        showMessage(
            data.error,
            "danger"
        );

    }

}




async function logout() {

    await fetch(
        "/auth/logout",
        {

            method: "GET",

            credentials: "include"

        }
    );

    sessionStorage.setItem(
        "logout_message",
        "Logged out successfully"
    );

    window.location =
        "/login";


}