console.log("WEBCAM.JS IS LOADED");

const video = document.getElementById("video");
const emotion = document.getElementById("emotion");
const confidence = document.getElementById("confidence");


// --------------------------------------------------
// OVERLAY CANVAS
// --------------------------------------------------

const overlay = document.getElementById("overlay");
const overlayContext = overlay.getContext("2d");


// --------------------------------------------------
// LATEST PREDICTION
// --------------------------------------------------

let latestPrediction = null;


// --------------------------------------------------
// START CAMERA
// --------------------------------------------------

navigator.mediaDevices.getUserMedia({
    video: true
})
.then(stream => {

    video.srcObject = stream;

})
.catch(error => {

    console.log("Camera error:", error);

});


// --------------------------------------------------
// HIDDEN CANVAS
// Used to capture webcam frames
// --------------------------------------------------

const canvas = document.createElement("canvas");
const context = canvas.getContext("2d");

const probabilitiesContainer =
    document.getElementById("probabilities");

function drawProbabilities(probabilities) {

    if (!probabilities) {
        return;
    }

    probabilitiesContainer.innerHTML = "";

    for (const [emotionName, probability] of Object.entries(probabilities)) {

        const row = document.createElement("div");

        row.style.marginBottom = "15px";


        const label = document.createElement("div");

        label.style.display = "flex";
        label.style.justifyContent = "space-between";
        label.style.marginBottom = "5px";

        label.innerHTML = `
            <span>${emotionName}</span>
            <strong>${probability}%</strong>
        `;


        const barBackground =
            document.createElement("div");

        barBackground.style.width = "100%";
        barBackground.style.height = "12px";
        barBackground.style.background = "#dee2e6";
        barBackground.style.borderRadius = "6px";
        barBackground.style.overflow = "hidden";


        const bar =
            document.createElement("div");

        bar.style.width =
            probability + "%";

        bar.style.height = "100%";

        bar.style.background =
            "#0d6efd";

        bar.style.borderRadius = "6px";

        bar.style.transition =
            "width 0.3s ease";


        barBackground.appendChild(bar);

        row.appendChild(label);

        row.appendChild(barBackground);

        probabilitiesContainer.appendChild(row);
    }
}
// --------------------------------------------------
// CSRF TOKEN
// --------------------------------------------------

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


// --------------------------------------------------
// PREPARE OVERLAY
// --------------------------------------------------

function prepareOverlay() {

    const displayWidth = video.clientWidth;
    const displayHeight = video.clientHeight;

    if (
        overlay.width !== displayWidth ||
        overlay.height !== displayHeight
    ) {

        overlay.width = displayWidth;
        overlay.height = displayHeight;
    }
}


// --------------------------------------------------
// DRAW EVERYTHING
// --------------------------------------------------

function drawVisualization() {

    if (!video.videoWidth || !video.videoHeight) {
        return;
    }


    // Make sure canvas matches video
    prepareOverlay();


    // Clear previous frame
    overlayContext.clearRect(
        0,
        0,
        overlay.width,
        overlay.height
    );


    // Nothing to draw yet
    if (!latestPrediction) {
        return;
    }


    // ----------------------------------------------
    // Check face
    // ----------------------------------------------

    if (!latestPrediction.face_detected) {
        return;
    }


    const bbox = latestPrediction.bbox;

    const landmarks =
        latestPrediction.landmarks;


    const emotionName =
        latestPrediction.emotion;

    const confidenceValue =
        latestPrediction.confidence;


    const cameraWidth =
        video.videoWidth;

    const cameraHeight =
        video.videoHeight;

    const displayWidth =
        video.clientWidth;

    const displayHeight =
        video.clientHeight;


    const scaleX =
        displayWidth / cameraWidth;

    const scaleY =
        displayHeight / cameraHeight;


    // ==============================================
    // DRAW BOUNDING BOX
    // ==============================================

    if (bbox) {

        const x =
            bbox.x * scaleX;

        const y =
            bbox.y * scaleY;

        const width =
            bbox.width * scaleX;

        const height =
            bbox.height * scaleY;


        overlayContext.strokeStyle =
            "red";

        overlayContext.lineWidth =
            5;


        overlayContext.strokeRect(
            x,
            y,
            width,
            height
        );


        // ------------------------------------------
        // Emotion label
        // ------------------------------------------

        overlayContext.font =
            "bold 20px Arial";

        overlayContext.fillStyle =
            "red";


        overlayContext.fillText(
            emotionName +
            " " +
            confidenceValue +
            "%",
            x,
            Math.max(
                25,
                y - 10
            )
        );
    }


    // ==============================================
    // DRAW FACIAL LANDMARKS
    // ==============================================

    if (landmarks && landmarks.length > 0) {

        overlayContext.fillStyle =
            "lime";


        for (const landmark of landmarks) {

            const x =
                landmark.x *
                displayWidth;

            const y =
                landmark.y *
                displayHeight;


            overlayContext.beginPath();

            overlayContext.arc(
                x,
                y,
                2,
                0,
                Math.PI * 2
            );

            overlayContext.fill();
        }
    }
}


// --------------------------------------------------
// CONTINUOUS DRAWING
// --------------------------------------------------

function animate() {

    drawVisualization();

    requestAnimationFrame(
        animate
    );
}


// Start visualization
animate();


// --------------------------------------------------
// PREDICTION EVERY 500ms
// --------------------------------------------------

setInterval(() => {

    if (video.readyState !== 4) {
        return;
    }


    // ----------------------------------------------
    // Capture webcam frame
    // ----------------------------------------------

    canvas.width =
        video.videoWidth;

    canvas.height =
        video.videoHeight;


    context.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
    );


    // ----------------------------------------------
    // Convert image to Base64
    // ----------------------------------------------

    const image =
        canvas.toDataURL(
            "image/jpeg"
        );


    // ----------------------------------------------
    // Send image to Django
    // ----------------------------------------------

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

        console.log(
            "DJANGO RESPONSE:",
            data
        );


        // ------------------------------------------
        // Store latest prediction
        // ------------------------------------------

        latestPrediction = data;


        // ------------------------------------------
        // Update probability panel
        // ------------------------------------------

        drawProbabilities(
            data.probabilities
        );


        // ------------------------------------------
        // Update emotion text
        // ------------------------------------------

        if (!data.face_detected) {

            emotion.innerHTML =
                "😊 Emotion: <b>No face detected</b>";

            confidence.innerHTML =
                "Confidence: 0%";

            return;
        }


        emotion.innerHTML =
            "😊 Emotion: <b>" +
            data.emotion +
            "</b>";


        confidence.innerHTML =
            "Confidence: " +
            data.confidence +
            "%";

    })


}, 500);