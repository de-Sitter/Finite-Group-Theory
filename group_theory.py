from itertools import product, permutations

def is_group(table, n):
    # 对一个乘法表是否满足群的四条定义做出判断
    # 在群的乘法表中,封闭性自然满足

    identity=False
    if all(table[0][i] == i and table[i][0] == i for i in range(n)):
        identity=True
    if not identity:
        return False
    # 检查单位元是否在第一行和第一列

    for a in range(n):
        has_inv = False
        for b in range(n):
            if table[a][b] == 0 and table[b][a] == 0:
                has_inv = True
                break
        if not has_inv:
            return False
    # 检查每个群元素是否都有逆元

    for a in range(n):
        for b in range(n):
            for c in range(n):
                if table[table[a][b]][c] != table[a][table[b][c]]:
                    return False
    # 检查结合律是否满足(这是最复杂的一步)
    return True

def all_tables(n):
    # 生成一个n阶的乘法表
    for rows in product(permutations(range(n)), repeat=n):
        table = [list(row) for row in rows]
        yield table

def print_table(table):
    for row in table:
        print(' '.join(map(str, row)))
    print()

def standardize_table(table):
    """
    这是很重要但容易遗漏的一步,如果对一个群除了单位元以外的群元素进行置换操作后,
    得到的乘法表与之前得到的乘法表是相同的,那么它们只能算一种结构,因为群的结构与
    我们对于群元素的标记方式无关(但是注意单位元的特殊性导致它不能参与置换),如果
    遗漏这种置换等价性的判断将会导致重复计数.
    """
    n = len(table)
    min_table = None
    for perm in permutations(range(1, n)):
        mapping = [0] + list(perm)
        new_table = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                new_table[i][j] = mapping.index(table[mapping[i]][mapping[j]])
        flat = sum(new_table, [])
        if (min_table is None) or (flat < min_table):
            min_table = flat
    return tuple(min_table)

def main():
    n = int(input())
    seen = set()
    count = 0
    test=0
    for table in all_tables(n):
        test+=1
        print(f"We have tried {test} times")
        if is_group(table, n):
            std = standardize_table(table)
            if std in seen:
                continue
            seen.add(std)
            print(f"Group #{count+1}:")
            print_table(table)
            count += 1
    if count == 0:
        print("No group of this order.")
    else:
        print(f"Total groups: {count}")
    print("All unique group tables:")
    def tuple_to_table(t, n):
        return [list(t[i*n:(i+1)*n]) for i in range(n)]
    for std in seen:
        table = tuple_to_table(std, n)
        print_table(table)

if __name__ == "__main__":
    main()
