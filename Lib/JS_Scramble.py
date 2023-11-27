def scramble_image(mapping, image):
    M = len(image)
    N = len(image[0])
    mapped_image = [[0 for _ in range(N)] for _ in range(M)]
    for i in range(M):
        for j in range(N):
            x, y = mapping[i][j]
            mapped_image[i][j] = image[x][y]
    return mapped_image

def descramble_image(mapping, image):
    M = len(image)
    N = len(image[0])
    mapped_image = [[0 for _ in range(N)] for _ in range(M)]
    for i in range(M):
        for j in range(N):
            x, y = mapping[i][j]
            mapped_image[x][y] = image[i][j]
    return mapped_image


    