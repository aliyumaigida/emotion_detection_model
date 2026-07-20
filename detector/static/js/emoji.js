const emotionElement = document.getElementById("emotion-name");
const emoji = document.getElementById("emoji");

if (emotionElement && emoji) {

    const emotion = emotionElement.innerText.trim().toLowerCase();

    const emojiMap = {
        angry: "😠",
        fear: "😨",
        happy: "😄",
        sad: "😢",
        surprise: "😲",
        // disgust: "🤢",
        // neutral: "😐",
    };

    emoji.innerHTML = emojiMap[emotion] || "🙂";
}

