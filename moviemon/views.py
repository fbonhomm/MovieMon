from django.shortcuts import render

# Create your views here.
def TitleScreen(request):
    context = {
            'button': {
                'a': '/WorldMap',
                'b': '/load'
            },
            'event': {
                'film': 'test'
            }
    }
    return render(request, 'TitleScreen.html', context)

def WorldMap(request):
    pos_x = int(request.GET.get('x')) if request.GET.get('x') else 0
    pos_y = int(request.GET.get('y')) if request.GET.get('y') else 0


    up = '/WorldMap?x=%s&y=%s' % (str(pos_x), str(pos_y - 1))

    down ='/WorldMap?x=%s&y=%s' % (str(pos_x), str(pos_y + 1))
    left ='/WorldMap?x=%s&y=%s' % (str(pos_x - 1), str(pos_y))
    right = '/WorldMap?x=%s&y=%s' % (str(pos_x + 1), str(pos_y))

    # get move possibility
    context = {
        'button': {
            'up': up,
            'down': down,
            'left': left,
            'right': right
        },
        'grid': {
            'x': range(0,9),
            'y': range(0,9)
        },
        'player': (pos_y, pos_x)
    }
    print(context)
    return render(request, 'WorldMap.html', context)
