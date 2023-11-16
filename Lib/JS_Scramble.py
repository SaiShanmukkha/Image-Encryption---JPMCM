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

# if __name__ == "__main__":
#     mapping = [[(3, 1), (0, 3), (2, 0), (1, 2)], [(0, 1), (3, 0), (2, 2), (1, 3)], [(3, 2), (2, 3), (0, 0), (1, 1)], [(1, 0), (0, 2), (3, 3), (2, 1)]]
#     image = [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16]]
    
#     result = scramble_image(mapping, image)
#     # print(result)
#     rs = descramble_image(mapping, result)
#     # print(rs)
    