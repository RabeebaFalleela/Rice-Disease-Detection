
import os
import cv2
import numpy as np
import tensorflow as tf
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

# Import your corrected Form and Models
from .models import reg, getintouch, UploadedImage, UploadImage
from .forms import ImageForm 

# =================================================================
# 1. GLOBAL CONFIGURATION & MODEL LOADING
# =================================================================

# We use the path that actually worked for you previously
MODEL_PATH = "C:\\Users\\hp\\Downloads\\final_model (1).h5"

def load_rice_model():
    """Loads the model using the Download folder path."""
    try:
        # Load the model directly using legacy loader to handle nested structures
        loaded_model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        print("✅ Model loaded successfully from Downloads.")
        return loaded_model
    except Exception as e:
        print(f" Error loading model: {e}")
        return None

# Initialize the model ONCE
model = load_rice_model()

CLASS_NAMES = [
    'Bacterial Leaf Blight', 
    'Brown Spot', 
    'Healthy Rice Leaf', 
    'Leaf Blast', 
    'Leaf scald', 
    'Sheath Blight'
]

# =================================================================
# 2. GRAD-CAM EXPLAINABILITY ENGINE
# =================================================================

def get_gradcam(img_array, model, last_conv_layer_name, pred_index=None):
    """Generates the Grad-CAM heatmap array."""
    try:
        # Handle nested EfficientNet structure
        target_model = model
        if 'efficientnetb3' in [l.name for l in model.layers]:
            target_model = model.get_layer('efficientnetb3')
            
        grad_model = tf.keras.models.Model(
            [target_model.inputs], [target_model.get_layer(last_conv_layer_name).output, target_model.output]
        )
    except:
        grad_model = tf.keras.models.Model(
            [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
        )

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
    return heatmap.numpy()

# =================================================================
# 3. CORE PROCESSING VIEW
# =================================================================

def process_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if model loaded correctly
            if model is None:
                return render(request, 'input.html', {'form': form, 'error': 'Model not loaded.'})

            # 1. Save and Preprocess
            image_file = form.cleaned_data['image']
            img_instance = UploadedImage.objects.create(image=image_file)
            img_path = img_instance.image.path

            img = cv2.imread(img_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_resized = cv2.resize(img_rgb, (300, 300)) 
            img_array = np.expand_dims(img_resized, axis=0)
            img_ready = tf.keras.applications.efficientnet.preprocess_input(img_array)

            # 2. Prediction
            preds = model.predict(img_ready)
            pred_index = np.argmax(preds[0])
            predicted_class = CLASS_NAMES[pred_index]

            # 3. Grad-CAM
            try:
                heatmap = get_gradcam(img_ready, model, 'top_activation', pred_index)
                heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
                heatmap = np.uint8(255 * heatmap)
                heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
                superimposed_img = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)
                
                heatmap_filename = f"heatmap_{img_instance.id}.jpg"
                heatmap_dir = os.path.join(settings.MEDIA_ROOT, 'uploaded_images')
                if not os.path.exists(heatmap_dir): os.makedirs(heatmap_dir)
                
                heatmap_path = os.path.join(heatmap_dir, heatmap_filename)
                cv2.imwrite(heatmap_path, superimposed_img)
                heatmap_url = f"{settings.MEDIA_URL}uploaded_images/{heatmap_filename}"
            except Exception as e:
                print(f"Grad-CAM Error: {e}")
                heatmap_url = None

            return render(request, 'op.html', {
                'detected_diseases': predicted_class,
                'uploaded_image': img_instance,
                'heatmap_image': heatmap_url,
            })
    else:
        form = ImageForm()
    return render(request, 'input.html', {'form': form})





# =================================================================
# 4. USER & ADMIN MANAGEMENT (CLEANED)
# =================================================================

def index(request): return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name'); email = request.POST.get('email')
        password = request.POST.get('password'); farmer = request.POST.get('farmer')

        if reg.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error_message1': 'Email already exists.'})
        try:
            validate_password(password, reg)
            reg(name=name, password=password, email=email, farmer=farmer).save()
            return render(request, 'login.html')
        except ValidationError as e:
            return render(request, 'register.html', {'error_message': e})
    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        name = request.POST.get('name'); password = request.POST.get('password')
        user = reg.objects.filter(name=name, password=password).first()
        if user:
            request.session['name'] = user.name
            return redirect('home')
        return render(request, 'login.html', {'error_message': "Invalid credentials."})
    return render(request, 'login.html')

def profile(request):
    name = request.session.get('name')
    user = reg.objects.filter(name=name).first()
    return render(request, 'profile.html', {'user': user} if user else {})

def feedback(request):
    if request.method == "POST":
        getintouch(
            name=request.POST.get('name'), phone=request.POST.get('phone'),
            email=request.POST.get('email'), message=request.POST.get('message'),
            service=request.POST.get('service')
        ).save()
        return redirect('home')
    return render(request, 'feedback.html')

def adlog(request):
    if request.method == 'POST':
        if request.POST.get('username') == 'admin' and request.POST.get('password') == 'admin':
            return render(request, 'adhome.html')
    return render(request, "admin.html")

def contact(request): return render(request, 'contact.html')
def service(request): return render(request, 'service.html')
def team(request): return render(request, 'team.html')


def updateprofile(request):
    name=request.session['name']
    print('name is',name)
    cr=reg.objects.get(name=name)
    if cr:
        user_info={
            'name':cr.name,
            'email':cr.email,
            'password':cr.password,
            'farmer':cr.farmer,
            }
        return render(request,"updateprofile.html",user_info)
    else:
        return render(request,"updateprofile.html")
    
def pro_update(request):
    name=request.session['name']
    if request.method=='POST':
        name=request.POST.get('nametxt') 
        email=request.POST.get('emailtxt')
        password=request.POST.get('passwordtxt')
        farmer=request.POST.get('farmertxt')
        data=reg.objects.get(name=name)
        data.name=name
        data.email=email
        data.password=password
        data.farmer=farmer
        data.save()
        return redirect('profile')
    else:
        return render(request,"updateprofile.html")



def adhome(request):
    return render (request,"adhome.html")

def feedback(request):
    if request.method=="POST":
        name=request.POST.get('name')
        phone=request.POST.get('phone') 
        email=request.POST.get('email')
        message=request.POST.get('message')
        service=request.POST.get('service')
        getintouch(name=name,phone=phone,email=email,message=message,service=service).save()
        return render(request,'home.html')
    else:

        return render(request,'feedback.html')
    
def home(request):
    if request.method == 'POST':
        image=request.FILES.get('image')
        UploadImage(image=image).save()
        return redirect(home)
    return render (request,'home.html')

def logout(request):
    return render (request,'index.html')

def contact(request):
    return render (request,'contact.html')

def user(request):
    a=reg.objects.all()
    return render(request,'aduser.html',{'a':a})
def userremove(request,id):
    a=reg.objects.get(id=id)
    a.delete()
    return render (request,'adhome.html')


def adfeedback(request):
    a=getintouch.objects.all()
    return render(request,'adfeedback.html',{'a':a})

def feedremove(request,id):
    a=getintouch.objects.get(id=id)
    a.delete()
    return render (request,'adhome.html')

