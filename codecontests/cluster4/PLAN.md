# Library Design Plan for Cluster4

Based on the analysis of the problems in this cluster, I've identified that most problems deal with geometric concepts such as points, lines, triangles, and related calculations. Here's my plan for creating a comprehensive library:

## Core Components

### 1. Point Class
- Represent 2D points with x, y coordinates
- Basic operations: addition, subtraction, equality check
- Methods for distance calculations, vector operations
- Support for common geometric tests (collinearity, etc.)

### 2. Line Class
- Representation using slope and intercept or two points
- Methods for checking if a point is on a line
- Line intersection calculations
- Utilities for line orientation and position relationships

### 3. Triangle Class
- Representation using three points
- Area calculation
- Checking if a point is inside a triangle
- Triangle properties (right-angled, etc.)

### 4. Utility Functions
- GCD/LCM functions for reducing fractions
- Calculating slopes between points
- Checking collinearity of points
- Distance calculations (point-to-point, point-to-line)
- Vector operations (cross product, dot product)
- Angle calculations

### 5. Input/Output Helpers
- Fast I/O implementations
- Common parsing patterns for geometry problems

## Refactoring Approach

1. Start with implementing basic Point and Line classes with core functionality
2. Add utility functions as needed while refactoring solutions
3. Expand the library with more complex geometric operations as we encounter them
4. Keep track of refactored problems and ensure all tests pass

## Refactoring Checklist

As I refactor each problem, I'll mark it here:

- [x] 1046_i_say_hello_9380
- [x] 1163_c1_power_transmission_easy_edition_2411
- [x] 1163_c2_power_transmission_hard_edition_12093
- [x] 1271_c_shawarma_tent_643
- [x] 135_b_rectangle_and_square_9812
- [x] 136_d_rectangle_and_square_9500
- [x] 13_b_letter_a_6066
- [x] 1468_f_full_turn_7213
- [x] 165_a_supercentral_point_7945
- [x] 183_b_zoo_1910
- [x] 2_c_commentator_problem_4414
- [x] 32_e_hideandseek_3373
- [x] 334_b_eight_point_sets_7016
- [x] 407_a_triangle_11184
- [x] 464_b_restore_cube__2130
- [x] 498_a_crazy_town_4318
- [x] 499_c_crazy_town_6399
- [x] 514_b_han_solo_and_lazer_gun_9314
- [x] 552_d_vanya_and_triangles_5048
- [x] 598_f_cut_length_4738
- [x] 617_d_polyline_7236
- [x] 618_c_constellation_3489
- [x] 630_o_arrow_1929
- [x] 659_d_bicycle_race_5157
- [x] 749_b_parallelogram_is_back_2975
- [x] 850_a_five_dimensional_points_3812
- [x] 886_f_symmetric_projections_6728
- [x] 889_d_symmetric_projections_6832
- [x] 934_e_a_colourful_prospect_3399
- [x] 961_d_pair_of_lines_12769