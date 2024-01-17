from clarifai.client.model import Model

def process_script(script):
    inference_params = dict(width=1024, height=1024, steps=50, cfg_scale=8.0)
    model = Model("https://clarifai.com/stability-ai/stable-diffusion-2/models/stable-diffusion-xl")

    print("Starting script processing...")
    
    model_prediction = model.predict_by_bytes(script.encode(), input_type="text", inference_params=inference_params)
    output_base64 = model_prediction.outputs[0].data.image.base64

    print("Script processing is completed !")
    return output_base64