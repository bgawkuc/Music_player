set_paused = function () {
    document.getElementById("playpause-check").classList.add("paused");
}

play_song = function (id) {
    Amplitude.playNow(music.songs[id]);

    let player = document.getElementById("player");
    player.style.opacity = "100%";
    player.style.height = "200px";
    player.style.transform = null;
    player.style.visibility = "visible";
}

let music = {
    songs: {},
}

let lock = false;
let time_units = 0;
let last_index = null;

music.init = function () {

    amplitudeInit();

    function amplitudeInit() {
        let amplitudeSongs = [];

        for (let i = 0; i < music.songs.length; i++) {
            let song = music.songs[i];
            amplitudeSongs.push(song);
        }

        let amplitudeSettings = {
            'songs': amplitudeSongs,
            'volume': 50,
            'start_song': null,
            'callbacks': {
                loadstart: function () {
                    time_units -= 1; // remove first timeunit init play
                    if (time_units > 0 && last_index != null) {
                        $.ajax({
                            type: "POST",
                            url: '/stats/duration/',
                            data: {
                                csrfmiddlewaretoken: csrftoken,
                                song: Amplitude.getSongsState()[last_index].id,
                                time_units: time_units
                            }
                        });
                    }
                    time_units = 0;

                    if (last_index != null) {
                        $.ajax({
                            type: "POST",
                            url: '/stats/single/',
                            data: {
                                csrfmiddlewaretoken: csrftoken,
                                song: Amplitude.getSongsState()[Amplitude.getActiveIndex()].id
                            }
                        });
                    }
                    last_index = Amplitude.getActiveIndex()
                },
                timeupdate: () => {
                    if (!lock) {
                        time_units += 1;
                    }
                    console.log("beep")
                },
                seeking: () => {
                    lock = true;
                },
                seeked: () => {
                    lock = false;
                }
            }
        };

        for (let key in amplitudeSettings.playlists) {
            console.log(amplitudeSettings.playlists[key])
        }

        // console.log(amplitudeSettings['songs']);

        Amplitude.init(amplitudeSettings);
    }


}

let playpause_button = document.getElementById("playpause");
playpause_button.addEventListener("click", () => {
    document.getElementById("playpause-check").classList.toggle("paused");
})

let prev_button = document.getElementById("previous");
let next_button = document.getElementById("next");

prev_button.addEventListener("click", set_paused);
next_button.addEventListener("click", set_paused);

let songs_divs = document.getElementsByClassName("amplitude-song-container");
for (let song of songs_divs) {
    let id = song.getAttribute("data-amplitude-song-index");
    song.addEventListener("click", () => {
        play_song(id);
    });
    song.addEventListener("click", set_paused);
}

window.onunload = () => {
    if (time_units > 0 && last_index != null) {
        $.ajax({
            type: "POST",
            url: '/stats/duration/',
            data: {
                csrfmiddlewaretoken: csrftoken,
                song: Amplitude.getSongsState()[last_index].id,
                time_units: time_units
            },
            async: false // depends on browser
        });
    }
}