
# shamelessly stole from http://stackoverflow.com/questions/4080254
def du(d):
    file_walker = (
        os.path.join(root, f)
        for root, _, files in os.walk(d)
        for f in files )
    return sum(os.path.getsize(f) for f in file_walker)
