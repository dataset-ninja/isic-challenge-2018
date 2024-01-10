import csv
import os
import shutil
from urllib.parse import unquote, urlparse

import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import (
    file_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
)
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

    train3_images_path = "/home/alex/DATASETS/TODO/ISIC Challenge3/ISIC2018_Task3_Training_Input"
    train3_anns_path = "/home/alex/DATASETS/TODO/ISIC Challenge3/ISIC2018_Task3_Training_GroundTruth/ISIC2018_Task3_Training_GroundTruth.csv"
    val3_images_path = "/home/alex/DATASETS/TODO/ISIC Challenge3/ISIC2018_Task3_Validation_Input"
    val3_anns_path = "/home/alex/DATASETS/TODO/ISIC Challenge3/ISIC2018_Task3_Validation_GroundTruth/ISIC2018_Task3_Validation_GroundTruth.csv"
    test3_images_path = "/home/alex/DATASETS/TODO/ISIC Challenge3/ISIC2018_Task3_Test_Input"
    test3_anns_path = "/home/alex/DATASETS/TODO/ISIC Challenge3/ISIC2018_Task3_Test_GroundTruth/ISIC2018_Task3_Test_GroundTruth.csv"

    train3_diagnosis_path = (
        "/home/alex/DATASETS/TODO/ISIC Challenge3/ISIC2018_Task3_Training_LesionGroupings.csv"
    )

    ds_name_to_data = {
        "val": (
            val_images_path,
            val_masks1_path,
            val_masks2_path,
            val3_images_path,
            val3_anns_path,
        ),
        "train": (
            train_images_path,
            train_masks1_path,
            train_masks2_path,
            train3_images_path,
            train3_anns_path,
        ),
        "test": (
            test_images_path,
            test_masks1_path,
            test_masks2_path,
            test3_images_path,
            test3_anns_path,
        ),
    }

    def create_ann(image_path):
        labels = []
        tags = []

        image_name = get_file_name(image_path)

        if get_file_name_with_ext(image_path) in images3_names:
            task3 = sly.Tag(task3_meta)
            tags.append(task3)

        if ds_name == "train":
            diagnos_data = im3_train_name_to_diagnos.get(image_name)
            if diagnos_data is not None:
                lesion_id_value = diagnos_data[0]
                lesion_id = sly.Tag(lesion_id_meta, value=lesion_id_value)
                tags.append(lesion_id)
                diagnosis_name = diagnos_data[1]
                diagnosis_meta = meta.get_tag_meta(diagnosis_name)
                if diagnosis_meta is not None:
                    diagnosis = sly.Tag(diagnosis_meta)
                    tags.append(diagnosis)

        tag_index = im3_name_to_ann.get(image_name)
        if tag_index is not None:
            tag_meta = name_to_tag_meta[tag_index]
            tag = sly.Tag(tag_meta)
            tags.append(tag)

        mask1_path = os.path.join(masks1_path, image_name + masks1_ext)
        if file_exists(mask1_path):
            task1 = sly.Tag(task1_meta)
            tags.append(task1)
            task = sly.Tag(task_meta, value=1)
            ann_np = sly.imaging.image.read(mask1_path)[:, :, 0]
            img_height = ann_np.shape[0]
            img_wight = ann_np.shape[1]
            mask = ann_np == 255
            ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
            for i in range(1, ret):
                obj_mask = curr_mask == i
                curr_bitmap = sly.Bitmap(obj_mask)
                curr_label = sly.Label(curr_bitmap, cancer, tags=[task])
                labels.append(curr_label)

            task2 = sly.Tag(task2_meta)
            tags.append(task2)
            for idx, masks2_ext in enumerate(masks2_exts):
                task = sly.Tag(task_meta, value=2)
                obj_class = idx_to_class[idx]
                mask2_path = os.path.join(masks2_path, image_name + masks2_ext)
                ann_np = sly.imaging.image.read(mask2_path)[:, :, 0]
                mask = ann_np == 255
                ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
                for i in range(1, ret):
                    obj_mask = curr_mask == i
                    curr_bitmap = sly.Bitmap(obj_mask)
                    if curr_bitmap.area > 30:
                        curr_label = sly.Label(curr_bitmap, obj_class, tags=[task])
                        labels.append(curr_label)

        else:
            ann_np = sly.imaging.image.read(image_path)[:, :, 0]
            img_height = ann_np.shape[0]
            img_wight = ann_np.shape[1]

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    cancer = sly.ObjClass("skin cancer", sly.Bitmap, color=(230, 25, 75))
    globule = sly.ObjClass("globule", sly.Bitmap, color=(60, 180, 75))
    milia_like_cyst = sly.ObjClass("milia like cyst", sly.Bitmap, color=(255, 225, 25))
    negative_network = sly.ObjClass("negative network", sly.Bitmap, color=(0, 130, 200))
    pigment_network = sly.ObjClass("pigment network", sly.Bitmap, color=(245, 130, 48))
    streaks = sly.ObjClass("streaks", sly.Bitmap, color=(145, 30, 180))

    task1_meta = sly.TagMeta("task 1: lesion segmentation", sly.TagValueType.NONE)
    task2_meta = sly.TagMeta("task 2: attribution detection", sly.TagValueType.NONE)
    task3_meta = sly.TagMeta("task 3: disease classification", sly.TagValueType.NONE)
    task_meta = sly.TagMeta("task", sly.TagValueType.ANY_NUMBER)

    serial_meta = sly.TagMeta("serial imaging showing no change", sly.TagValueType.NONE)
    histopathology_meta = sly.TagMeta("histopathology", sly.TagValueType.NONE)
    single_meta = sly.TagMeta("single image expert consensus", sly.TagValueType.NONE)
    confocal_meta = sly.TagMeta(
        "confocal microscopy with consensus dermoscopy", sly.TagValueType.NONE
    )
    lesion_id_meta = sly.TagMeta("lesion id", sly.TagValueType.ANY_STRING)

    actinic = sly.TagMeta("actinic keratoses", sly.TagValueType.NONE)
    basal = sly.TagMeta("basal cell carcinoma", sly.TagValueType.NONE)
    benign = sly.TagMeta("benign keratosis-like lesions", sly.TagValueType.NONE)
    dermatofibroma = sly.TagMeta("dermatofibroma", sly.TagValueType.NONE)
    melanoma = sly.TagMeta("melanoma", sly.TagValueType.NONE)
    melanocytic = sly.TagMeta("melanocytic nevi", sly.TagValueType.NONE)
    vascular = sly.TagMeta("vascular lesions", sly.TagValueType.NONE)

    name_to_tag_meta = {
        "AKIEC": actinic,
        "BCC": basal,
        "BKL": benign,
        "DF": dermatofibroma,
        "MEL": melanoma,
        "NV": melanocytic,
        "VASC": vascular,
    }

    idx_to_class = {
        0: globule,
        1: milia_like_cyst,
        2: negative_network,
        3: pigment_network,
        4: streaks,
    }

    index_to_tag_name = {1: "MEL", 2: "NV", 3: "BCC", 4: "AKIEC", 5: "BKL", 6: "DF", 7: "VASC"}

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[
            cancer,
            globule,
            milia_like_cyst,
            negative_network,
            pigment_network,
            streaks,
        ],
        tag_metas=[
            task1_meta,
            task2_meta,
            task3_meta,
            serial_meta,
            histopathology_meta,
            single_meta,
            confocal_meta,
            actinic,
            basal,
            benign,
            dermatofibroma,
            melanoma,
            melanocytic,
            vascular,
            lesion_id_meta,
            task_meta,
        ],
    )
    api.project.update_meta(project.id, meta.to_json())

    im3_train_name_to_diagnos = {}

    with open(train3_diagnosis_path, "r") as file:
        csvreader = csv.reader(file)
        for idx, row in enumerate(csvreader):
            if idx == 0:
                continue
            im3_train_name_to_diagnos[row[0]] = row[1:]

    for ds_name, ds_data in ds_name_to_data.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        images_path, masks1_path, masks2_path, images3_path, anns3_path = ds_data

        im3_name_to_ann = {}

        with open(anns3_path, "r") as file:
            csvreader = csv.reader(file)
            for idx, row in enumerate(csvreader):
                if idx == 0:
                    continue
                class_index = row.index("1.0")
                im3_name_to_ann[row[0]] = index_to_tag_name[class_index]

        images_names1_2 = [
            im_name for im_name in os.listdir(images_path) if get_file_ext(im_name) == images_ext
        ]

        images3_names = [
            im_name for im_name in os.listdir(images3_path) if get_file_ext(im_name) == images_ext
        ]

        images_names = list(set(images_names1_2 + images3_names))

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for img_names_batch in sly.batched(images_names, batch_size=batch_size):
            images_pathes_batch = []
            for image_name in img_names_batch:
                im_path = os.path.join(images_path, image_name)
                if file_exists(im_path):
                    images_pathes_batch.append(im_path)
                else:
                    im_path = os.path.join(images3_path, image_name)
                    images_pathes_batch.append(im_path)

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns_batch = [create_ann(image_path) for image_path in images_pathes_batch]
            api.annotation.upload_anns(img_ids, anns_batch)

            progress.iters_done_report(len(img_names_batch))

    return project
