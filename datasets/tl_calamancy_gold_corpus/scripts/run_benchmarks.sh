# Run experiments for word vectors
python3 -m scripts.benchmark supervised_nsv_npt --num-trials 3 --gpu-id 0
python3 -m scripts.benchmark supervised_ysv_npt --num-trials 3 --vectors vectors/fasttext-tl --gpu-id 0 
python3 -m scripts.benchmark supervised_nsv_ypt --num-trials 3 --init-tok2vec assets/tl_tlunified_pt_e10.bin --gpu-id 0 
python3 -m scripts.benchmark supervised_ysv_ypt --num-trials 3 --vectors vectors/fasttext-tl --init-tok2vec assets/tl_tlunified_pt_e10.bin --gpu-id 0 