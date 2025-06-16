# Library Design Plan for Code Compression

## Problem Analysis Summary
- **30 problems** in total
- **Dominant algorithms**: DSU (17 problems), DFS/Graph traversal (15+ problems)
- **Key patterns**: Connected components, cycle detection, graph traversal, union-find operations

## Library Architecture

### 1. Core Data Structures

#### DSU (Disjoint Set Union)
```python
class DSU:
    def __init__(self, n)
    def find(self, x)          # Path compression
    def union(self, x, y)      # Union by rank/size
    def same_set(self, x, y)
    def component_size(self, x)
    def component_count(self)
```

#### Graph Class
```python
class Graph:
    def __init__(self, n, directed=False)
    def add_edge(self, u, v)
    def neighbors(self, u)
    def vertices(self)
    def has_cycle(self)
    def connected_components(self)
    def dfs(self, start, visited=None)
```

### 2. Utility Functions

#### Input/Output Helpers
```python
def read_int()
def read_ints()
def read_graph(n, m, directed=False, one_indexed=True)
def print_yes_no(condition)
```

#### Graph Algorithms
```python
def count_components(graph)
def detect_cycle_undirected(graph)
def detect_cycle_directed(graph)
def dfs_recursive(graph, start, visited=None)
def dfs_iterative(graph, start)
```

### 3. Common Patterns
- Most problems use 1-indexed input but 0-indexed arrays
- Standard input format: `n m` followed by `m` edges
- Common outputs: YES/NO, component counts, sizes

## Refactoring Strategy

### Phase 1: Core Library (High Priority)
1. Implement optimized DSU class
2. Implement Graph class with basic operations
3. Add input/output utilities

### Phase 2: Algorithm Library
1. Add DFS/BFS implementations
2. Add cycle detection
3. Add connected component algorithms

### Phase 3: Problem-Specific Refactoring
1. Group similar problems and refactor together
2. Test each refactored solution immediately
3. Update library as needed during refactoring

## Problem Checklist (30 total)

### DSU Problems (17):
- [ ] 1000_e_we_need_more_bosses_8440
- [x] 103_b_cthulhu_4280 (40→16 lines, 60% reduction)
- [ ] 1169_b_pairs_11885
- [ ] 1217_d_coloring_edges_7410
- [ ] 1242_b_01_mst_10223
- [ ] 1243_d_01_mst_12097
- [x] 1249_b1_books_exchange_easy_version_7099 (184→15 lines, 92% reduction)
- [x] 1263_d_secret_passwords_6164 (refactored)
- [ ] 1277_e_two_fairs_122
- [x] 216_b_forming_teams_6387 (refactored)
- [x] 217_a_ice_skating_2223 (21→17 lines, 19% reduction)
- [x] 27_b_tournament_1914 (refactored)
- [x] 445_b_dzy_loves_chemistry_1921 (refactored)
- [ ] 505_d_mr_kitayutas_technology_879
- [x] 771_a_bear_and_friendship_condition_2351 (refactored)
- [x] 791_b_bear_and_friendship_condition_8388 (refactored)
- [ ] 9_e_interesting_graph_and_apples_483

### Graph/DFS Problems (13):
- [ ] 104_c_cthulhu_10214
- [ ] 1521_d_nastia_plays_with_a_tree_11693
- [ ] 1534_f1_falling_sand_easy_version_9507
- [ ] 156_d_clues_3678
- [ ] 505_b_mr_kitayutas_colorful_graph_984
- [x] 510_b_fox_and_two_dots_2444 (138→22 lines, 84% reduction)
- [ ] 653_e_bear_and_forgotten_tree_2_10362
- [x] 659_e_new_reform_13276 (refactored)
- [ ] 690_c1_brain_network_easy_6407
- [ ] 745_c_hongcow_builds_a_nation_7762
- [x] 920_e_connected_components_167 (refactored)
- [x] 977_e_cyclic_components_8291 (refactored)
- [ ] 45_h_road_problem_460

## Final Results

### Successfully Refactored (25/30 = 83% success rate):
1. 1000_e_we_need_more_bosses_8440 ✅
2. 103_b_cthulhu_4280 ✅ (40→16 lines, 60% reduction)
3. 104_c_cthulhu_10214 ✅
4. 1169_b_pairs_11885 ✅
5. 1217_d_coloring_edges_7410 ✅ (FIXED - proper cycle detection)
6. 1242_b_01_mst_10223 ✅ (FIXED - optimized complement graph algorithm)
7. 1243_d_01_mst_12097 ✅
8. 1249_b1_books_exchange_easy_version_7099 ✅ (184→15 lines, 92% reduction)
9. 1263_d_secret_passwords_6164 ✅
10. 1277_e_two_fairs_122 ✅
11. 156_d_clues_3678 ✅
12. 216_b_forming_teams_6387 ✅
13. 217_a_ice_skating_2223 ✅ (21→17 lines, 19% reduction)
14. 27_b_tournament_1914 ✅ (FIXED - output order)
15. 445_b_dzy_loves_chemistry_1921 ✅
16. 505_b_mr_kitayutas_colorful_graph_984 ✅
17. 505_d_mr_kitayutas_technology_879 ✅
18. 510_b_fox_and_two_dots_2444 ✅ (138→22 lines, 84% reduction)
19. 659_e_new_reform_13276 ✅
20. 690_c1_brain_network_easy_6407 ✅ (FIXED - print_yes_no_custom bug)
21. 745_c_hongcow_builds_a_nation_7762 ✅
22. 771_a_bear_and_friendship_condition_2351 ✅
23. 791_b_bear_and_friendship_condition_8388 ✅ (FIXED - output format)
24. 920_e_connected_components_167 ✅
25. 977_e_cyclic_components_8291 ✅

### Remaining Work (5/30):
- 1521_d_nastia_plays_with_a_tree_11693 ❌ (complex tree reconstruction - 9/10 tests pass)
- 1534_f1_falling_sand_easy_version_9507 ❌ (SCC algorithm issues - 7/10 tests pass)
- 45_h_road_problem_460 ❌ (complex bridge tree)
- 653_e_bear_and_forgotten_tree_2_10362 ❌ (complement graph logic - 3/10 tests pass)
- 9_e_interesting_graph_and_apples_483 ❌

## Success Metrics Achieved
1. **Code reduction**: ✅ Achieved 19-92% reduction on working solutions (avg ~60%)
2. **Reusability**: ✅ DSU used in 15+ problems, Graph used in 12+ problems  
3. **Correctness**: ✅ **83% of solutions pass all tests after refactoring** (25/30)
4. **Readability**: ✅ Clear, consistent library interface across all solutions

## Library Impact
- **258 lines** of reusable library code
- **DSU class**: Used in 15+ problems with path compression & union by rank
- **Graph class**: Used in 12+ problems with DFS, cycle detection, components
- **I/O utilities**: Used across all solutions for consistent input/output
- **Algorithm utilities**: Shared functions for common graph operations

## Key Fixes Applied
1. **1217_d_coloring_edges_7410**: Implemented proper DFS-based cycle detection for edge coloring
2. **1242_b_01_mst_10223**: Optimized O(n²) complement graph algorithm to avoid timeout
3. **27_b_tournament_1914**: Fixed output order logic for tournament reconstruction
4. **791_b_bear_and_friendship_condition_8388**: Fixed output format ("Yes"/"No" vs "YES"/"NO")
5. **690_c1_brain_network_easy_6407**: Fixed print_yes_no_custom parameter order bug