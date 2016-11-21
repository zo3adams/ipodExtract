#!/usr/bin/python
import eyed3
import sys, getopt
import os
from sets import Set
from shutil import copyfile

def main(argv):
   ipod_root = ''
   output_dir = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ipod_root=","output_dir="])
   except getopt.GetoptError:
      print 'test.py -i <ipod_root> -o <output_dir>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <ipod_root_directory> -o <output_directory>'
         sys.exit()
      elif opt in ("-i", "--ipod_root"):
         ipod_root = arg
      elif opt in ("-o", "--output_dir"):
         output_dir = arg
   print 'ipod root dir is: "', ipod_root
   print 'Output dir is "', output_dir

   music_dir = ipod_root + os.sep + "iPod_Control" + os.sep + "MUSIC"
   print music_dir

   found_genres = Set([])

   simple_genre_map = { 'Hardcore/Punk':'Punk', 'Abstract Hip-Hop':'Hip Hop', 'Metal':'Rock', 'Electronica':'Electronic', 'Lo-Fi':'Electronic', 'Rap / hip hop':'Hip Hop',
           'Alternative & Punk':'Punk', 'Ska':'Punk', 'Gangsta':'Hip Hop', 'Club-House':'Electronic', 'General Alternative':'Rock', 'Cool Jazz':'Jazz', 'Reggae':'Reggae',
           'Trip-Hop':'Hip Hop', 'Electronica & Dance':'Electronic', 'Alternative Metal':'Rock', 'Southern Rock':'Rock', 'Underground Hip-Hop/Rap':'Hip Hop',
           'Instrumental':'Electronic', 'Rock/Pop':'Rock', 'NYC Post Punk':'Punk', 'Hardcore':'Punk', 'Alternative Hip-Hop':'Hip Hop', 'Mashup':'Hip Hop', 
           'Rap / Hop Hop':'Hip Hop', 'Rap & Hip Hop':'Hip Hop', 'Rock & Roll':'Rock', 'Punk Rock':'Punk', 'Alternative':'Rock', 'Instrumental Hip-Hop':'Electronic',
           'Rap / Hip Hop':'Hip Hop', 'General Pop':'Pop', 'Drum & Bass':'Electronic', 'HipHop/Rap':'Hip Hop', 'Hard Rock':'Rock','Swamp Rock':'Rock', 'Hip-Hop':'Hip Hop',
           'Classic Rock':'Rock', 'Alternative Rock':'Rock', 'Disco':'Pop', 'Turntablism':'Electronic', 'Indie':'Rock', 'Hip-Hop/Rap':'Hip Hop','Dance':'Electornic', 
           'Rap':'Hip Hop', 'Folk-Rock':'Rock', 'Blues':'Rock', 'Hip Hop/Rap':'Hip Hop', 'Folk/Punk':'Punk'}
   mp3_copy_count = 0
 
   for root, dirs, files in os.walk(music_dir, topdown=False):
       for name in files:
           file_name = os.path.join(root, name)
           audiofile = eyed3.load(file_name)
           orig_extension = file_name.split('.')[1]

           if audiofile:
               try:
                   genre = audiofile.tag.genre.name
                   found_genres.add(genre)
                   if genre in simple_genre_map:
                       genre = simple_genre_map.get(genre)

                   artist = audiofile.tag.artist 
                   album =  audiofile.tag.album 
                   title = audiofile.tag.title 
                   track_num = audiofile.tag.track_num[1]
                   if not track_num:
                       track_num = 0
                   result = "found: genre {0},  artist {1}, album {2}, track {3}, title {4}".format(genre, artist, album, track_num, title)
                   print result

                   #make artist dir
                   print "making genre directories from output_dir {} and genre {}".format(output_dir, genre)
                   path_to_write = os.path.join(output_dir,genre)
                   if not os.path.exists(path_to_write):
                       os.makedirs(path_to_write)
                   path_to_write = os.path.join(path_to_write,artist) 
                   if not os.path.exists(path_to_write):
                       os.makedirs(path_to_write)
                   path_to_write = os.path.join(path_to_write, album)
                   if not os.path.exists(path_to_write):
                       os.makedirs(path_to_write)
                   file_name_to_write = "{0:03d}_{1}.{2}".format(track_num, title, orig_extension)
                   output_file_full_path = os.path.join(path_to_write, file_name_to_write)
                   if not os.path.exists(output_file_full_path):
                       copyfile(file_name, os.path.join(path_to_write, file_name_to_write))
                       mp3_copy_count += 1 

               except:
                   print("Unexpected error:", sys.exc_info()[0])


    
   print "found_genres: {}".format(found_genres)
   print "moved {} total files".format(mp3_copy_count)

if __name__ == "__main__":
   main(sys.argv[1:])






