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
                </div>
                <div class="song-thumbnail ">
                        <img src="${song.cover_art_url}">
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