def josephus_scrambling_parameters(jkey, M, N):
    MP = (int(jkey[:8], 2)%M) + 1
    NP = (int(jkey[8:16], 2)%N) + 1
    MStep = int(jkey[16:20], 2) + 1
    NStep = int(jkey[20:], 2) + 1
    return (MP, NP, MStep, NStep)

def JS_generate_column_sequence(M,N, NP, NStep):
    tmp = NP - 1
    ns = NStep
    col_lst = []
    for _ in range(M):
        i = tmp
        b = list(range(N))
        ci = []
        for k in range(1, N+1):
            ci.append(b[i])
            b.pop(i)
            if len(b) == 0:
                NStep += 1
                break
            i = ((i-1) + NStep) % (N-k)
            NStep += 1
        tmp = ci[k-1] - 1
        col_lst.append(ci)
    return col_lst

def JS_generate_row_sequence(M, MP, MStep):
    a = list(range(M))
    i = MP - 1
    ri = []
    for k in range(1, M+1):
        ri.append(a[i])
        a.pop(i)
        if len(a) == 0: 
            break
        i = ((i -1) + MStep) % (M-k)
        MStep += 1
    return ri

def generate_index_matrix(ri, col_lst, M, N):
    mapping = []
    for i in range(M):
        ci = col_lst[i]
        lst = []
        for j in range(N):
            r = ci[j]
            l = (ri[r%M] + i) % M
            lst.append((l,r))
        mapping.append(lst)
    return mapping
    
def generate_mapping(M, N, MP, NP, MStep, NStep):
    ri = JS_generate_row_sequence(M, MP, MStep)
    col_lst = JS_generate_column_sequence(M, N, NP, NStep)
    result = generate_index_matrix(ri, col_lst, M, N)
    return result

    