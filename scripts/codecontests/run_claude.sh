mkdir -p results

# Loop through all cluster directories
for i in {0..7}; do
  CLUSTER_DIR="codecontests/cluster$i"

  # Check if this cluster directory exists
  if [ -d "$CLUSTER_DIR" ]; then
    echo "Processing $CLUSTER_DIR..."

    # Push into the cluster directory
    pushd "$CLUSTER_DIR" > /dev/null

    # Run Claude with instructions from cluster directory
    claude --dangerously-skip-permissions -p "Read the instructions in INSTRUCTIONS.md. Be sure to read all the solutions to get an idea of what the library should look like. Then make a plan for the library in PLAN.md. Then implement the library in library.py while refactoring the solutions in the current directory. As you are refactoring solutions, run tests as described in INSTRUCTIONS.md to ensure they are correct. If tests fail, you are free to examine the inputs and outputs. Continue editing the library as you refactor solutions. Make sure solutions that use any changed library functions still pass. Your goal is to make the library and solutions as compact as possible."
    # Twice for laziness
    claude --dangerously-skip-permissions -p "Read the instructions in INSTRUCTIONS.md. Be sure to read all the solutions to get an idea of what the library should look like. Read your plan in PLAN.md. Finish implementing the library in library.py while continuing to refactor the solutions in the current directory. As you are refactoring solutions, run tests as described in INSTRUCTIONS.md to ensure they are correct. If tests fail, you are free to examine the inputs and outputs. Continue editing the library as you refactor solutions. Make sure solutions that use any changed library functions still pass. Your goal is to make the library and solutions as compact as possible."


    # Pop back to the original directory
    popd > /dev/null

    # Evaluate pass rates after Claude processing
    evaluate_cluster $i > results/cluster_${i}_results.txt

    echo "Completed $CLUSTER_DIR"
  else
    echo "Skipping $CLUSTER_DIR - directory does not exist"
  fi
done
