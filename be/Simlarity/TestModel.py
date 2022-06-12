import time
from Simlarity import toolsFunction
from Simlarity import dataProcessTools

def compute_proxEmbedbatch2(
        wordsEmbeddings=None,  # words embeddings
        wordsEmbeddings_path=None,  # the file path of words embeddings
        word_dimension=0,  # dimension of words embeddings
        dimension=0,  # the dimension of paths embeddings
        wordsSize=0,  # the size of words vocabulary
        subpaths_map=None,  # contains sub-paths
        subpaths_file=None,  # the file which contains sub-paths
        maxlen_subpaths=1000,  # the max length for sub-paths
        maxlen=100,  # Sequence longer then this get ignored
        main_dir="",
        test_data_file='',  # the file path of test data
        top_num=10,  # the top num to predict
        ideal_data_file='',  # ground truth
        alpha=0,
        func=None,  # model function
        batch_size = 4,
        # 应该是输入query，返回一个list
        query = "",
        candidates = [],
):

    if wordsEmbeddings is None:
        if wordsEmbeddings_path is not None:
            wordsEmbeddings, dimension, wordsSize = dataProcessTools.getWordsEmbeddings(wordsEmbeddings_path)
        else:
            print ('There is not path for wordsEmbeddings, exit!!!')
            exit(0)

    if subpaths_map is None:
        if subpaths_file is not None:
            subpaths_map = dataProcessTools.loadAllSubPaths(subpaths_file, maxlen_subpaths)
        else:
            print ('There is not path for sub-paths, exit!!!')
            exit(0)

    query = int(query)
    map = {}
    for i in range(0, len(candidates)):
        key1 = str(query) + '-' + str(candidates[i])
        key2 = str(candidates[i]) + '-' + str(query)
        if key1 in subpaths_map or key2 in subpaths_map:
            candidates.append(int(candidates[i]))
        else:
            map[int(candidates[i])]= -1000.
    canindex = 0
    nextlen = min(len(candidates) - canindex,batch_size)
    sub_candidates = candidates[canindex : canindex + nextlen]
    while(canindex < len(candidates) ):
        subPaths_matrix,subPaths_mask,subPaths_lens,path_discount,groups_tensor = dataProcessTools.prepareDataForTestBatch(
            query, sub_candidates, subpaths_map,alpha)
        if len(subPaths_matrix) > 0 :
            scores =func(subPaths_matrix, subPaths_mask, subPaths_lens, groups_tensor, path_discount, wordsEmbeddings)
            for index in range(len(sub_candidates)):
                map[sub_candidates[index]] = scores[index]
        else:
            for index in range(len(sub_candidates)):
                map[sub_candidates[index]] = -1000.
        canindex += nextlen
        nextlen = min(len(candidates) - canindex, batch_size)
        sub_candidates = candidates[canindex: canindex + nextlen]


    tops_in_line, top2 = toolsFunction.mapSortByValueDESC2(map,
                                                           top_num)  # 返回一个节点的列表，节点按相似度分数大小排序，排前top个点，若长度<top，有多少排多少
    return tops_in_line

