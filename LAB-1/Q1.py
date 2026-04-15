
import sys
import os

# Add parent directory to sys.path to import my_deque
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

adj = {
    'Chicago': {'Detroit': 283, 'Cleveland': 354, 'Indianapolis': 182},
    'Detroit': {'Chicago': 283, 'Buffalo': 256, 'Cleveland': 169},
    'Cleveland': {'Chicago': 345, 'Detroit': 169, 'Buffalo': 189, 'Pittsburgh': 134, 'Columbus': 144},
    'Indianapolis': {'Chicago': 182, 'Columbus': 176},
    'Columbus': {'Indianapolis': 176, 'Cleveland': 144, 'Pittsburgh': 185},
    'Buffalo': {'Detroit': 256, 'Cleveland': 189, 'Syracuse': 150, 'Pittsburgh': 215},
    'Pittsburgh': {'Cleveland': 134, 'Columbus': 185, 'Buffalo': 215, 'Philadelphia': 305, 'Baltimore': 247},
    'Syracuse': {'Buffalo': 150, 'Philadelphia': 253, 'New York': 254, 'Boston': 312},
    'Philadelphia': {'Syracuse': 253, 'Pittsburgh': 305, 'New York': 97, 'Baltimore': 101},
    'Baltimore': {'Pittsburgh': 247, 'Philadelphia': 101},
    'New York': {'Syracuse': 254, 'Philadelphia': 97, 'Providence': 181, 'Boston': 215},
    'Providence': {'New York': 181, 'Boston': 50},
    'Boston': {'Syracuse': 312, 'New York': 215, 'Providence': 50, 'Portland': 107},
    'Portland': {'Boston': 107}
}



from my_deque import MyDeque

def bfs(adj, s, g):
    """BFS to find all paths."""
    q = MyDeque([(s, [s], 0)])
    res = []
    while q:
        u, p, c = q.popleft()
        for v, w in adj[u].items():
            if v not in p:
                if v == g:
                    res.append((p + [v], c + w))
                else:
                    q.append((v, p + [v], c + w))
    return res

def dfs(adj, u, g, p=None, c=0):
    """Recursive DFS to find all paths."""
    if p is None: p = [u]
    if u == g: return [(p, c)]
    res = []
    for v, w in adj[u].items():
        if v not in p:
            paths = dfs(adj, v, g, p + [v], c + w)
            for path in paths: res.append(path)
    return res


st, en = "Syracuse", "Chicago"
print(f"Searching for all paths from {st} to {en}...\n")

print("--- BFS Result ---")
bfs_res = bfs(adj, st, en)
for i, (p, c) in enumerate(bfs_res, 1):
    print(f"Path {i}: {' -> '.join(p)} | Cost: {c}")

print("\n--- DFS Result ---")
dfs_res = dfs(adj, st, en)
for i, (p, c) in enumerate(dfs_res, 1):
    print(f"Path {i}: {' -> '.join(p)} | Cost: {c}")

if bfs_res:
    ans = min(bfs_res, key=lambda x: x[1])
    print(f"\nMin Cost Path: {' -> '.join(ans[0])} | Cost {ans[1]}")
# import hashlib

# ============================================================
# CONFIG
# ============================================================

# TARGET_HASH = "d54f6fb706a228fa3a95f98e4a455b5b0ff3a607cef32ccfd57ca4f155bf0f3f"
# import os

# CHEESE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cheese_list.txt")

# # Normalization options:
# # exact:     keep string as-is
# # lower:     lowercase entire string
# # upper:     uppercase entire string
# NORMALIZE_MODE = "exact"

# # space handling:
# # keep:      keep spaces
# # underscore:replace spaces with underscores
# # remove:    remove spaces entirely
# SPACE_MODE = "keep"

# # special character handling:
# # keep:      keep as-is
# # remove:    remove non-alphanumerics except space (customizable)
# SPECIAL_MODE = "keep"

# # ============================================================
# # NORMALIZATION FUNCTIONS
# # ============================================================

# def normalize(name):
#     original = name.strip()

#     # case normalization
#     if NORMALIZE_MODE == "lower":
#         name = original.lower()
#     elif NORMALIZE_MODE == "upper":
#         name = original.upper()
#     else:
#         name = original

#     # space handling
#     if SPACE_MODE == "underscore":
#         name = name.replace(" ", "_")
#     elif SPACE_MODE == "remove":
#         name = name.replace(" ", "")

#     # special character handling
#     if SPECIAL_MODE == "remove":
#         # keep only alphanumeric + space + underscore
#         filtered = []
#         for ch in name:
#             if ch.isalnum() or ch in (" ", "_"):
#                 filtered.append(ch)
#         name = "".join(filtered)

#     return name

# # ============================================================
# # MAIN
# # ============================================================

# def sha256_hex(s: str) -> str:
#     return hashlib.sha256(s.encode("utf-8")).hexdigest()

# def main():
#     with open(CHEESE_FILE, "r", encoding="utf-8") as f:
#         cheeses = [line.rstrip("\n") for line in f if line.strip()]

#     print(f"Deep brute-forcing on {len(cheeses)} cheeses...")

#     def get_variants(s):
#         yield s.strip()
#         yield s.strip().lower()
#         yield s.strip().upper()
        
#         # Standard replacements
#         yield s.strip().replace(" ", "")
#         yield s.strip().lower().replace(" ", "")
#         yield s.strip().replace(" ", "_")
#         yield s.strip().lower().replace(" ", "_")
        
#         # Alphanumeric only (remove punctuation like parens, hyphens)
#         s_alnum = "".join(c for c in s if c.isalnum())
#         yield s_alnum
#         yield s_alnum.lower()
#         yield s_alnum.upper()
        
#         # Alphanumeric + spaces (for multi-word cheeses but without punctuation)
#         s_alnum_sq = "".join(c for c in s if c.isalnum() or c == " ").strip()
#         yield s_alnum_sq
#         yield s_alnum_sq.lower()

#     cheeses_extra = cheeses + ["Squeexy", "Squeezy", "Easy Cheese", "Cheese", "Squeak", "Mouse"]
    
#     print(f"Deep brute-forcing on {len(cheeses_extra)} candidates...")

#     for cheese in cheeses_extra:
#         for base in get_variants(cheese):
            
#             # Prepare salt variants
#             salt_variants = []
            
#             # 1. Hex string salts (00..FF) - "2 nibbles represented as hex chars"
#             for i in range(256):
#                 h = f"{i:02x}"
#                 salt_variants.append(h)          # '0a'
#                 salt_variants.append(h.upper())  # '0A'
            
#             # 2. Raw byte salts (b'\x00'..b'\xFF') - "2 nibbles of data"
#             #    We need to treat base as bytes for this.
            
#             base_bytes = base.encode('utf-8')
            
#             # Check string salts
#             for salt in salt_variants:
#                 # patterns: base+salt, salt+base, base+sep+salt...
#                 # Try simple concatenation first (interpreting salt as string part of text)
#                 candidates = [base + salt, salt + base]
                
#                 # Try split salt (1 char prefix, 1 char suffix) for string salts
#                 if len(salt) == 2:
#                     candidates.append(salt[0] + base + salt[1])
                
#                 for cand in candidates:
#                     if sha256_hex(cand) == TARGET_HASH:
#                         print("[MATCH FOUND - String Salt]")
#                         print(f"Original:  {cheese}")
#                         print(f"Base:      {base}")
#                         print(f"Salt:      {salt}")
#                         print(f"Candidate: {cand}")
#                         return

#             # Check raw byte salts
#             for i in range(256):
#                 b_salt = bytes([i]) # 1 byte = 2 nibbles
                
#                 # base_bytes + b_salt, b_salt + base_bytes
#                 cand_bytes_list = [base_bytes + b_salt, b_salt + base_bytes]
                
#                 for cb in cand_bytes_list:
#                     if hashlib.sha256(cb).hexdigest() == TARGET_HASH:
#                          print("[MATCH FOUND - Byte Salt]")
#                          print(f"Original:  {cheese}")
#                          print(f"Base:      {base}")
#                          print(f"Salt (hex): {i:02x}")
#                          return

#     print("No match found after massive brute-force.")

# if __name__ == "__main__":
#     main()
