Files on the Raspberry PIs
==========================

# All of these files when used belong on the Raspberry PI!!! #

### Camera prefix files ###

  * camera.py is deprecated. It used to be for timelapse photos controlled by python on the rPI instead of a cronjob.
  * camera.sh is a quick shell script camera test script. Can also use `raspistill -v -set -o cam.jpg`
  * camera_single.py takes one photo when called and outputs some small print options.
      * Also captures all metadata from the camera at the time of taking the picture
      * Change `experiment` variable for your experiment metadata
      * Change width, height, and offset to match your rPI grid as well.
          * Our grid starts numbered at 11 so our offset is 10 and our width and height are 6 and 30 respectively.
      * Change the path to the images folder if choosing to not use (`/home/pi/Images`) for the rPI photo storage.
      * Image filenames are mostly unique using a `hostname_gridy_gridx_timestamp` structure.
      * Our hostnames include the last octet of their IP address since they are static IP addresses.
      
### Other files ###

  * copy_rename.py uses our currentl naming structure to copy the files into coordinate grid filenames and hostname octet filenames which correspond to viewing the grid from two different starting positions (top left and bottom right respectively.)
      * Rewrite portions if used for your setup.
  * zeropad.sh adds leading zeros to files using bash, as of this moment it just echos a filename with the proper padding.
