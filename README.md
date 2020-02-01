# Video pipeline

Scripts to automate processing videos captured while cycling
using a gopro. The tasks are

- retrieve videos from gopro
- determine interesting pieces in the video
- extract interesting subclips
- perform video transformations such as style transfer
- upload videos to youtube

# Setup

Configuration of the strava client is done in the file `secrets/strava.yml`.

# Processing video

## Command line interface

Most features are available through the command line interface, which can be started via

```
pipenv run python cli.py
```

## Automatic mounting sd card

Add to `/etc/fstab` the line

```
/dev/mmcblk0p1 /media/gopro_sdcard vfat users 0 0
```

ensure `/media/gopro_sdcard` exists.

Run script

```
./download.sh
```

to retrieve videos from sd card and move them to `videos/incoming`. Furthemore, object detection is run on the videos creating `*.MP4.json` files.

Also the file `interesting_video_parts.csv` is being updated with segments that are interesting (currently not containing any cars)
