# Library Design Plan

After analyzing the problems, I've identified several common patterns and functionalities that can be extracted into a reusable library. The main categories are:

## Core Components

1. **Graph Representation**
   - Adjacency list creation
   - Graph initialization functions
   - Edge input parsing

2. **Graph Algorithms**
   - DFS (Depth-First Search)
     - Recursive implementation
     - Iterative implementation
     - Component counting
     - Cycle detection
   - BFS (Breadth-First Search)
     - Standard implementation
     - Shortest path
   - Connected Components
     - Finding and counting connected components
   - Bridges and Articulation Points
     - Finding bridges in a graph
     - Bridge tree construction

3. **Disjoint Set Union (DSU)**
   - Standard implementation with path compression and rank/size optimization
   - Find and Union operations
   - Component size tracking

4. **Input/Output Utilities**
   - Fast I/O operations
   - Parsing functions for different input formats
   - Standard output formatters

## Implementation Approach

The library will be organized into separate classes/modules:
- `Graph`: For graph representation and basic operations
- `GraphAlgorithms`: For graph traversal and algorithms
- `DisjointSetUnion`: For DSU operations
- `IOUtils`: For input/output utilities

## Refactoring Checklist

As I refactor each problem solution, I will track them here:

- [ ] 1000_e_we_need_more_bosses_8440
- [ ] 103_b_cthulhu_4280
- [ ] 104_c_cthulhu_10214
- [ ] 1169_b_pairs_11885
- [ ] 1217_d_coloring_edges_7410
- [ ] 1242_b_01_mst_10223
- [ ] 1243_d_01_mst_12097
- [ ] 1249_b1_books_exchange_easy_version_7099
- [ ] 1263_d_secret_passwords_6164
- [ ] 1277_e_two_fairs_122
- [ ] 1521_d_nastia_plays_with_a_tree_11693
- [ ] 1534_f1_falling_sand_easy_version_9507
- [ ] 156_d_clues_3678
- [ ] 216_b_forming_teams_6387
- [ ] 217_a_ice_skating_2223
- [ ] 27_b_tournament_1914
- [ ] 445_b_dzy_loves_chemistry_1921
- [ ] 45_h_road_problem_460
- [ ] 505_b_mr_kitayutas_colorful_graph_984
- [ ] 505_d_mr_kitayutas_technology_879
- [ ] 510_b_fox_and_two_dots_2444
- [ ] 653_e_bear_and_forgotten_tree_2_10362
- [ ] 659_e_new_reform_13276
- [ ] 690_c1_brain_network_easy_6407
- [ ] 745_c_hongcow_builds_a_nation_7762
- [ ] 771_a_bear_and_friendship_condition_2351
- [ ] 791_b_bear_and_friendship_condition_8388
- [ ] 920_e_connected_components_167
- [ ] 977_e_cyclic_components_8291
- [ ] 9_e_interesting_graph_and_apples_483