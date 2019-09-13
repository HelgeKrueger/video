# Setup

Configuration of the strava client is done in the file `secrets/strava.yml`.


# Processing video

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

## Next video

```
pipenv run next
```
extracts the next subclib marked as `unseen` in `interesting_video_parts.csv` and marks it as `processing`.

A list of video segments can be displayed using
```
pipenv run list
```

With
```
pipenv run done [--status $STATUS]
```
one sets all `processing` entries to `done`.

## Uploading to youtube

By running
```
pipenv run python tools/upload_video.py --input $FILE --title $TITLE --description $DESCRIPTION
```
one can upload the video to youtube


# Helper scripts

## Horizontal plots of what is visible in a video

```
pipenv run python tools/plot_hoticontal_bars.py --input videos/incoming/xxx.MP$.json
```
creates a horizontal plot of what is seen in the video.
