from src.objects.displayer.WebDisplayer import WebApp


object = [
    {
        "type" : "text",
        "content": "je suis un grand titre",
        "style" : ["grosTitre", "Rouge"]
    },
    {
        "type": "image",
        "content": "url/de/limage.png",
        "style": ["centré", "grosse image"]
    }]


WebApp().show(object)