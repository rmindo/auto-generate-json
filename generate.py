import os
import re
import sys
import shutil


# Base object
base = {
  'set1': {
    'sentences': []
  },
  'set2': {
    'sentences': []
  },
}

# Path destination
dest = {
  'assets': 'assets/illustration/',
  'android': 'raw/',
  # 'android': 'android/app/src/main/res/raw/',
}

# Source path
source = {
  'audio': 'audio/',
  'illustration': 'illustration/',
}

# Clean string
def clean(string):
  return re.sub(r'\s', '_', re.sub(r'[^a-z-A-Z0-9\-\s_\.mp3]+', '', ''.join(string.strip())))


def generate(name):
  # Open file
  with open(name+'.tsv', 'r') as f:
    items = {}
    lines = f.readlines()
    
    # Audio
    def audio(name):
      ext = ''
      file = clean(name)
      regex = r'^((\d+)_([0-9a-z]{1})_)'

      # Remove .wav extension if exist
      if '.wav' in file:
        file = file.replace('.wav', '.mp3')
      # Check if it has extension already else add it
      if '.mp3' not in file:
        ext = '.mp3'

      # Source file
      src = os.path.realpath(source['audio']+file)
      # Remove numbers at the beginning
      name = (re.sub(regex, '', file) + ext).lower()

      if os.path.exists(src):
        shutil.copy(src, dest['android']+name)
      else:
        print('Error: audio name "'+ file +'" not exist')
      return name
    

    # Illustration
    def image(name):
      # Source file
      src = os.path.realpath(source['illustration']+name+'.png')
      # Illustration
      img = dest['assets']+clean(os.path.basename(src)).replace(' ', '_')

      if os.path.exists(src):
        shutil.copy(src, img)
      else:
        print('Error: image name "'+ name +'.png" not exist')
      return 'require("../'+img+'")'
    

    # Sentence
    def sentence(data):
      return data.replace("\xe2\x80\x99", "\'").replace("\xe2\x94\x80", "-")


    # Create a base object
    for i in range(1, 10):
      items['unit'+str(i)] = base

    # Parse the line
    for line in lines:
      item = line.split("\t")

      # remove non-numeric string
      key = re.sub(r'[^0-9-]+', '', item[1])
      key = re.sub(r'-[0-9]', '', key)

      # Empty array of set from unit
      group = items['unit'+str(item[0])]['set'+str(key)]
      # Set
      group['key'] = int(key)

      # Sentences
      sentences = {
        'audio': audio(item[4]),
        'sentence': sentence(item[2])
      }

      # Check if key sentence then add it to the group else to sentences
      if name == 'key-sentence':
        group['image'] = image(item[3])
      else:
        sentences['image'] = image(item[3])
      
      # Add it to the group or set
      group['sentences'].append(sentences)

    # Write data
    with open('../app/data/'+name+'.js', 'w') as file:
      file.write('export default '+ str(items).replace("'require", "require").replace(")'", ")"))


if len(sys.argv) > 1:
  data = [
    'words',
    'sentences',
    'key-sentences'
  ]
  if sys.argv[1] in data:
    generate(sys.argv[1])
  else:
    print('Invalid argument')
else:
  print('No arguments provided')