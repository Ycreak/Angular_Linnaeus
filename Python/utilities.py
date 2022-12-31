import pickle

def pickle_write(path, file_name, object):
    destination = path + file_name

    with open(destination, 'wb') as f:
        pickle.dump(object, f)

def pickle_read(path, file_name):
    destination = path + '/' + file_name

    with open(destination, 'rb') as f:
        return pickle.load(f)