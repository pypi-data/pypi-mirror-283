import cv2
import numpy as np
from moviepy.editor import ImageSequenceClip

# 얼굴 합성 함수
def blend_faces(img1, img2, alpha=0.5):
    return cv2.addWeighted(img1, alpha, img2, 1 - alpha, 0)

# 이미지 로드 및 전처리
def load_and_preprocess_image(file_path, size=(256, 256)):
    img = cv2.imread(file_path)
    img = cv2.resize(img, size)
    return img

# 이미지 파일 리스트
image_files = ['face1.jpg', 'face2.jpg', 'face3.jpg', ..., 'face20.jpg']

# 합성된 이미지 시퀀스 생성
images = []
for i in range(len(image_files) - 1):
    img1 = load_and_preprocess_image(image_files[i])
    img2 = load_and_preprocess_image(image_files[i + 1])
    for alpha in np.linspace(0, 1, 20):  # 20단계로 변환
        blended_image = blend_faces(img1, img2, alpha)
        images.append(blended_image)

# 슬라이드쇼 비디오 생성
clip = ImageSequenceClip([cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in images], fps=10)
clip.write_videofile("face_morphing_slideshow.mp4", codec='libx264')
