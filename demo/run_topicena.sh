INPUT="./asap20.csv"

set +e

echo "[1/10] SAFE_FINE_1 nn=8 nc=3 mcs=30 ms=5 pth=0.02"
topicena --input "$INPUT" --n_neighbors 8 --n_components 3 --min_cluster_size 30 --min_samples 5 --number_of_keywords 4 --prob_th 0.02 --output test_001

echo "[2/10] SAFE_FINE_2 nn=8 nc=3 mcs=35 ms=6 pth=0.02"
topicena --input "$INPUT" --n_neighbors 8 --n_components 3 --min_cluster_size 35 --min_samples 6 --number_of_keywords 4 --prob_th 0.02 --output test_002

echo "[3/10] SAFE_FINE_3 nn=9 nc=3 mcs=40 ms=6 pth=0.03"
topicena --input "$INPUT" --n_neighbors 9 --n_components 3 --min_cluster_size 40 --min_samples 6 --number_of_keywords 4 --prob_th 0.03 --output test_003

echo "[4/10] ENA_SWEET_1 nn=9 nc=4 mcs=40 ms=6 pth=0.03"
topicena --input "$INPUT" --n_neighbors 9 --n_components 4 --min_cluster_size 40 --min_samples 6 --number_of_keywords 4 --prob_th 0.03 --output test_004

echo "[5/10] ENA_SWEET_2 nn=9 nc=4 mcs=50 ms=7 pth=0.04"
topicena --input "$INPUT" --n_neighbors 9 --n_components 4 --min_cluster_size 50 --min_samples 7 --number_of_keywords 4 --prob_th 0.04 --output test_005

echo "[6/10] ENA_SWEET_3 nn=10 nc=4 mcs=50 ms=8 pth=0.05"
topicena --input "$INPUT" --n_neighbors 10 --n_components 4 --min_cluster_size 50 --min_samples 8 --number_of_keywords 4 --prob_th 0.05 --output test_006

echo "[7/10] MID_COARSE_1 nn=10 nc=4 mcs=60 ms=8 pth=0.06"
topicena --input "$INPUT" --n_neighbors 10 --n_components 4 --min_cluster_size 60 --min_samples 8 --number_of_keywords 4 --prob_th 0.06 --output test_007

echo "[8/10] MID_COARSE_2 nn=10 nc=5 mcs=60 ms=9 pth=0.07"
topicena --input "$INPUT" --n_neighbors 10 --n_components 5 --min_cluster_size 60 --min_samples 9 --number_of_keywords 4 --prob_th 0.07 --output test_008

echo "[9/10] COARSE_SEM_1 nn=10 nc=5 mcs=70 ms=10 pth=0.08"
topicena --input "$INPUT" --n_neighbors 10 --n_components 5 --min_cluster_size 70 --min_samples 10 --number_of_keywords 4 --prob_th 0.08 --output test_009

echo "[10/10] COARSE_SE
M_2 nn=10 nc=5 mcs=80 ms=10 pth=0.10"
topicena --input "$INPUT" --n_neighbors 10 --n_components 5 --min_cluster_size 80 --min_samples 10 --number_of_keywords 4 --prob_th 0.10 --output test_010
