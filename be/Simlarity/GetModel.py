import numpy
import theano
from theano import tensor
from collections import OrderedDict
from Simlarity import proxEmbedProcessModelBatch


def load_params(path, params):
    """
    load model params from file
    """
    pp = numpy.load(path)
    for kk, vv in params.items():
        if kk not in pp:
            raise Warning('%s is not in the archive' % kk)
        params[kk] = pp[kk]

    return params
def get_batch_proxEmbedModel(

        model_params_path='',  # the path of model parameters
        word_dimension=0,  # the dimension of words embedding
        dimension=0,  # the dimension of path embedding
        h_output_method='h',  # the output way of lstm
        discount_alpha=0.1,  # discount alpha
        subpaths_pooling_method='max-pooling',  # the combine way of sub-paths
):
    """
    get model from file
    """
    model_options = locals().copy()

    tparams = OrderedDict()
    tparams['lstm_W'] = None
    tparams['lstm_U'] = None
    tparams['lstm_b'] = None
    tparams['w'] = None
    # tparams['b'] = None
    tparams = load_params(model_params_path, tparams)

    subPaths_matrix, subPaths_mask, subPaths_lens, groups_tensor, path_discount, wordsEmbeddings, values = proxEmbedProcessModelBatch.proxEmbedModel(model_options,
                                                                                                      tparams)
    func = theano.function(
        [subPaths_matrix, subPaths_mask, subPaths_lens, groups_tensor, path_discount, wordsEmbeddings], values,
        on_unused_input='ignore')
    return func