
import subprocess,sys
for s in ["historical_artist_crawler.py","similarity_engine.py"]:
    subprocess.run([sys.executable,s],check=True)
print("HISTORICAL ARTIST PIPELINE COMPLETE")
