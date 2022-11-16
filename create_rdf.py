import subprocess
from pathlib import Path

"""
------------------------------------------------------------------------

Uses tarql to create RDF from CSV files

------------------------------------------------------------------------

"""

OKGREEN = '\033[92m'
ENDC = '\033[0m'
BOLD = '\033[1m'

# cur path of file
cur_path = Path(__file__).parent

dest = cur_path / "rdf_dataset"

if not dest.exists():
    dest.mkdir()

C2  = "./tarql/bin/tarql --ntriples ./sparql/videos.sparql ./clean_dataset/videos.csv > ./rdf_dataset/videos.ttl"
C3 = "./tarql/bin/tarql --ntriples ./sparql/video_tags.sparql ./clean_dataset/video_tags.csv > ./rdf_dataset/video_tags.ttl"
C4 = "cat ./rdf_dataset/videos.ttl ./rdf_dataset/video_tags.ttl > ./rdf_dataset/all.ttl"
C5 = "rm ./rdf_dataset/videos.ttl ./rdf_dataset/video_tags.ttl"

print("Creating RDF dataset")

print("Creating videos.ttl")
subprocess.call(C2, shell=True)
print("Creating video_tags.ttl")
subprocess.call(C3, shell=True)
print("Joining videos.ttl and video_tags.ttl into all.ttl and clearing temp files.")
subprocess.call(C4, shell=True)
subprocess.call(C5, shell=True)
print(f"{OKGREEN}{BOLD}\nSuccess!{ENDC}")