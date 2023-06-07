import logging

def prepField(name, field):
    if type(field) is str:
        field = {"_type": field}

    if field.get('_type') == "dict":
        field = prepType(name, field)

    return {**{"_name": name, "_type": "string" }, **field}

def prepDict(name, dict):
    return prepType(name, dict)

def prepType(name, type):
    fields = {k:prepField(k, v) for (k,v) in type.items() if not k.startswith('_')}
    return  {**type, **{"_name": name, "_fields": [v for v in fields.values()] }, **fields}
    
def prepModel(model):
    model = {k:prepType(k, v) for (k,v) in model.items()}
    return model

def build(src_path):
    from yaml import safe_load
    with open('src/model.yml', 'r') as file:
        logging.info(f'🌳 Loading Data Model src/model.yml')
        
        model = prepModel(safe_load(file))

    # Todo: If the model is changed rebuild everything.
    if src_path == "./src/model.yml":
        import pprintpp
        pprintpp.pprint(model)

    if src_path.endswith(".mustache"):
    
        logging.info(f'📄 Loading template {src_path} type ({src_path[:-10]})')
    
        from chevron import render
        with open(src_path, 'r') as src_file:
            
            dst_path = f'./dst/{src_path[6:-9]}'

            with open(dst_path, 'w+') as dest_file:
                logging.info(f'🖊️ Saving to 📄 {dst_path}')
                dest_file.write(render(src_file, model))

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(message)s'
        )

    import sys
    src_path = sys.argv[1] if len(sys.argv) > 1 else './src/test.txt.mustache'

    from time import time
    logging.info(f'🔨Build started 📄 {src_path}')
    start = time()
    build(src_path)
    logging.info("⏱️ Build complete! ({})".format(round(time() - start, 2)))
    
