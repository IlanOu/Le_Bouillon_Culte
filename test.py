from src.objects.displayer.WebDisplayer import WebApp


object = [
    {
        "type" : "text",
        "content": "je suis un grand titre",
        "images": [],
        "style" : ["text-big", "text-red"]
    },
    {
        "type": "image",
        "content": "",
        "images": ["C5_SO_8.jpg"],
        "style": ["image-small"]
    }]


WebApp().show(object)