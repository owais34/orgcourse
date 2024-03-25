
# playlist-tracker-api

A Rest api to keep track of your videos and playlists , track watchtimes and resume where you last left off.


## Prerequirements

You need to have the following installed to run this project locally.

* python3 - https://www.python.org/downloads/
* pip - https://pip.pypa.io/en/stable/installation/
* Download ffmpeg - https://ffmpeg.org/
* Add ffmpeg to your windows path environment variable

## Run Locally

Clone the project

```bash
  git clone https://github.com/owais34/playlist-tracker-api.git
```

Go to the project directory after opening powershell/bash

```bash
  cd playlist-tracker-api
```

Build and install in virtual environment

* windows

```PowerShell
python3 -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
```

* Unix

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Run the server

```
py app.py
```


## Running Tests

To run tests, run the following command

```bash
  pytest
```


## REST API

The Rest App can be accessed running locally on localhost:5000


### Request (Get all added playlists)

`GET localhost:5000/`

```
curl -i -H 'Accept: application/json' http://localhost:5000/
```

### Response

```json
[
  {
    "name": "coursetest", // name of the playlist/folder
    "id": 0,  // unique id
    "duration": "30 s ", // total duration/playtime
    "progress": 100 // progress as a percentage%
  },
  {
    "name": "Violet Evergarden [BD][1080p][HEVC 10bit x265][Dual Audio][Tenrai-Sensei]",
    "id": 1,
    "duration": "7 h 45 m 42 s ",
    "progress": 5
  }
]
```

### Request (Get specific details of playlist/folder)

`GET localhost:5000/resume/:id`
- Parameters :  id of the playlist

```
curl -i -H 'Accept: application/json' http://localhost:5000/resume/1
```

### Response
The response is structured intuitively like

* Playlist details
    - SubFolders/SubModuleList (list of subfolders containing videos)
        - videoList (list of videos under a sub module/sub folder)

```json
{
  "directoryPath": "D:\\movies\\Spirited.Away.2001.JAPANESE.PROPER.1080p.BluRay.H264.AAC-RARBG", \\ path to the resource
  "subModuleList": [
    {
      "directoryPath": "D:\\movies\\Spirited.Away.2001.JAPANESE.PROPER.1080p.BluRay.H264.AAC-RARBG",
      "name": "dummysubmodule",
      "videoList": [
        {
          "path": "D:\\movies\\Spirited.Away.2001.JAPANESE.PROPER.1080p.BluRay.H264.AAC-RARBG\\Spirited.Away.2001.JAPANESE.PROPER.1080p.BluRay.H264.AAC-RARBG.mp4",
          "name": "Spirited.Away.2001.JAPANESE.PROPER.1080p.BluRay.H264.AAC-RARBG.mp4",
          "duration": 7472263,
          "durationPlayed": 216983
        }
      ],
      "duration": 7472263,
      "durationPlayed": 216983
    }
  ],
  "moduleIndex": 0, // last accessed module index
  "stoppedAtTime": 216983, // stop time in milli seconds
  "videoIndex": 0, // last accessed video of the last accessed module
  "duration": 7472263, // total duration
  "durationPlayed": 216983 // duration of playlist already played
}
```

### Request (Update Watchtime of a playlist)

`POST localhost:5000/update`

Request body :

* id - Id of the playlist,
* currentModule - index of current module
* currentVideo - index of current video
* currentTime - Watch Time in seconds (decimal)


```
curl -H 'Accept: application/json' 
-d '{"id":1,"currentModule":0,"currentVideo":0,"currentTime":23.2}' 
-X POST
http://localhost:5000/update
```

### Response

```json
true
```

### Request (Get video url)

`GET localhost:5000/cdn/:path`

Parameters :

* path - path of the video with > as path delimiter

Example (should be used a url for  **src** attribute ) :

```html
<video src="http://localhost:5000/cdn/D:>movies>movie.mp4"></video>

```


## Badges

Add badges from somewhere like: [shields.io](https://shields.io/)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

