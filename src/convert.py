import os
import shutil
from urllib.parse import unquote, urlparse

import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import get_file_ext, get_file_name
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    train_images_path = "/home/alex/DATASETS/TODO/ISIC Challenge/ISIC2018_Task1-2_Training_Input"
    train_masks1_path = (
        "/home/alex/DATASETS/TODO/ISIC Challenge/ISIC2018_Task1_Training_GroundTruth"
    )
    train_masks2_path = (
        "/home/alex/DATASETS/TODO/ISIC Challenge/ISIC2018_Task2_Training_GroundTruth_v3"
    )

    val_images_path = "/home/alex/DATASETS/TODO/ISIC Challenge/ISIC2018_Task1-2_Validation_Input"
    val_masks1_path = (
        "/home/alex/DATASETS/TODO/ISIC Challenge/ISIC2018_Task1_Validation_GroundTruth"
    )
    val_masks2_path = (
        "/home/alex/DATASETS/TODO/ISIC Challenge/ISIC2018_Task2_Validation_GroundTruth"
    )

    test_images_path = "/home/alex/DATASETS/TODO/ISIC Challenge/ISIC2018_Task1-2_Test_Input"
    test_masks1_path = "/home/alex/DATASETS/TODO/ISIC Challenge/ISIC2018_Task1_Test_GroundTruth"
    test_masks2_path = "/home/alex/DATASETS/TODO/ISIC Challenge/ISIC2018_Task2_Test_GroundTruth"

    batch_size = 30
    images_ext = ".jpg"
    masks1_ext = "_segmentation.png"
    masks2_exts = [
        "_attribute_globules.png",
        "_attribute_milia_like_cyst.png",
        "_attribute_negative_network.png",
        "_attribute_pigment_network.png",
        "_attribute_streaks.png",
    ]
    mask_file_ext = ".png"

    ds_name_to_data = {
        "val": (val_images_path, val_masks1_path, val_masks2_path),
        "train": (train_images_path, train_masks1_path, train_masks2_path),
        "test": (test_images_path, test_masks1_path, test_masks2_path),
    }

    def create_ann(image_path):
        labels = []

        image_name = get_file_name(image_path)

        mask1_path = os.path.join(masks1_path, image_name + masks1_ext)
        ann_np = sly.imaging.image.read(mask1_path)[:, :, 0]
        img_height = ann_np.shape[0]
        img_wight = ann_np.shape[1]
        mask = ann_np == 255
        ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
        for i in range(1, ret):
            obj_mask = curr_mask == i
            curr_bitmap = sly.Bitmap(obj_mask)
            curr_label = sly.Label(curr_bitmap, cancer)
            labels.append(curr_label)

        for idx, masks2_ext in enumerate(masks2_exts):
            obj_class = idx_to_class[idx]
            mask2_path = os.path.join(masks2_path, image_name + masks2_ext)
            ann_np = sly.imaging.image.read(mask2_path)[:, :, 0]
            mask = ann_np == 255
            ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
            for i in range(1, ret):
                obj_mask = curr_mask == i
                curr_bitmap = sly.Bitmap(obj_mask)
                if curr_bitmap.area > 30:
                    curr_label = sly.Label(curr_bitmap, obj_class)
                    labels.append(curr_label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    cancer = sly.ObjClass("skin cancer", sly.Bitmap, color=(230, 25, 75))
    globule = sly.ObjClass("globule", sly.Bitmap, color=(60, 180, 75))
    milia_like_cyst = sly.ObjClass("milia like cyst", sly.Bitmap, color=(255, 225, 25))
    negative_network = sly.ObjClass("negative network", sly.Bitmap, color=(0, 130, 200))
    pigment_network = sly.ObjClass("pigment network", sly.Bitmap, color=(245, 130, 48))
    streaks = sly.ObjClass("streaks", sly.Bitmap, color=(145, 30, 180))

    idx_to_class = {
        0: globule,
        1: milia_like_cyst,
        2: negative_network,
        3: pigment_network,
        4: streaks,
    }

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[cancer, globule, milia_like_cyst, negative_network, pigment_network, streaks]
    )
    api.project.update_meta(project.id, meta.to_json())

    for ds_name, ds_data in ds_name_to_data.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        images_path, masks1_path, masks2_path = ds_data

        images_names = [
            im_name for im_name in os.listdir(images_path) if get_file_ext(im_name) == images_ext
        ]

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for img_names_batch in sly.batched(images_names, batch_size=batch_size):
            images_pathes_batch = [
                os.path.join(images_path, image_path) for image_path in img_names_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns_batch = [create_ann(image_path) for image_path in images_pathes_batch]
            api.annotation.upload_anns(img_ids, anns_batch)

            progress.iters_done_report(len(img_names_batch))

    return project
