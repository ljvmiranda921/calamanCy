#!/bin/bash

MODEL="tl_calamancy_md"  # Set this to tl_calamancy_md, tl_calamancy_lg, or tl_calamancy_trf as needed.

case $MODEL in
  tl_calamancy_md)
    echo "Executing actions for tl_calamancy_md..."
    python -m spacy project run tl-calamancy . \
        --vars.size md \
        --vars.vectors vectors/floret-tl-md
    ;;
  tl_calamancy_lg)
    echo "Executing actions for tl_calamancy_lg..."
    python -m spacy project run tl-calamancy . \
        --vars.size lg \
        --vars.vectors vectors/fasttext-tl
    ;;
  tl_calamancy_trf)
    echo "Executing actions for tl_calamancy_trf..."
    python -m spacy project run tl-calamancy-trf
    # Add your commands here
    ;;
  *)
    echo "Unknown MODEL: $MODEL"
    ;;
esac