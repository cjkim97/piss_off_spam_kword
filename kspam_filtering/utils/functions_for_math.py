'''
* 통계값 계산 함수 코드

'''

import itertools


def cartesian_product(n, foreign=False):
    '''
    [일반화된 카테션 곱]
    각 n개 리스트의 원소의 개수가 k1, k2, ... , kn개 일때 데카르트 곱을 구하는 코드
    '''
    
    case_list = []

    perm_list = []

    result_perm_list = []

    if foreign:
        d_possible = [i for i in range(n//4,-1,-1)]
        for d_pos in d_possible:
            n2 = n-4*d_pos
            c_possible = [i for i in range(n2//3,-1,-1)]
            for c_pos in c_possible:
                n3 = n2 - 3*c_pos
                b_possible = [i for i in range(n2//2,-1,-1)]
                for b_pos in b_possible:
                    n4 = n3 - 2*b_pos
                    a = n4
                    if (a>=0) and((a + 2*b_pos + 3*c_pos + 4*d_pos) == n):
                        case_list.append((a,b_pos,c_pos,d_pos))

        for case in case_list:
            tmp_perm = []
            start = 1
            for count in case:
                use_group = [start for i in range(count)]
                tmp_perm.extend(use_group)
                start+=1
            perm_list.append(tmp_perm)

    else:
        c_possible = [i for i in range(n//4,-1,-1)]
        for c_pos in c_possible:
            n2 = n-4*c_pos
            b_possible = [i for i in range(n2//3,-1,-1)]
            for b_pos in b_possible:
                n3 = n2 - 3*b_pos
                a = n3//2
                if (2*a + 3*b_pos + 4*c_pos) == n:
                    case_list.append((a,b_pos,c_pos))
        for case in case_list:
            tmp_perm = []

            start = 2
            for count in case:
                use_group = [start for i in range(count)]
                tmp_perm.extend(use_group)
                start+=1
            perm_list.append(tmp_perm)

    for perm in perm_list:
        nPr = list(itertools.permutations(perm, len(perm)))
        result_perm_list.extend(nPr)

    return set(result_perm_list)