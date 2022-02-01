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
                mem_tmp.setdefault(c, [[0, 0], []])
                mem_tmp[c][1].append(i)
            if r == 1:
                mem_tmp.setdefault(c, [[0, 0], []])
                mem_tmp[c][0][0] += 1
                mem_tmp[c][1].append(i)
            if r == 2:
                mem_tmp.setdefault(c, [[0, 0], []])
                mem_tmp[c][1].append(i)
                if self.ans[i] is None:
                    mem_tmp[c][0][1] += 1
                self.ans[i] = c
            
        for c, v in mem_tmp.items():
            mem_pre = 0
            if c in self.mem.keys():
                mem_pre += self.mem[c][0]
            ans_pre = 0
            if c in self.ans:
                ans_pre += sum([1 if ci == c else 0 for ci in self.ans])
            ans_pre -= v[0][1]
            mem_pre -= v[0][1]
            mem_post = v[0][0] - ans_pre
            
            n_mem = max(mem_pre, mem_post)
            
            if n_mem <= 0:
                if c in self.mem.keys():
                    self.mem.pop(c)
            else:
                if c in self.mem.keys():
                    self.mem[c][0] = n_mem
                else:
                    self.mem[c] = [n_mem, [0, 1, 2, 3, 4]]
                for i in v[1]:
                    if i in self.mem[c][1]:
                        self.mem[c][1].remove(i)
        
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
            
        ans_tmp = []
        for c in self.ans:
            if c is not None:
                ans_tmp.append(c)
        
        if len(self.mem) == 0 and len(ans_tmp) >= 2 and len(cand) > 1:
            d = set()
            for s in cand.keys():
                for c in s:
                    d.add(c)
            for c in set(self.ans):
                if c is not None:
                    d.remove(c)
            
            cand = {}
            for w in wd:
                a_flg = True
                p = 0
                for c in d:
                    if c in w:
                        p += 1
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