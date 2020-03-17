from math import sqrt
import random
import os


class Node:
    def __init__(self, grid, g=0, h=0, p_node=None):
        self.grid = grid
        self.g = g
        self.h = h
        self.p_node = p_node


# 针对N数码问题
class AStar:
    def __init__(self, start, end):
        self.N = int(sqrt(len(start)))
        self.open_list = []
        self.close_list = []
        self.step = 0
        self.start = start
        self.end = end
        self.path_list = []
        # 统计b
        self.b_list = []

    # 计算一个数列的逆序数
    @staticmethod
    def get_inversion_number(num_list):
        res = 0
        length = len(num_list)
        for i in range(length):
            for k in range(i+1, length):
                if num_list[i] > num_list[k]:
                    res += 1
        return res

    # 输出最终结果
    def print_grid(self):
        if self.path_list:
            N = self.N
            for node in self.path_list[::-1]:
                grid = node.grid
                os.system("cls")
                print("\b", end='')
                b = N * 5 + 1
                print("-" * b)
                for i in range(N):
                    row_i = []
                    for j in range(N):
                        row_i.append(grid[i * N + j])
                    print("|{}|".format("|".join([str(num or " ").center(4) for num in row_i])))
                    print("-" * b)
        else:
            print("Unsolvable !")

    # 得到可能的新的盘面
    def get_new_grid(self, current_grid):
        N = self.N
        next_grid = []
        possible_move = []
        zero = current_grid.index(0)
        zero_x = zero // N
        zero_y = zero % N
        if zero_y > 0:
            possible_move.append('a')
            new_grid = current_grid.copy()
            new_grid[zero] = new_grid[zero-1]
            new_grid[zero-1] = 0
            next_grid.append(new_grid)
        if zero_y < N - 1:
            possible_move.append('d')
            new_grid = current_grid.copy()
            new_grid[zero] = new_grid[zero+1]
            new_grid[zero+1] = 0
            next_grid.append(new_grid)
        if zero_x > 0:
            possible_move.append('w')
            new_grid = current_grid.copy()
            new_grid[zero] = new_grid[zero-N]
            new_grid[zero-N] = 0
            next_grid.append(new_grid)
        if zero_x < N - 1:
            possible_move.append('s')
            new_grid = current_grid.copy()
            new_grid[zero] = new_grid[zero+N]
            new_grid[zero+N] = 0
            next_grid.append(new_grid)
        return next_grid

    # 使用逆序数判断有解性
    def is_solvable(self):
        N = self.N
        start_list = self.start.copy()
        end_list = self.end.copy()
        start_list.remove(0)
        end_list.remove(0)
        x = self.get_inversion_number(start_list) % 2
        y = self.get_inversion_number(end_list) % 2
        if N % 2 == 1:
            if x != y:
                return False
            else:
                return True
        else:
            space_x1 = self.start.index(0) // N
            space_x2 = self.end.index(0) // N
            z = abs(space_x1 - space_x2) % 2
            if (x == y and z == 0) or (x != y and z == 1):
                return True
            else:
                return False

    # 计算曼哈顿距离
    def get_manhattan_distance(self, current_grid):
        d = 0
        N = self.N
        for i in range(1, N * N):
            p1, p2 = current_grid.index(i), self.end.index(i)
            x1 = p1 // N
            y1 = p1 % N
            x2 = p2 // N
            y2 = p2 % N
            d += abs(x1 - x2) + abs(y1 - y2)
        return d

    # 节点是否在open表
    def is_in_open(self, node):
        for n in self.open_list:
            if node.grid == n.grid:
                return n
        return None

    # 节点是否在close表
    def is_in_close(self, node):
        for n in self.close_list:
            if node.grid == n.grid:
                return True
        return False

    # 从open表找估值f最小的节点
    def find_min_node(self):
        min_node = self.open_list[0]
        for node in self.open_list:
            if node.g + node.h < min_node.g + min_node.h:
                min_node = node
        return min_node

    # open表里是否有目标节点
    def end_in_open(self):
        for n in self.open_list:
            if n.grid == self.end:
                return n
        return None

    # 主搜索逻辑，f = g + h
    def search(self):
        if not self.is_solvable():
            return False
        start_node = Node(self.start, 0, self.get_manhattan_distance(self.start))
        self.open_list.append(start_node)
        while self.open_list:
            # 如果open表里有目标节点，搜索成功
            end_node = self.end_in_open()
            if end_node:
                # 记录结果路径
                temp_node = end_node
                self.path_list.append(temp_node)
                while temp_node.p_node:
                    temp_node = temp_node.p_node
                    self.path_list.append(temp_node)
                return True
            # 取f值最小的节点
            current_node = self.find_min_node()
            self.open_list.remove(current_node)
            self.close_list.append(current_node)
            self.step = current_node.g
            next_grid = self.get_new_grid(current_node.grid)
            # 统计b
            branch_factor = len(next_grid)
            # 扩展当前节点的子节点
            for grid in next_grid:
                child_node = Node(grid, current_node.g+1, self.get_manhattan_distance(grid), current_node)
                # 该子节点在close表
                if self.is_in_close(child_node):
                    continue
                else:
                    node = self.is_in_open(child_node)
                    # 该子节点在open表
                    if node:
                        if child_node.g < node.g:
                            node.g = child_node.g
                            node.p_node = child_node.p_node
                    # 该子节点是全新的
                    else:
                        self.open_list.append(child_node)
                        # 统计b
                        self.b_list.append(branch_factor)
        return False


if __name__ == '__main__':
    n = int(input("Please input the count of game:"))
    temp = 0
    branch_list = []
    depth_list = []
    existed_start = []
    while temp < n:
        state1 = [1, 2, 3, 4, 5, 6, 8, 7, 0]
        state2 = state1.copy()
        random.shuffle(state1)
        while state1 in existed_start:
            random.shuffle(state1)
        if state1 == state2:
            continue
        a_star = AStar(state1, state2)
        if not a_star.is_solvable():
            continue
        a_star.search()
        existed_start.append(state1)
        # print("search complete")
        branch_list.append(round(sum(a_star.b_list)/len(a_star.b_list), 2))
        depth_list.append(a_star.step)
        temp += 1
        # a_star.print_grid()
    B = sum(branch_list) / len(branch_list)
    print(B)
    D = sum(depth_list) / len(depth_list)
    print(D)
    print(sqrt(B)/D)
