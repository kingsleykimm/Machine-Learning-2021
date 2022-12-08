import sys; args = sys.argv[1:]
from PIL import Image; img = Image.open(args[0])
import random

def distance(tup1, tup2):
    return sum([(tup2[k]-tup1[k]) ** 2 for k in range(3)]) ** 0.5
def choose_random_means(k, img, pix):
    means = []
    x = (int)(random.uniform(0, img.size[0]-1))
    y = (int)(random.uniform(0, img.size[1]-1))
    init = pix[x, y]
    pix_copy = []
    prob_distribution = []
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pix_copy.append(pix[i, j])
    for val in range(k):
        prob_distribution = []
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                if pix[i, j] in means:
                    prob_distribution.append(0)
                else:
                    prob_distribution.append(distance(pix[i, j], init))
                # if dist > max_dist:
                #     max_dist = dist
                #     init = pix[i, j]
        init = random.choices(pix_copy, cum_weights=prob_distribution)[0]
        means.append(init)
    # for i in range(k):
    #     x = (int)(random.uniform(0, img.size[0]-1))
    #     y = (int)(random.uniform(0, img.size[1]-1))
    #     means.append(pix[x,y])
    return means

# goal test: no hopping
def check_move_count(mc):
    for x in mc:
        if x != 0: return False
    return True

# calculate distance with the current color with each mean
# return the index of means
def dist(col, means):
    minIndex, dist_sum = 0, 255**2+255**2+255**2
    for i in range(len(means)):
        dist_k = ((means[i][0]-col[0]) ** 2 + (means[i][1]-col[1])**2 + (means[i][2]-col[2])**2) ** 0.5
        if dist_k < dist_sum:
            minIndex = i
            dist_sum = dist_k
    return minIndex 


def check_distance(means, tup1, i):
    min_dist = distance(means[i], tup1)
    for j in range(len(means)):
        if j == i:
            continue
        else:
            if min_dist > 1/2 * distance(means[j], tup1):
                return False
    return True
def clustering_mod(img, pix, rgb, cb, mc, means, count, prev_pb): #rgb is a list of the distinct pixels
    temp_pb, temp_mc, temp_m, temp_cb = [[] for x in means], [], [], [0 for x in range(len(means))]
    # prev_pb_copy = [[False for j in range(len(prev_pb[i]))] for i in range(len(prev_pb))]
    # for i in range(len(prev_pb)):
    #     for j in range(len(prev_pb[i])):
    #         if check_distance(means, prev_pb[i][j], i):
    #             prev_pb_copy[i][j] = True

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            check = True
            # for i in range(len(prev_pb)):
            #     if tup in prev_pb[i]:
            #         if check_distance(means, tup, i):
            #             check = False
            #             temp_cb[i] += 1
            #             temp_pb[i].append(tup)
            if check == True:
                index = dist(pix[i, j], means)
                temp_cb[index] += 1 #bucketing here
                temp_pb[index].append(pix[i, j])


    # for i in range(img.size[0]):
    #     for j in range(img.size[1]):
    #         temp_cb[dist(pix[i, j], means)] += 1
    #         temp_pb[dist(pix[i, j], means)].append(pix[i, j])
    temp_mc = []
    for i in range(len(temp_cb)):
        temp_mc.append(abs(temp_cb[i] - cb[i]))

    temp_m = []
    for li in temp_pb: #going through the new buckets
        sum_r, sum_g, sum_b = 0.0, 0.0, 0.0
        for tup in li:
            sum_r += tup[0]
            sum_g += tup[1]
            sum_b += tup[2]
        temp_m.append((sum_r / len(li), sum_g / len(li), sum_b / len(li))) #calculating new means
    
    # print ('diff', count, ':', temp_mc)
    return temp_cb, temp_mc, temp_m, temp_pb

def clustering(img, pix, rgb, cb, mc, means, count, prev_pb): #rgb is a list of the distinct pixels
    temp_pb, temp_mc, temp_m, temp_cb = [[] for x in means], [], [], [0 for x in range(len(means))]
    # prev_pb_copy = [[False for j in range(len(prev_pb[i]))] for i in range(len(prev_pb))]
    # for i in range(len(prev_pb)):
    #     for j in range(len(prev_pb[i])):
    #         if check_distance(means, prev_pb[i][j], i):
    #             prev_pb_copy[i][j] = True

    for tup in rgb.keys():
        check = True
        # for i in range(len(prev_pb)):
        #     if tup in prev_pb[i]:
        #         if check_distance(means, tup, i):
        #             check = False
        #             temp_cb[i] += 1
        #             temp_pb[i].append(tup)
        if check == True:
            index = dist(tup, means)
            temp_cb[index] += 1 #bucketing here
            temp_pb[index].append(tup)


    # for i in range(img.size[0]):
    #     for j in range(img.size[1]):
    #         temp_cb[dist(pix[i, j], means)] += 1
    #         temp_pb[dist(pix[i, j], means)].append(pix[i, j])
    temp_mc = []
    for i in range(len(temp_cb)):
        temp_mc.append(abs(temp_cb[i] - cb[i]))

    temp_m = []
    
    for li in temp_pb: #going through the new buckets
        sum_r, sum_g, sum_b = 0.0, 0.0, 0.0
        running_sum = 0
        for tup in li:
            sum_r += tup[0] * rgb[tup]
            sum_g += tup[1] * rgb[tup]
            sum_b += tup[2] * rgb[tup]
            running_sum += rgb[tup]
        temp_m.append((sum_r / running_sum, sum_g / running_sum, sum_b / running_sum)) #calculating new means
    
    # print ('diff', count, ':', temp_mc)
    return temp_cb, temp_mc, temp_m, temp_pb

def update_picture(img, pix, means):
    region_dict = [0 for x in means]
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            ind = dist(pix[i, j], means)
            pix[i, j] = tuple((map(int, means[ind])))
            region_dict[ind] += 1
    return pix, region_dict
   
def distinct_pix_count(img, pix):
    cols = {}
    max_col, max_count = pix[0, 0], 0
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pix[i, j] not in cols.keys():
                cols[pix[i, j]] = 1
            else:
                cols[pix[i, j]] += 1
    for col in cols.keys():
        if cols[col] > max_count:
            max_col = col
            max_count = cols[col]
    return len(cols.keys()), max_col, max_count, cols
def isValid(pix, dimx, dimy, i, j, color, visited):
    if i < 0 or i >= dimx or j < 0 or j >= dimy or\
        pix[i, j] != color or (i, j) in visited:
        return False
    return True
def floodfill(img, pix, x, y, color, visited):
    queue = []
    queue.append((x, y))

    while queue:
        top = queue.pop(0)
        visited.add(top)
        i = top[0]
        j = top[1]

        if isValid(pix, img.size[0], img.size[1], i-1, j, color, visited):
            queue.append((i-1, j))
            visited.add((i-1, j))
        if isValid(pix, img.size[0], img.size[1], i-1, j-1, color, visited):
            queue.append((i-1, j-1))
            visited.add((i-1, j-1))
        if isValid(pix, img.size[0], img.size[1], i-1, j+1, color, visited):
            queue.append((i-1, j+1))
            visited.add((i-1, j+1))
        if isValid(pix, img.size[0], img.size[1], i+1, j, color, visited):
            queue.append((i+1, j))
            visited.add((i+1, j))
        if isValid(pix, img.size[0], img.size[1], i+1, j+1, color, visited):
            queue.append((i+1, j+1))
            visited.add((i+1, j+1))
        if isValid(pix, img.size[0], img.size[1], i+1, j-1, color, visited):
            queue.append((i+1, j-1))
            visited.add((i+1, j-1))
        if isValid(pix, img.size[0], img.size[1], i, j-1, color, visited):
            queue.append((i, j-1))
            visited.add((i, j-1))
        if isValid(pix, img.size[0], img.size[1], i, j+1, color, visited):
            queue.append((i, j+1))
            visited.add((i, j+1))

        
def count_regions(img, region_dict, pix, means): #
    region_count = [0 for x in means]
    visited = set()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if (i, j) not in visited:
                floodfill(img, pix, i, j, pix[i, j], visited)
                for k in range(len(means)):
                    if tuple(map(int, means[k])) == pix[i, j]:
                        region_count[k] += 1
    return region_count

def last_test(img, pix, means, count_buckets):
    buckets = [[] for x in means]
    new_buckets = [[] for x in means]
    new_means = []
    ret = True
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            buckets[dist(pix[i, j], means)].append(pix[i, j])
    
    for li in buckets:
        sum_r, sum_g, sum_b = 0, 0, 0
        for pixel in li:
            sum_r += pixel[0]
            sum_g += pixel[1]
            sum_b += pixel[2]
        new_means.append((sum_r / len(li), sum_g / len(li), sum_b / len(li)))
    # for i in range(len(new_means)):
    #     print(new_means[i])
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            new_buckets[dist(pix[i, j], new_means)].append(pix[i, j])
    for i in range(len(buckets)):
        # print(len(buckets[i]) - len(new_buckets[i]))
        if len(buckets[i]) - len(new_buckets[i]) != 0:
            ret = False
    return ret
    
        
def main():
    k = int(args[1])
    pix = img.load()   # pix[0, 0] : (r, g, b) 
    rgb = []
    assigned = []
    print ('Size:', img.size[0], 'x', img.size[1])
    print ('Pixels:', img.size[0]*img.size[1])
    d_count, m_col, m_count, rgb = distinct_pix_count(img, pix)
    print ('Distinct pixel count:', d_count)
    print ('Most common pixel:', m_col, '=>', m_count)

    count_buckets = [0 for x in range(k)]
    move_count = [10 for x in range(k)]
    means = choose_random_means(k, img, pix)
    # print ('random means:', means)
    count = 1
    check = False
    while check == False:
        count += 1
        count_buckets, move_count, means, assigned = clustering(img, pix, rgb, count_buckets, move_count, means, count, assigned)
        if check_move_count(move_count) == True:
            check = True
        # if count == 2:
            # print ('first means:', means)
            # print ('starting sizes:', count_buckets)
    # print(last_test(img, pix, means, count_buckets))
    # while check_move_count(move_count) == False:
    #     count_buckets, move_count, means, assigned = clustering_mod(img, pix, rgb, count_buckets, move_count, means, count, assigned)
    
    pix, region_dict = update_picture(img, pix, means)
    # print ('Final sizes:', count_buckets)
    print ('Final means:')
    for i in range(len(means)):
        print (str(i+1) + ':', means[i], '=>', region_dict[i])
    regions = count_regions(img, region_dict, pix, means)  #  num of area fills
    output = ''
    for i in range(len(regions)):
        if i == len(regions)-1:
            output += str(regions[i])
        else:
            output += str(regions[i]) + ', '
    print('Region counts:', output)
    img.save('kmeans/{}.png'.format("2022tkim"), 'PNG')
    # img.save("output.png", 'PNG')

   #img.show()
   
if __name__ == '__main__': 
   main()
#Kingsley Kim 3, 22