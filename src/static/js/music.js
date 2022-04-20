let playpause_button = document.getElementById("playpause");
playpause_button.addEventListener("click",  () => {
    document.getElementById("playpause-check").classList.toggle("paused");
})

let prev_button = document.getElementById("previous");
let next_button = document.getElementById("next");

set_paused = function (){
    document.getElementById("playpause-check").classList.add("paused");
}

prev_button.addEventListener("click", set_paused);
next_button.addEventListener("click", set_paused);

var music = {
    songs: {},
}

music.init = function () {

    amplitudeInit();

    function amplitudeInit() {
        let amplitudeSongs = [];

        for (var i = 0; i < music.songs.length; i++) {
            let container = document.createElement('div');
            let playlist = document.getElementById('songs')
            let song = music.songs[i];

            let classNames = 'amplitude-song-container amplitude-play';

            container.addEventListener("click", set_paused)
            container.setAttribute('data-amplitude-song-index', i.toString());
            container.className = classNames;
            container.innerHTML = `
                <div data-amplitude-song-index=${i} class="song-info">
                    <div class="song-basic">
                        <div class="song-title">${song.name}</div>
                        <div class="song-artist">${song.artist}</div>
                    </div>
                    <div class="song-addit">
                        <div class="genre">${song.genre}</div>
                        <div class="duration">${song.duration}</div>
                    </div>
                    <div class="song-details">
                        <a href="song-details/${song.id}"><i class="fa fa-info"></i></a>
                    </div>
                </div>
                 
                <div class="song-thumbnail ">
                        <img src="${song.cover_art_url}" alt="album image">
                        <div class="activity">
                        </div>
                </div>
            `
            playlist.appendChild(container);
            amplitudeSongs.push(song);
        }

        let amplitudeSettings = {
            'songs': amplitudeSongs,
            'volume': 50
        };

        for (let key in amplitudeSettings.playlists) {
            console.log(amplitudeSettings.playlists[key])
        }

        // console.log(amplitudeSettings['songs']);

        Amplitude.init(amplitudeSettings);


    }


}
