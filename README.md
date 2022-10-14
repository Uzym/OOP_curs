pip install -U openmim
mim install mmcv-full
git clone https://github.com/open-mmlab/mmpose.git
cd mmpose
pip install -r requirements.txt
pip install -v -e .
# "-v" means verbose, or more output
# "-e" means installing a project in editable mode,
# thus any local modifications made to the code will take effect without reinstallation.
pip install mmpose
python demo/top_down_img_demo.py \
    configs/face/2d_kpt_sview_rgb_img/topdown_heatmap/aflw/hrnetv2_w18_aflw_256x256.py \
    https://download.openmmlab.com/mmpose/face/hrnetv2/hrnetv2_w18_aflw_256x256-f2bbc62b_20210125.pth \
    --img-root tests/data/aflw/ --json-file tests/data/aflw/test_aflw.json \
    --out-img-root vis_results
top_down_img_demo.py  - разобрать
++++++++++++++


СКРИПТ ДЛЯ 1 ФОТКИ + тензор координат

python3 demo/face_img_demo.py     configs/face/2d_kpt_sview_rgb_img/topdown_heatmap/aflw/hrnetv2_w18_aflw_256x256.py     https://download.openmmlab.com/mmpose/face/hrnetv2/hrnetv2_w18_aflw_256x256-f2bbc62b_20210125.pth     --img-root tests/data/aflw/     --img 0.jpeg --out-img-root vis_results
