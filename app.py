import argparse
import gradio as gr

from src.model_predictor import ModelPredictor

class GradioApp:
    def __init__(self, ):
        self._initialize_predictor()

    def _initialize_predictor(self):
        self.predictor = ModelPredictor()

    async def show_result(self, text_query):
        return await self.predictor.predict(text_query)
    
def show_gradio_ui():

    process = GradioApp()

    with gr.Blocks() as DBP_Block:
        with gr.Row():
            text_query = gr.Textbox(label = "Input Query", scale = 3, lines= 10)
            
        with gr.Row():
            submit_btn = gr.Button("Submit")

        with gr.Row():
            output = gr.Textbox(label = "Output", scale = 3, lines= 10, interactive = False)

        # Activities
        submit_btn.click(fn = process.show_result, 
                         inputs= [text_query], 
                         outputs= output, api_name = "DBProcess",)

    DBP_Block.launch(share = True)

    return DBP_Block

if __name__ == "__main__":
    show_gradio_ui()