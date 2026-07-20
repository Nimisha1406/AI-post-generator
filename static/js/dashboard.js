console.log("dashboard.js loaded");

async function checkAuth() {

    let response = await fetch("/auth/me", {
        credentials: "include"
    });

    if (!response.ok) {
        window.location = "/login";
    }

}

checkAuth();




async function checkLinkedIn() {

    let response = await fetch("/linkedin/status", {
        credentials: "include"
    });

    let data = await response.json();

    console.log("LinkedIn status response:", data);

    let status = document.getElementById("linkedin_status");
    let button = document.getElementById("linkedin_button");

    if (data.connected) {

        status.innerHTML = `
            <div class="text-center">
                <img
                    src="${data.picture}"
                    class="rounded-circle shadow mb-3"
                    width="90"
                    height="90"
                    style="object-fit: cover;"
                >

                <h5 class="mb-1">${data.name}</h5>

                <p class="text-success">
                    <i class="bi bi-check-circle-fill"></i>
                    LinkedIn Connected
                </p>
            </div>
        `;

        button.innerHTML = "Disconnect LinkedIn";
        button.className = "btn btn-danger w-100 mt-3 rounded-3";
        button.onclick = disconnectLinkedIn;

    }
    else {

        status.innerHTML = `
            <p class="text-muted">
                Not Connected
            </p>
        `;

        button.innerHTML = "Connect LinkedIn";
        button.className = "btn btn-primary w-100 mt-3 rounded-3";
        button.onclick = connectLinkedIn;
    }
}




function connectLinkedIn() {

    window.location.href =
        "/linkedin/connect";

}



async function disconnectLinkedIn() {

    let token = localStorage.getItem("token");

    const response = await fetch(
        "/linkedin/disconnect",
        {
            method: "POST",
            headers: {
                "Authorization":
                    "Bearer " + token
            },
            credentials: "include"
        }
    );


    const data = await response.json();

    const message = document.getElementById("message");


    if (data.message) {

        message.innerHTML = `
            <div class="alert alert-success">
                ${data.message}
            </div>
        `;

    } else {

        message.innerHTML = `
            <div class="alert alert-danger">
                ${data.error}
            </div>
        `;

    }

    checkLinkedIn();

    setTimeout(() => {

        message.innerHTML = "";

    }, 3000);

}



async function generatePost() {

    let token = localStorage.getItem("token");

    let topic = document.getElementById("topic").value;

    const message = document.getElementById("message");

    const button = document.getElementById("generatePostBtn");

    button.disabled = true;

    message.innerHTML = `
        <div class="alert alert-info">
            Generating content...
        </div>
    `;

    if (!topic) {

        message.innerHTML = `
            <div class="alert alert-warning">
                Please enter a topic
            </div>
        `;

        button.disabled = false;

        setTimeout(() => {

            message.innerHTML = "";

        }, 3000);

        return;

    }

    let response = await fetch(
        "/posts/generate",
        {
            method: "POST",

            credentials: "include",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                topic: topic
            })
        }
    );

    let data;

    try {

        data = await response.json();

    }
    catch (error) {

        message.innerHTML = `
        <div class="alert alert-danger">
            Server returned invalid response
        </div>
    `;

        button.disabled = false;
        return;

    }

    if (data.error) {

        message.innerHTML = `
            <div class="alert alert-danger">
                ${data.error}
            </div>
        `;

        button.disabled = false;

        setTimeout(() => {

            message.innerHTML = "";

        }, 3000);

        return;

    }

    window.generatedPost = {

        id: data.id,

        content: data.post,

        image: null

    };

    updatePreview();

    button.disabled = false;

    message.innerHTML = `
        <div class="alert alert-success">
            Content generated successfully.
        </div>
    `;

    setTimeout(() => {

        message.innerHTML = "";

    }, 3000);

}




function showLinkedInMessage() {

    console.log("checking linkedin message");

    const params = new URLSearchParams(window.location.search);

    if (params.get("linkedin") === "success") {

        const message = document.getElementById("message");

        if (message) {

            message.style.display = "block";

            message.innerHTML = `
                <div class="alert alert-success">
                    LinkedIn connected successfully
                </div>
            `;
        }

        setTimeout(() => {

            window.history.replaceState(
                {},
                document.title,
                "/dashboard"
            );

            message.innerHTML = "";

        }, 3000);

    }

}



document.addEventListener("DOMContentLoaded", function () {

    console.log("DOM loaded");

    checkLinkedIn();

    showLinkedInMessage();

    document
        .getElementById("image_option")
        .addEventListener("change", function () {

            let aiSection =
                document.getElementById("ai_image_section");

            let uploadSection =
                document.getElementById("upload_image_section");

            if (this.value === "ai") {

                aiSection.style.display = "block";
                uploadSection.style.display = "none";

            }

            else if (this.value === "upload") {

                aiSection.style.display = "none";
                uploadSection.style.display = "block";

            }

            else {

                aiSection.style.display = "none";
                uploadSection.style.display = "none";

            }

        });

});


async function publishPost(postId) {

    let token = localStorage.getItem("token");

    let response = await fetch(
        `/posts/publish/${postId}`,
        {
            method: "POST",
            headers: {
                "Authorization":
                    "Bearer " + token
            }
        }
    );

    let data = await response.json();

    const message = document.getElementById("message");

    if (data.message) {

        message.innerHTML = `
            <div class="alert alert-success">
                ${data.message}
            </div>
        `;

    } else {

        message.innerHTML = `
            <div class="alert alert-danger">
                ${data.error}
            </div>
        `;

    }

    setTimeout(() => {

        message.innerHTML = "";

    }, 3000);

}



async function uploadImage() {

    let file =
        document.getElementById("image_upload").files[0];

    const message =
        document.getElementById("message");

    if (!file) {

        message.innerHTML = `
            <div class="alert alert-warning">
                Please select an image
            </div>
        `;

        setTimeout(() => {

            message.innerHTML = "";

        }, 3000);

        return;

    }

    if (!window.generatedPost) {

        message.innerHTML = `
            <div class="alert alert-warning">
                Generate content first
            </div>
        `;

        setTimeout(() => {

            message.innerHTML = "";

        }, 3000);

        return;

    }

    let formData = new FormData();

    formData.append(
        "image",
        file
    );

    let token =
        localStorage.getItem("token");

    let response =
        await fetch(
            "/posts/upload-image",
            {

                method: "POST",

                headers: {

                    "Authorization":
                        "Bearer " + token

                },

                body: formData

            }
        );

    let data =
        await response.json();

    console.log(
        "Upload response:",
        data
    );

    if (data.error) {

        message.innerHTML = `
            <div class="alert alert-danger">
                ${data.error}
            </div>
        `;

        setTimeout(() => {

            message.innerHTML = "";

        }, 3000);

        return;

    }

    window.generatedPost.image =
        data.image_path;

    await saveImagePath(
        data.image_path,
        "uploaded"
    );

    updatePreview();

    message.innerHTML = `
        <div class="alert alert-success">
            Image uploaded successfully
        </div>
    `;

    setTimeout(() => {

        message.innerHTML = "";

    }, 3000);

}



async function generateImage() {

    const message =
        document.getElementById("message");

    if (!window.generatedPost) {

        message.innerHTML = `
            <div class="alert alert-warning">
                Generate content first
            </div>
        `;

        setTimeout(() => {

            message.innerHTML = "";

        }, 3000);

        return;

    }

    const button = document.getElementById("generateImageBtn");

    button.disabled = true;

    message.innerHTML = `
        <div class="alert alert-info">
            Generating image...
        </div>
    `;

    let token =
        localStorage.getItem("token");

    let response =
        await fetch(
            "/posts/generate-image",
            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json",

                    "Authorization":
                        "Bearer " + token

                },

                body: JSON.stringify({

                    content:
                        window.generatedPost.content

                })

            }
        );

    let data =
        await response.json();

    if (data.error) {

        message.innerHTML = `
            <div class="alert alert-danger">
                ${data.error}
            </div>
        `;

        button.disabled = false;

        setTimeout(() => {

            message.innerHTML = "";

        }, 3000);

        return;

    }

    window.generatedPost.image =
        data.image_path;

    await saveImagePath(
        data.image_path,
        "generated"
    );

    updatePreview();

    button.disabled = false;

    message.innerHTML = `
        <div class="alert alert-success">
            Image generated successfully.
        </div>
    `;

    setTimeout(() => {

        message.innerHTML = "";

    }, 3000);

}



function showSchedule() {

    document.getElementById(
        "schedule_box"
    ).style.display = "block";

}



function updatePreview() {

    let post =
        window.generatedPost;

    if (!post) {

        return;

    }

    document.getElementById(
        "linkedin_preview"
    ).innerHTML = `

    <div class="card border-0">

        <div class="card-body">

            ${post.image

            ?

            `
                <img
                    src="/${post.image}"
                    class="img-fluid rounded mb-3"
                    style="width:100%; object-fit:cover;"
                >
                `

            :

            ""

        }

            <p style="white-space:pre-line;">

                ${post.content || ""}

            </p>

        </div>

    </div>

    `;

}



async function postNow() {

    const message =
        document.getElementById("message");

    if (!window.generatedPost) {

        message.innerHTML = `
            <div class="alert alert-warning">
                Generate content first
            </div>
        `;

        setTimeout(() => {

            message.innerHTML = "";

        }, 3000);

        return;

    }

    let token = localStorage.getItem("token");

    const button = document.getElementById("postNowBtn");

    button.disabled = true;

    message.innerHTML = `
        <div class="alert alert-info">
            Posting to LinkedIn...
        </div>
    `;

    let response = await fetch(
        `/posts/publish/${window.generatedPost.id}`,
        {
            method: "POST",

            headers: {
                "Authorization":
                    "Bearer " + token
            }
        }
    );

    let data = await response.json();

    if (data.message) {

        message.innerHTML = `
            <div class="alert alert-success">
                Posted to LinkedIn successfully.
            </div>
        `;

    }

    else {

        message.innerHTML = `
            <div class="alert alert-danger">
                ${data.error}
            </div>
        `;

    }

    button.disabled = false;

    setTimeout(() => {

        message.innerHTML = "";

    }, 3000);

}


async function saveImagePath(
    imagePath,
    imageType
) {

    let token =
        localStorage.getItem("token");

    await fetch(
        `/posts/save-image/${window.generatedPost.id}`,
        {

            method: "POST",

            headers: {

                "Content-Type":
                    "application/json",

                "Authorization":
                    "Bearer " + token

            },

            body: JSON.stringify({

                image_path: imagePath,

                image_type: imageType

            })

        }
    );

}




async function schedulePost() {

    const message =
        document.getElementById("message");

    if (!window.generatedPost) {

        message.innerHTML = `
            <div class="alert alert-warning">
                Generate content first
            </div>
        `;

        setTimeout(() => {

            message.innerHTML = "";

        }, 3000);

        return;

    }

    let time =
        document.getElementById(
            "schedule_time"
        ).value;

    if (!time) {

        message.innerHTML = `
            <div class="alert alert-warning">
                Select date and time
            </div>
        `;

        setTimeout(() => {

            message.innerHTML = "";

        }, 3000);

        return;

    }

    let token =
        localStorage.getItem("token");

    const button =
        document.getElementById("scheduleBtn");

    button.disabled = true;

    message.innerHTML = `
        <div class="alert alert-info">
            Confirming schedule...
        </div>
    `;

    let response =
        await fetch(
            "/posts/schedule",
            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json",

                    "Authorization":
                        "Bearer " + token

                },

                body: JSON.stringify({

                    time: time,

                    content:
                        window.generatedPost.content,

                    image:
                        window.generatedPost.image

                })

            }
        );

    let data =
        await response.json();

    if (data.message) {

        message.innerHTML = `
            <div class="alert alert-success">
                Schedule confirmed for publishing.
            </div>
        `;

    }

    else {

        message.innerHTML = `
            <div class="alert alert-danger">
                ${data.error}
            </div>
        `;

    }

    button.disabled = false;

    setTimeout(() => {

        message.innerHTML = "";

    }, 3000);

}