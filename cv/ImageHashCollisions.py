from enum import Enum
import pickle
import os
import os.path
import time

from PIL import Image
import imagehash

ihashtable = {}
train_hashes = []


class HashFunction(Enum):
    pHash = imagehash.phash
    aHash = imagehash.average_hash
    dHash = imagehash.dhash
    wHash = imagehash.whash
    clrHash = imagehash.colorhash
    crpHash = imagehash.crop_resistant_hash


def calculate_hashes(img, **hash_function_set):
    pass


def calculate_hashes(img, hash_funcs=[imagehash.phash, imagehash.average_hash, imagehash.dhash,
                                      imagehash.whash]):
    hashes = []
    for hash_func in hash_funcs:
        hashes.append(hash_func(Image.open(img)))
    return hashes


def initialize_train_hashes(path, hashes_pickle='image_hashes.pickle'):
    myList = os.listdir(path)
    print('Total Images Detected', len(myList))
    global train_hashes
    train_phash = {}
    train_ahash = {}
    train_dhash = {}
    train_whash = {}
    # train_crhash = {}

    if os.path.isfile(hashes_pickle):
        with open(hashes_pickle, 'rb') as handle:
            train_hashes = pickle.load(handle)
    else:
        for img in myList:
            imagename = os.path.splitext(img)[0]
            hashes = calculate_hashes(f'{path}/{img}')
            train_phash[imagename] = hashes[0]
            train_ahash[imagename] = hashes[1]
            train_dhash[imagename] = hashes[2]
            train_whash[imagename] = hashes[3]
            # train_crhash[imagename] = imagehash.crop_resistant_hash(Image.open(f'{path}/{img}'))
        train_hashes.extend([train_phash, train_ahash, train_dhash, train_whash])
        with open(hashes_pickle, 'wb') as handle1:
            pickle.dump(train_hashes, handle1, protocol=pickle.HIGHEST_PROTOCOL)


def calculate_distances(img_hash, trh_dict):
    print(img_hash)

    dist = {}
    trd = dict(trh_dict)
    print(trd.keys())
    for iname in trd.keys():
        dist[iname] = img_hash - trd[iname]
    return dist


def match_image(img):
    if(len(train_hashes) > 0):
        img_hashes = calculate_hashes(img)
        distances = []
        for idx, trh in enumerate(train_hashes):
            dist = calculate_distances(img_hashes[idx], trh)
            distances.append(dist)
        return distances
    else:
        raise ("Training Set not initialized!")


def initialize_ihash_table(path, filename_pickle='filename.pickle'):
    global ihashtable
    global crhashes
    if os.path.isfile(filename_pickle):
        with open(filename_pickle, 'rb') as handle:
            ihashtable = pickle.load(handle)
    else:
        myList = os.listdir(path)
        print('Total Images Detected', len(myList))
        for img in myList:
            imagename = os.path.splitext(img)[0]
            hashes = calculate_hashes(f'{path}/{img}')
            phashes = hashes[0]
            phashstr = "p#"+str(phashes)
            ahashes = hashes[1]
            ahashstr = "a#"+str(ahashes)
            dhashes = hashes[2]
            dhashstr = "d#"+str(dhashes)
            whashes = hashes[3]
            whashstr = "w#"+str(whashes)

            if str(phashstr) not in ihashtable:
                ihashtable[phashstr] = list()
            ihashtable[phashstr].append((imagename, phashes))

            if str(ahashstr) not in ihashtable:
                ihashtable[ahashstr] = list()
            ihashtable[ahashstr].append((imagename, ahashes))

            if str(dhashstr) not in ihashtable:
                ihashtable[dhashstr] = list()
            ihashtable[dhashstr].append((imagename, dhashes))

            if str(whashstr) not in ihashtable:
                ihashtable[whashstr] = list()
            ihashtable[whashstr].append((imagename, whashes))

        with open(filename_pickle, 'wb') as handle:
            pickle.dump(ihashtable, handle, protocol=pickle.HIGHEST_PROTOCOL)


initialize_ihash_table('ImgTrain/Sample')
print(len(ihashtable))

print("--- print duplicates ---")
for k in ihashtable.keys():
    # print(ihashtable[k])
    # print(len(ihashtable[k]))
    collisions = len(ihashtable[k])
    if collisions > 1:
        print(k, f"({collisions})")
        for t in ihashtable[k]:
            print("--", t[0])

imgquery = Image.open('ImgTrain/wmgc.jpg')
imgtest = Image.open('ImgTrain/Orig1.jpg')
# h1 = imagehash.crop_resistant_hash(imgquery)
# h2 = imagehash.crop_resistant_hash(imgtest)
#
# wh1 = imagehash.whash(imgquery)
# wh2 = imagehash.whash(imgtest)
#
# dh1 = imagehash.dhash(imgquery)
# dh2 = imagehash.dhash(imgtest)
#
# ph1 = imagehash.whash(imgquery)
# ph2 = imagehash.whash(imgtest)
#
# print(ph1)
# print(ph2)
# print(ph1 - ph2)
#
# print(dh1)
# print(dh2)
# print(dh1 - dh2)
#
# print(wh1)
# print(wh2)
# print(wh1 - wh2)
#
# print(h1)
# print(h2)
# print(h1.hash_diff(h2))

initialize_train_hashes('ImgTrain/Master')
# print(len(train_hashes))

distances = match_image('ImgTrain/wmgc.jpg')
print(len(distances))

match1 = min(distances[0], key=distances[0].get)
match2 = min(distances[1], key=distances[1].get)
match3 = min(distances[2], key=distances[2].get)
match4 = min(distances[3], key=distances[3].get)

print(match1, match2, match3, match4)
print(distances[0][match1], distances[1][match2], distances[2][match3], distances[3][match4])

matches = set((match1, match2, match3, match4))

for m in matches:
    h1 = imagehash.crop_resistant_hash(Image.open('ImgTrain/Sample/'+m+'.jpg'))
    h2 = imagehash.crop_resistant_hash(Image.open(GC_SAMPLE4))
    print(m, h1.hash_diff(h2))



# for qh in queryhashes:
#     qhstrp = "p#" + str(qh[0])
#     qhstra = "a#" + str(qh[1])
#     qhstrd = "d#" + str(qh[2])
#     qhstrw = "w#" + str(qh[4])
#     if (qhstrp in ihashtable) or (qhstra in ihashtable) or (qhstrd in ihashtable) or (qhstrw in ihashtable):
#         matches = len(ihashtable[qhstrp])
#         if matches > 1:
#             for m in matches:
#                 print(m[0])
#     else:
#         plist = []
#         alist = []
#         dlist = []
#         wlist = []
#         for hk in ihashtable.keys():
#             htype = str(hk)[0]
#             for hashvalues in ihashtable[hk]:
#                 for hval in hashvalues:
#                     if htype == 'p':
#                         plist.append(hval[0], qh[]
#
#                         hashval =

