import sys,os

if __name__ == "__main__":
    #因为你的脚本不算是django的一部分，所以需要导入django的环境变量，详见django的manage
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ironfort.settings")
    import django
    django.setup()
    #以上可以使用django的所有东西，包括数据库

    from backend import main
    interactive_obj = main.ArgvHandler(sys.argv)
    interactive_obj.call()

