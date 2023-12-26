var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition

const recognition = new SpeechRecognition();
recognition.continuous = false;
recognition.lang = 'en-US';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

let animating = false;

const all_letters = [
    "æ",  "d",  "ɛ",  "ɪ",  "ɔ",  "u",
    "a",  "ð",  "f",  "l",  "p",  "ʊ",
    "b",  "e",  "g",  "m",  "s",
    "c",  "ə",  "h",  "o",  "t",
];

const send_message = async (message) => {
    const response = await fetch("/message", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({"message": message})
    });

    const json = await response.json();
    const duration = json.duration - 300;
    const audio_uri = "data:audio/wav;base64,"+json.audio;
    const letters = [];
    const stripped_response = json.ipa.toLowerCase().replace(/[\?!'ˈ ]/g, '');
    console.log(stripped_response);

    for(let i = 0; i < stripped_response.length; i++) {
        let letter = stripped_response[i];
        if( ! all_letters.includes(letter) ) {
            letter = all_letters[parseInt(Math.random()*all_letters.length)];
        }
        letters.push(letter);
    }

    const animation_speed = duration / stripped_response.length;

    const audio = new Audio(audio_uri);
    setTimeout(() => {
        stop_animation();
        recognition.start();
    }, duration + animation_speed);

    start_animation(letters, animation_speed);
    audio.play();
}

const start = () => {
    document.querySelector("#background").classList.remove("blurred");
    document.querySelector("#start").remove();

    recognition.start();

    recognition.onresult = function(event) {
        const message = event.results[0][0].transcript;

        send_message(message);
    }

    recognition.onspeechend = function() {
        recognition.stop();
    }

    recognition.onerror = function(event) {
        console.error(event.error);
    }
};

const next_frame = (letters, index, animation_speed) => {
    if( index > letters.length-1 ) {
        index = 0;
    }

    const bg_num1 = Number( index % 2 == 1 );
    const bg_num2 = Number( index % 2 == 0 );
    const background1 = "background" + bg_num1;
    const background2 = "background" + bg_num2;
    const letter = letters[index];
    setTimeout(() => {
        if( ! animating ) {
            return;
        }

        const bg_element1 = document.querySelector("#"+background1);
        const bg_element2 = document.querySelector("#"+background2);
        bg_element2.style.backgroundImage = "url('/static/images/letters/"+letter+".jpg')";
        bg_element2.style.zIndex = 1;
        bg_element1.style.zIndex = 2;

        next_frame(letters, index+1, animation_speed);
    }, animation_speed);
}

const start_animation = (letters, animation_speed) => {
    let index = 0;

    animating = true;
    next_frame(letters, index, animation_speed);
}

const stop_animation = () => {
    animating = false;
    document.querySelectorAll(".background").forEach(
        (e) => e.style.backgroundImage = "none"
    );
}
