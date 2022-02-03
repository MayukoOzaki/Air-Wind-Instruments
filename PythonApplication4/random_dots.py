import numpy as np
import matplotlib.pyplot as plt
import cv2


def make_pattern(shape=(16, 16)):
    return np.random.uniform(0, 1, shape)


pattern = make_pattern((1280, 960))

ret, thresh1 = cv2.threshold(pattern, 0.01, 1, cv2.THRESH_BINARY)

plt.imshow(thresh1, cmap='gray')

#cv2.imwrite(r"C: \Users\mayuk\Documents\random\randomdot002.png",thresh1)
plt.imsave("randomdot005.png", thresh1, cmap='gray', dpi=350)

plt.show()

