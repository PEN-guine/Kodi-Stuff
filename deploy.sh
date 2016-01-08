cd ~/Apps/kodi-dev/Kodi-Stuff/
zip -r plugin.video.apalimarathi-0.0.8.zip plugin.video.apalimarathi/
mv plugin.video.apalimarathi-0.0.8.zip deployments/zips/plugin.video.apalimarathi/
cp plugin.video.apalimarathi/changelog.txt deployments/zips/plugin.video.apalimarathi/changelog-0.0.8.txt

cd ~/Apps/kodi-dev/Kodi-Stuff/deployments/zips/plugin.video.apalimarathi/
ln -fs changelog-0.0.8.txt changelog.txt

cd ~/Apps/kodi-dev/Kodi-Stuff/deployments/
python3 ~/Apps/kodi/addons/addon_md5_generator.py
