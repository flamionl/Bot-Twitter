import numpy as np

from keras.applications import densenet, inception_v3, mobilenet, resnet50, vgg16, xception
from keras.preprocessing.image import img_to_array, load_img
from keras.models import Model



def load_network(name='ResNet50'):
    """Load a pretrained deep network.
    
    Parameters
    -----------
    name: name of network to use (str, opt)
    
    Returns
    -------
    network: pretrained network (dict)
    
    Notes
    -----
    Loading a network can take a few tens of seconds.  The first
    time a network is loaded, its weights are downloaded (> 100Mo).
    
    network must used with transform_image and contains:
     - target_size: image size that can processed (tuple of int)
     - preprocess_input: image preprocessing for network (function)
     - last_layer_embedding: compute last layer output (function)
    
    Each network corresponds to a different transformation size:
     - DenseNet    = 1920 (https://arxiv.org/pdf/1608.06993.pdf)
     - InceptionV3 = 2048 (https://arxiv.org/pdf/1512.00567.pdf)
     - MobileNet   = 1000 (https://arxiv.org/pdf/1704.04861.pdf)
     - ResNet50    = 2048 (https://arxiv.org/pdf/1512.03385.pdf)
     - VGG16       = 4096 (https://arxiv.org/pdf/1409.1556.pdf)
     - Xception    = 2048 (https://arxiv.org/pdf/1610.02357.pdf)

    """
    
    # load network pretrained on ImageNet
    if name == 'DenseNet':
        model = densenet.DenseNet201(weights='imagenet')
        target_size = (224, 224)
        preprocess_input = densenet.preprocess_input
    elif name == 'InceptionV3':
        model = inception_v3.InceptionV3(weights='imagenet')
        target_size = (299, 299)
        preprocess_input = inception_v3.preprocess_input
    elif name == 'MobileNet':
        model = mobilenet.MobileNet(weights='imagenet')
        target_size = (224, 224)
        preprocess_input = mobilenet.preprocess_input
    elif name == 'ResNet50':
        model = resnet50.ResNet50(weights='imagenet')
        target_size = (224, 224)
        preprocess_input = resnet50.preprocess_input
    elif name == 'VGG16':
        model = vgg16.VGG16(weights='imagenet')
        target_size = (224, 224)
        preprocess_input = vgg16.preprocess_input
    elif name == 'Xception':
        model = xception.Xception(weights='imagenet')
        target_size = (299, 299)
        preprocess_input = xception.preprocess_input
    
    # embed image with last layer of the model
    return {'target_size':target_size,
            'preprocess_input':preprocess_input,
            'last_layer_embedding':Model(inputs=model.input, outputs=model.layers[-2].output).predict}
    
    

def transform_image(path, network):
    """Transforms an image using a pretrained deep network.
    
    Parameters
    -----------
    path: image location (str)
    network: pretrained network (dict)
    
    Returns
    -------
    representation: numerical representation of the image (list)
    
    Notes
    -----
    Transforming an image can take a few seconds.
    
    See load_network for more details on pretrained networks.

    """
    
    # load and reshape image
    img = img_to_array(load_img(path, target_size=network['target_size']))
    
    # expand and preprocess imag)
    img = network['preprocess_input'](np.expand_dims(img, axis=0))
                                  
    # embed image with last layer of the model
    return list(network['last_layer_embedding'](img)[0])
