from django.shortcuts import render,redirect
import datetime
from foodlog.models import day_record,food_pic,box,health_element
from user.models import user_info
from django.utils import timezone
from foodlog.ai import *
import numpy as np
# Create your views here.


global det_net,det_meta,clf_model,class_dict
det_net,det_meta,clf_model,class_dict = init_models(basic_path)

# media_path = "/Users/apple/Documents/code/website/sift/"
media_path = "/home/qingpeng/website/sift/"
result_path = "./media/result/"
if not os.path.exists(result_path):
    os.mkdir(result_path)


def analyze_pic(new_pic,data_path):
    print("\n [*]Starting \n")

    r = darknet.detect(det_net, det_meta, str.encode(media_path + data_path))
    img = Image.open(media_path + data_path)

    boxes = []
    for id,boxx in enumerate(r):
        prob_is_food = boxx[1]
        x,y,w,h = boxx[2][0],boxx[2][1],boxx[2][2],boxx[2][3]
        cropped = img.crop((x-w/2,y-h/2,x+w/2,y+h/2))  # (left, upper, right, lower)
        prediction = predict(clf_model, cropped)
        class_id = np.argsort(prediction[0])[::-1][0]
        prob_which_food = prediction[0][class_id]
        str_class = str(class_dict[class_id])
        draw_box(img, boxx,"box%d"%(id+1),prob_which_food)
        box_he = health_element(
            Carbohydrates = np.random.rand()*40,
            Proteins = np.random.rand()*30,
            Fats = np.random.rand()*20,
            Minerals = np.random.rand()*10,
        )
        box_he.save()
        new_box = box(
            pic_id=new_pic,
            index_in_pic=id,
            he_id=box_he,
            left=float(x-w/2),
            upper=float(y-h/2),
            right=float(x+w/2),
            down=float(y+h/2),
            prob=prob_which_food,
            food_class=str_class
        )
        new_box.save()

        pic_he = new_pic.he_id
        pic_he.Carbohydrates += box_he.Carbohydrates
        pic_he.Proteins += box_he.Proteins
        pic_he.Fats += box_he.Fats
        pic_he.Minerals += box_he.Minerals
        pic_he.save()

        boxx_dic = {}
        boxx_dic['index'] = id
        boxx_dic['class'] = str_class
        boxx_dic['Carbohydrates'] = box_he.Carbohydrates
        boxx_dic['Proteins'] = box_he.Proteins
        boxx_dic['Fats'] = box_he.Fats
        boxx_dic['Minerals'] = box_he.Minerals
        boxes.append(boxx_dic)
    img.save(result_path+data_path[12:])
    return boxes

def draw_box(img, boxx,str_class,prob):
    draw = ImageDraw.Draw(img)
    x, y, w, h = boxx[2][0], boxx[2][1], boxx[2][2], boxx[2][3]
    x = x - w / 2
    y = y - h / 2
    line = 5
    for i in range(1, line + 1):
        draw.rectangle((x + (line - i), y + (line - i), x + w + i, y + h + i), outline='red')
    font = ImageFont.truetype(media_path + '/Times New Roman.ttf', 24)
    draw.text((x, y), "%s: %.2f"%(str_class,prob), font=font,fill="black")
    return img

def generate_random_id():
    time = datetime.datetime.now()
    id = time.strftime("%Y%m%d%H%M%S")
    return id

def index(request):
    is_login = request.session.get('is_login')
    if not is_login:
        return redirect('/login')

    context = {}
    username = request.session['user']
    context['name'] = username
    cur_user = user_info.objects.get(username=username)
    today = datetime.date.today()

    select_date = request.GET.get('date',default=today)

    context['Carbohydrates'] = 0
    context['Proteins'] = 0
    context['Fats'] = 0
    context['Minerals'] = 0

    dr = day_record.objects.filter(user_id=cur_user, date=select_date)
    if dr.exists():
        today_report = dr[0]
        today_food = food_pic.objects.filter(user_id=cur_user,day_record_id=today_report).order_by('upload_time')
        if today_food.exists():
            context['food_list'] = []
            for index,food in enumerate(today_food):
                food_dict = {}
                sub_food = box.objects.filter(pic_id=food).order_by('index_in_pic')
                food_dict['name'] = ""
                food_dict['index'] = food.pic_id
                if sub_food.exists():
                    for sub in sub_food:
                        food_dict['name'] += " %s," %(sub.food_class)
                food_dict['upload_time'] = food.upload_time.strftime("%H:%M, %p")
                food_dict['img_url'] = food.img.url
                context['food_list'].append(food_dict)

            context['Carbohydrates'] = dr[0].he_id.Carbohydrates
            context['Proteins'] = dr[0].he_id.Proteins
            context['Fats'] = dr[0].he_id.Fats
            context['Minerals'] = dr[0].he_id.Minerals

    print(context)

    return render(request, 'index.html', context)

def scan(request):
    is_login = request.session.get('is_login')
    if not is_login:
        return redirect('/login')

    username = request.session['user']
    cur_user = user_info.objects.get(username=username)
    today = datetime.date.today()

    context = {}
    context["name"] = username
    if request.method == 'POST':
        dr = day_record.objects.filter(user_id=cur_user,date=today)
        if not dr.exists():
            new_day_he = health_element()
            new_day_he.save()
            new_day_record = day_record(
                user_id=cur_user,
                he_id=new_day_he,
                date=today,
            )
            new_day_record.save()
            today_record = new_day_record
        else:
            today_record = dr[0]

        new_day_he = health_element()
        new_day_he.save()
        new_pic = food_pic(
            user_id = cur_user,
            he_id=new_day_he,
            day_record_id = today_record,
            img=request.FILES.get('img'),
            upload_time = timezone.now()
        )
        new_pic.save()
        context['boxes'] = analyze_pic(new_pic, new_pic.img.url)
        # img = Image.open(media_path + new_pic.img.url)
        # img.save(result_path + new_pic.img.url[12:])

        today_he = today_record.he_id
        today_he.Carbohydrates += new_pic.he_id.Carbohydrates
        today_he.Proteins += new_pic.he_id.Proteins
        today_he.Fats += new_pic.he_id.Fats
        today_he.Minerals += new_pic.he_id.Minerals
        today_he.save()

        context['img_url'] = new_pic.img.url
        context['result_url'] = result_path[1:] + new_pic.img.url[12:]

        return render(request, 'single-report.html', context)

    return render(request, 'scan-food.html', context)

def single_report(request):
    is_login = request.session.get('is_login')
    if not is_login:
        return redirect('/login')

    username = request.session['user']
    context = {}
    context["name"] = username
    # context['result_url'] = result_path[1:] + "/20200222194812_24.jpeg"
    # context['boxes'] = [
    #     {'index': 1, 'class': 'bread1', 'Carbohydrates': 50, 'Proteins': 40, 'Fats': 30, 'Minerals': 20},
    #     {'index': 2, 'class': 'bread2', 'Carbohydrates': 50, 'Proteins': 40, 'Fats': 30, 'Minerals': 20},
    #     {'index': 3, 'class': 'bread3', 'Carbohydrates': 50, 'Proteins': 40, 'Fats': 30, 'Minerals': 20}
    #
    # ]
    # print(request.GET['index'])
    food = food_pic.objects.get(pic_id=request.GET['index'])
    context['img_url'] = food.img.url
    context['result_url'] = result_path[1:] + food.img.url[12:]
    boxes = box.objects.filter(pic_id=food)
    if boxes.exists():
        context['boxes'] = []
        for boxx in boxes:
            context['boxes'].append({
                'index':boxx.index_in_pic+1,
                'class':boxx.food_class,
                'Carbohydrates':boxx.he_id.Carbohydrates,
                'Proteins': boxx.he_id.Proteins,
                'Fats': boxx.he_id.Fats,
                'Minerals': boxx.he_id.Minerals,
            })

    return render(request, 'single-report.html', context)

def yesterday_report(request):
    is_login = request.session.get('is_login')
    if not is_login:
        return redirect('/login')

    context = {}
    username = request.session['user']
    context['name'] = username
    cur_user = user_info.objects.get(username=username)
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    return redirect('/index/?date=%s'%(yesterday))

def get_current_week():
    monday, sunday = datetime.date.today(),datetime.date.today()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day
    return monday, sunday


def week_report(request):
    is_login = request.session.get('is_login')
    if not is_login:
        return redirect('/login')

    context = {}
    username = request.session['user']
    context['name'] = username
    cur_user = user_info.objects.get(username=username)
    today = datetime.date.today()
    start,end = get_current_week()
    # print(start,end)
    context['start'] = start
    context['end'] = end

    context['nutrition_by_day'] = [[0,0,0,0] for i in range(7)]
    days_report = day_record.objects.filter(date__range=(start, end)).order_by('date')
    if days_report.exists():
        for day in days_report:
            print(day.date)
            offset_day = int((day.date - start)/datetime.timedelta(days=1))
            context['nutrition_by_day'][offset_day][0] = day.he_id.Carbohydrates
            context['nutrition_by_day'][offset_day][1] = day.he_id.Proteins
            context['nutrition_by_day'][offset_day][2] = day.he_id.Fats
            context['nutrition_by_day'][offset_day][3] = day.he_id.Minerals

    nutritions = [0,0,0,0]
    for i in range(7):
        for j in range(4):
            nutritions[j] += context['nutrition_by_day'][i][j]


    context['nutrition_percent'] = [0,0,0,0]
    for i in range(4):
        context['nutrition_percent'][i] = float(nutritions[i]/sum(nutritions))

    return render(request, 'weekly-report.html', context)


def year_report(request):
    is_login = request.session.get('is_login')
    if not is_login:
        return redirect('/login')

    context = {}
    username = request.session['user']
    context['name'] = username
    cur_user = user_info.objects.get(username=username)
    today = datetime.date.today()

    context['year'] = today.year

    return render(request, 'yearly-report.html', context)