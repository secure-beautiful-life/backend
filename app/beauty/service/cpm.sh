conda init bash
conda activate cpm
f'python ./CPM/main.py --device cpu ' \
f'--style {config.PRODUCT_IMAGE_DIR}/{product_file_name} ' \
f'--input {config.USER_PROFILE_IMAGE_DIR}/{profile_file_name} ' \
f'--savedir ${config.BEAUTY_IMAGE_DIR} --filename {random_file_name} &&' \
conda deactivate

