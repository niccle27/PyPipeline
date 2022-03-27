import pickle

def load_pickle(path):
    m_dict = None
    try:
        with open(path, "rb") as reader:
            m_dict = pickle.load(reader)
    except FileNotFoundError:
        pass
    return m_dict

def write_pickle(mdict, path):
    with open(path, 'wb') as w:
        pickle.dump(mdict, w, protocol=pickle.HIGHEST_PROTOCOL)

