import torch
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
import config
from icecream import ic


def predict_on_test_set(
    testing_folder_path, transform, backbone, memory_bank, best_threshold
):
    """Predict on the test set and display results

    :param testing_folder_path: The directory containing subfolders 'good' and 'defect'
    :param transform: The image transformation pipeline
    :param backbone: The feature extraction model
    :param memory_bank: The memory bank for feature matching
    :param best_threshold: The threshold for anomaly detection
    """

    backbone.eval()

    for defect_type in ["good", "defect"]:
        current_folder = testing_folder_path / defect_type
        print(f"Processing folder: {current_folder}")

        # iterate over each image in the current folder
        for path in current_folder.iterdir():
            if path.suffix.endswith(".jpg"):
                ic(path.name)

                # start making predictions
                test_image = transform(Image.open(path)).to(config.DEVICE).unsqueeze(0)

                with torch.no_grad():
                    features = backbone(test_image)

                distances = torch.cdist(features, memory_bank, p=2.0)

                dist_score, dist_score_idxs = torch.min(distances, dim=1)
                s_star = torch.max(dist_score)
                segm_map = dist_score.view(1, 1, 28, 28)

                segm_map = (
                    torch.nn.functional.interpolate(
                        segm_map, size=(224, 224), mode="bilinear"
                    )
                    .cpu()
                    .squeeze()
                    .numpy()
                )

                y_score_image = s_star.cpu().numpy()

                y_pred_image = 1 * (y_score_image >= best_threshold)
                class_label = ["OK", "NOK"]

                plt.figure(figsize=(15, 5))
                plt.subplot(1, 3, 1)
                plt.imshow(test_image.squeeze().permute(1, 2, 0).cpu().numpy())
                plt.title(f"Result: {defect_type}")

                plt.subplot(1, 3, 2)
                heat_map = segm_map
                plt.imshow(
                    heat_map, cmap="jet", vmin=best_threshold, vmax=best_threshold * 2
                )
                plt.title(
                    f"Anomaly score: {y_score_image / best_threshold:0.4f} || {class_label[y_pred_image]}"
                )

                plt.subplot(1, 3, 3)
                plt.imshow((heat_map > best_threshold * 1.25), cmap="gray")
                plt.title("Segmentation map")

                plt.show()

    backbone.train()
