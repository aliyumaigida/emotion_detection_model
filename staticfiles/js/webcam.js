const video = document.getElementById("video");
const emotion = document.getElementById("emotion");
const confidence = document.getElementById("confidence");

// Start webcam
navigator.mediaDevices.getUserMedia({
    video: true
})
.then(stream => {
    video.srcObject = stream;
});

// Create hidden canvas
const canvas = document.createElement("canvas");
const context = canvas.getContext("2d");

// Get CSRF token
function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                break;
            }
        }
    }

    return cookieValue;
}

const csrftoken = getCookie("csrftoken");

// Capture frame every 500ms
setInterval(() => {

    if (video.readyState !== 4) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    context.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
    );

    const image = canvas.toDataURL("image/jpeg");

    fetch("/predict-live/", {

        method: "POST",

        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },

        body: JSON.stringify({
            image: image
        })

    })
    .then(response => response.json())

    .then(data => {

        emotion.innerHTML =
            "😊 Emotion: <b>" + data.emotion + "</b>";

        confidence.innerHTML =
            "Confidence: " + data.confidence + "%";

    })

    .catch(error => {

        console.log(error);

    });

}, 500);