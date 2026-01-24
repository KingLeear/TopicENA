INPUT="./asap20.csv"
NUM_KEYWORDS=2
MIN_TOPIC_SIZE=20

set +e

RUN_ID=1

echo "===== TopicENA grid search started ====="

for WSB in 15 20 30; do
  for NN in 40 60 80; do
    for MD in 0.15 0.20 0.25; do
      for MCS in 60 80 100; do
        for PTH in 0.01 0.05 0.1 0.2; do

            OUT=$(printf "testwsb_%03d" "$RUN_ID")

            echo "[$RUN_ID] n_neighbors=$NN min_dist=$MD min_cluster_size=$MCS min_topic_size=$MIN_TOPIC_SIZE prob_th=$PTH window_size=$WSB-> $OUT"

            topicena \
            --input "$INPUT" \
            --n_neighbors "$NN" \
            --min_dist "$MD" \
            --min_cluster_size "$MCS" \
            --min_topic_size "$MIN_TOPIC_SIZE" \
            --number_of_keywords "$NUM_KEYWORDS" \
            --prob_th "$PTH" \
            --output "$OUT" \
            --window_size_back "$WSB" \
            || echo "[FAIL] $OUT (nn=$NN md=$MD mcs=$MCS pth=$PTH)"

            RUN_ID=$((RUN_ID + 1))

        done
      done
    done
  done
done