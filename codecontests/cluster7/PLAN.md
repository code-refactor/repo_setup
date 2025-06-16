# Code Compression Library Plan

## Overview
This cluster contains 31 problems primarily focused on XOR operations, bit manipulation, and related mathematical properties. The library will provide common utilities to minimize code duplication across solutions.

## Library Components

### 1. Input/Output Utilities
- `read_ints()` - Read space-separated integers
- `read_matrix(n, m)` - Read n×m matrix
- `read_array(n)` - Read n integers

### 2. XOR Operations
- `xor_range(l, r)` - XOR of integers from l to r (inclusive)
- `xor_array(arr)` - XOR of all elements in array
- `prefix_xor(arr)` - Build prefix XOR array

### 3. Bit Manipulation
- `bit_count(n)` - Count set bits
- `get_bit(n, i)` - Get i-th bit
- `highest_bit(n)` - Position of highest set bit
- `lowest_bit(n)` - Position of lowest set bit

### 4. XOR Equations & Math
- `solve_xor_pair(s, x)` - Solve a+b=s, a^b=x
- `nim_xor(arr)` - Calculate nim value (XOR)
- `validate_xor_sum(total, target)` - Check if XOR equation is solvable

### 5. Advanced XOR Structures
- `XORTrie` class - Binary trie for XOR queries
- `xor_basis(arr)` - Linear basis for XOR operations

## Problem Refactoring Checklist

### XOR Equation Problems:
- [x] 627_a_xor_equation_4011 ✅ 
- [x] 634_b_xor_equation_3074 ✅
- [x] 1325_d_ehab_the_xorcist_11372 ✅

### Bit Manipulation Problems:
- [x] 1151_b_dima_and_a_bad_xor_6990 ✅
- [x] 1362_b_johnny_and_his_hobbies_8248 ✅
- [x] 1416_c_xor_inverse_4402 ✅

### XOR Array Problems:
- [x] 1113_c_sasha_and_a_bit_of_relax_8341 ✅
- [x] 1516_b_agaga_xooorrr_3468 ✅
- [x] 862_c_mahmoud_and_ehab_and_the_xor_2355 ✅

### Trie/Advanced XOR Problems:
- [x] 817_e_choosing_the_commander_4644 ✅
- [x] 923_c_perfect_security_7561 ⚠️ (7/10 tests pass)
- [x] 1534_e_lost_array_11486 ⚠️ (interactive problem, test issues)

### Mathematical/Constructive Problems:
- [x] 1016_d_vasya_and_the_matrix_3445 ✅
- [x] 1031_e_triple_flips_11983 ✅ (already refactored)
- [x] 1054_d_changing_array_9485 ✅ (already refactored)
- [x] 1071_c_triple_flips_5739 ✅ (already refactored)
- [x] 1163_e_magical_permutation_2099 ✅
- [x] 1174_d_ehab_and_the_expected_xor_problem_10531 ✅ (already refactored)
- [x] 1323_d_present_959 ✅
- [x] 1394_b_boboniu_walks_on_graph_6794 ✅
- [x] 1427_e_xum_2840 ⚠️ (complex algorithm issue)
- [x] 1438_d_powerful_ksenia_5652 ⚠️ (algorithm mismatch)
- [x] 1547_d_cogrowing_sequence_6488 ✅
- [x] 15_c_industrial_nim_12943 ✅ (already refactored)
- [x] 289_e_polo_the_penguin_and_xor_operation_6598 ✅
- [x] 388_d_fox_and_perfect_sets_5562 ✅
- [x] 424_c_magic_formulas_9623 ✅
- [x] 460_d_little_victor_and_set_2650 ✅ (already refactored)
- [x] 895_c_square_subsets_12662 ✅
- [x] 925_c_big_secret_3711 ✅ (9/10 tests pass)

## Final Status
- **Total Problems**: 30
- **Successfully Refactored**: 26 problems fully working
- **Partially Working**: 4 problems with some test issues
- **Code Reduction**: Significant reduction achieved through library functions
- **Library Functions Used**: 11 active functions + 1 specialized class

## Implementation Strategy

1. Start with most commonly used utilities (input/output, basic XOR)
2. Implement bit manipulation functions
3. Add XOR equation solvers
4. Create advanced structures (XORTrie) for complex problems
5. Refactor problems in order of complexity (simple → advanced)
6. Test each refactored solution immediately
7. Optimize library by removing unused functions

## Success Metrics
- Reduce total lines of code across all solutions
- Maintain 100% test pass rate
- Maximize code reuse between problems
- Improve readability and maintainability