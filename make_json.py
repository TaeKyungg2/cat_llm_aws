emotion=["sad","runaway","cute","angry"]
def imageid_and_json(context):
    context=context.split('%')
    json={}
    if len(context)>1 and context[1] in emotion:
        json["image_id"]=context[1]+".gif"
    else:
        json["image_id"]="cat.gif"
    json["answer"]=context[0]
    return json
