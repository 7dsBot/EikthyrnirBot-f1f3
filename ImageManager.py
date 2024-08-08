import numpy as np

from PIL import Image

class ImageManager:
    def __init__(self):
        pass

    def get_image_from_path(self, path):
        if not path:
            raise Exception(f"Le chemin de l'image {path} est invalide.")

        return Image.open(path)

    def get_similarity_percentage(self, img1_path, img2_path, threshold=30):
        # Charger les images
        img1 = self.get_image_from_path(img1_path)
        img2 = self.get_image_from_path(img2_path)

        # Vérifier si les tailles des images sont différentes
        if img1.size != img2.size:
            return 0

        # Convertir les images en tableaux numpy pour une comparaison efficace
        np_img1 = np.array(img1)
        np_img2 = np.array(img2)

        # Calculer la différence absolue entre les deux images
        diff = np.abs(np_img1 - np_img2)

        # Compter les bons pixels (ceux dont la différence est inférieure ou égale au seuil)
        good_pixels = np.sum(diff <= threshold)

        # Calculer le pourcentage de pixels identiques
        total_pixels = np_img1.size
        percentage = good_pixels / total_pixels

        return percentage