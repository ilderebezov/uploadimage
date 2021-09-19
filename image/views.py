from django.shortcuts import render, redirect
from .form import ImageForm
from .models import Image
from PIL import Image as Im
from PIL import ImageColor as ImCo

# Create your views here.


def index(request):
    res = 'None'
    if request.method == "POST":
        form = ImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            obj = form.instance
            image = Im.open(form.files['image'])
            black = (0, 0, 0)
            white = (255, 255, 255)
            num_black = num_white = hex_code_num = 0
            hex_code = request.POST['HEX_code']
            #hex_code = '#000000'
            hex_to_rgb = ImCo.getcolor(hex_code, "RGB")
            for i in range(image.size[0]):
                for j in range(image.size[1]):
                    pixel = image.getpixel((i, j))
                    if pixel == white:
                        num_white += 1
                    elif pixel == black:
                        num_black += 1
                    if pixel == hex_to_rgb:
                        hex_code_num += 1
            if num_black > num_white:
                res = 'black'
            else:
                res = 'white'
            return render(request, "index.html", {"obj": obj, "result": res, "hex_code": hex_code,
                            "hex_code_num": hex_code_num})
    else:
        form = ImageForm()
        img = Image.objects.all()
    return render(request, "index.html", {"img": img, "form": form, "result": res})
