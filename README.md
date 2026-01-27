# Rice Leaf Disease Detection 

A deep learning-powered web application designed to help farmers and researchers identify rice plant diseases from leaf images. The system uses a fine-tuned **EfficientNetB3** architecture and provides visual justifications for its predictions using **Grad-CAM** heatmaps.



##  Key Features
* **Disease Identification:** Detects 6 common rice diseases (Bacterial Leaf Blight, Brown Spot, Healthy, Leaf Blast, Leaf Scald, and Sheath Blight).
* **Explainable AI (XAI):** Generates a Grad-CAM heatmap to highlight the specific regions of the leaf that led to the AI's diagnosis.
* **User Management:** Secure registration and login system for farmers to track their diagnostic history.
* **Responsive UI:** A clean, modern dashboard built with Django templates and CSS.

##  Tech Stack
* **Backend:** Django (Python)
* **Deep Learning:** TensorFlow / Keras
* **Computer Vision:** OpenCV (for image processing and heatmap overlay)
* **Frontend:** HTML5, CSS3, JavaScript

##  Installation & Setup

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd riceplantproject
2. Install dependencies
Bash
pip install -r requirements.txt
3. Download the Model
Due to file size limits, the trained model (final_model.h5) is not included in this repository.

Download the model from: https://drive.google.com/file/d/1p88MIq4b7-rYAUdYaWSPHuNq90phe6MY/view?usp=drive_link


4. Database Setup
Bash
python manage.py makemigrations
python manage.py migrate
5. Run the Server
Bash
python manage.py runserver
Access the app at http://127.0.0.1:8000/

How It Works
Input: User uploads a photo of a rice leaf.

Processing: The image is resized to 300x300 and normalized for EfficientNetB3.

Inference: The model predicts the disease class.

Heatmap: The get_gradcam function looks at the gradients of the last convolutional layer (top_activation) to see where the model "looked."

Result: The user sees the diagnosis and a side-by-side comparison of the original leaf and the heatmap.

##  Visualization & Results

The following diagnostic reports demonstrate the model's ability to localize the infected areas using **Grad-CAM** (Gradient-weighted Class Activation Mapping).

### 1. Brown Spot Detection
The heatmap focuses on the small, circular necrotic lesions spread across the leaf surface.
![image alt]([riceplantproject%20(2)/riceplantproject/riceplantproject/Screenshots/brown_spot.png](https://github.com/RabeebaFalleela/Rice-Disease-Detection/blob/b96a7d474627d1891f7a91940eea2308517c8679/riceplantproject%20(2)/riceplantproject/riceplantproject/Screenshots/brown_spot.png))

### 2. Leaf Scald Detection
The model successfully identifies the characteristic large, banded lesions at the leaf tips.
![Leaf Scald Diagnosis](riceplantproject%20(2)/riceplantproject/riceplantproject/Screenshots/leaf_scald.png)

### 3. Sheath Blight Detection
Activation is concentrated on the irregular "snake-skin" patterns found on the rice plant.
![Sheath Blight Diagnosis](riceplantproject%20(2)/riceplantproject/riceplantproject/Screenshots/sheath_blight.png)
