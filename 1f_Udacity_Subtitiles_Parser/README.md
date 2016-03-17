## Udacity Subtitles Parser

This script turned out to be very handy for my peers in Udacity courses.

Udacity provides .rst downloadable files for the subtitles. The files are in the following format::
  
  timestamp
  sentence
  \n
  timestamp
  sentence

The script generates a single file in the following pattern::
  
  Lecture 1
    Lesson 1
    --------------
    Lesson 2
    --------------
    ...
  ================
