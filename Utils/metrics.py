from keras.optimizers import *


def dice_coeff(y_true,y_pred):
    axis = tuple(range(1, len(y_true.shape)))
    intersection = K.sum(y_true * y_pred, axis=axis)
    dice = (2. * intersection + K.epsilon()) / (
        K.sum(y_true * y_true, axis=axis) + K.sum(y_pred * y_pred, axis=axis) + K.epsilon())
    return K.mean(dice)


def dice_loss(y_true, y_pred):
    return 0.6*(1-dice_coeff(y_true[:,:,:,1], y_pred[:,:,:,1]))+0.4*(1-dice_coeff(y_true[:,:,:, 0], y_pred[:,:,:, 0]))


def smooth_loss(y_true, y_pred):
    H = y_pred.shape[-3]
    W = y_pred.shape[-2]

    loss = K.abs(y_pred[:,1:H-1,1:W-1,:] - y_pred[:,0:H-2,1:W-1,:]) + \
           K.abs(y_pred[:,1:H-1,1:W-1,:] - y_pred[:,2:H,1:W-1,:]) + \
           K.abs(y_pred[:, 1:H - 1, 1:W - 1, :] - y_pred[:, 1:H - 1, 0:W - 2, :]) + \
           K.abs(y_pred[:, 1:H - 1, 1:W - 1, :] - y_pred[:, 1:H - 1, 2:W, :])

    M1 = K.cast(K.equal(y_true[:,1:H-1,1:W-1,:], y_true[:,0:H-2,1:W-1,:]),'float32')
    M2 = K.cast(K.equal(y_true[:,1:H-1,1:W-1,:], y_true[:,2:H,1:W-1,:]),'float32')
    M3 = K.cast(K.equal(y_true[:,1:H-1,1:W-1,:], y_true[:,1:H-1,0:W-2,:]),'float32')
    M4 = K.cast(K.equal(y_true[:,1:H-1,1:W-1,:], y_true[:,1:H-1,2:W,:]),'float32')

    mask = M1*M2*M3*M4

    return K.mean(loss*mask)


def Dice_Smooth_loss(y_true, y_pred):
    return smooth_loss(y_true, y_pred) + dice_loss(y_true, y_pred)

