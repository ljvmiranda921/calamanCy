# Word vector experiments
## Main results
python3 -m scripts.benchmark supervised_nsv_npt --num-trials 3 --gpu-id 0
python3 -m scripts.benchmark supervised_ysv_npt --num-trials 3 --vectors vectors/fasttext-tl --gpu-id 0 
python3 -m scripts.benchmark supervised_nsv_ypt --num-trials 3 --init-tok2vec assets/tl_tlunified_pt_chars.bin --gpu-id 0 
python3 -m scripts.benchmark supervised_ysv_ypt --num-trials 3 --vectors vectors/fasttext-tl --init-tok2vec assets/tl_tlunified_pt_chars.bin --gpu-id 0 
## Pretrain characters vs pretrain vectors
python3 -m scripts.benchmark supervised_nsv_ypt_vects --num-trials 3 --config ner_vects.cfg --init-tok2vec assets/tl_tlunified_pt_chars.bin --gpu-id 0 
## fastText, fastText TLUnified, floret TLUnified 
python3 -m scripts.benchmark supervised_ysv_npt_fasttext_tlunified --num-trials 3 --vectors vectors/fasttext-tl-tlunified --gpu-id 0 
python3 -m scripts.benchmark supervised_ysv_npt_floret_tlunified --num-trials 3 --vectors vectors/floret-tl-tlunified --gpu-id 0 