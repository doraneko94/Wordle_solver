import pickle, sys

class Wordle:
    
    def __init__(self):
        
        self.fin = [False for _ in range(26)]
        self.mem = dict()
        self.ans = [None, None, None, None, None]
        self.points = [5.264, 1.275, 1.665, 2.288, 5.755, 0.817, 1.212, 1.589, 3.173, 0.284, 0.865, 2.922, 1.667, 2.792, 3.538, 1.378, 0.114, 3.357, 4.42 , 2.882, 2.078, 0.724, 0.759, 0.155, 1.274, 0.338]
        
    def update(self, w_str, r_str):
        
        word = [c for c in w_str]
        result = [int(c) for c in r_str]
        mem_tmp = {}
        for i, (c, r) in enumerate(zip(word, result)):
            b = ord(c) - 97
            if r == 0:
                self.fin[b] = True
                if c in mem_tmp.keys():
                    mem_tmp[c][0][0] += 1
                    mem_tmp[c][1].append(i)
                else:
                    mem_tmp[c] = [[1, 0, 0], [i]]
            if r == 1:
                if c in mem_tmp.keys():
                    mem_tmp[c][0][1] += 1
                    mem_tmp[c][1].append(i)
                else:
                    mem_tmp[c] = [[0, 1, 0], [i]]
            if r == 2:
                self.ans[i] = c
                if c in mem_tmp.keys():
                    mem_tmp[c][0][2] += 1
                    mem_tmp[c][1].append(i)
                else:
                    mem_tmp[c] = [[0, 0, 1], [i]]
            
        for c, v in mem_tmp.items():
            if c in self.mem.keys():
                n_mem = max(self.mem[c][0] - v[0][2], v[0][1])
                if n_mem == 0:
                    self.mem.pop(c)
                else:
                    self.mem[c][0] = n_mem
                    for i in v[1]:
                        if i in self.mem[c][1]:
                            self.mem[c][1].remove(i)
            elif v[0][1] > 0:
                self.mem[c] = [v[0][1], [i for i in range(5) if i not in v[1]]]
        
    def print_all(self):
        
        print("fin: ", self.fin)
        print("mem: ", self.mem)
        print("ans: ", self.ans)
        
    def solve(self, wd):
        
        cand = {}
        mem_counts = {}
        for c in self.ans:
            if c is not None:
                mem_counts.setdefault(c, 0)
                mem_counts[c] += 1
        for c, v in self.mem.items():
            mem_counts.setdefault(c, 0)
            mem_counts[c] += v[0]

        for w in wd:
            b_flg = False
            chars = {}
            for i, c in enumerate(w):
                if self.ans[i] is not None:
                    if c != self.ans[i]:
                        b_flg = True
                        break
                else:
                    if c in self.mem.keys():
                        if i not in self.mem[c][1]:
                            b_flg = True
                            break
                    else:
                        if self.fin[ord(c) - 97]:
                            b_flg = True
                            break
                if c in chars.keys():
                    chars[c] += 1
                else:
                    chars[c] = 1
            if b_flg:
                continue
               
            for c, n in chars.items():
                if self.fin[ord(c) - 97] and n > mem_counts[c]:
                        b_flg = True
                        break
            for c, n in mem_counts.items():
                if c not in chars.keys() or n > chars[c]:
                    b_flg = True
                    break
                    
            if b_flg:
                continue
            p = sum([self.points[ord(c) - 97] for c in chars.keys()])
            cand[w] = p
        return sorted(cand.items(), key = lambda w : w[1])[::-1]

with open("wordle_dict.pkl", "rb") as f:
    wd = pickle.load(f)

wdl = Wordle()

for _ in range(6):
    count = 0
    w_cand = wdl.solve(wd)
    print("Enter: ", w_cand[count][0])
    while True:
        r_str = input("Results?: ")
        if len(r_str) == 5:
            break
        elif r_str == "e":
            sys.exit()
        else:
            count += 1
            print("Enter: ", w_cand[count][0])
    wdl.update(w_cand[count][0], r_str)