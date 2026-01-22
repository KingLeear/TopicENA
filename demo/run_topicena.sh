INPUT="./asap20.csv"
NUM_KEYWORDS=5
MIN_TOPIC_SIZE=20

set +e


# echo "[1/10] SAFE_FINE_1 nn=9 nc=4 mcs=40 ms=6 pth=0.03"
# topicena --input "$INPUT" \
#   --n_neighbors 9 --n_components 4 \
#   --min_cluster_size 40 --min_samples 6 \
#   --number_of_keywords "$NUM_KEYWORDS" \
#   --prob_th 0.03 \
#   --output test_001

# echo "[2/10] SAFE_FINE_2 nn=9 nc=4 mcs=45 ms=7 pth=0.03"
# topicena --input "$INPUT" \
#   --n_neighbors 9 --n_components 4 \
#   --min_cluster_size 45 --min_samples 7 \
#   --number_of_keywords "$NUM_KEYWORDS" \
#   --prob_th 0.03 \
#   --output test_002

# echo "[3/10] ENA_SWEET_1 nn=9 nc=4 mcs=50 ms=7 pth=0.04"
# topicena --input "$INPUT" \
#   --n_neighbors 9 --n_components 4 \
#   --min_cluster_size 50 --min_samples 7 \
#   --number_of_keywords "$NUM_KEYWORDS" \
#   --prob_th 0.04 \
#   --output test_003

# echo "[4/10] ENA_SWEET_2 nn=10 nc=4 mcs=50 ms=8 pth=0.04"
# topicena --input "$INPUT" \
#   --n_neighbors 10 --n_components 4 \
#   --min_cluster_size 50 --min_samples 8 \
#   --number_of_keywords "$NUM_KEYWORDS" \
#   --prob_th 0.04 \
#   --output test_004

# echo "[5/10] ENA_SWEET_3 nn=10 nc=4 mcs=60 ms=8 pth=0.05"
# topicena --input "$INPUT" \
#   --n_neighbors 10 --n_components 4 \
#   --min_cluster_size 60 --min_samples 8 \
#   --number_of_keywords "$NUM_KEYWORDS" \
#   --prob_th 0.05 \
#   --output test_005

# echo "[6/10] MID_COARSE_1 nn=10 nc=5 mcs=60 ms=9 pth=0.06"
# topicena --input "$INPUT" \
#   --n_neighbors 10 --n_components 5 \
#   --min_cluster_size 60 --min_samples 9 \
#   --number_of_keywords "$NUM_KEYWORDS" \
#   --prob_th 0.06 \
#   --output test_006

# echo "[7/10] MID_COARSE_2 nn=10 nc=5 mcs=70 ms=9 pth=0.07"
# topicena --input "$INPUT" \
#   --n_neighbors 10 --n_components 5 \
#   --min_cluster_size 70 --min_samples 9 \
#   --number_of_keywords "$NUM_KEYWORDS" \
#   --prob_th 0.07 \
#   --output test_007

# echo "[8/10] COARSE_SEM_1 nn=10 nc=5 mcs=80 ms=10 pth=0.08"
# topicena --input "$INPUT" \
#   --n_neighbors 10 --n_components 5 \
#   --min_cluster_size 80 --min_samples 10 \
#   --number_of_keywords "$NUM_KEYWORDS" \
#   --prob_th 0.08 \
#   --output test_008

# echo "[9/10] COARSE_SEM_2 nn=10 nc=5 mcs=90 ms=10 pth=0.09"
# topicena --input "$INPUT" \
#   --n_neighbors 10 --n_components 5 \
#   --min_cluster_size 90 --min_samples 10 \
#   --number_of_keywords "$NUM_KEYWORDS" \
#   --prob_th 0.09 \
#   --output test_009

# echo "[10/10] COARSE_SEM_3 nn=10 nc=5 mcs=100 ms=10 pth=0.10"
# topicena --input "$INPUT" \
#   --n_neighbors 10 --n_components 5 \
#   --min_cluster_size 100 --min_samples 10 \
#   --number_of_keywords "$NUM_KEYWORDS" \
#   --prob_th 0.10 \
#   --output test_010




# echo "[1/10] SAFE_FINE_1 nn=9 nc=4 mcs=60 ms=8 pth=0.03"
# # topicena --input "$INPUT" --n_neighbors 9 --n_components 4 --min_cluster_size 60 --min_samples 8 --number_of_keywords "$NUM_KEYWORDS" --prob_th 0.03 --output test_001

# echo "[2/10] SAFE_FINE_2 nn=9 nc=4 mcs=70 ms=8 pth=0.03"
# topicena --input "$INPUT" --n_neighbors 9 --n_components 4 --min_cluster_size 70 --min_samples 8 --number_of_keywords "$NUM_KEYWORDS" --prob_th 0.03 --output test_002

# echo "[3/10] ENA_SWEET_1 nn=10 nc=4 mcs=70 ms=9 pth=0.04"
# topicena --input "$INPUT" --n_neighbors 10 --n_components 4 --min_cluster_size 70 --min_samples 9 --number_of_keywords "$NUM_KEYWORDS" --prob_th 0.04 --output test_003

# echo "[4/10] ENA_SWEET_2 nn=10 nc=4 mcs=80 ms=9 pth=0.04"
# topicena --input "$INPUT" --n_neighbors 10 --n_components 4 --min_cluster_size 80 --min_samples 9 --number_of_keywords "$NUM_KEYWORDS" --prob_th 0.04 --output test_004

# echo "[5/10] ENA_SWEET_3 nn=10 nc=5 mcs=80 ms=10 pth=0.05"
# topicena --input "$INPUT" --n_neighbors 10 --n_components 5 --min_cluster_size 80 --min_samples 10 --number_of_keywords "$NUM_KEYWORDS" --prob_th 0.05 --output test_005

# echo "[6/10] MID_COARSE_1 nn=10 nc=5 mcs=90 ms=10 pth=0.06"
# topicena --input "$INPUT" --n_neighbors 10 --n_components 5 --min_cluster_size 90 --min_samples 10 --number_of_keywords "$NUM_KEYWORDS" --prob_th 0.06 --output test_006

# echo "[7/10] MID_COARSE_2 nn=10 nc=5 mcs=100 ms=10 pth=0.07"
# topicena --input "$INPUT" --n_neighbors 10 --n_components 5 --min_cluster_size 100 --min_samples 10 --number_of_keywords "$NUM_KEYWORDS" --prob_th 0.07 --output test_007

# echo "[8/10] COARSE_SEM_1 nn=10 nc=5 mcs=120 ms=10 pth=0.08"
# topicena --input "$INPUT" --n_neighbors 10 --n_components 5 --min_cluster_size 120 --min_samples 10 --number_of_keywords "$NUM_KEYWORDS" --prob_th 0.08 --output test_008

# echo "[9/10] COARSE_SEM_2 nn=10 nc=5 mcs=140 ms=10 pth=0.09"
# topicena --input "$INPUT" --n_neighbors 10 --n_components 5 --min_cluster_size 140 --min_samples 10 --number_of_keywords "$NUM_KEYWORDS" --prob_th 0.09 --output test_009

# echo "[10/10] COARSE_SEM_3 nn=10 nc=5 mcs=160 ms=10 pth=0.10"
# topicena --input "$INPUT" --n_neighbors 10 --n_components 5 --min_cluster_size 160 --min_samples 10 --number_of_keywords "$NUM_KEYWORDS" --prob_th 0.10 --output test_010






RUN_ID=1

echo "===== TopicENA grid search started ====="

for NN in 40 60 80; do
  for MD in 0.15 0.20 0.25; do
    for MCS in 60 80 100; do
      for PTH in 0.01 0.05 0.1; do

        OUT=$(printf "test_%03d" "$RUN_ID")

        echo "[$RUN_ID] nn=$NN min_dist=$MD mcs=$MCS mts=$MIN_TOPIC_SIZE pth=$PTH -> $OUT"

        topicena \
          --input "$INPUT" \
          --n_neighbors "$NN" \
          --min_dist "$MD" \
          --min_cluster_size "$MCS" \
          --min_topic_size "$MIN_TOPIC_SIZE" \
          --number_of_keywords "$NUM_KEYWORDS" \
          --prob_th "$PTH" \
          --output "$OUT" \
        || echo "[FAIL] $OUT (nn=$NN md=$MD mcs=$MCS pth=$PTH)"

        RUN_ID=$((RUN_ID + 1))

      done
    done
  done
done