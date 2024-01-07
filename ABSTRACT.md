## Motivation

The authors of the **ISIC Challenge 2018** dataset emphasize that skin cancer, being the most prevalent form of cancer, poses challenges in early detection due to visual similarities with benign lesions. The challenge discussed in their workshop represents the latest iteration of the largest automated skin cancer recognition challenge within the community. Hosted by the International Skin Imaging Collaboration (ISIC), the challenge was aimed to advance methods for segmentation, clinical attribute detection, and disease classification in dermoscopic images. In collaboration with the machine learning challenge, the authors planned to execute a significant reader study focused on disease diagnosis.

## ISIC Challenge 2018 Overview

In their work the authors summarized the results of the largest skin image analysis challenge in the world, hosted by the International Skin Imaging Collaboration (ISIC), a global partnership that has organized the world’s largest public repository of dermoscopic images of skin. The dataset include over 12,500 images across 3 tasks. The key changed to evaluation criteria and study design were implemented to better reflect the complexity of clinical scenarios encountered in practice. These changes included:

1. A new segmentation metric to better account for extreme deviations from interobserver variability,
2. Implementation of balanced accuracy for classification decisions to minimize influence of prevalence and prior distributions that may not be consistent in practice
3. Inclusion of external test data from institutions excluded from representation in the training dataset, to better assess how algorithms generalize beyond the environments for which they were trained.

Note, that similar datasets are also available on the instance:

- [Skin Cancer: HAM10000](https://datasetninja.com/skin-cancer-ham10000)
- [ISIC Challenge 2017: Part 1 - Lesion Segmentation](https://datasetninja.com/isic-2017-part-1)
- [ISIC Challenge 2017: Part 3 - Disease Classification Task](https://datasetninja.com/isic-2017-part-3)

## Dataset description

The dataset was separated into 3 image analysis tasks of lesion segmentation, attribute detection, and disease classification:

<img src="https://github.com/dataset-ninja/isic-challenge-2018/assets/120389559/fc9151cb-3635-4c92-8e13-490ecb0a192d" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Example training data and ground truth from Part 1: Lesion Segmentation, Part 2: Attribution Detection, and Part 3: Disease Classification.</span>

## Lesion Segmentation

For lesion segmentation, 2,594 dermoscopic images with ground truth segmentation masks were provided for training. For validation and test sets, 100 and 1,000 images were provided, respectively, without ground truth masks. Evaluation criteria historically has been the Jaccard index, averaged over all images in the dataset. In practice, ground truth segmentation masks are influenced by inter-observer and intra-observer variability, due to variations in human annotators and variations in annotation software. An ideal evaluation would generate several ground truth segmentation masks for every image using multiple annotators and software systems. Then, for each image, predicted masks would be compared to the multiple ground truth masks to determine whether the predicted mask falls outside or within observer variability. However, this would multiply the manual labor required to generate ground truth masks, rendering such an evaluation impractical and infeasible. As an approximation to this ideal evaluation criteria, we introduced “Thresholded Jaccard”, which works similarly to standard Jaccard, with one important exception: if the Jaccard value of a particular mask falls below a threshold T, the Jaccard is set to zero. The value of the threshold T defines the point in which a segmentation is considered “incorrect”.

## Lesion Attribute Detection

For attribute detection 2,594 images with 12,970 ground truth segmentation masks for 5 attributes were provided for training. For validation and held-out test sets, 100 and 1,000 images were provided, respectively, without masks. Jaccard was used as the evaluation metric in order to facilitate possible re-use of methods developed for segmentation, and encourage greater participation. As some dermoscopic attributes may be entirely absent from certain images, the Jaccard value for such attributes is ill-defined (division by 0). To overcome this difficulty, the Jaccard was measured by computing the TP, FP, and FN for the entire dataset, rather than a single image at a time.

## Lesion Disease Classification

For disease classification 10,015 dermoscopic images with 7 ground truth classification labels were provided for training: _actinic keratoses_, _basal cell carcinoma_, _benign keratosis-like lesions_, _dermatofibroma_, _melanoma_, _melanocytic nevi_, _vascular lesions_ tags. For validation and held-out test sets, 193 and 1,512 images were provided, respectively, without ground truth. Held-out test data was further split into two partitions:

1. An “internal” partition, consisting of 1,196 images selected from data sources that were consistent with the training dataset (two institutions in Austria and Australia)
2. An “external” partition, consisting of 316 images additionally selected from data sources not reflected in the training dataset (institutions from Turkey, New
   Zealand, Sweden, and Argentina).
   Evaluation was carried out using balanced accuracy (mean recall across classes after mutually exclusive classification decision), because dataset prevalence may not be reflective of real world disease prevalence, especially with regard to overrepresentation of melanomas.

The authors were provided some supplemental information, which you may find helpful when splitting the disease classification training data for users own internal training / evaluation processes. For each image in the disease classification training set , there is a lesion identifier (the _lesion id_ tag) and a diagnosis confirm type methodology. Images with the same _lesion id_ value show the same primary lesion on a patient, though the images may be taken at different camera positions, lighting conditions, and points in time. Images with a more rigorous diagnosis confirm type methodology are typically more difficult cases for human expert clinicians to evaluate, particularly when the images ultimate diagnosis is benign. In ascending order of rigorousness as applied to cases of the present dataset, the diagnosis confirm type methodologies are _single image expert consensus_, _serial imaging showing no change_, _confocal microscopy with consensus dermoscopy_, _histopathology_.
